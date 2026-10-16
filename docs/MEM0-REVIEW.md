# Mem0：先核对整个处理链，再谈接入

日期：2026-10-17；源码快照 `0724291bd864cf807e88ee8981c8226644e8fb42`。本页只评估Python开源库中所读路径，不把结论外推为云平台、自托管HTTP服务或其他版本的完整审计。

## 能借鉴的部分

Mem0已有记忆提取、向量检索和保存/更正/删除等接口。确有语义检索需求时，它是比在智序里重新实现一套向量记忆库更值得评估的候选。库代码里的检索和列举使用 `filters` 内的 `user_id` / `agent_id` / `run_id`，新增记录则接受相应顶层参数；应按安装版本实际签名适配，不照抄旧教程。

## 三个不能跳过的事实

1. **本地数据库不代表离线。** 已读配置中，LLM和embedding默认provider均为OpenAI。`infer=False`绕过事实推断，但所读新增路径仍生成embedding；不能称为零模型调用、零费用或不会发送文本。还应核对向量服务、可选reranker和遥测的实际配置。源码中的遥测开关有默认启用行为；本轮未运行或修改它。
2. **“add”不一定只追加。** 默认 `infer=True` 会让模型提取事实并决定新增、更新或删除相关记忆。允许保存一条事实，不自动等于允许任意重写其他记录。接入层必须约束实际可能发生的操作和记录范围；若没有可验证的预览或受控执行边界，不声称已实现逐条授权。非推断模式也只能写入用户明确同意的精选记录，不是整段聊天导入授权。
3. **过滤参数不等于调用者身份验证。** 所读Python库的按ID读取/更新/删除接口与带范围的搜索签名不同。需要在真实适配层或服务端证明调用者不能跨范围使用ID；不能从search带user_id推断所有操作都有访问控制。自托管服务与云产品需单独检查，不能仅凭库接口判定它们的安全性。

## 智序当前取舍

没有在本项目安装Mem0、提供密钥、调用模型、创建向量库、读取私人历史或启用后台服务。目前仍是源码审查候选，不能列为当前宿主可用的C方案。原生记忆够用时继续A；缺少权限或验证时选择D。

实际考虑接入时，先确认缺口与预算/联网条件，再用独立合成数据验证具体版本：相同事实的新增与更正、同名不同主体、跨范围ID访问拒绝、推断产生更新/删除的范围、删除后读取，以及服务错误时是否发生部分写入。费用和数据去向以完整处理链为准，不以数据库部署位置推断。

## 已读来源

- [Memory实现：新增、检索及按ID操作](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/memory/main.py)
- [总配置](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/configs/base.py)
- [LLM默认配置](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/llms/configs.py)
- [Embedding默认配置](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/embeddings/configs.py)
- [遥测开关实现](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/mem0/memory/telemetry.py)
- [README对库、自托管和云产品的区分](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/README.md)
- [Apache-2.0许可证](https://github.com/mem0ai/mem0/blob/0724291bd864cf807e88ee8981c8226644e8fb42/LICENSE)

未复制代码或提示文本，未运行上游测试；源码阅读不证明真实运行行为、模型事实提取质量或某个已发布包的能力。

## English summary

Pinned Python-library source review only. Default LLM and embedding configurations use OpenAI; disabling inference does not remove embedding calls. Inference-enabled add can propose additions, updates and deletions, so action authorization must follow effects rather than the method name. Scoped search parameters do not by themselves establish authorization for ID-based operations. Evaluate the full model, storage and telemetry path, actual costs and host permission before adoption; no provider was installed or activated here.
