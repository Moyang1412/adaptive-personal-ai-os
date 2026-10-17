# PersonaMem-v3 selection review · 2026-10-17

Source: [pinned repository](https://github.com/bowen-upenn/PersonaMem-v3/tree/ad80a3b1b322129fb0585ead33b129a87bb4e387). Read README and LICENSE; inspected the rubric applicability/penalty maps, source-A builder, source-B builder and score function in [personalization_rubric.py](https://github.com/bowen-upenn/PersonaMem-v3/blob/ad80a3b1b322129fb0585ead33b129a87bb4e387/evaluation/personalization_rubric.py). This is a targeted source review, not an end-to-end harness audit or executed benchmark.

## Useful distinctions

The inspected rubric separates task usefulness, restraint and privacy/stale-context checks. Its source-B path uses later engagements for diagnostic scoring, rather than as an agent instruction. Source-A construction also includes a scorer-only nearby-time slice, so names/comments alone do not establish a temporal boundary; actual caller data flow needs auditing. We adopt a short research instruction to keep future evidence and grader labels out of the evaluated agent's inputs.

The [v1 paper](https://arxiv.org/html/2608.21381v1) was inspected for construction, over-personalization, temporal/recall limits and limitations. Its user worlds build on cohort-aggregated/resampled engagement data and model-generated expansion; they are not direct evidence from ZhiXu users. The paper describes model-dependent effects of adding memory, so we do not treat a larger profile or another engine as automatically better. Its psychological scaffolds are not clinical diagnoses.

## Not adopted

- The repository [license](https://github.com/bowen-upenn/PersonaMem-v3/blob/ad80a3b1b322129fb0585ead33b129a87bb4e387/LICENSE) separates MIT code from CC-BY-NC-4.0 source/derived data. No dataset or personal profiles were downloaded, copied into the Skill or used commercially here.
- No full framework, provider, GPU setup or paid model/judge calls. No inference of sensitive traits from the owner's activity, and no automatic cross-platform harvesting.
- No copied numeric weights, success threshold or universal ban on explaining personalization. The inspected score function defaults missing hard-rule keys through a boolean conversion and can assign numeric outputs after judge gaps; our existing bookkeeping preserves unobservable/unknown states instead. This static observation is not a claim that every benchmark run is affected.
- Existing ZhiXu relevance, consent, current-user-correction and direct-help rules already cover most personalization restraint. We add boundary specifications rather than repeat a whole new personality protocol. Restraint must not become an excuse to withhold an ordinary useful answer.

Four authored scenarios cover irrelevant history, private context excluded from a draft, an explicit wish to explore beyond an old preference, and future-label leakage. They are original synthetic specifications, not copied benchmark records or executed model trials. No improved personalization score, host activation or real-life benefit is established by this review.
