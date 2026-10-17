"""Read-only arithmetic for one explicitly supplied cash-flow scenario.

No bank access, transactions, storage writes, forecasts of income or financial
recommendation. Amounts and dates are unverified caller assumptions. Standard
library only; keep using an existing suitable calculator/tool when available.
"""
import argparse
from collections import defaultdict
from datetime import date
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact_fields(value, fields, label):
    require(isinstance(value, dict) and set(value) == fields, f'invalid {label} fields')


def parse_date(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), 'use a complete ISO date')
    return date.fromisoformat(value)


def units(value, scale, *, signed=False):
    require(isinstance(value, str) and re.fullmatch(r'-?(?:0|[1-9][0-9]{0,11})(?:\.[0-9]{1,3})?', value), 'amounts must be unambiguous decimal strings')
    negative = value.startswith('-')
    require(signed or not negative, 'event amounts must be nonnegative')
    parts = value.lstrip('-').split('.')
    fraction = parts[1] if len(parts) == 2 else ''
    require(len(fraction) <= scale, 'amount exceeds selected precision; no silent rounding')
    amount = int(parts[0]) * 10**scale + int(fraction.ljust(scale, '0') or '0')
    return -amount if negative else amount


def formatted(value, scale):
    sign = '-' if value < 0 else ''
    whole, fraction = divmod(abs(value), 10**scale)
    return f'{sign}{whole}' + (f'.{fraction:0{scale}d}' if scale else '')


def calculate(data):
    exact_fields(data, {'schema_version', 'currency', 'scale', 'as_of', 'horizon', 'opening_available', 'events'}, 'scenario')
    require(type(data['schema_version']) is int and data['schema_version'] == 1, 'schema_version must be 1')
    require(isinstance(data['currency'], str) and re.fullmatch('[A-Z]{3}', data['currency']), 'supply one three-letter currency label')
    scale = data['scale']
    require(type(scale) is int and 0 <= scale <= 3, 'scale must be an integer from 0 to 3')
    start, end = parse_date(data['as_of']), parse_date(data['horizon'])
    require(start <= end, 'horizon must not precede as_of')
    opening = units(data['opening_available'], scale, signed=True)
    require(isinstance(data['events'], list) and len(data['events']) <= 1000, 'events must be a list of at most 1000 items')
    grouped, ignored, seen = defaultdict(list), [], set()
    for event in data['events']:
        exact_fields(event, {'id', 'date', 'direction', 'amount', 'bound', 'certainty'}, 'event')
        eid = event['id']
        require(isinstance(eid, str) and eid == eid.strip() and 0 < len(eid) <= 100 and eid not in seen, 'event IDs must be nonempty, trimmed and unique')
        seen.add(eid)
        when = parse_date(event['date'])
        require(start <= when <= end, 'event date outside the selected horizon; avoid double counting already received money')
        require(event['direction'] in ('income', 'expense'), 'direction must be income or expense')
        require(event['bound'] in ('exact', 'minimum'), 'bound must be exact or minimum')
        require(event['certainty'] in ('confirmed', 'uncertain'), 'invalid certainty')
        amount = None if event['amount'] is None else units(event['amount'], scale)
        if event['direction'] == 'income':
            require(event['bound'] == 'exact', 'this helper does not support income ranges')
            if event['certainty'] == 'uncertain':
                ignored.append(eid)
                continue
            require(amount is not None, 'confirmed income needs an explicit amount')
        else:
            require(event['certainty'] == 'confirmed', 'use separate scenarios for optional expenses')
            require(amount is not None or event['bound'] == 'minimum', 'unknown expense amount cannot be labelled exact')
        grouped[when].append((event, amount))

    balance, upper_bound = opening, False
    days, negative_closing, timing_risks, unknown_amounts = [], [], [], []

    def balance_value(value, bounded):
        return {'amount': formatted(value, scale), 'kind': 'upper_bound' if bounded else 'conditional_exact'}

    for when, events in sorted(grouped.items()):
        previous, previous_bound = balance, upper_bound
        expenses = sum(amount or 0 for event, amount in events if event['direction'] == 'expense')
        income = sum(amount for event, amount in events if event['direction'] == 'income')
        minimum_ids = [event['id'] for event, _ in events if event['direction'] == 'expense' and event['bound'] == 'minimum']
        missing = [event['id'] for event, amount in events if event['direction'] == 'expense' and amount is None]
        unknown_amounts.extend(missing)
        upper_bound = upper_bound or bool(minimum_ids)
        before_income = balance - expenses
        balance = before_income + income
        day = when.isoformat()
        if balance < 0:
            negative_closing.append(day)
        if before_income < 0 <= balance and income > 0:
            timing_risks.append(day)
        days.append({'date': day,
                     'included_event_ids': [event['id'] for event, _ in events],
                     'opening': balance_value(previous, previous_bound),
                     'listed_expense_minimum': formatted(expenses, scale),
                     'assumed_confirmed_income': formatted(income, scale),
                     'expenses_first_balance': balance_value(before_income, upper_bound),
                     'closing': balance_value(balance, upper_bound),
                     'same_day_order_unverified': bool(income and any(e['direction'] == 'expense' for e, _ in events)),
                     'minimum_expense_ids': minimum_ids, 'unknown_expense_amount_ids': missing})
    return {'currency_label': data['currency'], 'scale': scale, 'as_of': data['as_of'], 'horizon': data['horizon'],
            'input_facts_verified': False, 'opening_available_negative': opening < 0,
            'date_rows': 'Only dates with included events are listed; the balance carries forward between them.', 'days': days,
            'ending': balance_value(balance, upper_bound),
            'negative_projected_closing_dates': negative_closing,
            'possible_intraday_shortfall_dates': timing_risks,
            'ignored_uncertain_income_ids': ignored,
            'unknown_expense_amount_ids': unknown_amounts,
            'limits': 'Calculation only, not permission or advice to spend. Future confirmed income is assumed, not verified cash. Same-day expenses are placed before income to expose timing risk, not to assert actual order. Missing/minimum expenses make balances upper bounds, never proof of affordability. Excludes unlisted fees, restricted funds, currency conversion, borrowing and investment outcomes.'}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--input', type=Path)
    choice.add_argument('--example', action='store_true', help='Print fictional input only; no calculation or files are written')
    args = parser.parse_args()
    if args.example:
        print(json.dumps({'schema_version': 1, 'currency': 'CNY', 'scale': 2,
                          'as_of': '2030-04-01', 'horizon': '2030-04-30', 'opening_available': '300.00',
                          'events': [
                              {'id': 'fictional-bill', 'date': '2030-04-03', 'direction': 'expense', 'amount': '500.00', 'bound': 'exact', 'certainty': 'confirmed'},
                              {'id': 'fictional-receipt', 'date': '2030-04-10', 'direction': 'income', 'amount': '1000.00', 'bound': 'exact', 'certainty': 'confirmed'}]}, indent=2))
        return
    try:
        require(args.input.is_file() and not args.input.is_symlink(), 'choose an explicit regular input file')
        require(args.input.stat().st_size <= 1024 * 1024, 'input exceeds 1 MiB')
        data = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
        print(json.dumps(calculate(data), ensure_ascii=False, indent=2, allow_nan=False))
    except (OSError, ValueError) as error:
        parser.exit(2, f'Cannot calculate scenario: {error}\n')


if __name__ == '__main__':
    main()
