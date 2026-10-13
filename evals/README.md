# Evaluation: structure is not behavior

[Validation status](../docs/VALIDATION.md)

[Non-learning candidate pilot](../docs/VALIDATION-NONLEARNING.md) records paired
synthetic outputs, blind review, regression replays and unverified outcomes. It
does not establish an improvement over the previous version.

[Provider cases](provider-cases.json) · [Provider contract](../skills/adaptive-personal-ai-os/references/provider-contract.md)

The synthetic cases describe observable intended behavior. Running `python evals/validate_routing_cases.py` checks the data format, IDs, field types and class consistency only. It performs no model or host execution.

Run actual acceptance separately in each supported host, recording host/model versions, the installed Skill path and loader evidence, prompts, outputs, tool side effects and reviewer decisions. Use new sessions where appropriate and synthetic private files only.

Inspect four distinct dimensions: correct activation; correct mode and response; consent/scope boundaries; actual continuity and independent learning. A helpful answer without evidence that the Skill loaded is not a passing activation test. A file write is not proof of learning.

For each change, run the original failure plus adjacent positive, negative and ambiguity cases. Report counts and failures, not a universal success guarantee. Any observed unauthorized disclosure or destructive action blocks release until investigated. The small authored case set does not establish production reliability or statistical superiority.

Private-profile behavior is instruction/host-driven in this version, not enforced by a bundled service. Test actual files and claims accordingly. Never claim locks, automated rollback or provider filters exist when the host does not supply them.

`python evals/validate_provider_cases.py` checks the synthetic provider case schema. `python -m unittest evals.test_provider_selection evals.test_memory_lifecycle` checks the side-effect-free assessment reference and a fictional revision-guarded provider fixture. The fixture is an in-memory, same-process simulation: its “new session” and provider-switch cases do not start another process, exercise a real provider, prove persistence across sessions, or establish true parallel-agent locking. These checks do not prove that a real provider is installed or that Codex, Claude Code or DSH can call it.

Provider acceptance must keep these facts separate:

- Documentation claim: an official source describes a capability.
- Installation: the package or host integration is present.
- Configuration: the provider is enabled for this user and scope.
- Session callability: this Agent can call it now.
- Isolated verification: synthetic save/read/correct/delete and scope/concurrency checks passed.

If any required level is unknown, recommend no extra engine. A provider switch must stop old writes and migrate only explicitly selected records.

The optional `must_not` field is a human-review assertion; the legacy schema validator does not inspect its semantics. Keep all raw personal transcripts out of public issues and commits.

## Evaluating the two learning entry points

The [dual-entry cases](routing-cases.md#dual-learning-entry-points) cover intended behavior for task-based learning and an optional brief baseline. Both use the [learning protocol](../skills/adaptive-personal-ai-os/references/learning.md). The cases and checks below are an evaluation plan; adding or parsing them does not establish learning efficacy.

The [2026-10-13 local candidate report](../docs/VALIDATION-DUAL-LEARNING.md) records the checks actually run, synthetic subagent outputs, a wording defect and an isolated replay. It is not a real-learner or host-activation acceptance result.

First run actual host/model acceptance with synthetic scenarios. Record exact versions, loaded Skill evidence, prompts, outputs, tool effects and reviewer decisions. Check both entry points and a multi-turn sequence that switches in each direction: does teaching begin promptly, does a skipped item leave ability unknown, and does observed independent versus assisted performance survive the switch? Repeat key scenarios in new sessions to expose variability; preserve failures and the number of runs. Use synthetic files when checking no-save behavior. Do not use real private histories as fixtures.

Review each behavior against observable evidence:

| Dimension | Evidence to inspect | Insufficient evidence |
| --- | --- | --- |
| Useful start and adaptive support | A relevant first action; a question has a stated consequence for the next teaching step; examples and hints adjust to the specific need. | Counting fewer questions or assuming all questioning is bad. |
| Shared competence standard | Specific skill, task, actual assistance, observed result and uncertainty remain distinct in either mode. | A global level, confidence statement, response speed or technical vocabulary. |
| Independent performance | A new suitable task with a checked rubric; no hints, answer exposure or AI-produced answer before the attempt. | Success while following an example, copied work or two models agreeing. |
| Retention and transfer | Delayed performance and a different relevant task, reported separately with the interval, task relationship and help used. | An immediate repeat of the same problem or a scheduled check that never happened. |
| Choice and privacy | Direct help, skipped checks and mode switches work; tool logs show no unauthorized profile/card writes. | A promise of no writes without inspecting tool effects, or a claim that the host retains no history. |

Then evaluate learner outcomes separately, with consenting participants and tasks appropriate to their goal. Fix the target skill and success rubric before comparing approaches; validate task correctness and comparable difficulty. Record prior relevant performance and help provided. Keep training tasks separate from independent outcome tasks. Choose and report a justified delayed-check interval and a new transfer task; a missing follow-up remains unknown, never a pass or a zero substituted silently.

For efficiency, compare learning outcomes together with total learner time and burden, including onboarding, baseline, practice, interruptions and checks. Report completion and follow-up rates, independent immediate and delayed/transfer performance, help dependence, and time to the same prespecified independent criterion. Report time among successful learners with its denominator and dropout rate, so faster completion by a selected subset is not presented as an overall improvement. Self-reported burden and satisfaction are useful secondary measures, not substitutes for learning. Neither fewer questions nor faster assisted task completion establishes efficiency.

An exploratory comparison should state sample size, uncertainty and observed limitations. Self-selected groups, easier tasks or before/after gains cannot establish that an entry point caused improvement. For causal claims, use a suitably designed controlled comparison, such as random assignment among consenting participants, with equivalent goals, difficulty, rubrics and outcome checks; record switches and analyze them transparently rather than silently excluding them. Determine sample needs from the intended claim, not from the size of this authored case set. General teaching research supports a rationale within its studied conditions; it does not certify ZhiXu, either entry point, or a guaranteed benefit for an individual learner.

Keep three results separate in reports: schema validation, observed host behavior, and learner-outcome/efficiency evidence. If only the validator ran, mark the other two **not executed**. Publish only authorized, privacy-safe aggregate findings; never turn participant transcripts into public cases by light paraphrase.

## Comparing non-learning workflows

The [non-learning cases](routing-cases.md#non-learning-workflows) specify desired behavior; the original schema validator does not execute them. This maintenance round uses structural checks and only a small exploratory set of synthetic dialogues where explicitly recorded. It provides no statistical estimate of reliability, superiority or real-user benefit. List the actual cases and repeats executed in the report; all remaining specifications stay **not executed**. Neither a planned comparison nor an expected answer is an observed result.

For a behavior comparison, identify reproducible prior and candidate bundles by commit plus any patch/file hashes. Keep the previous learning changes in the baseline when the question is the effect of a non-learning change. Use the same task inputs, model/provider and settings, tool access, authorization, synthetic initial files, environment and budget for both versions. Record the loaded Skill path and trace separately. Restore fixtures between runs; isolate sessions to avoid carryover. Freeze relevant source snapshots or log differing live retrieval results, rather than silently attributing an environment difference to the Skill.

Define observable success conditions and failure categories before reviewing outputs. Present paired outputs in randomized order without version labels to a reviewer where practical. Review the result and tool trace, not whether the answer quotes the instructions. Record who reviewed them and whether genuine blinding or independent review was possible; self-review stays self-review. Do not build a string-contains scorer and describe it as a behavioral test. A model judge needs an independently checked rubric and calibration; agreement between models alone is not confirmation.

Report effects separately from costs:

| Dimension | Example outcome evidence | Separate cost evidence |
| --- | --- | --- |
| Planning | Work fits actual capacity; dependencies and completion conditions are respected. | User turns, clarification burden, planning time and later rework. |
| Decisions | Ineligible options are excluded; material uncertainty and a recommendation-change condition are visible. | Research delay, trial expense, interaction and tool calls. |
| Research | Important claims match inspected sources; duplicated and conflicting evidence are handled correctly. | Retrieval count, elapsed time and output size. |
| Continuity and memory | Correct entity, event time and version; plans, reports and observed actions remain distinct; actual tool scope is respected. | Retrieval overhead, unnecessary rereading and required user corrections. |
| Review and communication | A useful, evidence-bounded adjustment or requested draft; no invented motives or completion. | Added questions, reading burden and extra steps. |

Use case-level judgments such as met, partly met, failed and unobservable, with supporting output/tool evidence; keep environment unavailable distinct from behavior failure. Do not collapse quality and cost into an invented weighted score. Fewer questions, a shorter answer or more tool calls do not establish improvement by themselves. A prompt-only response cannot validate persistence or read-only enforcement; those need actual isolated fixture and tool-effect checks.

Repeat key cases in fresh sessions under both versions and report every attempt, including initial failures and retries. State the number and rationale for repeats; a few successful runs do not establish a failure rate. Preserve negative cases and adjacent boundaries. Reserve separately authored tasks that were not used to tune the instructions; disclose whether a real held-out set exists. If a reserved case informs a repair, it is no longer held out for a subsequent claim. Do not call a reworded copy of a training case an independent held-out task.

Keep raw synthetic outputs, conditions, reviewer disagreements and failures in the evidence record. Report schema counts, executed behavior counts and any downstream user-outcome evidence separately, with their denominators. This small pilot is for finding defects and deciding what to test next; claims about real planning efficiency, decision quality, recall or wellbeing require appropriate consented outcome evaluation and cannot be inferred from these authored examples.

## Evaluating everyday life support

The [everyday-life cases](routing-cases.md#everyday-life-support) add 18 fictional specifications: 6 positive, 4 negative and 8 boundary cases. All earlier 67 cases remain unchanged, including the previous learning and non-learning corrections. The complete routing dataset contains 85 specifications. Running the schema validator only checks format; it does not execute any of these behaviors. The [life-support candidate report](../docs/VALIDATION-LIFE.md) records four paired synthetic comparisons and three additional candidate responses, their conditions, judgments and gaps. It does not establish host acceptance or improved life outcomes; the broader checks below remain an evaluation plan.

Use the [paired comparison protocol](#comparing-non-learning-workflows) above and preserve the prior learning/non-learning bundle in the baseline when assessing a life-only change. Record the exact candidate and baseline files or hashes, model/provider settings, source retrieval, loaded Skill evidence, synthetic initial state and tools. Compare the same inputs under matched conditions; restore fixtures between runs. Repeat key positive, nonactivation and safety/authority scenarios in fresh sessions, disclosing the number of attempts and every failure or repair. Separately authored forward tasks may help detect transfer, but disclose whether they were actually reserved and whether any result informed a repair; independent authorship alone does not establish a held-out evaluation.

Inspect intended results rather than vocabulary:

| Dimension | Evidence to inspect | Insufficient evidence |
| --- | --- | --- |
| Routing and burden | The requested draft, recipe or fact is delivered directly; substantive support starts with a feasible action and only material clarification. | The presence of words about family, food, habits, health or money; a required mode menu or profile. |
| Goals and constraints | Irregular cues, coordination work, available time and protected enjoyment are reflected in the proposed action. Missing reports remain unknown. | Compliance counts, streaks, a packed schedule, mandatory records or promised productivity gains. |
| Cash-flow decisions | Available funds, confirmed later income and uncertain receivables are separate; balance is checked at relevant payment dates with visible conditions. | A positive monthly total, an expected invoice or a software budget category treated as spendable cash. |
| Career exploration and competence | Duties and opportunities have appropriate evidence; self-ratings and assisted work remain distinct from unassisted task performance. | A quiz label, an AI-produced artifact, a polished resume or a guaranteed job outcome. |
| Health and safety boundaries | Ordinary support is proportionate; persistent symptoms and disclosed acute danger receive appropriate direct support without compulsory intake. Sleep hygiene is not represented as treatment. | Quotas for every person, a diagnostic label, guessed local contacts or completion of an exercise goal. |
| Cooperation and authority | Chore drafts remain proposals; coercion changes the safe next step. Tool traces match valid standing authorization and the exact file/contact/reminder/account scope. | One person's consent attributed to others, a promise of safety, or a requested plan treated as authority for external action. |
| Privacy and continuity | Actual synthetic file/provider/tool effects honor no-save and no-history scope; saved artifacts are claimed only after observed success. | A verbal no-save promise alone, automatic profiling, an unexecuted save plan or a claim that host history is disabled. |

Judge each case as met, partly met, failed or unobservable with output and tool evidence; keep unavailable tools or sources separate from behavior failure. Use isolated synthetic files for V4-E-B007/B008 and inspect actual effects to test authorization or persistence. Do not use real health records, household finances or conversations. The `must_not` assertions guide human review; do not convert them into string-contains scoring and label that a behavioral test. State whether review is independent, blinded or self-review, preserving disagreements.

Keep schema validation, observed behavior, host activation and downstream outcomes separate. Prompt-only synthetic responses do not prove host loading, tool permissions, persistence or actual safety-service availability. Mark unexecuted cases and missing traces explicitly. A feasible proposed habit, cash-flow plan, career task or rest period does not establish improved habit automaticity, health, finances, employment, relationships or wellbeing. Those claims need an appropriate consented outcome evaluation, actual follow-up and stated uncertainty; they cannot be inferred from these authored cases or their schema count.
