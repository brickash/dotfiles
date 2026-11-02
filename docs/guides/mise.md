# mise 全局配置

[返回 README](../../README.md)

## 来源与范围

`home/private_dot_config/mise/config.toml.tmpl` 原样取自个人备份 `dotfiles-back`，该版本源自 [signalridge/dotfiles](https://github.com/signalridge/dotfiles) 的 `a978087ba7393d87f5264f2c06562adbb70b71ad`。模板渲染到 `~/.config/mise/config.toml`，仅在 macOS 声明 `mac-cleanup`。与当前本地 signalridge 模板相比，本版本不包含按工作环境条件启用的 JAIST VPN 认证工具；不自动同步上游。

这里只管理配置文件，不安装 mise、启用 shell integration，也不引入上游 `mise install` 或 `mise up` 自动化。模板注释中的 nix、MCP wrappers、`social-post`、CLIProxyAPI 等是参考环境说明，不代表本仓库提供这些组件，也不能假定已部署相关认证或保护措施。

## 声明与注意事项

- 声明 Node `lts`、Python `3.14`、Lua `5.4`，以及 Bun、Terraform、uv、Go、Rust 等；另有多个 pipx、Go 和 npm 工具，包括 AI 工具及发布工具。完整清单以模板为准。
- `latest` 和 `lts` 会随上游变化，不是可重现的固定版本；其中部分工具采用明确版本。
- 保留 `auto_install = true`：即使本仓库没有安装脚本，启用 mise 后的工作流也可能自动安装缺失工具。部署前应审阅完整清单。
- npm 后端使用 Bun；Node 仍可能是工具的运行依赖。Bun 默认跳过生命周期脚本，依赖 postinstall 下载原生组件的功能可能不可用。
- `trusted_config_paths` 包含 `~/Projects` 和 `~/Work`；这些目录中的配置将被 mise 信任，应确认目录及其中项目的来源。
- `_.path` 添加 `./node_modules/.bin` 和 `./bin`，项目本地程序可能影响命令解析。
- 模板原样保留上游注释，提到的版本日期、上游工具及保护性包装器不一定适用于本机；尤其不要假设发布工具自动具有确认保护。

## 维护与部署

修改仓库模板而不是生成后的文件。部署前先确认工具声明和当前本机差异：

```sh
chezmoi diff ~/.config/mise/config.toml
chezmoi apply ~/.config/mise/config.toml
```

部署配置文件不等于工具已安装；不要对渲染后的配置执行 `chezmoi add` 覆盖模板。若需要安装或升级工具，应先审阅声明，并明确决定是否执行相应的 mise 命令。
