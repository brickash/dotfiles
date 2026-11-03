# tmux 会话与快捷键

[返回 README](../../README.md)

## 来源与纳管范围

配置基于 [signalridge/dotfiles](https://github.com/signalridge/dotfiles) 的 `8ac90fa08b5224aefd39ded2a626a8f884c24814` 版本：

| 仓库文件 | 作用 |
|---|---|
| `home/private_dot_config/tmux/tmux.conf.tmpl` | tmux 主配置，部署到 `~/.config/tmux/tmux.conf` |
| `home/private_dot_config/tmux/executable_tmux2k-ai.sh` | 状态栏的 Claude/Codex 面板状态检测 |
| `home/private_dot_config/tmux/tmux-nerd-font-window-name.yml` | 窗口名称图标配置 |
| `home/.chezmoiexternal.toml` | 下载固定提交并验证 SHA-256 的 TPM 插件管理器 |

上游使用 `.headless` 控制嵌套 tmux 的 suspend 插件；本仓库没有设置该值时按非 headless 处理。TPM 由 chezmoi external 管理，因此不再把 TPM 自身列为 TPM 管理的插件，避免从非 Git 归档目录重复克隆；其他上游插件配置保留。新增的保存目录初始化只限制**新创建**目录的权限，不会修改已有目录的权限。

## 启动与会话

Shell 不会自动进入 tmux；在终端手动运行：

```sh
tmux new -s work      # 创建名为 work 的会话
tmux ls               # 查看会话
tmux attach -t work   # 重新连接
```

从会话断开不会主动终止其中的程序。SSH 断线后要恢复远程任务，必须在**远程主机**运行 tmux，再在远程重新连接。会话恢复插件只能尽力恢复窗口、路径及部分程序，不等同于保存所有进程的运行状态。

## 常用快捷键

前缀键为 `Ctrl+B`：先按前缀并松开，再按表中的键。

| 前缀后的键 | 操作 |
|---|---|
| `d` | 断开当前客户端，保留会话 |
| `c` | 在当前目录创建窗口 |
| `\|` / `-` | 左右 / 上下分屏 |
| `h / j / k / l` | 向左 / 下 / 上 / 右切换 pane |
| `H / J / K / L` | 调整 pane 大小 |
| `g` | 打开 lazygit 弹窗 |
| `T` | 打开 sesh 会话与目录选择器；其中 `Ctrl+F` 搜索目录 |
| `O` | 打开 sessionx 会话管理 |
| `p` / `P` | 切换浮动 pane / 打开浮动 pane 菜单 |
| `a` | 进入 vi 风格复制模式；`v` 开始选择，`y` 复制 |
| `Ctrl+S` / `Ctrl+R` | 保存 / 恢复会话 |
| `r` | 重载 tmux 配置 |
| `x` / `X` | 关闭当前 pane / 窗口；**不经确认** |
| `I` | 通过 TPM 安装所声明插件 |

`F12` 可暂时关闭外层 tmux 快捷键，方便操作嵌套的远程 tmux；再按一次恢复。Ghostty 自身的窗口/分屏快捷键独立于 tmux 的 pane 快捷键。

## 插件、依赖与新设备

本机及 Brewfile 已配置 tmux、Bash、sesh、fzf、fd、zoxide、lazygit。tmux2k 要求 Bash 5.2+，确保启动 tmux 的环境中 `bash` 指向较新版本；交互 Zsh 可用 `command -v bash`、`bash --version` 检查。图标使用 Nerd Font；Ghostty 当前使用 Maple Mono NF CN。

首次在新设备运行 `chezmoi apply` 会下载固定版本的 TPM；打开 tmux 后按 `Ctrl+B`、`I` 下载配置列出的插件。TPM 使用网络克隆插件，**各插件的版本没有固定**，后续安装或更新可能得到不同代码。TPM 本身由 chezmoi 管理，更新其版本需修改 external 的提交及校验和。不要把插件目录、会话文件或私有历史加入本仓库。

状态栏脚本会检查 tmux 中 Claude/Codex 的前台进程和部分面板输出；它还支持读取其他工具写入的生命周期状态文件，但本仓库没有安装或改写 Claude/Codex hooks。没有 hooks 时状态只能尽力推测，不能作为任务完成状态的可靠依据。脚本可能读取对应面板的近期输出，并使用本机私有临时目录保存/读取状态元数据。

## 持久化与隐私

上游 `tmux-resurrect` / `tmux-continuum` 设置为每 15 分钟自动保存并尝试自动恢复，**包括捕获 pane 内容**；手动保存同样会捕获。自动保存依赖状态栏刷新，且插件检测到多个 tmux 服务时会避免自动保存，以防不同服务互相覆盖。终端中显示的令牌、密码、命令输出或工作内容可能以未加密文件保存在本机。

默认路径为 `${XDG_DATA_HOME:-$HOME/.local/share}/tmux/resurrect`；如果已存在 `~/.tmux/resurrect`，插件优先使用旧路径。tmux 启动时会以私有权限创建不存在的默认目录，但不会更改已存在目录或手动配置目录的权限；迁移或设置自定义路径时请自行检查。关闭捕获需调整 `@resurrect-capture-pane-contents`；关闭自动保存/恢复需同时审阅 continuum 配置。

## 配置维护

```sh
chezmoi diff ~/.config/tmux/tmux.conf
chezmoi apply ~/.config/tmux/tmux.conf
```

已运行的 tmux 服务不会自动读取新配置；在该会话按 `Ctrl+B`、`r`，或执行 `tmux source-file ~/.config/tmux/tmux.conf`。不同的 tmux 服务和远程主机需要分别部署和重载。配置使用 `tmux-256color` 作为 tmux 内的终端类型，SSH 到远程主机时远程系统需要具备对应 terminfo。
