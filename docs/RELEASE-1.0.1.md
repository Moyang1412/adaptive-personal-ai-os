# 智序 1.0.1：Claude 插件适配

日期：2026-10-16。版本号 `1.0.1`，标签 `v1.0.1`。本版增加 Claude 插件分发方式，保留同一公共 Skill 核心、名称与 MIT 许可；v1.0.0 标签、资产和历史验证报告保持原样。

- [GitHub Release](https://github.com/Moyang1412/adaptive-personal-ai-os/releases/tag/v1.0.1)
- [固定版本的 Skill 源码](https://github.com/Moyang1412/adaptive-personal-ai-os/tree/v1.0.1/skills/adaptive-personal-ai-os)
- [Claude 插件指南](CLAUDE-PLUGIN.md) · [直接 Skill 安装](INSTALL.md) · [1.0.0 历史记录](RELEASE-1.0.0.md)

## 变化

- 新增插件 `zhixu` 和仓库市场 `zhixu-skills`。Claude Desktop / Cowork 可添加仓库 `Moyang1412/adaptive-personal-ai-os`，再安装插件；也可上传独立插件 ZIP。
- 提供 `zhixu-1.0.1-plugin.zip`、`zhixu-1.0.1-skill.zip`、两个包各自的文件 manifest 和 `SHA256SUMS`。插件 ZIP 含 `.claude-plugin/` 与 `skills/`；Skill ZIP 含单个 `adaptive-personal-ai-os/` 目录。
- 缩短入口 frontmatter 的 description，并更新版本元数据。既有学习、生活、计划、决策和记忆工作方法保持不变。
- 文档补充桌面安装、Claude Code 命令和入口切换。同一宿主只启用裸 Skill 或插件其中之一。

没有新增 hooks、MCP 服务、后台任务、记忆引擎或权限授权，也不携带私人档案、聊天记录、凭据或评测数据。Python 只用于维护者打包，使用者无需为插件安装 Python。

## 检查与适用边界

文件和分发检查应分别核对插件与市场 JSON、Skill frontmatter、版本一致性、本地相对引用、ZIP CRC、逐文件 SHA-256 与公开包范围。下载时用 `SHA256SUMS` 核对资产，再用 manifest 对照包内文件；哈希清单不等于签名认证。

这些检查只证明对应文件与分发结构的情况。实际执行结果由本次构建报告和发布核对记录提供，不能沿用 1.0.0 或更早候选的通过记录。

本版发布前已执行的[检查记录](../evals/results/release-1.0.1.json)：

| 检查 | 实际结果 |
| --- | --- |
| 插件与市场清单 | Claude Code 2.1.280 严格验证均通过，无错误或警告 |
| 路由与 provider 规格格式 | 85 条与 8 条通过，仅格式验证 |
| 离线参考和记忆夹具 | 23 项测试通过，不是真实 provider 验收 |
| 两种 ZIP | 插件 21 项、Skill 18 项，18 个核心文件一致，CRC 与逐文件哈希通过 |
| 独立无 Git 构建与重建 | 归档基线叠加待提交文件后可构建，重复构建的 6 个公共附件逐字节一致 |
| 隔离 Claude Code 安装 | 从本地市场安装后列出 `zhixu@zhixu-skills`、1.0.1、enabled；未运行模型会话 |

正式提交归档的包、源提交与分发校验信息随 Release 提供。目录或清单通过不表示 Claude Desktop 已安装或已激活。

**尚未实机验收：**Claude Desktop / Cowork 的真实识别、启用、会话加载与路由，以及组织策略下的可用性。Claude Code、Codex、DSH 的真实多轮行为和学习、生活效果也不能由插件结构检查推得。发布和资产下载回读不表示这些未知项目通过。

## 升级与回退

升级前核对实际加载路径，把已有公共 Skill 副本备份到宿主不扫描的目录。保留私人资料和宿主设置。切换插件后停用旧入口，并在新会话检查实际发现与加载；回答合理本身不是激活证据。

需要回退时停用 `zhixu`，恢复原公共副本，或重新安装 [v1.0.0 Skill](https://github.com/Moyang1412/adaptive-personal-ai-os/tree/v1.0.0/skills/adaptive-personal-ai-os)。不覆盖私人配置或记忆，不同时启用两个入口。本版不提供自动回滚或已安装副本的自动升级。
