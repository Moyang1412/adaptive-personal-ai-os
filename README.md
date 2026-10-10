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

把 `skills/adaptive-personal-ai-os` 复制到 Codex 的 Skills 目录，然后重新加载或重启 Codex。

### macOS / Linux

```bash
skill_root="${CODEX_HOME:-$HOME/.codex}/skills/adaptive-personal-ai-os"
mkdir -p "$skill_root"
cp -R skills/adaptive-personal-ai-os/. "$skill_root/"
```

### Windows PowerShell

```powershell
$codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$skillRoot = Join-Path $codexRoot "skills\adaptive-personal-ai-os"
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
Copy-Item -Recurse -Force "skills\adaptive-personal-ai-os\*" $skillRoot
```

如果你的 Codex 使用其他 Skill 安装器，直接安装 `skills/adaptive-personal-ai-os` 目录即可。这个仓库不要求额外运行时、API 密钥或第三方服务。

## 使用方式

不需要复制长提示词。自然语言即可：

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

需要明确模式时可使用：`总台：`、`项目：`、`研究：`、`决策：`、`教练：`、`红队：`、`交给 Codex：`、`让验证器检查：`、`复盘：`、`写回状态：`。

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

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。提交前至少检查：Skill 触发范围、负向触发、隐私泄露、审批边界和 `quick_validate.py` 结果。不要提交真实个人上下文、私有仓库信息、凭据或生产日志。

## 许可证

本项目采用 MIT License，见 [LICENSE](LICENSE)。
