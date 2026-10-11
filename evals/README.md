# Evaluation: structure is not behavior

[Validation status](../docs/VALIDATION.md)

The synthetic cases describe observable intended behavior. Running `python evals/validate_routing_cases.py` checks the data format, IDs, field types and class consistency only. It performs no model or host execution.

Run actual acceptance separately in each supported host, recording host/model versions, the installed Skill path and loader evidence, prompts, outputs, tool side effects and reviewer decisions. Use new sessions where appropriate and synthetic private files only.

Inspect four distinct dimensions: correct activation; correct mode and response; consent/scope boundaries; actual continuity and independent learning. A helpful answer without evidence that the Skill loaded is not a passing activation test. A file write is not proof of learning.

For each change, run the original failure plus adjacent positive, negative and ambiguity cases. Report counts and failures, not a universal success guarantee. Any observed unauthorized disclosure or destructive action blocks release until investigated. The small authored case set does not establish production reliability or statistical superiority.

Private-profile behavior is instruction/host-driven in this version, not enforced by a bundled service. Test actual files and claims accordingly. Never claim locks, automated rollback or provider filters exist when the host does not supply them.

The optional `must_not` field is a human-review assertion; the legacy schema validator does not inspect its semantics. Keep all raw personal transcripts out of public issues and commits.
