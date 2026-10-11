# Personal memory and portability

## Scope

This release uses relevant native context and user-approved Markdown files through actual host tools. It does not ship an automatic memory engine, importer, synchronizer or permission-enforcement service. Instructions guide cooperation; they are not an OS security boundary.

Start without configuration. Reuse relevant context already supplied. Only when continuity is useful, offer the user a persistence choice and exact private location. Do not browse all existing histories to construct a profile.

## Consent

| Choice | Behavior |
|---|---|
| Session only / off | Do not read or write ZhiXu persistent notes for the task. |
| Confirm before saving | Show the candidate, subject, scope and destination before a save. |
| Authorized low-risk accumulation | Save new low-sensitivity preferences/progress within the agreed standing scope; sensitive data and major changes need explicit consent. |

A direct “remember this” can authorize that exact save when destination and scope are already established. Do not repeat identical approval unnecessarily. “Today I am busy, keep it short” is temporary, not standing permission.

These choices do not disable the host's native auto-memory or chat history. Explain that those are separate settings. Never promise global forgetting.

## Private location and minimal files

Use a dedicated user-selected directory outside this public repository and installed Skill. `~/ZhiXu-Private/` is an example, not an automatically created/discovered directory. Learn its path from the user or an explicitly configured pointer; do not scan the filesystem for it.

`PROFILE.md` can contain collaboration preferences and consent boundaries. `MEMORY.md` can contain a small set of confirmed records. Existing project/learning files can remain where the user already manages them. The minimal record template is in [Templates](templates.md).

Preserve content, subject (`self`, `project` or `third-party`), exact scope, provenance, date, confidence/status and authorized model service/account. For changing facts, add a review/expiry date. Do not treat expired records as current; they remain until explicitly revised/deleted.

Never store passwords, keys, session cookies or verification codes. Do not save health, relationship or financial details by default. Avoid invented personality labels and demographic inference. A friend's story must not become a fact about the user.

## Read, correct and forget

Read only files and sections relevant to the current domain. Life-only questions must not pull in unrelated project history. Check whether the current provider/account is authorized before loading private content. If that boundary is unknown, clarify before reading.

When correcting a fact, identify the original record and inspect the latest file. Use a minimal host edit, preserving unrelated content. Update the subject or remove the incorrect statement as requested. Report the actual written location and verification; do not claim success from a draft.

For forgetting, remove the identified content only with the appropriate user request and host permissions. Do not preserve a copy in a new note or public changelog. Explain that old conversations, native memories, backups and content already in model context are separate. Do not re-import a deleted fact without permission.

## Native-memory bridge

Use relevant already-loaded context first. Additional native-memory access must name approved files or sources. Present a proposed minimal summary before importing; keep originals untouched. Do not bulk-import history or replace the host's own memory system.

Current user corrections supersede stale background within host policy. If sources conflict and cannot be reconciled, expose the conflict instead of silently merging them into a false fact.

## Switching hosts and services

The same user can authorize multiple agents to read one private workspace. Host brand and model provider are different: one host may use several services/accounts. Installing the same Skill grants no permission to share memories with a new provider.

Before sharing, confirm the destination and selected records. Prefer a curated summary rather than the whole profile. Do not promise automatic cross-device sync. A local file read by a cloud-backed agent may enter that provider's context; local storage is not local inference or encryption.

For shared files, use one writer at a time or verified host conflict/version controls. Re-read after another agent changes a file and reconcile before editing. This release does not implement transactional locks or automatic merges. If the host cannot protect competing writes, stop parallel writes rather than pretending they are safe.

## Evolution boundary

Individual preferences stay individual. Project methods stay in that project. Only explicitly requested public maintenance uses sanitized examples and reviewed changes. Neither repeated mistakes nor successful personal experiments authorize uploading a private file or modifying global policy.
