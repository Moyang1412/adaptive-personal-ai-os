# 安装与排错 · Install

[中文首页](../README.md) · [English](../README.en.md)

## 最短路径

已有 Agent 的用户，可以把首页的安装请求与 Skill 文件夹地址交给它，让它先核对自己的加载目录，再安装并报告证据。也可以通过 GitHub 的 Code → Download ZIP 下载仓库，打开 `skills/adaptive-personal-ai-os/`。

**只需把整个 `adaptive-personal-ai-os` 文件夹复制到当前宿主实际扫描的 Skills 根目录。** 保留 SKILL.md、references、agents、LICENSE 和 VERSION；不需要复制根目录文档或 evals。

| Host | 常见用户级根目录 |
|---|---|
| Codex | `~/.agents/skills` |
| Claude Code | `~/.claude/skills` |
| DSH | `~/.agents/skills` 或 `~/.dsh/skills`，以启用的提供方与配置为准 |

`~` 指当前用户目录；Windows 用户可从自己的主目录进入对应隐藏目录。自定义环境、云端环境和组织策略可能不同，必须查看宿主实际配置。安装在一台电脑上，不会安装到另一台电脑或云端。

本版是无额外运行依赖的指令包。**没有 `install.py`、自动记忆脚本、安装诊断器或自动回滚工具。** 不要运行旧预览里提到但仓库不存在的命令。

## 先保护已有配置

已有同名文件夹时，先检查它是否被用户修改，不直接覆盖。把旧副本备份到宿主不扫描的目录，再人工比较和替换公共文件。不要把备份留在 Skills 扫描目录造成重复发现。

安装不需要改写 AGENTS.md、CLAUDE.md、原生记忆、凭据、模型配置或启动项。不要为了安装降低安全设置。私人资料始终放在独立目录。

## 两层验证

**文件层：**确认最终路径是 `<skills-root>/adaptive-personal-ai-os/SKILL.md`，frontmatter 的 name 正确，references 相对链接完整。

**宿主层：**在技能列表或加载记录里找到同名 Skill，检查真实路径，显式调用，再测试自然语言请求和一条不应触发的简单翻译。没有宿主层证据，只能说文件安装完成。

Codex 显式调用 `$adaptive-personal-ai-os`；Claude Code 使用 `/adaptive-personal-ai-os`；DSH 在其当前 Skill 入口选择。版本差异详见[平台适配](../skills/adaptive-personal-ai-os/references/platforms.md)。

## 常见问题

| 现象 | 优先检查 |
|---|---|
| 列表中没有 | 大小写、实际扫描目录、提供方是否启用、是否需要新会话 |
| 加载了旧版本 | 项目级、用户级、旧目录或同步来源中是否存在同名副本 |
| 不能读取私人档案 | 是否授权了确切目录、当前服务与账号、文件系统是否可访问 |
| 新对话失去进度 | 是否实际写入了状态，新的 Agent 是否被明确允许读取 |
| 不停输出长报告 | 用“简短一点”反馈；检查是否加载了旧核心或冲突规则 |
| 回答正确但不见加载记录 | 不宣布激活成功，继续核对宿主证据 |

## English quick reference

Download the repository or delegate installation to your agent. Copy the entire Skill folder to the host's verified skills root. No Python or additional service is required. Review existing copies before replacing them, keep backups outside discovery roots, and never overwrite private context or host settings.

Verify both the files and the host catalog/loader trace. Explicit invocation differs by host. There is no installer, automatic memory engine or runtime doctor in this release.
