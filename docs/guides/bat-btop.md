# bat 与 btop 配置

[返回 README](../../README.md)

配置原样来自 [signalridge/dotfiles](https://github.com/signalridge/dotfiles) 的 `8ac90fa08b5224aefd39ded2a626a8f884c24814` 版本：

| 仓库源文件 | 部署位置 | 用途 |
|---|---|---|
| `home/private_dot_config/bat/config` | `~/.config/bat/config` | 文件预览与语法高亮 |
| `home/private_dot_config/btop/btop.conf` | `~/.config/btop/btop.conf` | 系统资源监控 |

## bat

配置使用 Dracula 主题，显示行号、Git 修改标记、文件头和边框，并定义部分文件扩展名的语法映射、4 列制表宽度及自动换行。直接运行 `bat 文件名` 查看；显示效果也受终端和输出方式影响。

本机 bat 0.26.1 的语法列表没有参考配置引用的 `Go HTML Template`；因此 `*.tmpl` 的这条映射不能提供该语法高亮，除非另行安装对应语法。可用 `bat --list-languages` 和 `bat --list-themes` 检查实际支持的语法与主题。

## btop

配置使用 Dracula 主题，刷新间隔为 1000 毫秒。运行 `btop` 查看 CPU、内存、磁盘、网络和进程，按 `q` 退出。

本机 btop 1.4.8 在正常退出时会将完整配置写回 `btop.conf`，即使仓库只管理参考项目的两行配置。因此运行后 `chezmoi diff` 可能出现大量默认项；若只想恢复仓库配置，审阅差异后运行 `chezmoi apply ~/.config/btop/btop.conf`。若在 btop 内修改设置并希望保存到仓库，应先审阅实际文件，再决定是否使用 `chezmoi add ~/.config/btop/btop.conf`。

## 维护

配置通过 chezmoi 部署；修改仓库源文件后，使用以下命令预览并应用：
```sh
chezmoi diff ~/.config/bat/config ~/.config/btop/btop.conf
chezmoi apply --parent-dirs ~/.config/bat/config ~/.config/btop/btop.conf
```

本仓库管理配置，不负责安装程序或额外的 bat 语法。需要时请先通过 Homebrew 等方式安装 bat 和 btop。
