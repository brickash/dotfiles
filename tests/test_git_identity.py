import os
from pathlib import Path
import subprocess
import tempfile
import unittest


TOOL = Path(__file__).resolve().parents[1] / "home/dot_local/bin/executable_git-identity"


class GitIdentityTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.root = self.home / "custom config" / "git"
        self.root.mkdir(parents=True)
        self.env = dict(os.environ, HOME=str(self.home), XDG_CONFIG_HOME=str(self.root.parent),
                        GIT_CONFIG_GLOBAL=str(self.root / "config"), GIT_CONFIG_NOSYSTEM="1")
        self.git("config", "--global", "user.name", "Default")
        self.git("config", "--global", "user.email", "default@example.com")
        self.git("config", "--global", "include.path", str(self.root / "identities.config"))

    def run_command(self, *args, cwd=None, check=True):
        return subprocess.run(args, cwd=cwd or self.home, env=self.env, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)

    def git(self, *args, cwd=None):
        return self.run_command("git", *args, cwd=cwd).stdout.strip()

    def tool(self, *args, check=True):
        return self.run_command("python3", str(TOOL), *map(str, args), check=check)

    def repo(self, name):
        path = self.home / name
        path.mkdir(parents=True, exist_ok=True)
        self.git("init", "-q", str(path))
        return path

    def email(self, path):
        return self.git("config", "user.email", cwd=path)

    def test_nested_directories_collisions_and_repository_override(self):
        parent = self.repo("work space")
        nested = self.repo("work space/nested")
        other = self.repo("work-space")
        self.tool("add", nested, "Nested", "nested@example.com")
        self.tool("add", parent, "Parent", "parent@example.com")
        self.tool("add", other, "Other", "other@example.com")
        self.assertEqual(self.email(parent), "parent@example.com")
        self.assertEqual(self.email(nested), "nested@example.com")
        self.tool("remove", other)
        self.assertEqual(self.email(other), "default@example.com")
        self.assertEqual(self.email(parent), "parent@example.com")
        self.git("config", "user.email", "local@example.com", cwd=nested)
        self.assertEqual(self.email(nested), "local@example.com")

    def test_legacy_mapping_and_collision_refuse_deletion(self):
        repo = self.repo('team "研发"')
        identities = self.root / "identities"
        identities.mkdir()
        identity = identities / "legacy.config"
        identity.write_text('[user]\n name = Legacy\n email = legacy@example.com\n')
        mapping = self.root / "identities.map"
        mapping.write_text(f"{repo}\tlegacy\n")
        self.tool("refresh")
        self.assertEqual(self.email(repo), "legacy@example.com")
        self.tool("add", repo, 'New "Name"', "new@example.com")
        self.assertIn('New "Name" <new@example.com>', self.tool("list").stdout)
        mapping.write_text(f"{repo}\tlegacy\n{self.home}/other\tlegacy\n")
        self.assertNotEqual(self.tool("remove", repo, check=False).returncode, 0)
        self.assertTrue(identity.exists())

    def test_rejects_glob_directories_and_preserves_private_permissions(self):
        repo = self.repo("valid")
        self.tool("add", repo, "Name", "email@example.com")
        identity = next((self.root / "identities").glob("*.config"))
        for file in (identity, self.root / "identities.map", self.root / "identities.config"):
            self.assertEqual(file.stat().st_mode & 0o777, 0o600)
        bad = self.home / "bad*name"
        bad.mkdir()
        self.assertNotEqual(self.tool("add", bad, "Name", "email@example.com", check=False).returncode, 0)
        self.assertEqual(self.email(repo), "email@example.com")


if __name__ == "__main__":
    unittest.main()
