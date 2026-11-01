# Ghostty 配置与使用

[返回 README](../../README.md)

## 来源与纳管范围

仓库中的 `private_dot_config/ghostty/config` 部署到 `~/.config/ghostty/config`。它从本机配置纳管，以 [lltx 的现代化终端配置指南](https://gist.github.com/lltx/a61f98fdb761c9af7c5fd6cbfe963842)的 Ghostty 部分为参考；不自动同步该指南，也不因此安装或纳管其中的 Zoxide、Yazi 和 Oh-My-Zsh。

与查阅时的参考配置相比，本机增加了 `TokyoNight` 主题行及几个注释掉的候选主题。配置中 `Kanagawa Wave` 和 `TokyoNight` 两行均未注释；本机 `ghostty +show-config` 显示当前生效的是后面的 `TokyoNight`。切换主题时应检查实际生效值，避免被前面的配置行误导。

配置包含 macOS 专用选项；仓库目前没有按操作系统排除此文件。仓库不安装 Ghostty 或字体，需自行安装 `Maple Mono NF CN`；缺少字体时实际显示可能回退。

## 界面与日常行为

- 字体大小为 15，字形加粗，增加行高；窗口初始大小为 80 列 × 24 行，关闭窗口状态保存。
- 光标为闪烁竖线；输入时隐藏鼠标，选中文本配置为 `copy-on-select = both`。
- 快速终端从屏幕顶部出现，使用鼠标所在屏幕；失焦自动隐藏，动画时长 0.15 秒。
- `confirm-close-surface = false` 关闭关闭终端面板时的确认，注意避免误关正在运行的任务。
- 粘贴保护和 bracketed paste 安全选项均已开启，但不代替检查粘贴内容。
- 自动检测 shell integration，并启用 `cursor`、`sudo`、`no-title`、`ssh-env`、`ssh-terminfo` 和 `path`。其中 `ssh-terminfo` 可在适用的 SSH 调用中向远端安装终端能力描述；连接受限服务器时应考虑这一行为。
- 回滚缓冲区限制为 25,000,000 字节，不是无限历史。

## 快捷键

以下是配置文件中显式设置的快捷键；Ghostty 还可能提供默认快捷键。`Cmd` 是 macOS Command，`Alt` 是 Option。

| 操作 | 快捷键 |
|---|---|
| 新建标签页／关闭当前面板 | `Cmd+T`／`Cmd+W` |
| 上一个／下一个标签页 | `Cmd+Shift+←`／`Cmd+Shift+→` |
| 向右／向下分屏 | `Cmd+D`／`Cmd+Shift+D` |
| 切换到相邻分屏 | `Cmd+Alt+方向键` |
| 均分分屏／切换分屏放大 | `Cmd+Shift+E`／`Cmd+Shift+F` |
| 增大／减小／重置字号 | `Cmd++`／`Cmd+-`／`Cmd+0` |
| 滚动到顶部／底部 | `Cmd+↑`／`Cmd+↓` |
| 显示或隐藏快速终端 | `Ctrl+反引号`（全局快捷键） |
| 重载配置 | `Cmd+Shift+,` |

全局快捷键要求 Ghostty 正在运行，也可能受系统权限或其他应用快捷键冲突影响。

## 修改、部署与验证

直接编辑仓库配置时，先预览与本机的差异，再只部署 Ghostty 配置：

```sh
chezmoi diff ~/.config/ghostty/config
chezmoi apply ~/.config/ghostty/config
```

如果先修改了本机文件，确认本机版本是要保留的版本后，再同步回仓库：

```sh
chezmoi diff ~/.config/ghostty/config
chezmoi add ~/.config/ghostty/config
chezmoi diff ~/.config/ghostty/config
```

`chezmoi add` 会用本机文件更新仓库源文件；不要用它覆盖尚未保存的仓库侧修改。部署后按 `Cmd+Shift+,` 重载；部分选项可能需要新建窗口或重启 Ghostty。

配置修改或升级 Ghostty 后可检查语法与实际读取的配置。macOS 安装包内命令如下；若 `ghostty` 已在 PATH 中，也可直接使用 `ghostty +validate-config` 和 `ghostty +show-config`：

```sh
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
/Applications/Ghostty.app/Contents/MacOS/ghostty +show-config
```

校验成功不代表字体、全局快捷键、远端 SSH 或所有窗口行为都已实际验证；需在 Ghostty 和目标环境中检查。若另有 Ghostty 配置文件，也应检查是否与此文件叠加或覆盖。
