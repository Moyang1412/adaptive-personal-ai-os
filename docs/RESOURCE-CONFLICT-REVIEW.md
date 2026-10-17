# Preserve existing work during resource conflicts · 2026-10-17

[ClashBench v1](https://arxiv.org/html/2609.19892v1): read construction, independent task/incumbent checks, evaluation protocol and limitations. Its controlled single-host stress tests distinguish completing a new task from preserving an existing workload. Most condition/case pairs have one stochastic run; reported rates are not real-world incident probabilities. Prompt safeguards did not eliminate preemption in that setting. We adopt the separate-outcome distinction, not a claim that new instructions enforce isolation.

Repository inspected at [f8ea2a26544c5959cc626b768158c348c122b41d](https://github.com/TarferSoul/CLASHBench/tree/f8ea2a26544c5959cc626b768158c348c122b41d): README, docs/PROTOCOL.md and the roommate_laundry_slot_v1 grade_state.py. The selected grader checks both a requested reservation and preservation of the incumbent reservation/audit history; it is one case, not a full implementation audit. No LICENSE/COPYING file was found in the complete recursive tree, and the root LICENSE request returned 404. Do not treat public visibility as permission to copy its code, fixtures or dataset. None was copied, installed or executed; no Docker image, credential or model API was used.

[InterruptBench v1](https://arxiv.org/html/2604.00892v1): read setup and interruption construction. Its addition/revision/retraction updates are informational and preserve the original final ground truth. It does not by itself establish recovery after arbitrary irreversible cancellation or undo. Existing ZhiXu current-goal/reconciliation rules cover the inspected distinction, so no new interruption engine or duplicate protocol was added.

## Narrow implementation

Previously the references protected uncommitted work and commitments generally.
The candidate explicitly handles a contested resource: identify ownership and
scope, prefer a compatible non-disruptive alternative, expose an unavoidable
conflict, and check incumbent health separately from the new result. Permission
to finish a task is not blanket permission to seize a shared resource. This still
allows an expressly authorized replacement under host policy; it is not a rule
that all processes or reservations are immutable.

Four authored scenarios cover an occupied service port, a shared booking,
explicit replacement of the user's own disposable process, and missing evidence
of incumbent health. Schema checks do not demonstrate agent safety. The existing
critical-violation field remains separate from usefulness; no automatic scorer
or new storage is introduced.
