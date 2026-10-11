# Validation · v0.3.0 Preview

Date: 2026-10-11. Baseline: public main `23f4af2bdc4d1afef7aa18964402f828a54ae697`.

This report covers the published instruction bundle, not an automated memory service.

## Checks performed

- The 66-line core and Codex metadata parsed as YAML; names and version inspected. The standalone bundle contains 9 files.
- The existing public `evals/validate_routing_cases.py` ran against 40 synthetic cases: 15 positive, 7 negative, 18 ambiguous. Its source is unchanged from v0.2. This is schema validation, not model evaluation.
- All 54 relative Markdown links resolve locally; no missing targets were found. Self-contained package file presence was checked.
- Chinese/English Markdown parsed and local HTML previews generated. Browser screenshot navigation was blocked by the environment, so no visual GitHub/mobile rendering pass is claimed.
- A configured private-identifier and credential-pattern scan was applied to release files. No findings is not a comprehensive security audit or anonymization of historical Git metadata.

## Not established

- Real Codex, Claude Code or DSH activation, implicit routing or multi-turn behavior.
- Installation on the maintainer's personal computer, cross-device synchronization, or private Skill updates.
- Learning efficacy, optimal curricula or guaranteed safety/privacy across models.
- Code-enforced memory permissions, concurrent writes, automatic installer or rollback: these modules are not shipped.

A separate local automation prototype passed 69 tests, but its source upload was blocked by platform safety review and is not part of this public release. Those tests do not validate the published instruction-only memory workflow. The blocked upload was not retried through an alternate transport.

Live host acceptance should use synthetic private files, record actual host/model versions and loader evidence, and preserve both failures and limitations. See [evaluation protocol](../evals/README.md).
