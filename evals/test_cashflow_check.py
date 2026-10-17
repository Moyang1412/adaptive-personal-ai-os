"""Synthetic arithmetic tests, not bank integration or financial advice."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/adaptive-personal-ai-os/scripts/check_cashflow.py'
spec = importlib.util.spec_from_file_location('cashflow_check', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
calculate = module.calculate


def event(eid, direction, amount, day='2030-04-03', **changes):
    result = {'id': eid, 'date': day, 'direction': direction, 'amount': amount, 'bound': 'exact', 'certainty': 'confirmed'}
    result.update(changes)
    return result


def scenario(*events, **changes):
    result = {'schema_version': 1, 'currency': 'CNY', 'scale': 2, 'as_of': '2030-04-01', 'horizon': '2030-04-30', 'opening_available': '300.00', 'events': list(events)}
    result.update(changes)
    return result


class CashflowTests(unittest.TestCase):
    def test_decimal_arithmetic_is_exact(self):
        r = calculate(scenario(event('a', 'income', '0.10'), event('b', 'income', '0.20'), opening_available='0'))
        self.assertEqual(r['ending']['amount'], '0.30')

    def test_month_end_surplus_does_not_hide_earlier_shortfall(self):
        r = calculate(scenario(event('bill', 'expense', '500'), event('receipt', 'income', '1000', '2030-04-10')))
        self.assertEqual(r['negative_projected_closing_dates'], ['2030-04-03'])
        self.assertEqual(r['ending']['amount'], '800.00')

    def test_uncertain_income_is_excluded(self):
        r = calculate(scenario(event('maybe', 'income', '1000', certainty='uncertain'), event('bill', 'expense', '500')))
        self.assertEqual(r['ending']['amount'], '-200.00')
        self.assertEqual(r['ignored_uncertain_income_ids'], ['maybe'])

    def test_unknown_uncertain_income_is_not_zero_cash(self):
        r = calculate(scenario(event('maybe', 'income', None, certainty='uncertain')))
        self.assertEqual(r['ignored_uncertain_income_ids'], ['maybe'])
        self.assertEqual(r['days'], [])

    def test_minimum_expense_produces_upper_bound(self):
        r = calculate(scenario(event('repair', 'expense', '100', bound='minimum')))
        self.assertEqual(r['ending'], {'amount': '200.00', 'kind': 'upper_bound'})

    def test_unknown_expense_is_visible_and_not_affordability(self):
        r = calculate(scenario(event('unknown', 'expense', None, bound='minimum')))
        self.assertEqual(r['unknown_expense_amount_ids'], ['unknown'])
        self.assertEqual(r['ending']['kind'], 'upper_bound')

    def test_upper_bound_persists_after_later_income(self):
        r = calculate(scenario(event('unknown', 'expense', None, bound='minimum'), event('receipt', 'income', '1000', '2030-04-10')))
        self.assertEqual(r['days'][-1]['opening']['kind'], 'upper_bound')
        self.assertEqual(r['ending']['kind'], 'upper_bound')

    def test_same_day_order_is_not_assumed_safe(self):
        r = calculate(scenario(event('receipt', 'income', '1000'), event('bill', 'expense', '500')))
        self.assertEqual(r['possible_intraday_shortfall_dates'], ['2030-04-03'])
        self.assertTrue(r['days'][0]['same_day_order_unverified'])
        self.assertEqual(r['days'][0]['expenses_first_balance']['amount'], '-200.00')

    def test_events_are_sorted_without_mutation(self):
        data = scenario(event('late', 'income', '100', '2030-04-10'), event('early', 'expense', '50'))
        before = deepcopy(data)
        self.assertEqual([x['date'] for x in calculate(data)['days']], ['2030-04-03', '2030-04-10'])
        self.assertEqual(data, before)

    def test_precision_is_explicit(self):
        self.assertEqual(calculate(scenario(opening_available='12', currency='JPY', scale=0))['ending']['amount'], '12')
        self.assertEqual(calculate(scenario(opening_available='12.345', currency='BHD', scale=3))['ending']['amount'], '12.345')
        with self.assertRaises(ValueError):
            calculate(scenario(opening_available='12.345'))

    def test_invalid_amounts(self):
        for amount in (True, 0.1, '1,000', '1e3', 'NaN', '', ' 1', '01', '1000000000000'):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                calculate(scenario(opening_available=amount))
        with self.assertRaises(ValueError):
            calculate(scenario(event('bad', 'income', '-1')))

    def test_invalid_dates_and_horizon(self):
        for day in ('2030-02-30', '04-03', '2030-03-31', '2030-05-01'):
            with self.subTest(day=day), self.assertRaises(ValueError):
                calculate(scenario(event('bad', 'expense', '1', day)))
        with self.assertRaises(ValueError):
            calculate(scenario(horizon='2030-03-31'))

    def test_duplicate_ids_and_mixed_currency_fields(self):
        with self.assertRaises(ValueError):
            calculate(scenario(event('same', 'income', '1'), event('same', 'expense', '1')))
        with self.assertRaises(ValueError):
            calculate(scenario(event('bad', 'income', '1', currency='USD')))

    def test_unknown_or_ranges_cannot_be_silently_exact(self):
        bad = [event('a', 'income', None), event('b', 'income', '1', bound='minimum'),
               event('c', 'expense', None), event('d', 'expense', '1', certainty='uncertain')]
        for row in bad:
            with self.subTest(row=row), self.assertRaises(ValueError):
                calculate(scenario(row))

    def test_boolean_metadata_rejected(self):
        for changes in ({'scale': True}, {'schema_version': True}, {'currency': 'CN'}, {'opening_available': None}):
            with self.assertRaises(ValueError):
                calculate(scenario(**changes))

    def test_empty_and_negative_opening(self):
        result = calculate(scenario(opening_available='-5'))
        self.assertTrue(result['opening_available_negative'])
        self.assertEqual(result['ending']['amount'], '-5.00')
        self.assertFalse(result['input_facts_verified'])

    def test_cli_example_and_named_input_are_read_only(self):
        example = subprocess.run([sys.executable, str(SCRIPT), '--example'], capture_output=True, text=True)
        self.assertEqual(example.returncode, 0, example.stderr)
        data = json.loads(example.stdout)
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'synthetic.json'
            source.write_text(json.dumps(data), encoding='utf-8')
            before = source.read_bytes()
            run = subprocess.run([sys.executable, str(SCRIPT), '--input', str(source)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['ending']['amount'], '800.00')
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual(list(Path(folder).iterdir()), [source])
            source.write_text('{"scale":2,"scale":2}')
            bad = subprocess.run([sys.executable, str(SCRIPT), '--input', str(source)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            self.assertIn('duplicate JSON key', bad.stderr)


if __name__ == '__main__':
    unittest.main()
