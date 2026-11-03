# Zsh、Starship 与 Sheldon

[返回 README](../../README.md)

## 来源与范围

以下文件引入自 [signalridge/dotfiles](https://github.com/signalridge/dotfiles) 本地基线 `8ac90fa08b5224aefd39ded2a626a8f884c24814`，不自动同步。除 `~/.zshrc` 在加载插件前增加 `compinit` 外，参考源文件保持原样；在本机直接加载时，tmux 补全因 `compdef` 尚未定义而报错，因此需要先初始化补全。

| 仓库文件 | 本机目标 | 作用 |
|---|---|---|
| `home/dot_zshenv` | `~/.zshenv` | XDG 和 PATH；所有 Zsh 进程读取 |
| `home/dot_zprofile.tmpl` | `~/.zprofile` | 登录环境、locale、bat 主题及 macOS OrbStack 初始化 |
| `home/dot_zshrc` | `~/.zshrc` | 交互式入口，加载以下 `.custom` 文件 |
| `home/dot_custom/` | `~/.custom/` | 工具初始化、环境变量、补全、别名、函数及备份脚本 |
| `home/private_dot_config/starship.toml` | `~/.config/starship.toml` | Dracula 提示符、工具图标、Git 与 worktree 信息 |
| `home/private_dot_config/sheldon/plugins.toml` | `~/.config/sheldon/plugins.toml` | Zsh 插件来源和加载方式 |

参考仓库未声明根目录许可证；引入依据用户确认的授权。引用不代表自动获得其他上游插件的许可。

## 启动行为与依赖

- `~/.zshenv` 对交互式和非交互式 Zsh 都生效，会设置 XDG、调整 PATH、移除 mise shims 路径并设置其他参考环境变量。更改后也应检查脚本和远程命令。
- `~/.zshrc` 加载 `.custom` 脚本；其中 `eval.sh` 在交互且有 TTY 时按命令是否存在初始化 Starship、fzf、Sheldon、Carapace、Navi、Zoxide、mise、Atuin 和 direnv。未安装的命令会跳过，不代表相关功能可用。
- Sheldon 配置包含来自 Oh-My-Zsh 仓库的 tmux 插件，但不安装完整 Oh-My-Zsh 框架。其他插件包括 zsh-defer、autosuggestions、syntax-highlighting 和 fzf-tab；`sheldon source` 可能联网安装插件。参考配置未固定各插件提交，恢复时内容可能随上游变化。
- `~/.custom/exports.sh` 原样设置 `TERM=xterm-256color`、`COLORTERM=truecolor` 和 Dracula fzf 颜色；这会覆盖 Ghostty 原本提供的 `TERM`，影响远端 terminfo 和终端能力。tmux 自动启动在参考配置中关闭。
- mise activation 会启用当前 mise 配置；该配置保留 `auto_install = true`，后续工作流可能安装缺失工具。Shell 配置不保证为参考项目的 Nix、aqua、OrbStack 或其他配套工具提供完整环境。
- 参考配置包含 `cat`→`bat`、`ls`→`eza` 等条件别名以及 `cp -iv`、`mv -iv` 别名；原生命令可使用 `command cat`、`command cp` 等调用。`.custom/functions.sh` 还包含 worktree、Git 和 AI 工作流，请先审阅再使用。
- `~/.custom/backup.sh` 来自参考项目，默认调用 `rclone sync`。**同步可能删除远端目标中不再存在的文件**；没有配置和审阅远端前不要执行。它不会因 Shell 启动自动运行。

Starship 和 Zoxide 已包含在本仓库的 Brewfile 中；仓库只部署清单，不自动安装工具。复制参考 Shell 配置不包含 Yazi 的 `y` 包装函数；直接运行 `yazi` 不会使退出后的 Shell 自动切换目录。

## 维护与部署

修改仓库源文件；首次部署或同步前检查差异：

```sh
chezmoi diff ~/.zshenv ~/.zprofile ~/.zshrc ~/.custom ~/.config/starship.toml ~/.config/sheldon
chezmoi apply ~/.zshenv ~/.zprofile ~/.zshrc ~/.custom ~/.config/starship.toml ~/.config/sheldon
```

初始化模板中的 `platform` 根据运行系统生成，用于渲染参考 `.zprofile`。更新 chezmoi 配置模板后需执行 `chezmoi init`；它不会自动应用用户文件。部署后启动新的交互式登录 Zsh 验证，已有 Shell 不会自动重新加载配置。Sheldon、mise 和其他初始化器可能访问网络或修改自身缓存；检查时应使用隔离 HOME，避免执行备份等有副作用的函数。

`~/.custom/local.sh` 为可选本机覆盖文件，不由仓库管理；账号凭据和私人设置不要写入公开的 Shell 源文件。
