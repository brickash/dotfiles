# Tinycast

Tinycast 通过 Homebrew 安装，偏好设置通过应用原生的 Settings File 功能交给 chezmoi 管理。

## 纳管范围

| 内容 | 路径 | 是否纳管 |
|---|---|---|
| 应用安装 | `home/private_dot_config/homebrew/Brewfile` | 是 |
| 设置、快捷键、别名和窗口管理 | `~/.config/tinycast/settings.json` | 是 |
| 剪贴板历史 | `~/Library/Application Support/com.tinycast.app/clipboard.sqlite3` | 否 |
| Quicklinks | `~/Library/Application Support/com.tinycast.app/quicklinks.sqlite3` | 否 |
| 启动器学习记录 | `~/Library/Application Support/com.tinycast.app/launcher-ranking.json` | 否 |
| 窗口位置、文件选择记录等本机状态 | `~/Library/Preferences/com.tinycast.app.plist` | 否 |

`settings.json` 是 Tinycast 官方提供的可编辑镜像；`UserDefaults` 仍是应用内部的数据源。开启同步后，Tinycast 会监听该文件并实时应用修改，也会把应用内的设置改动写回文件。

剪贴板历史、Quicklinks 和启动器学习记录属于动态内容或本机状态，不提交到仓库。Snippets、Notes、Custom Commands、MCP、AI 连接以及部分涉及权限授权的开关也不会进入 Settings File；这是 Tinycast 的安全边界，不应通过复制数据库绕过。

## 首次部署

先应用 chezmoi 配置：

```sh
chezmoi apply ~/.config/tinycast/settings.json
```

然后在 Tinycast 中打开 **Settings → Backup → Settings File**，开启 **Sync settings file**。由于文件已经存在，选择 **Import**，不要选择会覆盖仓库配置的 **Replace**。

该开关本身不会写入 `settings.json`，必须在每台 Mac 上单独开启。

## 日常维护

在 Tinycast 设置界面修改后，应用会更新目标文件。将改动收回仓库：

```sh
chezmoi re-add ~/.config/tinycast/settings.json
chezmoi diff ~/.config/tinycast/settings.json
```

直接修改仓库中的 `home/private_dot_config/tinycast/settings.json` 后，部署并让 Tinycast 实时加载：

```sh
chezmoi apply ~/.config/tinycast/settings.json
```

## 验证

```sh
chezmoi source-path ~/.config/tinycast/settings.json
chezmoi diff ~/.config/tinycast/settings.json
defaults read com.tinycast.app settingsFileEnabled
```

`source-path` 应指向 `home/private_dot_config/tinycast/settings.json`，`diff` 应无输出，最后一个命令在已启用同步的机器上应输出 `1`。
