# Atuin 命令历史配置

[返回 README](../../README.md)

## 来源与范围

`home/private_dot_config/private_atuin/private_config.toml` 原样参考 [signalridge/dotfiles](https://github.com/signalridge/dotfiles) 的 `8ac90fa08b5224aefd39ded2a626a8f884c24814` 版本，部署到 `~/.config/atuin/config.toml`。`private_` 标记使目录和文件分别为 `0700` 和 `0600`。

本机 Atuin 18.24.4 在没有 `ATUIN_CONFIG_DIR` 时会查找该路径，但若 `~/.atuin/config.toml` 同时存在，会优先读取后者。迁移旧配置时先备份并移走旧文件，部署后用 `atuin info` 确认实际读取位置。

只管理配置文件；命令历史数据库、同步密钥、登录信息和日志仍留在本机，不进入仓库。Shell 中已有 Atuin 初始化；本仓库不自动安装 Atuin 或登录同步服务。

## 主要行为

- 自动同步 `auto_sync = false`；历史数据不会因该开关自动同步。`sync_frequency = "0"` 在本版 Atuin 表示启用自动同步时每条命令后尝试同步，并非禁用同步；若日后启用同步，先调整此项。
- `Ctrl+R` 使用全局范围、模糊搜索；向上箭头使用全局范围、前缀搜索。
- `enter_accept = true`：在历史搜索界面按 Enter 会直接执行选中的命令；可用 Tab 将命令放回命令行编辑。
- `secrets_filter = true` 启用 Atuin 的已知敏感信息模式过滤，但不能保证拦截所有密钥或密码。参考文件中将其描述为“忽略前导空格命令”的注释不准确，不应依赖该注释保护秘密。
- 其他未显式设置的选项沿用实际安装版本的默认值；配置文件本身不包含历史记录或凭据。

## 维护与部署

本机如已有配置，部署前先备份并审阅差异；不要覆盖历史数据库或密钥：

```sh
chezmoi diff ~/.config/atuin/config.toml
chezmoi apply ~/.config/atuin/config.toml
atuin config get --resolved auto_sync
```

优先在仓库中修改 `home/private_dot_config/private_atuin/private_config.toml`；若先修改本机配置并决定保留，可用 `chezmoi add ~/.config/atuin/config.toml` 同步回仓库。更换 Atuin 版本或设置 `ATUIN_HOME`、`ATUIN_CONFIG_DIR` 后，使用 `atuin info` 确认实际配置和数据库路径；配置部署不会自动迁移数据，也不会重启已有 daemon 或 Shell。
