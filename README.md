<div align="center">

# 智序 · ZhiXu

**同一套方法，你自己的记忆，不同的 Agent。**

Adaptive Personal AI OS · **v0.3.0 Preview**

[开始使用](#开始使用) · [实际场景](docs/EXAMPLES.md) · [私人记忆](docs/MEMORY.md) · [验证状态](docs/VALIDATION.md) · [English](README.en.md)

</div>

---

**直接说你想做什么，不必先学一套提示词。**

智序是一份可安装的 Agent Skill。它帮助你的 Agent 分清“替我完成”和“教我学会”，在需要时读取你授权的背景，并把值得保留的进度写到你自己的文件中。

不是新模型，不是独立 App，也不是全自动人生管家。

## 先看它怎么帮你

| 你说的话 | 智序的目标行为 |
|---|---|
| **“我想学摄影。”** | 先看用途和基础，参考合适课程，开始一个小练习。 |
| **“继续昨天的项目。”** | 读取真实状态，找到下一步；不把计划当成完成。 |
| **“一个终身受益的小习惯，不谈工作。”** | 尊重生活问题的边界，不自动推荐项目交付。 |
| **“记住我喜欢先给结论。”** | 按授权保存到私人档案；不改公共 Skill。 |
| **“这是朋友的经历，不是我的。”** | 纠正信息归属，不再据此推断你本人。 |

以上是待检验的行为要求，不是所有模型都能稳定做到的保证。[查看完整对话示例 →](docs/EXAMPLES.md)

## 开始使用

已有 **Codex、Claude Code 或 DSH** 即可尝试；核心不需要额外服务器、API 密钥或 Python。

**把下面这段交给你自己的 Agent：**

```text
请安装智序 Skill：
https://github.com/Moyang1412/adaptive-personal-ai-os/tree/main/skills/adaptive-personal-ai-os
先检查当前 Agent 的技能目录和已有同名版本。
不要覆盖个人配置、记忆或其他 Skill。
安装后报告实际路径，并用技能列表或加载记录核对是否生效。
```

这是交给有相应工具和权限的 Agent 的安装请求，不是保证每个平台都支持的一键命令。也可以下载仓库，手动复制整个 Skill 文件夹。

| Agent | 文档列出的用户级目录 | 显式调用 |
|---|---|---|
| Codex | `~/.agents/skills/` | `$adaptive-personal-ai-os` |
| Claude Code | `~/.claude/skills/` | `/adaptive-personal-ai-os` |
| DSH | `~/.agents/skills/` 或 DSH 配置的目录 | 从当前界面的 Skill 列表选择 |

**本版完成文件与文档层适配，三款 Agent 的实机行为仍待验收。** 自定义安装位置和组织策略可能不同。[完整安装与排错 →](docs/INSTALL.md)

安装后直接试：**“智序，我想学一个新东西，先带我开始第一步。”**

> 回答看起来正确，不代表 Skill 已经加载。先核对实际技能列表、文件路径或加载记录。

## 同样的 Skill，不同的个人体验

```text
公开 Skill：通用方法和流程
          ＋
你的私人档案：偏好、目标、学习进度、项目状态
          ＋
当前 Agent：它实际拥有的模型、工具和权限
```

**无需配置也能先用。** 需要长期连续性时，再选择“不保存”“确认后保存”或“授权低敏日常积累”。已有背景优先复用，不扫描全部历史，不强迫重新介绍自己。

私人资料留在使用者指定的独立目录。换 Agent 时可以授权它读取同一份档案；换模型服务或账号时，需要重新明确共享范围。公共 Skill 升级不应覆盖个人资料。

**当前使用宿主的读写能力和 Markdown 档案，没有独立记忆数据库、自动同步、原生历史导入器或代码级权限控制。** [如何保存、纠错、遗忘 →](docs/MEMORY.md)

## 学习要有依据，也要看你真的会不会

**明确目标 → 核对课程 → 小诊断 → 练习与反馈 → 独立新题 → 延迟复测 → 调整路线**

采用有研究依据的方法，不代表这份 Skill 已证明能提高学习成绩。不会保证最优路线，也不会把“AI 帮你做对了”算成“你学会了”。[学习协议与研究依据 →](skills/adaptive-personal-ai-os/references/learning.md)

## 继续了解

| 指南 | 解决什么问题 |
|---|---|
| [安装与排错](docs/INSTALL.md) | 装在哪里、怎么确认、如何升级 |
| [实际场景](docs/EXAMPLES.md) | 学习、生活、项目、记忆纠错怎样衔接 |
| [私人记忆](docs/MEMORY.md) | 谁能读、记什么、怎么改和删除 |
| [架构](ARCHITECTURE.md) / [升级](UPGRADING.md) | 公共规则与个人资料怎样分开 |
| [验证报告](docs/VALIDATION.md) / [评测](evals/README.md) | 实际检查过什么，哪些仍然待验 |
| [安全](SECURITY.md) / [贡献](CONTRIBUTING.md) | 风险边界与参与方式 |

**MIT License · 无后台服务 · 无内置遥测 · 非 OpenAI、Anthropic 或 DeepSeek 官方项目。**
