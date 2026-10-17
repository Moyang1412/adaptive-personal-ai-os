# 记忆方案接入与迁移

[返回首页](../README.md) · [Provider contract](../skills/adaptive-personal-ai-os/references/provider-contract.md) · [English guide](PROVIDERS.en.md)

智序先使用当前 Agent 的原生记忆和已授权的相关背景。首次确实需要跨会话连续性时，先评估记忆方案；在当前范围复用选择结果。仍需连续性且宿主、账号、范围或能力实质变化时，只复查受影响部分，不会每次聊天重复询问。

## 四个选择

| 选项 | 适用条件 | 行为 |
|---|---|---|
| A 原生记忆 | 原生能力覆盖本次范围 | 继续使用宿主原生记忆，不增加 provider |
| B 原生记忆 + 私人档案 | 明确需要跨 Agent，私人档案所需操作、范围与有效版本/锁保护均有验证依据 | 原生记忆继续归宿主，精选记录才进入私人档案 |
| C 已安装的成熟 provider | 有明确缺口，并且 provider 已安装、启用、可调用、许可证和维护状态清楚，隔离测试通过 | 只把授权范围的记录交给该 provider |
| D 暂不使用额外记忆 | 没有缺口、没有权限、provider 未验证，或用户不想保存 | 不创建或调用额外引擎 |

候选参考实现新增private_profile_verified_capabilities，默认空集合；只授权档案和声明冲突控制，不再被当作B方案已具备能力。需要核对的是档案本身的所需操作与范围保护，不能借用原生记忆的可用性。验证可以复用当前仍有效的证据，不要求每次新建测试或重复授权。

安装了 Skill、看到了官方文档或知道某个项目存在，都不能单独证明 provider 可用。每个 provider 需要报告名称、版本、位置、本地/联网、能力、存储位置、许可证、维护状态、接口和证据等级。字段定义见 [provider contract](../skills/adaptive-personal-ai-os/references/provider-contract.md)。

多个已验证provider都满足要求时，还要比较真实任务适配、现有选择、存储/联网条件和已知成本；不能按名字或热度宣称最好。参考模块会返回D及候选ID，表示尚未选择额外引擎，而不是擅自启用第一个；候选排序只用于稳定展示。缺少影响决定的条件时，继续能独立完成的任务。

## Adapter 接入清单

1. 先描述当前环境，不扫描全部历史、主目录、凭据或聊天记录。
2. 分开记录“文档声称”“已安装”“已启用”“当前会话可调用”“隔离测试通过”。
3. 对目标能力做合成数据测试：保存、新会话读取、更正、再次读取、删除、删除后确认不再使用。
4. 确认范围隔离、导出/导入边界、联网条件和删除语义。
5. 为每类记录指定唯一来源。共享范围必须有单写入者或 provider 自己的版本/锁保护。
6. 让用户确认选项、范围、目标账号和迁移记录后，才执行写入或迁移。

## 方案何时需要重看

原选择仍适用时直接复用，不每轮重新问。确实需要长期连续性，且宿主、模型服务/账号、范围或可调用能力发生实质变化时，只重查受影响的部分；换客户端本身不授权把旧资料交给新服务。

记忆服务暂不可用时，可以从当前已授权资料继续任务，未完成的保存明确记为未完成。不自动换服务写入，不建立第二套档案，也不删除旧记录；需要时先给可带走的最小续接草稿。能力恢复和权限仍有效后，再继续原范围内的持久操作。

## 迁移与停用

切换 provider 时，先停止旧 provider 的写入，再读取用户明确选择的记录，核对目标范围和来源，写入新 provider，并回读目标记录、确认旧 provider 不再写入。迁移许可不自动包含删除源记录；删除需另有明确范围和宿主要求的确认，不能把迁移工具的清理建议当成授权。没有授权迁移的记录保持在原处，不把全部历史复制到新库。

停用额外 provider 后，新的读写请求回退到原生记忆或选项 D。旧 provider 不应继续写入；已经进入旧会话或云端模型上下文的内容不会因为停用自动消失，需要分别处理。

用户可以随时要求 Agent 展示当前方案、provider 版本、数据位置、已保存记录和共享范围；更正或删除单条/全部记录；停用额外 provider；导出并迁移明确授权的记录；撤销跨 Agent 共享。每次操作都要报告实际结果，权限不足时只能报告未执行。

本地保存不代表内容永远不会离开设备。Agent 将记录加入云端模型上下文时，相关内容可能发送给模型服务商。不要保存密码、密钥、验证码；健康、关系和财务信息默认不长期保存。

本仓库只提供判断、路由、授权和边界说明，以及一个无副作用的评估参考模块。它不包含数据库、向量检索、自动导入、自动同步或后台记忆服务。没有成熟 provider 时，优先选择 D；手工 Markdown 只是最小文件型备用记录，不是完整记忆引擎。


## 源码审查候选 / Source-reviewed candidate

[MCP Memory review](MCP-MEMORY-REVIEW.md) records a pinned source inspection, concrete scope/concurrency limits and what remains untested. It is not an installation or recommendation of a currently available provider.

[Mem0 source review](MEM0-REVIEW.md) examines model/embedding calls, inference-driven mutations and operation-specific scope checks in a pinned Python-library version; it is not live acceptance.


## 根据现有环境缩小候选，而不是按热度安装

| 已核对对象 | 适合进一步评估的实际缺口 | 接入前仍需证明 |
|---|---|---|
| [MCP Memory](MCP-MEMORY-REVIEW.md) | 已有MCP宿主，需要小型本地图谱记录 | 明确文件/读取范围、关联端点、确切版本的并发行为 |
| [Mem0](MEM0-REVIEW.md) | 确实需要事实提取与语义检索 | 完整模型/embedding成本与去向、推断的更新/删除、各操作授权 |
| [LangMem](LANGMEM-REVIEW.md) | 已有LangGraph与store，希望复用记忆构件 | namespace身份绑定、具体允许动作、后端重启持久性和冲突控制 |
| [Letta / MemGPT](LETTA-REVIEW.md) | 已在使用Letta，或明确选择有状态Agent体系 | 当前MemFS与历史V1区别、本地/云端数据路径、共享范围、同步和冲突证据；不是通用即插即用记忆库 |

这是源码审查后的条件清单，不是这些方案都值得安装，更不是当前已验证provider列表。原生能力覆盖需求时，继续用原生能力。

长期记忆需求必须有跨会话能力证据，即使调用者只列出读取或保存；当前对话读得到不等于下次还能用。此要求同样适用于原生记忆、私人档案和外部 provider。

评估参考代码的能力与范围集合只接受列表、元组、set或frozenset中的有效名称，不接受开关字典或字符串。尤其不能把read=false一类字典的键直接当成已验证能力；适配器必须先按真实证据构造集合。类型错误返回ValueError，参考代码仍不执行真实存储操作。
