# Memory capability and completion review · 2026-10-17

This is a correction to the side-effect-free assessment reference and runtime instructions, not an installed memory engine or real provider test.

## Reproduced before the fix

1. A persistent, cross-Agent request requiring read/delete/cross_agent, with private-profile permission and a conflict-control flag but no verified profile operations, returned B. It now returns D until the profile itself has the required verified operations, scope, cross-session availability and active guard.
2. A persistent request listing only read, with native availability and read but no cross_session evidence, returned A. It now returns D; adding verified cross_session retains A. External-provider assessment applies the same effective requirement.

The caller supplies capability evidence. This pure reference does not independently authenticate that evidence, test a host, access files or enforce provider permissions. Existing valid evidence can be reused; missing evidence does not authorize a new probe or private write.

## Regression evidence

Five added test methods cover missing profile evidence, cross-session requirements, scope/guard omissions, immutable validated capability inputs, and permission/active-guard requirements. Negative scope/guard tests otherwise include cross-session support to avoid passing for the wrong reason. An explicit empty provider-capability set is no longer replaced with full defaults by the test fixture.

All 95 offline unit tests pass. The 129 routing cases (46 positive, 24 negative, 59 ambiguous) and 10 provider cases (3 positive, 6 negative, 1 ambiguous) pass schema validation only. Positive provider specifications now state the capabilities needed for their expected choice; separate negative cases retain the missing-evidence boundary. These are not new executed model trials.

## Runtime instruction change

The provider contract and memory selection guidance distinguish permission from verified capability and current-session access from persistence. A queued acknowledgment or job ID establishes submission only. Completion, indexing and cross-session availability can be separate stages; use documented result/readback semantics without inventing polling endpoints or duplicating uncertain writes. A past capability test does not prove a later write completed.

No provider installed, no personal memory read or written, no account connected, and no host activation or production memory guarantee established in this pass.
