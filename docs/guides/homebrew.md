# Homebrew 软件清单

[返回 README](../../README.md)

## 范围

`private_dot_config/homebrew/Brewfile` 来自本机执行 `brew bundle dump` 导出的快照，部署目标为 `~/.config/homebrew/Brewfile`。清单包含 tap、Homebrew formula 和 cask、Mac App Store 应用、VS Code 扩展和 uv 工具；它记录导出时的安装状态，并非经过筛选的必需软件清单或精确版本锁文件。公开或在其他机器使用前，应审阅应用名称、第三方 tap 及 `trusted: true` 条目。

本仓库不自动安装 Homebrew，也不在 `chezmoi apply` 时执行 `brew bundle install`。部署 Brewfile 只同步清单；App Store 登录和应用配置需要另行处理。清单中的 Node 和 uv 也在 mise 配置中声明，二者并存时以 PATH 和 mise 设置决定实际使用的程序。

## 查看与使用

显式指定路径，不依赖 `XDG_CONFIG_HOME` 或 Homebrew 全局 Brewfile 路径设置：

```sh
brew bundle list --file="$HOME/.config/homebrew/Brewfile"
brew bundle check --file="$HOME/.config/homebrew/Brewfile"
```

需要在目标机器安装时，先审阅完整清单、第三方来源及商店登录状态，再由用户自行运行：

```sh
brew bundle install --no-upgrade --file="$HOME/.config/homebrew/Brewfile"
```

安装会执行软件安装及清单中声明的操作，可能需要网络、授权和 App Store 登录。不要使用 `brew bundle cleanup` 常规同步：它会卸载清单以外的依赖。

## 修改与同步

优先编辑仓库中的 Brewfile；部署前先查看差异：

```sh
chezmoi diff ~/.config/homebrew/Brewfile
chezmoi apply ~/.config/homebrew/Brewfile
```

若本机清单已修改并决定保留，可用 `chezmoi add ~/.config/homebrew/Brewfile` 同步回仓库。若需重新获取本机安装快照，应导出到单独的临时文件进行比较，审阅后再合并；不要无条件覆盖已维护的清单：

```sh
brew bundle dump --file=/tmp/Brewfile.snapshot
```
