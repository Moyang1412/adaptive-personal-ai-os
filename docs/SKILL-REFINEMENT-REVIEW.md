# Selective Skill refinement · 2026-10-17

## Inspected primary material

- [SkillAxe v1, 2026-06-09](https://arxiv.org/html/2606.10546v1): read diagnostic methods, experimental conditions, SpreadsheetBench results and limitations. Separating activation, rule quality and execution is useful. However, rule-derived grading can miss a self-consistent wrong strategy; LLM judges and interactions between skills remain limitations. In its 50-task SpreadsheetBench comparison, both the 69-skill and refined 22-skill libraries scored 52%, versus 16% without skills. That table supports fewer skills at equal observed accuracy, not higher accuracy than the unrefined library. We adopt a manual attribution checklist, not its numerical credit formula, judge calls or automatic rewriting.
- [SkillCorpus v1, 2026-07-17](https://arxiv.org/html/2607.15557v1): read retrieval discussion, limitations, worked failure and release statement. Its embedded-spreadsheet example shows that topic relevance does not ensure procedural fit. The paper's text-only skill safety/quality scoring is not runtime security verification. It both uses release language and says artifacts will be released upon acceptance; availability and redistribution rights of a concrete corpus were not verified. No corpus was fetched or installed.
- [Anthropic context engineering, 2025-09-29](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): read prompt, progressive retrieval and compaction guidance. It favors relevant minimal information while warning that excessive compression loses needed detail. This is engineering guidance, not a controlled ZhiXu comparison.
- [GSM-IC v3](https://arxiv.org/html/2302.00093v3): read task construction, evaluated models and results. Its irrelevant-context arithmetic experiments used code-davinci-002/text-davinci-003, not current Codex installations. They motivate checking distractors, not transferring old scores to current hosts.

## Local inspection, not an efficacy claim

At source 827ad45f1a827e533842c005d04eb728d8b77f0b, the 16 runtime Markdown files total 106,345 UTF-8 bytes. SKILL.md is 8,932 bytes; learning.md is 15,368. Loading both would expose 24,300 file bytes; this is not a tokenizer count, actual host loading trace, price or latency measurement. Existing routing already requests only relevant references. We therefore did not add another generic context-management protocol, import a corpus or mechanically split every file.

The runtime change is a small procedural-fit check in the existing platform selection section. The maintainer accounting guide gains a diagnostic checklist that retains original outcomes and distinguishes missing activation from faulty guidance or a disputed verifier. Three original scenarios cover an embedded artifact, disputed verifier and absent loader evidence; their schema validation is not behavior validation. The bookkeeping tool still performs no grading, model calls or installation.

## Entry-point deduplication candidate

The next edit removes the repeated five-step memory-selection walkthrough from
SKILL.md, replacing it with a mandatory reference-loading pointer and compact
boundary summary. This is relocation of detailed guidance already present in
shipped references, not removal of consent, verification or scope requirements.

Preserved locations:
- Native-first and A/B/C/D selection: memory.md, Provider evaluation and choice.
- Documented/installed/enabled/callable/tested distinction: the same section and provider-contract.md.
- Scope/account changes and standing permission: memory.md, Recheck only when the context changes and Consent.
- One writer/source and migration: memory.md, Switching and migration; provider-contract.md lifecycle rules.
- Network and cost conditions: provider-contract.md provider selection and isolation requirements.

SKILL.md changes from 8,932 to 8,095 UTF-8 bytes (837 fewer, about 9.4%). No tokenizer or model run was used.

The frontmatter, public Skill name, route table and runtime file list stay the
same. Packaging verifies local reference closure, not whether a particular model
actually follows the new pointer. This structural candidate needs real-host
comparison before any quality or token-cost claim; byte reduction alone is not
an efficacy result. Keep the prior f7d1db8 snapshot available for comparison.
