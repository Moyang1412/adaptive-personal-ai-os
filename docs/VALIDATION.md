# Validation status

## 2026-10-17 maintenance candidate

Branch: `dot/overnight-improvements-20261017`, based on v1.0.1 main. This is not a new release. Current offline evidence: 90 unit tests, 125 routing-case schema checks and 8 provider-case schema checks; reproducible plugin/Skill packaging, CRC/per-file readback and local runtime references. The official specification permits compatibility; a local parsed-field check passes, but the official skills-ref CLI was not run. No live host activation, controlled model-behavior study or learner study was performed in this pass. See the [maintenance record](REUSE-REVIEW-2026-10-17.md) and [life/evaluation expansion](RESEARCH-EXPANSION-2026-10-17.md). Of the offline checks, 18 validate paired-run bookkeeping and 17 validate the optional cash-flow arithmetic helper; authored routing cases remain unexecuted behavior specifications unless a separately scoped pilot states otherwise.

An additional [four-pair synthetic response pilot](../evals/results/2026-10-17-life-expansion/REPORT.md) compared the prior and expanded instruction snapshots. Both versions met the basic requirements in unblinded author review; no superiority was observed. Exact model settings and actual installed-host activation remain unverified, so the accounting utility reports no comparable installed-Skill pairs. This does not replace the unexecuted host and real-life outcome checks above.

The following reports remain historical evidence for their own snapshots.

## Validation · v1.0.0

Date: 2026-10-13. Version 1.0.0 is ZhiXu's first stable release, incorporating
dual-mode learning, adaptive workflows and everyday life support. Publication
does not establish scientific efficacy or completed live host acceptance. See
the [1.0.0 release record](RELEASE-1.0.0.md) for the actual release-file checks,
version identity and known validator limitations.

The three earlier rounds evaluated local candidates marked `0.4.0-preview`:

| Candidate round | Recorded evidence and limits |
|---|---|
| [Dual-mode learning](VALIDATION-DUAL-LEARNING.md) | Synthetic instruction-following and a short continuation; no real learner outcomes or host acceptance. |
| [Other adaptive workflows](VALIDATION-NONLEARNING.md) | Four single-run pairs, three additional outputs and two repair checks; initial errors and limits are retained. No overall improvement established. |
| [Everyday life](VALIDATION-LIFE.md) | Four single-run anonymous pairs tied, plus three candidate-only scenes; 11 outputs total. No overall efficiency or real-life benefit established. |

Each report and raw result retains its original snapshot hashes and historical
publication status. The final transition to 1.0.0 changes release metadata,
without another behavior change. Earlier outputs do not automatically become
behavioral validation of the 1.0.0 artifact. File checks, schema checks, model
answers, actual host activation and user outcomes remain separate evidence.

Research papers, official guides and GitHub projects inform methods; they are
not trials of ZhiXu. Real Codex, Claude Code and DSH activation, multi-turn
behavior, installed-provider effects and learning or life outcomes remain
unverified. Installed copies do not update automatically.

---

## Historical report · v0.4.0 Preview

Date: 2026-10-12. Baseline: public main `d043fc8c19bf2a99c6af7f361878b9300c790422`. Published remote release commit: `8727037ee8fee3e2ba638ec60b49ce5f121dbc96`.

This report covers the published instruction bundle and a side-effect-free provider assessment reference, not an automated memory service.

## Checks performed

- The core and Codex metadata parsed as YAML; names and version inspected. The standalone bundle includes the provider contract and remains instruction-first.
- The existing public `evals/validate_routing_cases.py` ran against 40 synthetic cases: 15 positive, 7 negative, 18 ambiguous. Its source is unchanged from v0.2. This is schema validation, not model evaluation.
- `python -m unittest evals.test_provider_selection evals.test_memory_lifecycle` ran synthetic checks for first-use triggering, native-first routing, provider evidence, A/B/C/D selection, consent, scope, selected-provider switching, export routing and revision-guarded writes. The in-memory fixture is not a shipped memory engine, a new-session test, a real provider test or a true parallel-agent test.
- `python evals/validate_provider_cases.py` checked the provider-case JSON schema and category balance only. It did not execute a provider, route a request or prove native-first, cross-Agent scope, consent, switching or concurrency behavior.
- All 82 relative Markdown links resolve locally; no missing targets were found. Self-contained package file presence was checked.
- 36 Markdown files parsed to HTML locally. Browser screenshot navigation was blocked by the environment, so no visual GitHub/mobile rendering pass is claimed.
- A configured private-identifier and credential-pattern scan was applied to release files. No findings is not a comprehensive security audit or anonymization of historical Git metadata.

## Not established

- Real Codex, Claude Code or DSH activation, implicit routing, multi-turn behavior or provider callability; this turn only validates the local reference module and synthetic fixtures.
- Installation on the maintainer's personal computer, cross-device synchronization, or private Skill updates.
- Learning efficacy, optimal curricula or guaranteed safety/privacy across models.
- A production provider's license, maintenance, storage, deletion, concurrency or cloud data behavior; adapters must report and re-test those values in the user's environment.
- Code-enforced memory permissions, a database, vector retrieval, automatic importer/synchronization, automatic installer or rollback: these modules are not shipped.
- Stopping an extra provider and falling back to a host's native memory remains a documented host workflow; the side-effect-free reference module does not execute that fallback.

Live host acceptance should use synthetic private files, record actual host/model versions and loader evidence, and preserve both failures and limitations. Codex, Claude Code and DSH are currently **documentation or adapter layer complete; live acceptance unverified**. See [evaluation protocol](../evals/README.md) and [provider integration](PROVIDERS.md).
