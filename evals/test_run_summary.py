"""Synthetic records test bookkeeping, not actual assistant behavior or efficacy."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.summarize_eval_runs import summarize


def record(variant, **changes):
    value = {'case_id': 'fictional-errand', 'variant': variant, 'attempt': 1,
             'execution': 'completed', 'verdict': 'met', 'source': 'observed',
             'conditions': {'model': 'fixture-model', 'host': 'fixture-host',
                            'settings': 'same-settings', 'fixture': 'same-inputs', 'rubric': 'rubric-v1'},
             'review': {'kind': 'human', 'reviewer': 'fictional-reviewer', 'blind': True},
             'activation': 'verified', 'evidence': ['synthetic-output-1'],
             'note': 'Fabricated unit-test input, not an observed model run.',
             'critical_violation': False, 'metrics': {'elapsed_seconds': 10, 'tool_calls': 2}}
    value.update(changes)
    return value


def document(*runs):
    return {'schema_version': 1, 'cases': ['fictional-errand'], 'repeats': 1,
            'variants': {'baseline': 'a' * 40, 'candidate': 'b' * 40}, 'runs': list(runs)}


class SummaryTests(unittest.TestCase):
    def test_empty_is_not_success(self):
        result = summarize(document())
        self.assertEqual(len(result['missing_runs']), 2)
        self.assertEqual(result['variants']['candidate']['met_fraction_of_judged']['denominator'], 0)
        self.assertEqual(result['paired_changes'], {})

    def test_matching_pair_and_separate_cost(self):
        result = summarize(document(record('baseline', verdict='partial'), record('candidate', metrics={'elapsed_seconds': 12})))
        self.assertEqual(result['paired_changes'], {'better': 1})
        self.assertEqual(result['pairs'][0]['cost_delta_candidate_minus_baseline'], {'elapsed_seconds': 2})

    def test_regressions_are_retained(self):
        result = summarize(document(record('baseline'), record('candidate', verdict='failed')))
        self.assertEqual(result['paired_changes'], {'worse': 1})

    def test_no_best_of_retry_selection(self):
        data = document(record('baseline'), record('candidate', verdict='failed'), record('baseline', attempt=2), record('candidate', attempt=2))
        data['repeats'] = 2
        result = summarize(data)
        self.assertEqual(result['paired_changes'], {'worse': 1, 'same': 1})
        self.assertEqual(result['variants']['candidate']['met_fraction_of_judged'], {'numerator': 1, 'denominator': 2})

    def test_demonstration_excluded(self):
        result = summarize(document(record('baseline', source='demonstration'), record('candidate', source='demonstration')))
        self.assertEqual(result['variants']['candidate']['observed_execution'], {})
        self.assertEqual(result['pairs'][0]['reason'], 'demonstration_not_observation')

    def test_blocked_does_not_become_failure(self):
        result = summarize(document(record('baseline'), record('candidate', execution='blocked', verdict='unobservable', evidence=[])))
        self.assertEqual(result['pairs'][0]['reason'], 'incomplete_or_unjudged')
        self.assertEqual(result['variants']['candidate']['observed_completed_verdicts'], {})

    def test_not_run_cannot_pass(self):
        with self.assertRaises(ValueError):
            summarize(document(record('candidate', execution='not_run')))

    def test_activation_remains_unverified(self):
        result = summarize(document(record('baseline'), record('candidate', activation='unverified')))
        self.assertEqual(result['pairs'][0]['reason'], 'activation_unverified')

    def test_each_condition_mismatch(self):
        for field in ('model', 'host', 'fixture', 'settings', 'rubric'):
            a, b = record('baseline'), record('candidate')
            b['conditions'][field] = 'changed'
            with self.subTest(field=field):
                self.assertEqual(summarize(document(a, b))['pairs'][0]['reason'], 'unmatched_conditions_or_review')

    def test_review_mismatch_and_self_review(self):
        a, b = record('baseline'), record('candidate')
        b['review'] = {'kind': 'self', 'reviewer': 'author', 'blind': False}
        self.assertFalse(summarize(document(a, b))['pairs'][0]['comparable'])
        b['review']['blind'] = True
        with self.assertRaises(ValueError):
            summarize(document(a, b))

    def test_critical_events_not_hidden_by_passes(self):
        result = summarize(document(record('candidate', critical_violation=True)))
        self.assertEqual(len(result['reported_critical_violations']), 1)
        self.assertNotIn('release_ready', result)

    def test_unknown_review_stays_unknown(self):
        result = summarize(document(record('candidate', critical_violation=None)))
        self.assertEqual(result['variants']['candidate']['critical_review_unknown'], 1)

    def test_duplicate_and_unknown_run(self):
        for runs in [(record('baseline'), record('baseline')), (record('candidate', case_id='unlisted'),)]:
            with self.assertRaises(ValueError):
                summarize(document(*runs))

    def test_completed_requires_evidence(self):
        with self.assertRaises(ValueError):
            summarize(document(record('candidate', evidence=[])))

    def test_invalid_numbers_and_truthy_flags(self):
        for value in (True, -1, float('nan'), float('inf'), 10**1000, '10'):
            with self.subTest(value=str(value)[:30]), self.assertRaises(ValueError):
                summarize(document(record('candidate', metrics={'elapsed_seconds': value})))
        for changes in ({'attempt': True}, {'critical_violation': 'false'}):
            with self.assertRaises(ValueError):
                summarize(document(record('candidate', **changes)))

    def test_invalid_document_metadata(self):
        for field, value in [('schema_version', True), ('repeats', 0), ('cases', ['x', 'x'])]:
            data = document()
            data[field] = value
            with self.assertRaises(ValueError):
                summarize(data)

    def test_input_is_not_mutated(self):
        data = document(record('baseline'), record('candidate'))
        before = deepcopy(data)
        summarize(data)
        self.assertEqual(data, before)

    def test_cli_only_reads_named_file(self):
        script = Path(__file__).resolve().parents[1] / 'scripts/summarize_eval_runs.py'
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'runs.json'
            source.write_text(json.dumps(document()), encoding='utf-8')
            untouched = root / 'do-not-read.txt'
            untouched.write_text('synthetic unrelated private fixture', encoding='utf-8')
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            run = subprocess.run([sys.executable, str(script), '--input', str(source)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['paired_changes'], {})
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})
            source.write_text('{"schema_version":1,"schema_version":1}', encoding='utf-8')
            bad = subprocess.run([sys.executable, str(script), '--input', str(source)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            self.assertIn('duplicate JSON key', bad.stderr)


if __name__ == '__main__':
    unittest.main()
