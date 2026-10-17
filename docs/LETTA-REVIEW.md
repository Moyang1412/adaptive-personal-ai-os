# Letta / MemGPT: architecture review, not a new dependency

Inspected 2026-10-17. No installation, login, model request, memory import,
provider invocation or user-data transfer was performed.

## Separate the historical paper from the current product

[MemGPT v2 (2024-02-12)](https://arxiv.org/html/2310.08560v2): inspected memory hierarchy, queue management, function execution and pagination. Moving selected external records into a limited context is an architectural pattern; it does not create physically infinite context, perfect recall or access control. Its study is not acceptance evidence for a 2026 Letta installation or for ZhiXu. ZhiXu already has relevant-only retrieval and explicit persistence boundaries, so another paging engine was not added.

The old [letta-ai/letta repository at 5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a](https://github.com/letta-ai/letta/tree/5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a) now directs active development to letta-code and places the retired V1 API server on an archive branch. A search result describing shared V1 memory blocks must not be treated as the current implementation contract.

Current source inspected at [letta-ai/letta-code, 0d3ad1239ef0c15108e274f28e4f7cf08a79c305](https://github.com/letta-ai/letta-code/tree/0d3ad1239ef0c15108e274f28e4f7cf08a79c305). The root license is Apache-2.0; no code or instruction text was copied. File-level dependencies and any optional modules would still need their own license and security review before reuse.

## Current documented and source-observed boundaries

- [MemFS documentation](https://docs.letta.com/concepts/memfs/) describes Git-backed memory, different local-only and cloud-backed persistence, and separate conversation-history search. Root memory files enter the prompt; deeper indexed directories load on demand. Vector/semantic search is not included in MemFS by default. These are product documentation claims, not verified capabilities in this workspace.
- [Shared memory documentation](https://docs.letta.com/concepts/shared-memory) describes organization-owned repositories for cloud-hosted agents. An attached repository can supply skills; local-only agents use their own MemFS/project files. A local checkout is not proof that another agent received a push, that access is authorized, or that concurrent edits merged correctly.
- [src/agent/shared-memory-skills.ts](https://github.com/letta-ai/letta-code/blob/0d3ad1239ef0c15108e274f28e4f7cf08a79c305/src/agent/shared-memory-skills.ts) resolves attached repository mounts rather than every sibling directory, explicitly because detached checkouts can remain on disk. It has an attachment-list cache and invalidation function. This is skill-discovery behavior, not evidence of an OS-level read barrier, immediate global revocation or physical deletion.
- [src/headless-memfs-policy.ts](https://github.com/letta-ai/letta-code/blob/0d3ad1239ef0c15108e274f28e4f7cf08a79c305/src/headless-memfs-policy.ts) computes stateless-session flags. Reading this helper does not verify every caller or prove that all message retention/network effects are disabled. The attached-repository interface was also inspected; server-side permission enforcement was not audited.

## Decision for ZhiXu

Letta is a stateful-agent stack, not a memory database that installing this Skill
magically enables in another host. It is worth assessing if the user already uses
Letta or deliberately chooses that stack. It is not justified as a default extra
dependency for an otherwise working Codex, Claude Code or DSH installation.

Reuse the existing provider assessment: exact host/backend version, authorized
service/account, selected records, local versus remote persistence, supported
operations, observed restart availability, conflict handling and model/embedding
costs. Installation/discovery, attachment, local commit, remote push and another
agent's usable state require distinct evidence. Detaching is not global forgetting.
These distinctions already exist in the runtime contract; the change here is a
source-reviewed option and version boundary in the public provider guide, not a
new runtime policy, provider descriptor or claim that Letta passed acceptance.
