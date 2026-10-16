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
