# LazyVim 配置

[返回 README](../../README.md)

## 纳管范围

`home/private_dot_config/nvim/` 来自本机 `~/.config/nvim/`，以现有 [LazyVim starter](https://github.com/LazyVim/starter) 为基础，不使用参考项目的配置覆盖本机设置。仓库管理：

- `init.lua`、`lua/config/` 和 `lua/plugins/`：启动入口、配置和插件声明。
- `lazyvim.json`：LazyVim extras；纳管时本机未启用 extras。
- `lazy-lock.json`：插件版本锁定记录。
- `.neoconf.json`、`stylua.toml`：相关配置。
- `LICENSE`：随本机 starter 附带的 Apache 2.0 许可文件。

`lua/plugins/example.lua` 是本机自带示例，开头直接返回空表，不会启用示例中的插件。仓库不管理 Neovim 下载的插件、缓存、运行状态，也不纳管 starter 的 README 或 `.gitignore`。

## 维护与部署

优先修改仓库源文件；部署前审阅本机差异，避免覆盖在 Neovim 中产生的更新：

```sh
chezmoi diff ~/.config/nvim
chezmoi apply ~/.config/nvim
```

如先修改了本机配置，只同步确认需要的文件，例如：

```sh
chezmoi add ~/.config/nvim/lua/config/options.lua
chezmoi add ~/.config/nvim/lazyvim.json ~/.config/nvim/lazy-lock.json
```

更新插件后，`lazy-lock.json` 可能变化；先检查差异，再决定是否同步到仓库。新增插件配置也需单独纳管。不要不加筛选地对整个目录运行 `chezmoi add`，以免加入不打算管理的文件或敏感信息。

配置里的 `lazy.nvim` 缺失时会从 GitHub 克隆，且启用了定期插件更新检查；部署配置并不安装 Neovim 或插件，也不保证离线首次启动成功。首次使用前需准备 Neovim、Git 和网络，具体依赖取决于启用的插件。

纳管后可用 `chezmoi diff ~/.config/nvim` 检查同步状态，并启动 `nvim` 验证插件加载和实际编辑行为；锁文件不等于插件均已安装或功能已验证。
