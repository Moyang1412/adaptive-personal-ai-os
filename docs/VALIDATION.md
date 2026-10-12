# Validation · v0.4.0 Preview

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
