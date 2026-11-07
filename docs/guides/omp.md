# OMP 配置

OMP 通过 Homebrew 安装，chezmoi 只管理主配置文件，不管理运行时目录。

## 纳管范围

| 仓库文件 | 本机目标 | 作用 |
|---|---|---|
| `home/dot_omp/private_agent/private_config.yml` | `~/.omp/agent/config.yml` | 全局模型角色、主题、输入区和交互偏好 |

`private_` 属性使 `~/.omp/agent` 和 `config.yml` 保持私有权限。当前配置不包含 API Key、OAuth Token 或 Broker Token；加入此类字段前必须确认不会提交凭据。

以下内容不纳管：

- `~/.omp/agent/sessions/` 和会话历史；
- `~/.omp/agent/*.db*`、`~/.omp/stats.db*` 等数据库；
- `~/.omp/logs/`、`cache/`、`run/` 和浏览器 Profile；
- `~/.omp/plugins/node_modules/` 与其他可重新生成的插件依赖；
- 认证凭据和远程主机状态。

不要整体执行 `chezmoi add ~/.omp`，否则会把会话、日志、数据库甚至凭据带入仓库。

## 配置层级

OMP 按以下顺序合并配置：

1. 全局配置 `~/.omp/agent/config.yml`；
2. 项目配置 `<project>/.omp`；
3. 启动参数 `--config <config.yml>` 的单次覆盖。

项目专用设置应放在对应项目中，不应写进本仓库的全局配置。

## 修改与验证

通过 OMP 修改全局配置后，将目标文件收回仓库：

```sh
omp config set theme.dark titanium
chezmoi re-add ~/.omp/agent/config.yml
```

部署并检查：

```sh
chezmoi apply ~/.omp/agent/config.yml
omp config list --scope global --json
omp config list --scope project --json
```

第二条命令应显示仓库配置中的显式全局值；在没有项目级 `.omp` 的目录中，第三条命令应输出空对象。
