# 智序（ZhiXu）· Adaptive Personal AI OS

一个面向 Codex 的通用个人 AI 工作流 Skill。它把自然语言请求路由到计划、研究、决策、学习、写作、工程、验证、记忆和人工审批流程，并通过项目状态文件和反馈复盘持续改进。

**Adaptive Personal AI OS** 是本项目的英文名；中文名为 **自适应个人智能操作系统**。这里的 “OS” 是工作流架构的比喻：它负责理解目标、调用合适的方法、复用上下文、推动行动并根据反馈演进，不是一个新的操作系统发行版。

**智序（ZhiXu）** 是项目的日常别名。“智”代表理解、学习、判断和 AI；“序”代表路由、步骤、状态、复盘和持续演进。公开仓库和 Codex Skill 使用稳定的技术标识 `adaptive-personal-ai-os`，便于安装、搜索和自动调用。

This is a general-purpose Codex Skill for building a personal AI operating system. It is designed to reuse context, route mixed requests, support project onboarding, preserve human approval boundaries, and turn repeated feedback into scoped improvements.

## 它解决什么问题

普通 AI 对话往往每次从零开始：给出一个答案，却不记录状态，也不区分“帮我完成”和“教我学会”。这个 Skill 提供一套轻量协议：

- 先识别目标、约束、风险和当前状态；
- 根据任务选择总台、研究、决策、教练、工程、验证或红队模式；
- 复杂任务拆成可执行动作和完成定义；
- 让用户在需要长期能力的领域主动尝试并接受反馈；
- 将项目事实保存在用户自己的工作区，而不是硬编码进 Skill；
- 通过复盘和小范围实验升级规则，不因一次成功就改变全局行为。

## 适用范围

适合跨领域的个人工作流，例如生活安排、项目管理、学习、研究、决策、关系沟通、健康信息整理、资源规划、写作和 Codex 工程协作。它不提供托管服务、数据库、账号连接或自动访问个人数据，也不替代医疗、法律或财务专业意见。

对于孤立的一次性代码问题、翻译、文档排版、表格处理或事实查询，优先使用更具体的 Skill；只有用户明确要求使用个人 AI OS，或任务需要跨领域上下文、状态复用和审批流程时，才启用本 Skill。

## 安装到 Codex

最简单的安装方式是：克隆仓库，把 Skill 目录复制到 Codex 的 Skills 目录，然后重新加载或重启 Codex。

### macOS / Linux

```bash
git clone https://github.com/Moyang1412/adaptive-personal-ai-os.git
cd adaptive-personal-ai-os
skill_root="${CODEX_HOME:-$HOME/.codex}/skills/adaptive-personal-ai-os"
mkdir -p "$skill_root"
cp -R skills/adaptive-personal-ai-os/. "$skill_root/"
```

### Windows PowerShell

```powershell
git clone https://github.com/Moyang1412/adaptive-personal-ai-os.git
Set-Location adaptive-personal-ai-os
$codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$skillRoot = Join-Path $codexRoot "skills\adaptive-personal-ai-os"
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
Copy-Item -Recurse -Force "skills\adaptive-personal-ai-os\*" $skillRoot
```

如果已经下载或解压仓库，可以跳过 `git clone`，在仓库根目录运行复制部分即可。`CODEX_HOME` 已经设置时，安装位置会自动跟随它；否则使用默认的 `~/.codex/skills`。

如果你的 Codex 使用其他 Skill 安装器，直接安装 `skills/adaptive-personal-ai-os` 目录即可。这个仓库不要求额外运行时、API 密钥或第三方服务。

### 安装后自检

重启或重新加载 Codex 后，直接发送下面这句话：

```text
用智序帮我安排今天最重要的三件事，先给结论和下一步。
```

如果它能先识别目标、时间和约束，再给出 1—3 个优先动作，说明 Skill 已经被加载。也可以显式写出 `$adaptive-personal-ai-os`，用于排查自动触发是否生效。

## 使用方式

不需要复制长提示词，也不需要记住固定格式。直接说你想达成的结果即可；Skill 会根据语义选择工作模式。

### 口语化请求

```text
我想学会做产品，先判断我现在的水平，再给我第一步练习。
```

```text
新项目：路径是 xxx，目标是做一个本地工具，先只读接入并建立项目地图。
```

```text
帮我在两个方案里做决定，结合时间、预算、最坏情况和可逆性。
```

```text
交给 Codex：修改这个项目的登录流程，不要改数据库结构，完成后跑现有测试。
```

下面这些前缀是可选的快捷方式，不写也能自动路由：`总台：`、`项目：`、`研究：`、`决策：`、`教练：`、`红队：`、`交给 Codex：`、`让验证器检查：`、`复盘：`、`写回状态：`。

### 直接程度和回答长度

可以在自然语言里告诉它你希望参与到什么程度：

| 你可以这样说 | 默认行为 |
|---|---|
| “直接给我结果” / “先替我做完” | 顾问或执行模式，优先交付可用结果 |
| “教我” / “让我真正学会” | 教练模式，先诊断，再练习、反馈和复测 |
| “只给我下一步” / “简洁一点” | 输出行动卡或短结论，减少解释 |
| “详细分析” / “给我研究报告” | 输出证据、假设、反方意见和验证方法 |
| 没有特别说明 | 简单任务保持简短；复杂任务按结论、依据、优先级、下一步、验证和风险组织 |

如果任务需要修改文件、访问外部服务或对外发布，Skill 会把范围、完成定义和需要批准的动作说清楚；用户不必先写一段复杂提示词。

## 可选状态文件

Skill 不会假装拥有用户背景。用户可以在自己的工作区建立以下文件；不存在时，系统必须明确说明没有读取到：

```text
PERSONAL_CONTEXT.md   # 用户主动提供的稳定偏好和长期约束
PROJECT_INDEX.md      # 项目清单、负责人、状态和下一步
项目目录/AGENTS.md    # 项目专属工作规则
项目目录/STATUS.md    # 当前事实、阻塞和证据
项目目录/HANDOFF.md   # 下一次继续所需的交接信息
项目目录/DECISIONS.md # 已确认决定和理由
```

可以从 `templates/project/` 复制起始模板。敏感的关系、健康、财务和凭据内容默认不写入长期状态，除非用户明确要求并了解保存范围。

## 推荐的最小配置

把模板复制到你自己的工作区即可开始；不需要先写长提示词：

```text
你的工作区/
├── WORKFLOW_PROFILE.md      # 从 templates/WORKFLOW_PROFILE.md 复制，可选
├── PERSONAL_CONTEXT.md      # 从 templates/PERSONAL_CONTEXT.md 复制，可选
├── PROJECT_INDEX.md         # 从 templates/project/PROJECT_INDEX.md 复制，可选
└── 你的项目/
    ├── AI_OS_ADAPTER.md     # 从 templates/project/AI_OS_ADAPTER.md 复制
    ├── AGENTS.md
    ├── STATUS.md
    ├── HANDOFF.md
    └── DECISIONS.md
```

`WORKFLOW_PROFILE.md` 管协作偏好，`PERSONAL_CONTEXT.md` 管用户主动保存的背景，
`AI_OS_ADAPTER.md` 管单个项目的术语、命令和完成定义。它们不会自动写入 Skill，
也不应提交到公开仓库。完整分层、隐私隔离和升级流程见 [ARCHITECTURE.md](ARCHITECTURE.md)
与 [UPGRADING.md](UPGRADING.md)。

### 可选的最小初始化

第一次使用时，可以只建立一个个人上下文文件和一个项目状态文件。把下面的路径替换成你实际使用的工作区：

```bash
workspace_dir="/path/to/your/workspace"
cp templates/PERSONAL_CONTEXT.md "$workspace_dir/PERSONAL_CONTEXT.md"
cp templates/project/PROJECT_INDEX.md "$workspace_dir/PROJECT_INDEX.md"
```

也可以把这些文件放在某个项目目录中。没有这些文件时，Skill 仍然可以工作，但会明确告诉你没有读取到长期背景或项目状态，不会自行猜测。

## 设计原则

- 稳定内核与项目适配器分离；
- 理论优先看证据、适配性和可验证性，不堆砌最新名词；
- 教练模式培养独立能力，顾问模式提供直接判断，执行模式完成已授权工作；
- 多步骤流程由状态和阶段控制，不依赖一段提示词保证顺序；
- 高风险、破坏性或对外动作必须先给出可审阅结果并等待用户批准；
- 失败、纠正和回归优先形成局部改进，只有有证据时才升级为全局规则。

## 隐私与安全

这是提示词和工作流文件，不是数据收集服务。仓库不包含用户个人背景、项目私密信息、凭据或生产日志。使用者应当：

- 不把 API 密钥、Token、Cookie、密码、私有路径或私人对话提交到仓库；
- 将个人状态文件放在自己的工作区，而不是公开仓库；
- 对 shell、文件、网络、浏览器和外部工具使用最小权限；
- 发布、部署、付款、删除、合并和对外发送前保留人工审批；
- 对医疗、法律、财务和安全事项查阅可靠的一手资料并寻求专业帮助。

本项目不是 OpenAI 官方产品，也不代表任何模型或平台的保证。

## 贡献

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。提交前至少检查：Skill 触发范围、负向触发、隐私泄露、审批边界和 `python evals/validate_routing_cases.py` 结果。不要提交真实个人上下文、私有仓库信息、凭据或生产日志。

## 许可证

本项目采用 MIT License，见 [LICENSE](LICENSE)。
