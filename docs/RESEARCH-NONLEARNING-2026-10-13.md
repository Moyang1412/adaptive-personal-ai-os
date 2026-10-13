# 智序非教学模式：研究与本地改进

检索日期：2026-10-13。本轮查看了 6 个相关 GitHub 实现、8 篇主要论文，以及 2 份工程指南。阅读深度见下表，并非每篇逐页精读，也没有运行这些外部项目。

结论：现有工作足以支持一些可检验的设计改进，不能证明智序已经提高了真实用户的效率。采用的共同方向是：少做无关收集，先解决当前问题；判断绑定来源和适用条件；通过实际结果校正。保留双模式教学，本轮扩展计划、决策、研究、复盘、沟通、项目续接与记忆。

本轮只改本地维护源码；版本仍为 `0.4.0-preview`，未提交、发布或替换已安装副本。原始行为输出与验证边界见 [验证报告](VALIDATION-NONLEARNING.md)。

## GitHub 上哪些值得借鉴

以下链接固定到查看文件的提交版本。提交时间不等于整个项目最后更新时间，也不构成维护质量或产品效果评级。

| 实现及本轮阅读入口 | 可以用于智序的机制 | 不直接采用的部分 |
|---|---|---|
| [LifeOS，原 PAI：Algorithm](https://github.com/danielmiessler/LifeOS/blob/5e2f2e8c0abde612da0e99c16c0d07d4ec21b88c/LifeOS/install/LIFEOS/ALGORITHM/v8.20.2.md)、[Evals](https://github.com/danielmiessler/LifeOS/blob/5e2f2e8c0abde612da0e99c16c0d07d4ec21b88c/LifeOS/install/skills/Evals/SKILL.md)、[TELOS](https://github.com/danielmiessler/LifeOS/blob/5e2f2e8c0abde612da0e99c16c0d07d4ec21b88c/LifeOS/install/USER/TELOS/README.md)；2026-09-04 提交 | 从目标推出可检查的完成条件；区分缺证据和失败；复用已有目标信息 | 完整基础设施、每次强制长流程、把未经确认的个人推断写入记忆 |
| [Fabric：计划风险分析](https://github.com/danielmiessler/fabric/blob/177b3a9d284895c907d6eb3a64937d174add4cd5/data/patterns/t_threat_model_plans/system.md)、[思路审查](https://github.com/danielmiessler/fabric/blob/177b3a9d284895c907d6eb3a64937d174add4cd5/data/patterns/t_red_team_thinking/system.md)；2026-10-10 提交 | 按任务找失败条件和遗漏约束 | 固定数量、固定词数的输出；为了批判而制造问题；假设已经了解用户全部背景 |
| [LangMem：结构化记忆提取与更新](https://github.com/langchain-ai/langmem/blob/0b664e9736e15d13bfc53a249f73175aec3027c6/src/langmem/knowledge/extraction.py)；2025-07-09 文件提交 | 比较已有记录后再判断新增、更新或删除；按主体和范围组织 | 不安装新记忆引擎；不从隐含线索推断稳定人格，不虚构精确置信概率 |
| [Letta Code：Agent 提示与记忆分层](https://github.com/letta-ai/letta-code/blob/ceb7ec8911b3ad476fb71a6f23e24aa9c6ff5722/src/agent/prompts/letta.md)；2026-09-26 文件提交 | 短摘要作为索引，必要时回到外部详细记录 | 不把已存记忆当成可信指令；自主记忆架构不能替代用户授权 |
| [Mem0：提取与更新提示](https://github.com/mem0ai/mem0/blob/a488e19044e4de9322a4e82be8d49ee67a322151/mem0/configs/prompts.py)；2026-04-14 文件提交 | 区分用户陈述与助手建议；保留原始来源，处理相对时间与变化 | 不采用“提到就默认保存”、广泛收集或把私有来源改称公开互联网的提示；代码中不同提示版本不能混成一个行为结论 |
| [Anthropic Skills：skill-creator](https://github.com/anthropics/skills/blob/b0cbd3df1533b396d281a6886d5132f623393a9c/skills/skill-creator/SKILL.md)；2026-03-06 文件提交 | 同任务比较旧版和新版，查看原答复；可行时隐藏版本盲评；同时检查质量与负担 | 不把自评通过当成效果研究，不照搬其宿主工具、必装组件或全部工作流 |

这是机制层面的原创改写，没有复制这些项目的实现、提示全文或用户资料。外部 README 和源码只能说明设计或实现；本轮未验证外部软件的运行质量、隐私保障或部署适用性。未来复制代码或实际集成前，应单独检查许可证、依赖、数据去向和目标宿主能力。

## 论文给了什么依据

| 原始研究与阅读范围 | 可支持的设计 | 推断边界 |
|---|---|---|
| Gollwitzer & Sheeran，2006，[实施意图元分析](https://doi.org/10.1016/S0065-2601(06)38002-1)，相关全文；[机构书目入口](https://www.socmot.uni-konstanz.de/publications/implementation-intentions-and-goal-achievement-meta-analysis-effects-and-processes) | 对启动或遗忘障碍，将已有目标连接到明确情境与可行动作 | 人类研究不是 AI 计划产品试验。若缺时间或资源，增加“如果……就……”不能弥补；不能把效应量解释成效率百分比 |
| Buehler、Griffin & Ross，1994，[计划谬误](https://doi.org/10.1037/0022-3514.67.3.366)，研究 4 和讨论；[全文](https://homepages.se.edu/cvonbergen/files/2013/01/Exploring-the-Planning-Fallacy_Why-People-Underestimate-Their-Task-Completion-Times.pdf) | 使用可比任务的实际耗时、时间范围和后续误差反馈 | 减少乐观偏差不等于降低所有绝对预测误差；不据此规定统一的 1.5 倍估时系数 |
| Tannenbaum & Cerasoli，2013，[复盘元分析](https://doi.org/10.1177/0018720812448394)，相关全文；[全文](https://cebma.org/assets/Uploads/Tannenbaum-Cerasoli.pdf) | 围绕具体事件，对比预期和实际，引入外部结果，选择可操作调整 | 研究包含参与者主动复盘；被动阅读 AI 总结不等同于该干预。不能承诺智序提高某个百分比的绩效 |
| [LongMemEval，ICLR 2025](https://arxiv.org/html/2410.10813v2)，方法和实验；[仓库](https://github.com/xiaowu0162/LongMemEval) | 将跨记录整合、事件时间、知识更新和证据不足时不猜测分开评估 | 长对话记忆基准不是现实个人管理效果；检索到记录和回答正确需要分别检查；模型判分仍需校核 |
| [LongMemEval-V2 / AgentRunbook，2026 预印本](https://arxiv.org/html/2605.12493v1)，机制和实验；[仓库](https://github.com/xiaowu0162/LongMemEval-V2) | 当前状态、工作流和环境条件一起看；用简短记录索引支撑证据查找 | 属于实验性结果；文件记忆可能增加查询耗时，不照搬完整框架，不据此宣称跨宿主可靠 |
| [Lost in the Middle，TACL 2024](https://aclanthology.org/2024.tacl-1.9/)，相关全文 | 减少无关上下文；测试证据位于开头、中间、末尾时的表现 | 结果取决于被测模型和任务；不能宣称所有 2026 年模型都存在相同程度的问题 |
| [SkillsBench，2026 预印本](https://arxiv.org/html/2602.12670v1)，方法、讨论和限制 | Skill 改动需要任务结果对照；增加规则并不必然获益；保留无增益和负向案例 | 主要为容器内终端任务；模型、框架、任务选择、随机性与潜在污染均限制外推，不能把平均分提升移植成智序收益 |
| Huang 等，[Large Language Models Cannot Self-Correct Reasoning Yet，ICLR 2024](https://arxiv.org/abs/2310.01798)，[正文](https://arxiv.org/pdf/2310.01798)的方法与限制 | 优先检查实际结果和外部反馈，不将反复自我批评或模型间一致当成正确证据 | 检验的是当时模型与特定推理设置；不是所有后续模型都无法自纠错的断言 |

本轮主要采纳方向一致的机制，没有基于论文数量投票，也没有把不同研究的效应量合并成智序效果。书目或摘要支持的内容不能超出已读正文；未进行系统综述、偏倚风险全面评级或复现实验。

## 工程指南的用途

- Anthropic 的 [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)（2024-12-19）：从简单流程开始，让额外复杂度有明确用途，以环境结果提供反馈。
- Anthropic 的 [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（2026-01-09）：区分 Agent 自述与环境实际结果，检查轨迹、重复试验与评分器局限。

两者是供应商工程经验，不是智序的对照效果研究。本轮使用其评估思路，不把品牌或工程文章当成科学验收。

## 已落到 Skill 的改动

| 范围 | 用户可见变化 | 实际入口 |
|---|---|---|
| 计划 | 先看时间、依赖和资源能否容纳任务；不足就缩范围或调整安排；被打断后按剩余时间续接 | [planning-decisions.md](../skills/adaptive-personal-ai-os/references/planning-decisions.md) |
| 决策 | 先排除违反硬约束的选项，再看什么未知信息会改变选择；不强迫填写评分表 | [planning-decisions.md](../skills/adaptive-personal-ai-os/references/planning-decisions.md) |
| 研究 | 区分论文发现、实现自述、源码和本地实测；给出适用范围与未核实项，检索达到目的就停止 | [research.md](../skills/adaptive-personal-ai-os/references/research.md) |
| 记忆 | 分清事件时间和写入时间、建议和完成事实；有冲突回查来源，没找到不等于从未发生 | [memory.md](../skills/adaptive-personal-ai-os/references/memory.md) |
| 续接、复盘、沟通 | 交接须对照当前文件；复盘只提出证据支持的原因和可验证调整；直接提供所需草稿，保持发送授权边界 | [workflows.md](../skills/adaptive-personal-ai-os/references/workflows.md) |
| 入口与负担 | 新增按需路由，普通请求不先加载全部模式；不强制档案、问卷、文件或模式菜单 | [SKILL.md](../skills/adaptive-personal-ai-os/SKILL.md) |
| 评估 | 原有 50 条规格保留，新增 17 条非教学正例、负例、边界，其中 2 条来自本轮合成试用发现的问题；同任务对照并记录无增益和问题 | [evals/README.md](../evals/README.md)、[用例](../evals/routing-cases.md) |

新增规则仍由模型解释执行，并没有增加数据库、自动记忆同步、确定性授权服务或调度引擎。是否更科学，要看推断是否遵守证据；是否更高效，还需要同时观察任务质量、用户负担、工具消耗和耗时。[本轮验证报告](VALIDATION-NONLEARNING.md)不以文件增加或测试格式通过代替这些结果。
