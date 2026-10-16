# Focused reuse review

Checked 2026-10-17 (UTC+08). This is a source review and local maintenance record,
not a claim to have searched all GitHub projects or validated teaching efficacy.
No third-party scripts, connectors or memory engines were installed.

## Teaching sources

- [book-tutor](https://github.com/xixiaofinland/agent-skills/blob/main/skills/book-tutor/SKILL.md):
  inspected the actual instructions, including chapter configuration, small teaching
  units and progress notes. The root LICENSE URL returned 404, so license status
  remains unverified and no source text was copied. General ideas informed original
  source-location and continuation guidance in `references/learning.md`.
  Deliberately rejected mandatory probing before every explanation, mandatory checks
  after every answer, and unconditional vault writes: those conflict with ZhiXu's
  existing direct-help and consent boundaries.
- [Learning Commons lesson planning](https://github.com/learning-commons-org/agent-skills/blob/main/skills/k12-lesson-plan-creation/SKILL.md):
  inspected the actual workflow. It declares Apache-2.0 with LICENSE/NOTICE terms.
  Its classroom-material production workflow is not a general personal tutor.
  Retained the idea of inspecting subject-specific sources before claiming curriculum
  alignment; did not import its scripts, fixed output workflow or optional connector.

## Applied changes

1. Source/edition/section anchoring and honest missing-source fallback.
2. Minimal cross-host continuation note distinguishing exposure, assisted practice
   and demonstrated independent performance.
3. Task-first selection of extra skills, dependency/license checks and explicit
   inspection/installation/loading/execution evidence. No duplicate memory writer.
4. Four synthetic routing boundary cases. Passing the case validator only checks
   schema/coverage, not model behavior or learner outcomes.
5. Packaging validation no longer disappears under Python `-O`. Added offline
   regressions for normal/optimized reproducibility, version mismatch, broken runtime
   links and preservation of existing verification/release output.

## Evidence and remaining work

- Local Python unit suite: 28 passed at first checkpoint.
- Routing-case schema: 89 cases passed; provider-case schema: 8 cases passed.
- No live Codex/Claude/DSH activation or learner trial performed in this pass.
- No version bump, release, automatic private-profile upgrade or remote publication.

Keep this record updated with actual later checks, not intended results.

## Second checkpoint

- Python suite now 33 passing: added parent-directory symlink and staging-path protection, duplicate provider identity rejection, no provider enumeration for disabled/session-only memory, and immutable capability/scope snapshots.
- Normal packaging completed with CRC, per-file checksums and runtime links verified; generated candidate remains local and unreleased.
- The installed generic quick validator rejects the existing `compatibility` frontmatter field. This is an existing validator/spec mismatch, not silently removed from the public bundle. Package-specific validation passes; live host acceptance remains pending.
- Reviewed [Agent Skills evaluation guidance](https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/evaluating-skills.mdx) and [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md): a schema pass is not a behavioral benchmark. No clean-context model comparison was executed in this direct-maintenance pass.
- Reviewed repository overviews for [LangMem](https://github.com/langchain-ai/langmem) and [Mem0](https://github.com/mem0ai/mem0). Neither is installed or verified in the target hosts, so no engine is bundled or recommended as already available. Existing native-memory-first routing remains intact.

## Third checkpoint

- Python unit suite now 35 passed, including blank/non-text descriptions and invalid version paths.
- Entrypoint now routes explicit additional-Skill selection to the relevant platform reference; research links to the same guidance instead of duplicating it.
- Candidate packaging and relative-link checks passed after routing changes. No live host/model benchmark or efficacy claim has been added.

## Fourth checkpoint

- Native memory that meets the requested scope now returns before enumerating external provider descriptors; a generator regression proves unnecessary provider probing is skipped.
- Packaging reads name, description and version from the leading frontmatter only. A failing regression demonstrated that body text previously masked missing metadata; the corrected validator rejects those cases in optimized mode too.
- Python suite: 37 passed; routing/provider schema remain 89/8. These are offline engineering checks, not host activation or model-behavior evidence.
- The earlier candidate has since been published on an isolated maintenance branch; default branch and releases remain unchanged. No private records are included.

## Fifth checkpoint: selective reuse, not framework stacking

- Inspected [Superpowers systematic debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md), [verification-before-completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md), and its MIT license. Added a short, independently written project-debugging boundary: distinguish environment/fixture failures, trace one causal hypothesis, redact diagnostics and verify the relevant regression. Existing project scope and evidence rules remain primary. No scripts, hooks or upstream text were copied.
- Deliberately did not import universal mandatory skill invocation, a fixed retry-count architecture rule, unsupported numerical effectiveness claims, or full-suite reruns after every statement. Those add overhead or imply evidence the project does not have.
- Added three synthetic cases covering environment failures, unsafe diagnostic logging and a document-only negative. Routing schema: 92 cases; no model behavior run is implied.
- Inspected the current [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) and [reference validator](https://github.com/agentskills/agentskills/blob/main/skills-ref/src/skills_ref/validator.py). Both explicitly allow compatibility. Local PyYAML parsing plus assertions against the inspected field/length rules passed (description195, compatibility163). The official skills-ref CLI is absent and was not run; the older generic validator mismatch remains accurately recorded.
- Reviewed [ts-fsrs](https://github.com/open-spaced-repetition/ts-fsrs) scheduler documentation and MIT license as a possible future adapter for explicit flashcard/review requests. It is a scheduling library, not an automatic notification service or proof of independent learning. No scheduler, review-log collection, dependency or fixed review cadence was added to the instruction-only bundle.

## Sixth checkpoint: typed provider evidence

- Reproduced that Python type hints alone admitted the text "false" as truthy evidence or a network/sharing permission in the side-effect-free reference module. Evidence, requirements, provider network flags and operation flags now require actual booleans; native availability does too. A scope string cannot silently become a set of individually authorized characters.
- Five additional unit tests cover these malformed descriptors/requests. Current suite:42 passed; routing/provider schema92/8 unchanged. This hardens the reference implementation only; it is not a sandbox or enforcement layer for an actual host/provider.

## Seventh checkpoint: carry useful work through

- The workflow reference now explicitly continues authorized execution toward its completion condition, advances independent parts when one dependency is blocked, and avoids repetitive unchanged checks or unrelated feature additions. No background scheduling ability or additional authority is implied.
- Added three synthetic positive/boundary/negative cases: scoped implementation, a blocked check with independent work, and a status-only request. Routing schema:95 cases. No live model benchmark is claimed.
- Corrected the usage-examples page's stale claim that the current release was v0.4.0 Preview and removed obsolete unpublished labels. Historical evaluation reports retain their dates and snapshot identities. Candidate changes remain distinct from the unchanged v1.0.1 release.
- Candidate packaging completed after the runtime wording change;42 unit tests and8 provider-case schema checks remain the current offline evidence.

## Eighth checkpoint: continuity without blocking the task

- A previous memory choice is reused until a material host/account, scope or capability change affects a real continuity need. Only affected evidence/permission is revisited; ordinary new chats and unrelated requests do not trigger provider probing.
- Provider outages no longer need to halt work that can continue from authorized session material. Pending writes remain incomplete, no second writer is silently selected, and old records are preserved. This is guidance for host behavior, not an implemented outage detector or background retry service.
- The side-effect-free trigger reference accepts an explicit context-change flag, with strict boolean inputs and a relevant-need guard. Unit suite43; routing schema98; provider schema8. Added outage, new-service and no-memory-needed cases.

## Ninth checkpoint: DSH installation friction

- Re-read the actual [DSH filesystem provider README](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md): direct bundle depth, project/user priority, catalog/body lifecycle and warning behavior. Added targeted discovery/update guidance rather than another installer or duplicated Skill copy.
- Updated files do not replace retained old conversation instructions; reference edits do not imply a refreshed catalog. No DSH live activation has been claimed. Added three synthetic diagnosis/read-only/negative cases; routing schema101, unit suite43, provider schema8.

## Tenth checkpoint: qualification is not ranking

- Reproduced an arbitrary choice when two installed, verified providers qualified: the reference selected the alphabetically first ID. It now leaves extra persistence off (D), returns the qualified candidate IDs for comparison and requires an explicit scoped choice. Candidate ordering is presentation only.
- Runtime guidance compares task fit, existing selection, storage/network conditions and actual cost evidence instead of inventing weights or equating popularity with suitability. Independent useful work can continue while a material choice remains unresolved.
- Unit suite44 passed, including candidate-order reversal; routing/provider schema remain101/8. No real provider was installed, selected or written by these tests.

## Read-only upgrade comparison (candidate maintainer utility)

Added a standard-library-only comparator for a user-selected standalone bundle and the existing release manifest format. It reports matching/different/missing/unreadable public files, does not scan extra files or host roots, refuses manifest traversal and symlinks, and does not perform upgrades. Five synthetic tests cover unchanged bytes, local edits, missing/non-file entries, unsafe manifests, links and size limits. Authenticity, concurrent hostile mutation and host activation are explicitly outside its claim. This is an original utility, not a copied installer or added runtime dependency.

## MCP Memory: concrete source review instead of another engine

Reviewed `modelcontextprotocol/servers` at `bbb701e7ac1e57f3edd1c2836b94c5457eaf7b9c`: memory source, README, package configuration and root license. The current code contains a cross-process file lock as well as an in-process queue, so an old blanket claim that it lacks cross-process coordination would be wrong. Text searches and node opens still expose incident relation endpoints and are not authorization filters. Added a source-linked adoption assessment and a runtime rule to inspect the complete retrieval boundary before calling scope verified. No upstream code or automatic-profile prompt copied, no package installed, no real memory read/written, and no runtime capability marked verified. License transition is recorded rather than assumed MIT-only.

Proposed behavior checks (not executed model trials): (1) an allowed node returned with an out-of-scope relationship must not be called scoped isolation; (2) a verified separate authorized store remains a possible bounded solution, not an automatic installation; (3) a lock does not settle incompatible factual corrections. Existing unit/schema/package checks remain structural or fixture evidence only.

## Mem0: inspect model calls and mutation effects

Read pinned Python-library paths at `0724291bd864cf807e88ee8981c8226644e8fb42`: memory implementation, general/LLM/embedding configuration, telemetry implementation, README and Apache-2.0 license. The inspected default LLM and embedding providers are OpenAI; infer=false still embeds text. Inference-enabled add can select updates/deletions, and ID-based methods require their own authorization boundary rather than borrowing search-filter guarantees. Added the linked source review and concise whole-pipeline/effects guidance. No installs, API calls, credentials, private-text probes or provider configuration. These library findings are not an audit of the cloud or self-hosted HTTP products. Runtime instruction changes are not a behavioral or efficacy result.

## Align the entrypoint with the existing consent modes

The top-level first-write wording could be read as requiring another full preview on every save, despite the memory reference allowing authorized low-risk accumulation. Clarified first write/material-change setup, per-save preview in confirm mode, and reuse of unchanged valid standing scope under host policy. No new recipient, sensitive content or broadened scope inherits approval. Added three independently constructed routing specifications for routine course-progress saving, changed recipient and a one-off no-save formatting request. Schema now contains 104 cases (38 positive / 21 negative / 45 ambiguous); no model execution is claimed.

## Keep concise advice distinct from end-to-end execution

Aligned the entrypoint's “one next step” wording with the existing workflow: a concise next action can satisfy advice, while an authorized execution request should continue toward its requested outcome or a concrete blocker. Delegation still depends on permission. Existing continue-execution, partial-blocker and read-only-status specifications cover the intended distinctions; this wording review does not claim an observed model improvement.

## Make upgrade comparisons preserve local edits

Extended the optional read-only comparator with two-manifest, three-way classification: distinguish upstream-only replacements, already-current files, local-only edits, conflicts, new-path collisions and retired files. It reads only the selected manifest union, once per path, and never applies/deletes/merges. Both manifests are validated before content reads. Four additional tests cover all categories, no extra-file scans, unchanged local bytes, invalid paths/symlinks and real CLI report exit behavior; 53 unit tests now pass. An actual local candidate comparison identified 15 unchanged public files and 3 already at the target without writes. This is not an installer, atomic snapshot, authenticity check or host activation test.
