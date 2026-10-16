# MCP Memory：已看源码，尚未接入

核对日期：2026-10-17。对象为 `modelcontextprotocol/servers` 的 `src/memory`，源码快照 `bbb701e7ac1e57f3edd1c2836b94c5457eaf7b9c`。这不是已安装或已通过宿主验证的 provider，也不代表对应 npm 发布包具有相同实现。

## 对智序有什么用

它是可复用的本地 JSONL 知识图谱服务候选，通过 MCP 提供实体、观察与关系的读写。无需为了保存这些记录在智序里重复实现数据库。若原生记忆已经够用，仍不需要增加它。

源码中可观察到：

- 变更先排队，并使用相邻锁文件协调共享同一数据文件的不同进程；实现包含失效锁恢复与超时。这比只靠同进程队列更完整，但我们没有运行并发测试，不能填成当前宿主“已验证”。
- 保存采用同目录临时文件后替换，并保留既有权限；无法解析的行会在后续写入中保留，而非无声丢弃。不能据此承诺所有操作系统、网络磁盘或断电场景的持久性。
- 自定义 `MEMORY_FILE_PATH` 决定文件位置；相对路径以包目录为基准，不是当前项目。实际配置应核对一个明确授权的路径，不能照搬默认路径就认为项目之间隔离。

## 接入前必须解决的具体边界

1. `read_graph` 返回整个图。`search_nodes` 是名称、类型和观察的文本搜索，不是账号或项目的授权过滤器。
2. `search_nodes` / `open_nodes` 还会返回任一端匹配的关系；另一端可能是未请求实体的名称。只检查返回的实体列表不足以证明未越界。把实体命名为“项目A:某人”也不能构成访问控制。
3. 只有命名、标签或查询筛选时，不把 `scope` 标成已验证。选择独立且已授权的数据文件/进程，或已经验证的上游授权适配层；不能先把全图读入模型再过滤，称之为没有访问其他范围。
4. 锁防止文件写入相互覆盖，不等于两个Agent对同一事实给出矛盾更正时自动解决语义冲突。仍需确认来源、范围和更正依据。
5. 本地文件不等于内容不会进入云端模型。跨Agent接入必须核对每个服务/账号的共享授权。

上游README的自动识别用户、持续收集信息等示例提示不作为智序默认政策。安装、提供方权限、持久化与迁移各自遵守宿主授权，不因读过示例而生效。

## 怎样才可以推荐

当前状态：仅文档/源码审查；安装、启用、调用、隔离测试均未执行，`verified_capabilities` 保持空。当前继续选择A或D，不直接推荐C。

有实际缺口且用户授权接入后，使用独立合成数据测试：跨会话读回、更正、删除、两个进程同时写、失败恢复，以及两个同名实体分属不同范围和跨范围关系的输出。测试的是确切安装版本、实际路径与宿主配置，不能把本次源码阅读替代它。我们没有添加后台服务、写入真实记忆或配置MCP权限。

## 来源与许可

- [已读源码](https://github.com/modelcontextprotocol/servers/blob/bbb701e7ac1e57f3edd1c2836b94c5457eaf7b9c/src/memory/index.ts)
- [已读使用与并发说明](https://github.com/modelcontextprotocol/servers/blob/bbb701e7ac1e57f3edd1c2836b94c5457eaf7b9c/src/memory/README.md)
- [已读包配置](https://github.com/modelcontextprotocol/servers/blob/bbb701e7ac1e57f3edd1c2836b94c5457eaf7b9c/src/memory/package.json)
- [该快照许可证](https://github.com/modelcontextprotocol/servers/blob/bbb701e7ac1e57f3edd1c2836b94c5457eaf7b9c/LICENSE)：处于MIT向Apache-2.0过渡，文档另有CC-BY-4.0说明；不要概括成整个仓库单一MIT许可。本轮没有复制其代码或提示文本，也没有加入运行时依赖。

## English summary

Source-reviewed candidate only, pinned to the commit above; no installation or runtime acceptance. The implementation includes queued mutations, cross-process file locking and temporary-file replacement. These observations are not verified capabilities in the user's host. Graph search is not an authorization boundary, and relations can expose names outside the requested node set. Use an independently authorized scope boundary before reading, not post-filtering after a full-graph read. Keep native memory first and do not install another engine without a demonstrated gap and permission.
