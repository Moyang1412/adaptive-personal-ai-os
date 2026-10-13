# 智序 1.0.0：首个正式版

日期：2026-10-13。版本号 `1.0.0`，标签 `v1.0.0`，GitHub Release 为正式发布，不标记预发布。0.4.0 及更早版本保留为预览历史。

- [GitHub Release](https://github.com/Moyang1412/adaptive-personal-ai-os/releases/tag/v1.0.0)
- [版本固定的 Skill 源码](https://github.com/Moyang1412/adaptive-personal-ai-os/tree/v1.0.0/skills/adaptive-personal-ai-os)
- [升级说明](../UPGRADING.md) · [安装与排错](INSTALL.md) · [本版检查记录](../evals/results/release-1.0.0.json)

## 本版内容

保留同一个 Skill 名称、MIT 许可与自然语言入口。教学支持默认任务中学习和可选简短诊断，两者共用具体能力与帮助程度的证据标准。计划、决策、研究、记忆、任务续接、复盘及沟通按需要加载对应说明。新增生活参考覆盖日常习惯与家务、普通健康生活、家庭现金流、职业探索、关系与情绪、休闲。

公共包不包含个人档案、自动记忆数据库、银行/健康连接、提醒调度或权限执行服务。正式版是维护与分发标识，不代表所有宿主已经实机验收，也不代表科学效果认证。

## 既有证据与本次版本的关系

- [双入口教学试用](VALIDATION-DUAL-LEARNING.md)、[非教学试用](VALIDATION-NONLEARNING.md)、[生活试用](VALIDATION-LIFE.md)保留原始快照、初始错误及修正记录，不重写成 1.0.0 的行为结果。
- 生活轮有 11 条合成答复，四组匿名对照均持平；非教学轮没有证明新版整体更优。真实学习、生活效果与总体效率尚未建立。
- 发布准备只把根目录 `VERSION`、包内 `VERSION` 和 `SKILL.md` 的版本元数据从 `0.4.0-preview` 改为 `1.0.0`，没有继续调整运行时方法。工作副本内其余 16 个文件与最后候选快照逐字节相同。发布包采用 Git 暂存对象的字节，按仓库既有 `core.autocrlf` 设置归一化换行；该换行处理不当作规则修改，原始试验哈希仍保留。
- [非教学调研](RESEARCH-NONLEARNING-2026-10-13.md)与[生活调研](RESEARCH-LIFE-2026-10-13.md)分别列出来源、核读深度、借鉴与不适用范围。论文、指南和工程实现提供依据，没有证明本 Skill 效果。

## 发布检查

| 检查 | 实际结果与边界 |
|---|---|
| 路由案例格式 | `python -X utf8 evals/validate_routing_cases.py` 退出码 0；85 条规格，30 正例、15 负例、40 边界。不是 85 次模型行为执行 |
| Provider 案例格式 | `python -X utf8 evals/validate_provider_cases.py` 退出码 0；8 条规格，3 正例、4 负例、1 边界。不是真实 provider 验收 |
| 离线参考及内存夹具 | `python -X utf8 -m unittest evals.test_provider_selection evals.test_memory_lifecycle` 退出码 0；23 项测试。不是实机、新进程、跨会话持久化或并发服务证明 |
| 版本与入口结构 | 通过：根目录版本、包内版本及元数据均为 `1.0.0`，官方字段、类型和长度符合规范；16 个其他包内文件未改，入口只改版本元数据 |
| 文件引用与下载包 | 通过：186 处本地相对引用无缺失，包内引用未出包；18 个 ZIP 条目与 Git 暂存源码逐文件字节一致，ZIP 校验通过。不将远程网页或标题锚点说成全部检查 |
| 空白与发布范围 | `git diff --check` 退出码 0；显式选择维护文件，忽略的 `.zhixu/`、私人目录和个人安装不进入提交或下载包 |
| 配置的私密信息检查 | 67 个公开文本文件在配置模式内无发现；检查本地用户名、主目录、私人邮箱及常见凭据模式。不当作完整安全审计或历史匿名化 |

本机通用 `skill-creator/quick_validate.py` 的已知字段兼容性失败仍保留：它拒绝官方允许的 `compatibility` 字段。另作官方规范断言，未修改全局验证器，也未把退出码 1 改记通过。[原始问题](VALIDATION-DUAL-LEARNING.md#验证器兼容性问题)可查。

## 下载、安装与回退

GitHub Release 提供 `zhixu-1.0.0-skill.zip`、`zhixu-1.0.0-manifest.json` 和 `SHA256SUMS`。ZIP 只含单个 `adaptive-personal-ai-os/` 目录下的完整 18 个文件；仓库资料和 evals 使用 GitHub 源码存档获取。

下载后可用 `SHA256SUMS` 核对 ZIP，逐文件清单另列包内 SHA-256。清单不等于签名认证。在线发布成功与资产下载回读的实际结果另保存于 Release 附件，本文不把准备阶段的检查写成已发布事实。

升级前把已有公共副本备份到宿主不扫描的位置，替换公共 Skill 文件，保留用户自己的资料与宿主设置。需要回退时恢复该备份；本版没有自动回滚服务。当前维护操作不替换维护者电脑上已安装的副本。

## 尚未验证

Codex、Claude Code、DSH 的新会话自动发现、实际路由、多轮操作和工具授权边界仍待实机验收。没有真实用户结果、正式统计优势或通用安全保证。本次发布不把这些未知项目改成通过。
