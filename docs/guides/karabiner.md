# Karabiner-Elements 配置与使用

[返回 README](../../README.md) · [设计与来源调查](../references/karabiner-modifier-keys.md)

## 纳管范围

仓库中的 `home/private_dot_config/private_karabiner/private_karabiner.json` 部署到 `~/.config/karabiner/karabiner.json`。它最初从 `dotfiles-back` 恢复，之后同步了本机调整；当前选中 `Default profile`，虚拟键盘类型为 ANSI。配置中关闭了 Karabiner 更新检查。

仓库只管理主配置文件，不包含 Karabiner 的备份、规则资源或运行状态，也不安装软件或授予 macOS 权限。`private_` 标记使目标 Karabiner 目录和文件分别使用私有权限；整个 `~/.config` 目录也由仓库按私有权限管理。

## 当前按键行为

下表描述配置意图；实际输出仍受按键时序、系统设置和应用影响。`SpaceFN` 表示单独按住空格达到约 200 毫秒、功能层成功激活后，再按下列键。

| 操作 | 配置行为 |
|---|---|
| Caps Lock | 映射为左 Control |
| 单独短按左 Control | 发送 Escape；与其他键组合时作为 Control |
| 单独短按空格 | 发送空格 |
| SpaceFN + I / J / K / L | 上 / 左 / 下 / 右 |
| SpaceFN + H / N | Page Up / Page Down |
| SpaceFN + U / O | Home / End |
| SpaceFN + 1–0、`-`、`=` | F1–F12 |
| SpaceFN + Backspace | Forward Delete |
| SpaceFN + E / M / 逗号 | Escape / 反引号 / 波浪号 |
| SpaceFN + B | 空格（可按住重复） |
| SpaceFN + P / `[` / `]` / `\` / `/` | Print Screen / Scroll Lock / Pause / Insert / Menu |

Simple Modifications 先将 Caps Lock 转成左 Control，随后 Complex Modifications 处理左 Control 的单按行为；因此物理左 Control 也会受到单按 Escape 规则影响。单按、组合行为请用 EventViewer 和实际应用验证。

### SpaceFN 时序与防误触

空格激活规则配置了 200 毫秒按住阈值、300 毫秒单按超时和 200 毫秒延迟动作。快速按下其他键或长时间单独按住空格时，不应假定一定会触发功能层或输入普通空格；实际结果取决于事件顺序。

“Disable SpaceFN mode after last typing”规则旨在减少连续打字时空格误触功能层。由于快速输入 `Shift+字母` 时微信输入法误切换中英文，该规则已在本机暂时关闭并同步到仓库；关闭后用户观察到问题消失，具体原因尚未确认。

该规则通过 `_spacefn_mode` 和 `_lock_reset_spacefn_mode` 标记、200 毫秒延迟及取消后的 shell 命令控制空格激活；`spacefn_mode` 则是功能层状态，是另一个变量。shell 命令等待 0.2 秒，读取 Karabiner 状态文件并在满足条件时调用 `karabiner_cli` 重置变量。规则顺序与按键时序会影响结果，不能保证每次按键后都是固定 200 毫秒。

命令使用 `/library/application support/org.pqrs/tmp/karabiner_grabber_manipulator_environment.json` 和 `/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli`。原样保留的小写 `/library` 在区分大小写的文件系统上可能不可用；快速打字后的行为需要在目标机器实测。

- [ ] 排查微信输入法快速输入 `Shift+字母` 时误切换中英文：关闭整条防误触规则后用户观察到问题消失，但具体原因尚未确认。后续分别验证左右 Shift 处理及其他按键处理，并测试连续打字、普通空格与 SpaceFN；确认修复方案后再决定是否重新启用并同步仓库配置。

### 已保留但禁用的规则

- 单按左 Control → Caps Lock；当前只启用单按左 Control → Escape。
- 单按右 Control → Enter。
- SpaceFN + H/J/K/L 方向键；当前使用 I/J/K/L，H/N 用于翻页。
- 普通反引号键 → Escape；普通反引号键不再被这条规则改写。

## 维护与验证

在 Karabiner 界面修改后，先确认本机配置是要保留的版本，再同步到仓库；`chezmoi add` 会用本机文件更新仓库源文件：

```sh
chezmoi diff ~/.config/karabiner/karabiner.json
chezmoi add ~/.config/karabiner/karabiner.json
chezmoi diff ~/.config/karabiner/karabiner.json
```

反过来，从仓库部署到本机时，先检查差异，确认不会覆盖界面中的新修改：

```sh
chezmoi diff ~/.config/karabiner/karabiner.json
chezmoi apply ~/.config/karabiner/karabiner.json
```

避免同时在 Karabiner 界面和仓库编辑配置。恢复或修改后，在 EventViewer 和文本编辑器中检查 Caps Lock、物理左 Control 的单按与组合、普通空格及反引号、SpaceFN 方向键和 F 键；还应测试快速连续打字、长按空格后释放以及其他键盘和应用。根据 Karabiner 和 macOS 提示授予所需权限。

当前配置的 16 条复杂规则曾在 Karabiner-Elements 16.3.0 中通过 `--lint-complex-modifications` 格式校验；这不代表实际按键、shell 命令、所有设备或应用均已验证。

规则来源、选用理由及兼容性边界见[设计与来源调查](../references/karabiner-modifier-keys.md)。
