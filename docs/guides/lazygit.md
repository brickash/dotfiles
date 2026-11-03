# LazyGit 配置

[返回 README](../../README.md)

## 来源与兼容性

`home/private_dot_config/lazygit/config.yml` 基于 [signalridge/dotfiles](https://github.com/signalridge/dotfiles) 的 `8ac90fa08b5224aefd39ded2a626a8f884c24814` 版本，部署到 `~/.config/lazygit/config.yml`。保留上游完整设置；仅采用本机 LazyGit 0.66.2 自动执行的配置迁移：

- `gui.wrapLinesInStagingView` 改名为 `gui.wrapLinesInDiffView`。
- `git.pagers` 改名为 `git.diffRenderers`，对应的命令字段及 `extDiff` 类型按新格式调整。
- `keybinding.worktrees.viewWorktreeOptions` 移至 `keybinding.universal.newWorktree`。

配置包含 Dracula 配色、Nerd Font 3 图标、Git 行为、快捷键、差异渲染和自定义命令。图标需要终端使用支持 Nerd Font 3 的字体。

## 对 Git 操作的影响

该文件不会修改全局 Git 配置，但 LazyGit 在操作仓库时会按以下设置运行 Git 命令：

- `git.autoFetch: true`、`git.fetchAll: true`，`refresher.fetchInterval: 60`：运行期间自动获取所有远程更新，间隔为 60 秒。当前全局 Git 配置已开启 `fetch.prune` 和 `fetch.pruneTags`；自动 fetch 可能清理已从远程删除的远程跟踪分支和本地标签。普通 Git 命令也会受到这些原有全局 fetch 设置的影响。
- `git.skipHookPrefix: WIP`：以 `WIP` 开头的提交消息会跳过 Git hooks；文件视图中的 `w` 也是不运行 hook 的提交快捷键。是否跳过与具体提交方式有关，重要提交请检查。
- `git.autoStageResolvedConflicts: true`：LazyGit 检测到冲突已解决时会自动暂存相应文件，并可能提示继续 merge 或 rebase。
- `git.disableForcePushing: false`：配置不禁止强推；是否执行强推仍由用户操作决定。自定义 `F` 命令在 remotes 面板运行 `git fetch --all --prune`。
- 差异渲染使用 difftastic、delta 和 less；前两项依赖 `difft`、`delta` 命令。提交信息输入会按配置在 72 列换行。

上游自定义命令包含 shell 模板，例如 `code {{.SelectedFile.Name}}` 没有为文件名添加 shell 引号，提交信息和 PR 标题也直接插入单引号。包含空格、引号或 shell 元字符的文件名或输入可能导致命令失败或被 shell 解释；不要在不可信仓库或使用此类输入时运行这些自定义命令。普通 LazyGit 内置操作不依赖这些自定义命令。

## 使用与部署

在 Git 仓库中运行 `lazygit` 或 `git ui`，按 `?` 查看快捷键，按 `q` 退出。上游使用 `h/j/k/l` 导航，未改成 AeroSpace 的方向键布局。参考配置的 PR 命令依赖 `gh`，打开文件的命令依赖 `code`。

本仓库 Zsh 的 `~/.zshenv` 设置 `XDG_CONFIG_HOME`，从 Zsh 启动时 LazyGit 会读取 `~/.config/lazygit/config.yml`。macOS 上若其他启动环境没有设置该变量，LazyGit 可能改用 `~/Library/Application Support/lazygit`；可用 `lazygit --print-config-dir` 检查，或在一次调用中使用 `lazygit --use-config-file ~/.config/lazygit/config.yml` 指定配置。

```sh
chezmoi diff ~/.config/lazygit/config.yml
chezmoi apply --parent-dirs ~/.config/lazygit/config.yml
lazygit --print-config-dir
```

`chezmoi` 只管理配置文件，不管理 LazyGit 的状态数据。应用配置不会安装 LazyGit；本机 Homebrew 清单已包含它。
