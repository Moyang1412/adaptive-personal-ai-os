# Read-only paired-run accounting

This optional maintainer utility uses only the Python standard library. It does
not run a model, install a provider, grade an answer, open evidence links, scan
private files or approve a release. It summarizes explicitly supplied review
records so missing runs and retries cannot disappear into a success claim.

```sh
python scripts/summarize_eval_runs.py --input evals/fixtures/paired-runs-demo.json
python -m unittest evals.test_run_summary
```

The bundled input is **fabricated demonstration data**, including fake commit
labels, not model behavior. Its report correctly has zero observed/judged runs,
two missing second attempts and no comparable pair. Passing the unit tests checks
the utility, not the assistant. Real records should remain outside the public
repository unless they are independently synthetic and approved for publication.

## Input contract

Use the example JSON for field structure, replacing demonstration values only
with actual records. The top level defines the expected case IDs, repeat count,
exact baseline/candidate commit labels and supplied runs. Every case/variant/
attempt must be unique; missing combinations are reported. Do not reuse an
attempt number for a retry. Do not label a documentation-only commit as evidence
of a different loaded instruction bundle without recording the actual source.

Each run records:

- `source`: observed or demonstration. Demonstrations are excluded from observed
  outcomes regardless of their other labels.
- `execution`: completed, blocked or not_run. Blocked/not-run entries must have
  verdict unobservable. A completed execution may also remain unobservable.
- `verdict`: met, partial, failed or unobservable, assigned using an explicit
  rubric by the stated reviewer. These are not automatic semantic scores.
- `conditions`: model, host, settings, fixture and rubric identifiers. Use
  reproducible versions/hashes; record changed tools, access, budget or live
  sources in those conditions rather than claiming an otherwise matched pair.
- `review`: kind (human/self/model), reviewer/version and actual blinding. A
  self-review cannot be marked blind. Model review needs independently checked
  calibration outside this utility; merely supplying a reviewer name is not it.
- `activation`: verified or unverified, with actual loading evidence among the
  references if verified. A prompt saying “use the Skill” is not loader evidence.
- `evidence` and `note`: references to outputs/tool effects plus a rationale or
  blocking reason. The script never opens them or authenticates their contents.
- `critical_violation`: true, false or null (not assessed). Report observed scope,
  disclosure or destructive-action failures even if the task otherwise succeeded.
- `metrics`: optional elapsed_seconds, user_turns and tool_calls. Unknown values
  are omitted, not entered as zero; costs are kept separate from rubric outcomes.

The local format rejects unknown fields, duplicate JSON keys, truthy strings in
boolean fields, non-finite/negative metrics and invalid attempt numbers. Limits:
2 MiB input, at most 500 cases and 20 repeats, metric values at most 10^12. These
are parser/resource limits, not recommended experiment sizes or statistical rules.

## Reading the output

Per-variant observed totals retain failures, unobservable results and denominators;
all repeats remain present. Comparable pairs require observed completed judged
runs, verified activation and identical recorded conditions/review. Otherwise the
report states the mismatch. Quality changes are ordinal better/same/worse on the
recorded rubric, never an averaged quality-cost score. Cost deltas use only metrics
present on both sides. A faster run can still be worse or violate a boundary.

An empty input has no pass rate, not 100%. A reported violation cannot be cancelled
by many successful answers. Conversely, no reported violation does not establish
safety. Neither `observed` nor `verified` labels are independently checked by the
script; false labels still produce a misleading report. Check original evidence.
This small accounting format is not an Inspect log reader or benchmark substitute.

Follow the existing [paired evaluation protocol](README.md#comparing-non-learning-workflows)
for actual execution, fixture isolation, independent review and held-out tasks.
Do not present bookkeeping tests, synthetic demonstrations or non-comparable runs
as improved memory, teaching or real-life outcomes.

## Diagnose before rewriting a Skill

Keep the task outcome separate from an attribution hypothesis. Inspect the exact
loaded version, applicable instruction, observed action/artifact and verifier
expectation before deciding whether the problem was selection, missing or wrong
guidance, execution, unavailable tools, conflicting active instructions, or the
verifier itself. Several causes can coexist; unsupported attribution stays unknown.
A precise instruction alone does not prove the model saw or could execute it.

Use the existing note/evidence fields for this rationale; no new scoring engine
is implied. Do not erase an observed failure by assigning blame to the agent, or
improve a success count by switching graders after seeing the result. If a valid
alternative solution is rejected, retain the original verifier outcome and review
the artifact against the original user requirement separately. Revise a defective
rubric transparently and apply the revision to both variants. Do not weaken actual
requirements merely to reward a different path. A rule can be followed faithfully
and still be wrong, so instruction compliance is not outcome correctness.

See [source distinctions and context audit](../docs/SKILL-REFINEMENT-REVIEW.md).
