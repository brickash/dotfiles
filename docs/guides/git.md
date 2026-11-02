# Git 与 delta 配置

[返回 README](../../README.md)

## 上游来源与本地差异

- 上游仓库：[signalridge/dotfiles](https://github.com/signalridge/dotfiles)
- 当前比对基线：[`8ac90fa08b5224aefd39ded2a626a8f884c24814`](https://github.com/signalridge/dotfiles/commit/8ac90fa08b5224aefd39ded2a626a8f884c24814)
- 比对范围：上游的 `dot_gitconfig`、`private_dot_config/git/config.tmpl`、`private_dot_config/git/ignore`、`private_dot_config/git/message` 和 `private_dot_config/delta/config`；本仓库对应路径位于 `home/` 下。

与上述基线相比，除本仓库路径增加 `home/` 前缀外，`home/private_dot_config/git/config.tmpl` 使用本仓库的身份变量，并增加目录身份 include：

| 配置项 | 上游 | 本仓库 |
|---|---|---|
| `user.name` | `{{ .gitUsername }}` | `{{ .name }}` |
| `user.email` | `{{ .gitEmail }}` | `{{ .email }}` |

本仓库通过 `home/.chezmoi.yaml.tmpl` 提供 `name` 和 `email`，不依赖上游的初始化模板或 `gitUsername`、`gitEmail` 数据。其余四个文件在该基线下内容逐字节一致。这里记录的是这五个文件的差异，不代表两个仓库的其他配置一致。
`config.tmpl` 还包含本机目录身份配置的 `[include]`，由 `git-identity` 维护；不自动引入上游同名配置。

## 检查与合入上游

周期性检查由维护者手动执行，目前没有自动同步。先获取上游仓库（已有则跳过 `ghq get`），然后更新远程引用，比较当前基线与上游 `main`：

```sh
ghq get https://github.com/signalridge/dotfiles
cd "$(ghq root)/github.com/signalridge/dotfiles"
git fetch origin
git diff 8ac90fa08b5224aefd39ded2a626a8f884c24814 origin/main -- \
  dot_gitconfig private_dot_config/git/config.tmpl \
  private_dot_config/git/ignore private_dot_config/git/message \
  private_dot_config/delta/config
git rev-parse origin/main
```

逐项审阅配置行为、依赖和安全影响，再按需合入当前仓库；不要直接覆盖身份变量。合入后检查 Git 配置能否正常渲染、通过 `chezmoi diff` 审阅目标差异，并按「修改与部署」验证。更新本文的基线提交和本地差异记录，注明未采纳的上游变更；基线表示已审阅到的版本，不意味着所有上游变更都已采用。

## 纳管范围

| 仓库文件 | 部署目标 | 用途 |
|---|---|---|
| `home/dot_gitconfig` | `~/.gitconfig` | 配置位置说明 |
| `home/private_dot_config/git/config.tmpl` | `~/.config/git/config` | Git 身份、行为、工具和别名 |
| `home/private_dot_config/git/ignore` | `~/.config/git/ignore` | Git 全局忽略规则 |
| `home/private_dot_config/git/message` | `~/.config/git/message` | 提交信息模板 |
| `home/private_dot_config/delta/config` | `~/.config/delta/config` | delta 差异显示样式 |
| `home/private_dot_config/gh/private_config.yml` | `~/.config/gh/config.yml` | GitHub CLI 偏好 |
| `home/dot_local/bin/executable_git-identity` | `~/.local/bin/git-identity` | 管理本机目录身份 |

## 身份与认证

Git 模板使用 chezmoi 配置中的 `name` 和 `email`。使用 `chezmoi init --data=false` 重新输入后，预览并应用 Git 配置；仓库级配置仍可覆盖全局身份，修改身份不会改变已有提交。

```sh
chezmoi init --data=false
chezmoi diff ~/.config/git/config
chezmoi apply ~/.config/git/config
git config --show-origin --get user.name
git config --show-origin --get user.email
```

避免用 `git config --global` 修改由 chezmoi 管理的身份：它可能写入 `~/.gitconfig`，并覆盖 XDG 配置中的设置。直接查询有效配置时不带 `--global`，以包含两处全局配置及当前仓库的覆盖值。

### 按目录切换身份

`git-identity` 使用 Python 3 和 Git，将指定目录下的仓库切换到对应身份；未匹配时沿用上述默认身份。工具只管理本机身份数据，不把工作身份写入 dotfiles 仓库。先部署 Git 配置及命令，确认 `~/.local/bin` 在 PATH 中：

```sh
chezmoi diff ~/.config/git/config ~/.local/bin/git-identity
chezmoi apply ~/.config/git/config ~/.local/bin/git-identity
git-identity add ~/work "Work User" work@example.com
git-identity list
git-identity remove ~/work
```

命令还支持 `git-identity refresh`，根据已有映射重新生成 include 文件。`add` 要求目录存在，并以真实路径处理相对路径和符号链接；为避免 Git 路径通配符带来意外匹配，目录名不能包含 `*`、`?`、`[`、`]`、反斜杠、制表符或换行。多个目录可使用不同身份；嵌套目录优先于外层目录，仓库级配置仍可覆盖。删除不存在的映射会报错，不删除其他身份文件。

本机数据位于 `${XDG_CONFIG_HOME:-~/.config}/git/identities.map`、`identities.config` 和 `identities/*.config`，文件使用私有权限。工具兼容 back 仓库已有的映射和身份文件；如发现旧映射中的路径或标识碰撞，会拒绝修改，需先手动检查。迁移仓库不会迁移这些本机数据；换机器需重新配置或由用户安全迁移。

Git 模板在 chezmoi 渲染时将当时的 `XDG_CONFIG_HOME` 写入 include 路径，未设置时使用 `~/.config`。修改该环境变量后，须在新环境重新 `chezmoi apply ~/.config/git/config`，并自行处理旧数据；如果采用非默认 XDG 路径，还需确保 Git 实际加载了此受管全局配置（其目标仍是 `~/.config/git/config`）。不要假定改环境变量会自动移动身份数据。

GitHub HTTPS 凭据使用 `gh auth git-credential`；本仓库不保存登录令牌，部署配置不等于登录。可使用 `gh auth status` 检查登录状态，必要时运行 `gh auth login`。其他 Git 服务不使用此 GitHub 专用 helper。

本仓库纳管 `~/.config/gh/config.yml` 中的 GitHub CLI 偏好，包括 HTTPS、交互选项及 `gh co` 别名；不纳管 `hosts.yml` 或登录凭据。配置取自本机，保留了 back 仓库配置中共有的设置和本机额外偏好；不自动同步参考项目。

修改本机偏好后，可用 `chezmoi add ~/.config/gh/config.yml` 同步到仓库，先检查其中没有凭据或其他不希望提交的数据。从仓库部署时先使用 `chezmoi diff ~/.config/gh/config.yml` 预览，再用 `chezmoi apply ~/.config/gh/config.yml` 应用。

## 行为与依赖

- `git pull` 默认 rebase；`git fetch` 清理已删除的远程分支及标签。清理标签可能影响本地同名标签，使用前确认仓库需求。
- 提交编辑器为 `nvim`，差异使用 `difft` 和 `delta`，大文件过滤使用 `git-lfs`；缺少相应工具会影响相关操作。`git ui` 别名需要 `lazygit`。
- 全局忽略规则包括 `vendor/`、`build/`、`.env` 等。使用 `git check-ignore -v <路径>` 查看具体匹配；已跟踪文件不受忽略规则影响。
- 常用别名：`git st` 查看状态、`git lg` 查看最近提交、`git can` 修改上次提交、`git undo` 撤销上次提交并保留暂存、`git pf` 使用 `--force-with-lease` 推送。

## 修改与部署

编辑仓库内相应文件后，可只预览和部署 Git 与 delta 配置：

```sh
chezmoi diff ~/.gitconfig ~/.config/git/config ~/.config/git/ignore ~/.config/git/message ~/.config/delta/config
chezmoi apply ~/.gitconfig ~/.config/git/config ~/.config/git/ignore ~/.config/git/message ~/.config/delta/config
```

本仓库不自动安装上述工具依赖。
