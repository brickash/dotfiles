# dotfiles

使用 [chezmoi](https://www.chezmoi.io/) 管理个人配置。

## 仓库结构

```text
.
├── .chezmoiroot                          # 将 home/ 设为部署源
├── .chezmoiversion                       # 最低 chezmoi 版本 2.69.0
├── .github/workflows/                    # 安装脚本的 CI 检查
├── docs/                                 # 工具指南与参考调查，不部署
├── install.sh                            # 安装 chezmoi 并初始化、应用配置
├── scripts/readme-tree.sh                # 对齐 README 结构树注释
├── tests/                                # Git 身份功能回归测试
├── home/                                 # chezmoi 部署源
│   ├── .chezmoi.yaml.tmpl                # 初始化模板：仓库路径和身份数据
│   ├── .chezmoidata/aerospace.yaml       # AeroSpace 浮动应用清单
│   ├── .chezmoiignore                    # 部署目标的平台筛选
│   ├── dot_gitconfig                     # ~/.gitconfig 占位文件
│   ├── dot_custom/                       # 参考 Zsh 环境、别名和函数
│   ├── dot_zprofile.tmpl                 # 登录环境配置
│   ├── dot_zshenv                        # 所有 Zsh 进程读取的环境配置
│   ├── dot_zshrc                         # 交互式 Zsh 入口
│   ├── dot_local/bin/                    # Git 目录身份管理工具
│   └── private_dot_config/               # 部署到 ~/.config，目录权限为 0700
│       ├── aerospace/aerospace.toml.tmpl # AeroSpace 窗口管理配置模板
│       ├── private_atuin/                # Atuin 历史搜索配置
│       ├── bat/config                    # bat 文件查看配置
│       ├── btop/btop.conf                # btop 资源监控配置
│       ├── delta/config                  # Git 差异显示配置
│       ├── gh/private_config.yml         # GitHub CLI 偏好
│       ├── ghostty/config                # 本机 Ghostty 终端配置
│       ├── git/
│       │   ├── config.tmpl               # Git 全局配置模板
│       │   ├── ignore                    # Git 全局忽略规则
│       │   └── message                   # Git 提交信息模板
│       ├── homebrew/Brewfile             # 本机 Homebrew 软件清单
│       ├── lazygit/config.yml            # LazyGit 终端 Git 界面配置
│       ├── mise/config.toml.tmpl         # mise 全局工具与环境配置
│       ├── nvim/                         # 本机 LazyVim 配置
│       ├── sheldon/plugins.toml          # Zsh 插件管理
│       ├── starship.toml                 # Dracula 终端提示符
│       ├── private_karabiner/
│           └── private_karabiner.json    # Karabiner-Elements 配置
│       └── yazi/                         # Yazi 文件管理器配置
├── LICENSE
└── README.md
```

`.chezmoiroot` 指向 `home/`；仓库根目录的文档、脚本和测试不作为部署源。`.chezmoiversion` 要求 chezmoi 不低于 2.69.0。

chezmoi 将 `dot_` 转为以点开头的目标名称；`private_` 为目标设置私有权限。应用时 `~/.config` 目录权限会设为 `0700`，可能影响需要以其他用户身份访问该目录的服务。

修改上面的结构树后，在仓库根目录运行 `./scripts/readme-tree.sh` 对齐注释；使用 `./scripts/readme-tree.sh --check` 可只检查而不修改。脚本依赖 Perl。

## 使用与维护

在本仓库目录初始化 chezmoi 配置，不部署文件：

```sh
chezmoi init --source="$(pwd)"
```

初始化时填写姓名和邮箱，已有值会保留；它们保存在 `~/.config/chezmoi/chezmoi.yaml`，并用于渲染 Git 身份。配置中的 `sourceDir` 保存仓库根目录；chezmoi 通过 `.chezmoiroot` 自动定位 `home/`，部署目标不因源文件迁移而变化。

需要重新填写身份时：

```sh
chezmoi init --data=false
```

查看受管理文件、预览差异并应用：

```sh
chezmoi managed --include=files
chezmoi diff
chezmoi apply
chezmoi status
```

也可以运行 `./install.sh`；它会在缺少 chezmoi 时下载安装，然后直接执行初始化和应用。执行前请先审阅脚本和 `chezmoi diff`。

### 工具指南

| 文档 | 内容 |
|---|---|
| [Git 与 delta](docs/guides/git.md) | 身份、认证、依赖、配置行为和部署 |
| [Ghostty](docs/guides/ghostty.md) | 配置来源、快捷键、部署和验证 |
| [AeroSpace](docs/guides/aerospace.md) | 窗口布局、快捷键、浮动规则及部署 |
| [Homebrew](docs/guides/homebrew.md) | Brewfile 来源、维护和安装边界 |
| [mise](docs/guides/mise.md) | 工具声明、风险、部署和验证 |
| [LazyVim](docs/guides/lazyvim.md) | 纳管范围、插件锁文件和维护 |
| [LazyGit](docs/guides/lazygit.md) | Git 界面主题、使用和部署 |
| [Yazi](docs/guides/yazi.md) | 文件管理器配置、快捷键和部署 |
| [Atuin](docs/guides/atuin.md) | 历史搜索、同步设置和维护 |
| [bat 与 btop](docs/guides/bat-btop.md) | 终端文件查看与系统监控 |
| [Shell 与 Starship](docs/guides/shell.md) | Zsh 初始化、插件管理、依赖和风险 |
| [Karabiner-Elements](docs/guides/karabiner.md) | 按键规则、来源、部署和验证 |
| [键盘改键调查](docs/references/karabiner-modifier-keys.md) | 修饰键思路、兼容性和待验证事项 |

## 参考项目

Git 和 delta 配置参考 [signalridge/dotfiles](https://github.com/signalridge/dotfiles)；上游基线、本地差异和更新流程见 [Git 与 delta 指南](docs/guides/git.md)。不整体部署参考项目，也不自动同步其更新。

## License

MIT，详见 [LICENSE](LICENSE)。
