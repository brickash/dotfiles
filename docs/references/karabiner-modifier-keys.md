# Karabiner 键位设计与参考

[返回 README](../../README.md) · [当前配置与使用指南](../guides/karabiner.md)

本文记录当前键位设计的参考资料、取舍与验证边界；当前启用的具体按键及部署方法以[使用指南](../guides/karabiner.md)和仓库配置为准。仓库主配置最初取自 [dotfiles-back](https://github.com/brickash/dotfiles-back)，后来按本机需要调整；参考链接不意味着配置会自动跟随上游更新。

## Caps Lock、Control 与 Escape

[简书：macos 系统下实现 capslock 键指向 esc 和 ctrl 键](https://www.jianshu.com/p/3a23fafcb7de)介绍了两步方案：将 Caps Lock 简单映射为左 Control，再启用单按左 Control 发送 Escape 的复杂规则。文章最后编辑于 2022 年，界面步骤可能随软件版本变化。

本仓库采用相同的两步思路。对应的社区资源是 [Change control key 规则页面](https://ke-complex-modifications.pqrs.org/?rule=json%2Fcontrol.json)和 [JSON 数据](https://ke-complex-modifications.pqrs.org/json/control.json)。其中“Post escape if left_control is pressed alone”与仓库对应规则定义一致；同一规则集中的左 Control 单按 Caps Lock、右 Control 单按 Enter 在本配置中禁用。参考资料与规则名称不能单独证明备份最初从何处导入。

根据 [Karabiner 官方事件处理顺序](https://karabiner-elements.pqrs.org/docs/manual/misc/event-modification-chaining/)，Simple Modifications 在 Complex Modifications 之前执行。因此 Caps Lock 的简单映射与左 Control 的复杂规则可以衔接；物理左 Control 也符合该复杂规则。系统修饰键设置在后续阶段处理，最终结果仍应实际测试。

## SpaceFN 设计与取舍

[SpaceFN 规则页面](https://ke-complex-modifications.pqrs.org/?rule=json%2Fspacefn_plus.json)和 [JSON 数据](https://ke-complex-modifications.pqrs.org/json/spacefn_plus.json)提供空格功能层及多种可选映射。仓库保留本机配置，不自动导入或同步整套规则。

- **方向键采用 I/J/K/L**：与方向键布局一致；H/J/K/L 规则保留但禁用，避免 J、K 同时对应不同方向。H/N 当前用于 Page Up / Page Down。
- **普通反引号保留原用途**：禁用社区方案中普通反引号转 Escape 的规则；SpaceFN 中仍有反引号和波浪号映射。
- **打字防误触规则启用**：它尝试在连续输入期间阻止空格启动功能层，代价是刚打完字就使用 SpaceFN 可能不够顺手。规则含延迟动作、状态变量和本机 shell 命令，时序与路径风险见[使用指南](../guides/karabiner.md#spacefn-时序与防误触)。

Karabiner 的[复杂规则优先级](https://karabiner-elements.pqrs.org/docs/json/complex-modifications-manipulator-evaluation-priority/)为自上而下、首个匹配生效。启用新规则前应检查同一按键、修饰键及条件是否与已有规则重叠；例如 H/J/K/L 若与当前方向键、翻页规则同时启用，会产生遮挡。

## 其他文章中的可选思路

[少数派：Control + Option + Shift + Command，带你玩转 macOS 的修饰键](https://sspai.com/post/39331)还介绍了双重用途修饰键、Hyper 键、双击切换 Caps Lock、EventViewer 和粘滞键。当前仓库采用的只是左 Control 单按 Escape 等现有规则；Hyper、双击切换等不是已部署功能，应在明确需求、检查快捷键冲突后再考虑。

该文发表于 2017 年，涉及旧版 Karabiner、`private.xml`、Seil 和当时的 Hammerspoon 绕行方案；这些历史实现不能直接用于当前 Karabiner-Elements JSON，也不应将当年对 Elements 功能不足的描述视为现状。

## 检查边界

仓库配置已与本机配置比对；当前 16 条复杂规则使用 Karabiner-Elements 16.3.0 的 `karabiner_cli --lint-complex-modifications` 校验结果为 `ok`。此检查只覆盖规则格式，不证明整个配置在实际键盘、系统设置或应用中行为正确，也未验证防误触规则的 shell 命令。实际验证方法见[使用指南](../guides/karabiner.md#维护与验证)。
