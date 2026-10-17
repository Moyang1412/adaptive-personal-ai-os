# 论文与源码驱动的第二轮优化

版本：1.1.0-preview.2；日期：2026-10-18（Asia/Shanghai）。
基线：`10d613235e724b920a066c5d1183e9138620f317`，即 preview.1。
这是有目的的来源筛选与局部源码核对，不是系统综述、完整安全审计或上游复现实验。

## 实际改动

| 缺口 | 落点 | 明确保留的边界 |
|---|---|---|
| 会执行指定公式，不等于会自行选方法 | `learning.md` 加入相近、已学方法的适量混合练习及反馈 | 保留初始讲解、直接帮助和跳过；不强迫无关话题切换 |
| 方案选择要求跨会话，但操作路由可能漏掉要求 | 离线 `RouteRequest` 必填 `persistent_required`，为真时检查已验证的 `cross_session`；合同同步说明 | 非持久检查、清理或导出仍可在其他全部检查通过时路由；不把路由当实际执行 |
| 后续一步失败，被误当成整项失败或自动撤销 | `workflows.md` 分开已完成、不确定和未尝试步骤；从核实状态续接 | 补偿也会失败；保留之后的用户改动，不擅自扩大恢复范围 |
| 搜不到，被误当成已经彻底删除 | `memory.md` 报告已核验的记录、索引或已知派生摘要层 | 不扩大扫描/删除，不复述或重建已忘信息，不保证全局遗忘 |

没有增加运行依赖、记忆数据库、自动课程、外部裁判或自主修改公共 Skill 的机制。
入口仅更新版本，行为改动放在按需读取的四份引用中。

## 论文：读到哪里，采用什么

| 来源 | 已读与可用发现 | 取舍与限制 |
|---|---|---|
| [Rohrer et al., 2020](https://doi.org/10.1037/edu0000367)，[全文](https://gwern.net/doc/psychology/spaced-repetition/2019-rohrer.pdf) | 课堂随机研究的设计、延迟测验与讨论；题型混合让学习者面对方法选择 | 采用“选择与执行分开看”。不据此承诺所有学科、初学者或学习时间都改善；间隔与提取贡献未被完全隔离 |
| [Nakata & Suzuki, 2019](https://doi.org/10.1111/modl.12581)，[作者全文](https://yuichisuzuki.net/wp-content/uploads/2023/04/Nakata-Suzuki-2019-MLJ.pdf) | 英语语法练习的混合安排、练习错误与延迟结果 | 支持不要仅以练习顺畅判断学习；不外推到口语流利度或任意新手门槛，不把更多错误当作必然有效 |
| [Pardos & Bhandari, 2024](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0304013) | 提示生成、人工筛查、实验设计与限制 | 保留现有渐进提示与答案核验。未采用“模型自动提示已经与人工等效”的表述；无延迟迁移，失访与重复题限制解释 |
| [ACE, v1](https://arxiv.org/html/2510.04618v1) | §3 增量上下文更新及 §4 任务评估 | 继续小改动、保留证据与回归检查；不同任务和模型的结果不能变成智序收益。没有接入自动改写 |
| [MemCut, v1](https://arxiv.org/html/2610.21405v1) | 删除基线、来源闭包、残留恢复指标及限制 | 采用“检索失败不是删除证明”。虚构数据及标注来源关系不代表实际提供方具有完整派生追踪；未核验到可运行官方代码 |
| [Memora, v1](https://arxiv.org/html/2604.20006v1) | 有效信息使用与作废信息再次出现的区分 | 现有时效/冲突规则已覆盖，未叠加新记忆机制；评分条件改变须披露 |
| [LoCoMo-Plus, v1](https://arxiv.org/html/2602.10715v1) | 当前问题与早期约束表面不相似时的约束使用 | 保留相关范围与时效，不推导隐式人格画像。该研究不等于长期信念更新或多 Agent 共享评估 |

以上只支持方法取舍；未测智序的真实学习、工作效率、记忆可靠性或生活结果。

## 项目：固定版本与源码核对

以下均为选定文件静态阅读，没有安装或执行上游。公开可读不等于许可已经核实。

| 项目与固定提交 | 读过的关键路径 / 许可 | 实际结论 |
|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph/tree/0eb194fe6093812243de2249e7092029c87c8820) | `libs/langgraph/langgraph/pregel/_loop.py` 的 pending writes 与恢复成功节点路径；MIT | 借鉴保留已完成步骤的恢复方式。历史回放与断点续接不能混为一谈；智序没有实现其检查点引擎 |
| [ACE](https://github.com/ace-agent/ace/tree/82709de050e1db6e6ef2f07bcb0393560b94992a) | `playbook_utils.py`、`LICENSE.txt`；Apache-2.0 | 此快照的 curator 操作只实现 ADD，其他更新/合并/删除仍是 TODO。论文概念不能替代实际 API 能力 |
| [OATutor-GPT-Study](https://github.com/CAHLR/OATutor-GPT-Study/tree/04a6ccd27b0731a5e012a577d795287b320c41c0) | `src/App.js`、`HintSystem.js`、`SubHintSystem.js`、许可说明；软件 MIT，教学内容另为 CC BY 4.0 | 可参考分层提示；两个 hintPathway 在该快照都指向 DefaultPathway，不能宣称仅靠此快照已复现论文全部分组 |
| [Memora](https://github.com/geniesinc/Memora/tree/a6493188efc836d6511ed5e4163fe3ba87da30ff) | `evals/agent_eval/memory_to_answer.py`、根 LICENSE、`data/README.md`；Apache-2.0 | `strict_judges` 可在多裁判不可用时中止，默认允许带警示退回单裁判；两种条件结果不能直接对照论文协议 |
| [LoCoMo-Plus](https://github.com/xjtuleeyf/Locomo-Plus/tree/059f4e3d38f7f1f96765e8e2cb7de3097551bffb) | `evaluation_framework/task_eval/llm_as_judge.py`；固定树未见许可证文件，许可未确认 | 异常解析分支先检查 `correct` 子串，未结构化的 `incorrect` 也可能命中；未知/空标签归零。未复制此评分器，也未据静态问题推断论文结果错误 |

恢复规则另核对了 [LangGraph 官方检查点文档](https://docs.langchain.com/oss/python/langgraph/checkpointers)
与 [Microsoft 补偿事务模式](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction)。
补偿依赖具体业务与并发状态，自身也可能失败；“发起撤销”不能当成“恢复原状”。

## 本轮验证

- 修复前，在相同虚构描述符上，持久 READ/SAVE 的选择结果均为 D，路由却均返回 provider；断言复现失败。新增必填字段前的接口测试错误与该行为失败分开保存。
- 修复后 **112 项单元测试通过**，较基线增加 7 个持久路由测试方法；同进程模拟显式标记非持久要求。未运行真实记忆服务。
- **170 个路由规格**通过格式验证（55 正向、34 负向、81 边界）；增加方法选择与删除验证各 3 项、部分完成 4 项。**12 个提供方规格**通过格式验证。格式通过不等于模型执行这些案例。
- 新会话直接加载固定 Skill 快照，执行 **5 次合成任务**：同一学习输入的前后版本各一次，候选续接一次，候选删除状态说明一次，以及措辞收窄后的受支持整批恢复说明一次。未向执行者提供期待答案。
- 学习两次都正确开始无公式提示的相关练习；没有观察到优劣差异。候选续接只更新实际索引，保留用户备注和原回执；删除说明保留剩余摘要及授权边界。五次满足本次人工检查项；定向恢复说明正确保留原键、原载荷及后续核验，但没有执行真实服务。
- 原始输入、输出、快照哈希、修复前日志及局部文件结果见 [记录](../evals/results/2026-10-18-round2-forward.json)。这是不盲的维护者检查、每例一次、维护期间构造的任务；没有保留独立留出集，没有完整导出的工具轨迹。模型精确标识/采样设置不可取得，宿主指令也参与作用，不能归因于 Skill 或推导统计优势。

复审发现初稿“不要重放整个序列”过于绝对，可能误禁提供方唯一支持的同键同载荷整批恢复。已收窄为避免无谓重复已完成效果，并添加对应边界规格及一次新会话定向检查；先前四次输出保持原快照，不伪装成最终措辞测试。

分发校验：插件 24 个文件，独立 Skill 21 个文件，ZIP CRC、逐文件回读及运行时相对引用闭合通过；构建只在本地进行，未上传额外发布附件。

独立文件校验、发布位置和安装状态以 [验证状态](VALIDATION.md) 及实际 Git 标签为准。
其他设备的自动加载、真正跨会话存储和真实用户效果仍未验证。
