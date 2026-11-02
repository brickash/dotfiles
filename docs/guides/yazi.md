# Yazi 配置与使用

[返回 README](../../README.md)

## 来源与范围

仓库的 `home/private_dot_config/yazi/` 管理 `~/.config/yazi/` 下的 `yazi.toml`、`keymap.toml` 和 `theme.toml`。以 [lltx 的终端配置指南](https://gist.github.com/lltx/a61f98fdb761c9af7c5fd6cbfe963842)为参考，并对照 [Yazi 26.9.1 官方配置](https://yazi-rs.github.io/docs/configuration/yazi/)适配；快捷跳转到 dotfiles 的思路另参考 [signalridge/dotfiles](https://github.com/signalridge/dotfiles)。不自动同步参考配置。

保留三栏比例 `1:2:5`、自然排序、目录优先、大小显示、符号链接目标及 Lanczos3 图片预览。考虑到经常管理 dotfiles，默认显示隐藏文件，可在 Yazi 中按 `.` 切换。主题使用 Dracula 调色板，模式栏和文件类型颜色显式配置；其余未设置的样式由 Yazi 和终端决定。

与 Gist 的主要差异：

- 文本编辑优先使用 `$EDITOR`，未设置时使用 `nvim`；编辑器在终端前台运行。系统默认应用及 Finder 定位使用 Yazi 内置 opener，macOS 的 Finder 定位使用 `%s1`。
- 未启用 Gist 的 Git fetcher 或安装任何插件；未照搬旧版任务并发选项。其他未设置项沿用 Yazi 版本自身默认值。
- 主题调整为 Dracula 调色板，文件匹配按当前版本使用 `url`；三栏尺寸和图片参数不代表文件大小限制。

此配置不管理 Zoxide、Shell 初始化或退出 Yazi 后改变 Shell 目录的包装函数，也不安装 Yazi 或预览依赖。图片、视频、PDF 等功能取决于终端和已安装的预览工具。

## 快速跳转

依次按 `g` 再按下列键：

| 按键 | 目标 |
|---|---|
| `h` / `c` / `d` | 主目录 / `~/.config` / `~/Downloads` |
| `w` / `D` / `t` | `~/work` / `~/Desktop` / `/tmp` |
| `.` | 默认 chezmoi 仓库 `~/.local/share/chezmoi` |

如仓库放在其他路径，应修改 `keymap.toml` 中的 `g .`。其他操作使用 Yazi 默认快捷键；按 `~` 查看帮助。

## 维护与部署

```sh
chezmoi diff ~/.config/yazi
chezmoi apply ~/.config/yazi
```

优先在仓库中修改相应文件。若先在本机调整，确认要保留的文件后，可用 `chezmoi add ~/.config/yazi/yazi.toml`（或对应文件）同步回仓库；不要无差别导入插件、缓存或运行状态。修改后重新启动 Yazi 验证；配置解析成功不代表所有预览、外部编辑器或终端图形功能均已验证。
