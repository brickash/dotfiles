# AeroSpace 配置

[返回 README](../../README.md)

## 来源与范围

`home/private_dot_config/aerospace/aerospace.toml.tmpl` 部署到 `~/.config/aerospace/aerospace.toml`，参考 [signalridge/dotfiles 的 AeroSpace 模板](https://github.com/signalridge/dotfiles/blob/8ac90fa08b5224aefd39ded2a626a8f884c24814/private_dot_config/aerospace/aerospace.toml.tmpl)。布局和快捷键沿用参考配置；浮动应用清单采用个人备份 `dotfiles-back` 中的配置，存放在 `home/.chezmoidata/aerospace.yaml`，不引入参考项目的 work/private 分类。不会自动同步上游变更。

该配置仅在 macOS 纳管，不安装 AeroSpace，也不授予辅助功能权限。配置启用登录启动；部署或重载前，请先确认布局和快捷键符合自己的使用习惯。

## 布局与规则

默认使用平铺布局、8 像素间距；切换显示器焦点时将鼠标移动到显示器中心。设置窗口、画中画和部分 Finder 对话框按规则浮动。应用清单中的 System Settings、Preview、Calculator、Karabiner 设置和 EventViewer、RustDesk、Raycast **以及 Ghostty** 也设为浮动；如希望 Ghostty 平铺，从清单中移除其条目。

工作区 1–6 强制分配到显示器 1，7–8 到显示器 2，9–10 到显示器 3。编号依赖机器的实际显示器排列；在不同显示器环境部署前应审阅这些分配。

## 常用快捷键

`Alt` 为 Option。配置包含更多快捷键，以模板中的 `[mode.main.binding]` 和 `[mode.service.binding]` 为准。

| 操作 | 快捷键 |
|---|---|
| 聚焦相邻窗口（左／下／上／右） | `Alt+H/J/K/L` |
| 移动窗口 | `Alt+Shift+H/J/K/L` |
| 切换工作区 1–10 | `Alt+1`–`9`、`Alt+0` |
| 移动窗口到工作区并跟随 | `Alt+Shift+1`–`9`、`Alt+Shift+0` |
| 切换平铺／手风琴布局 | `Alt+/`／`Alt+,` |
| 全屏／切换浮动 | `Alt+F`／`Alt+Shift+F` |
| 关闭窗口 | `Alt+Q` |
| 进入服务模式 | `Alt+S` |

服务模式中 `Esc` 重载配置并返回主模式，`Backspace` 关闭当前窗口之外的所有窗口；使用前注意保存工作。

## 修改与部署

浮动应用在 `home/.chezmoidata/aerospace.yaml` 中维护，窗口规则、显示器分配和快捷键在模板中维护。不要对渲染后的目标文件执行 `chezmoi add`，以免覆盖模板结构。

```sh
chezmoi diff ~/.config/aerospace/aerospace.toml
chezmoi apply ~/.config/aerospace/aerospace.toml
```

部署前先审阅差异；重载 AeroSpace 可能立即改变窗口布局及快捷键。部署不会自动安装或启动 AeroSpace。首次部署后在 AeroSpace 中按需重载，并实际检查显示器分配、浮动规则和快捷键。
