"""Summarize explicitly supplied, reviewed paired runs; never execute or grade a model.

No network, provider discovery, transcript loading, file writes or release decision.
Input labels/evidence are caller assertions, not authenticated execution evidence.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re

CONDITIONS = {'model', 'host', 'settings', 'fixture', 'rubric'}
VERDICTS = {'met', 'partial', 'failed', 'unobservable'}
METRICS = {'elapsed_seconds', 'user_turns', 'tool_calls'}
RUN_FIELDS = {'case_id', 'variant', 'attempt', 'execution', 'verdict', 'source',
              'conditions', 'review', 'activation', 'evidence', 'note',
              'critical_violation', 'metrics'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 2000


def exact_keys(value, keys, label):
    require(isinstance(value, dict) and set(value) == keys, f'invalid {label} fields')


def validate(data):
    exact_keys(data, {'schema_version', 'cases', 'repeats', 'variants', 'runs'}, 'document')
    require(type(data['schema_version']) is int and data['schema_version'] == 1, 'schema_version must be 1')
    cases = data['cases']
    require(isinstance(cases, list) and 0 < len(cases) <= 500, 'cases must contain 1..500 IDs')
    require(all(text(x) for x in cases) and len(set(cases)) == len(cases), 'invalid or duplicate case IDs')
    require(type(data['repeats']) is int and 1 <= data['repeats'] <= 20, 'repeats must be 1..20')
    exact_keys(data['variants'], {'baseline', 'candidate'}, 'variants')
    require(all(isinstance(x, str) and re.fullmatch('[0-9a-f]{40}', x) for x in data['variants'].values()), 'variants require exact commit labels')
    require(data['variants']['baseline'] != data['variants']['candidate'], 'variant commit labels must differ')
    require(isinstance(data['runs'], list) and len(data['runs']) <= 20000, 'invalid runs list')
    seen = set()
    for r in data['runs']:
        exact_keys(r, RUN_FIELDS, 'run')
        require(isinstance(r['case_id'], str) and r['case_id'] in cases, 'unknown case')
        require(isinstance(r['variant'], str) and r['variant'] in data['variants'], 'unknown variant')
        require(type(r['attempt']) is int and 1 <= r['attempt'] <= data['repeats'], 'invalid attempt')
        key = (r['case_id'], r['variant'], r['attempt'])
        require(key not in seen, 'duplicate run; do not overwrite retries')
        seen.add(key)
        require(r['execution'] in ('completed', 'blocked', 'not_run'), 'invalid execution')
        require(isinstance(r['verdict'], str) and r['verdict'] in VERDICTS, 'invalid verdict')
        require(r['source'] in ('observed', 'demonstration'), 'invalid source')
        require(r['activation'] in ('verified', 'unverified'), 'invalid activation')
        require(r['critical_violation'] is None or type(r['critical_violation']) is bool, 'critical_violation must be boolean or null')
        require(text(r['note']), 'a review note or blocking reason is required')
        require(isinstance(r['evidence'], list) and len(r['evidence']) <= 30 and all(text(x) for x in r['evidence']), 'invalid evidence references')
        exact_keys(r['conditions'], CONDITIONS, 'conditions')
        require(all(text(x) for x in r['conditions'].values()), 'conditions require nonempty identifiers')
        exact_keys(r['review'], {'kind', 'reviewer', 'blind'}, 'review')
        require(r['review']['kind'] in ('human', 'self', 'model') and text(r['review']['reviewer']), 'invalid reviewer')
        require(type(r['review']['blind']) is bool, 'blind must be boolean')
        require(not (r['review']['kind'] == 'self' and r['review']['blind']), 'self-review cannot be labelled blind')
        if r['execution'] == 'completed':
            require(bool(r['evidence']), 'completed runs require evidence references')
        else:
            require(r['verdict'] == 'unobservable', 'blocked/not-run is not a behavior pass or failure')
        require(isinstance(r['metrics'], dict) and not (set(r['metrics']) - METRICS), 'invalid metrics')
        for name, value in r['metrics'].items():
            require(type(value) in (int, float) and 0 <= value <= 10**12 and math.isfinite(value), 'metrics must be finite numbers in 0..10^12, not booleans')
            if name != 'elapsed_seconds':
                require(type(value) is int, 'count metrics must be integers')
    return data


def summarize(data):
    validate(data)
    runs = data['runs']
    index = {(r['case_id'], r['variant'], r['attempt']): r for r in runs}
    variants = {}
    for variant in data['variants']:
        selected = [r for r in runs if r['variant'] == variant]
        observed = [r for r in selected if r['source'] == 'observed']
        completed = [r for r in observed if r['execution'] == 'completed']
        judged = [r for r in completed if r['verdict'] != 'unobservable']
        variants[variant] = {
            'expected_runs': len(data['cases']) * data['repeats'],
            'provided_runs': len(selected),
            'demonstrations': sum(r['source'] == 'demonstration' for r in selected),
            'observed_execution': dict(Counter(r['execution'] for r in observed)),
            'observed_completed_verdicts': dict(Counter(r['verdict'] for r in completed)),
            'met_fraction_of_judged': {'numerator': sum(r['verdict'] == 'met' for r in judged), 'denominator': len(judged)},
            'activation_unverified': sum(r['activation'] != 'verified' for r in completed),
            'critical_review_unknown': sum(r['critical_violation'] is None for r in observed),
            'review_kinds': dict(Counter(r['review']['kind'] for r in judged)),
        }
    missing, pairs, violations = [], [], []
    for r in runs:
        if r['source'] == 'observed' and r['critical_violation'] is True:
            violations.append({'case_id': r['case_id'], 'variant': r['variant'], 'attempt': r['attempt'], 'evidence': r['evidence']})
    for case_id in data['cases']:
        for attempt in range(1, data['repeats'] + 1):
            sides = [index.get((case_id, v, attempt)) for v in ('baseline', 'candidate')]
            for variant, r in zip(('baseline', 'candidate'), sides):
                if r is None:
                    missing.append({'case_id': case_id, 'variant': variant, 'attempt': attempt})
            reason = None
            if any(r is None for r in sides):
                reason = 'missing_run'
            elif any(r['source'] != 'observed' for r in sides):
                reason = 'demonstration_not_observation'
            elif any(r['execution'] != 'completed' or r['verdict'] == 'unobservable' for r in sides):
                reason = 'incomplete_or_unjudged'
            elif any(r['activation'] != 'verified' for r in sides):
                reason = 'activation_unverified'
            elif sides[0]['conditions'] != sides[1]['conditions'] or sides[0]['review'] != sides[1]['review']:
                reason = 'unmatched_conditions_or_review'
            item = {'case_id': case_id, 'attempt': attempt, 'comparable': reason is None}
            if reason:
                item['reason'] = reason
            else:
                a, b = sides
                order = {'failed': 0, 'partial': 1, 'met': 2}
                delta = order[b['verdict']] - order[a['verdict']]
                item['rubric_change'] = 'better' if delta > 0 else 'worse' if delta < 0 else 'same'
                item['baseline_verdict'], item['candidate_verdict'] = a['verdict'], b['verdict']
                item['cost_delta_candidate_minus_baseline'] = {name: b['metrics'][name] - a['metrics'][name] for name in sorted(a['metrics'].keys() & b['metrics'].keys())}
            pairs.append(item)
    return {'variants': variants, 'missing_runs': missing, 'pairs': pairs,
            'paired_changes': dict(Counter(p['rubric_change'] for p in pairs if p['comparable'])),
            'reported_critical_violations': violations,
            'scope': 'Aggregation of caller-supplied reviews only; no model execution, automatic grading, artifact reading or evidence authentication.',
            'limits': 'No causal, statistical, host-activation or real-life efficacy claim follows from this report. Zero reported violations does not prove safety. No release approval is computed.'}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    args = parser.parse_args()
    try:
        require(not args.input.is_symlink() and args.input.is_file(), 'input must be an explicit regular file, not a symlink')
        require(args.input.stat().st_size <= 2 * 1024 * 1024, 'input exceeds 2 MiB')
        data = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError('non-finite JSON value')))
        print(json.dumps(summarize(data), ensure_ascii=False, indent=2, allow_nan=False))
    except (OSError, ValueError) as error:
        parser.exit(2, f'Cannot summarize evaluations: {error}\n')


if __name__ == '__main__':
    main()
