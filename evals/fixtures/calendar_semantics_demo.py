"""Offline synthetic time arithmetic; not a calendar adapter or agent evaluation.

Uses only the installed Python/IANA database. Does not install data, read calendars,
parse ICS, expand recurrence rules, create events or validate a provider.
"""
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import json
import sys


def demonstrate():
    zone = ZoneInfo('America/New_York')
    before = datetime(2024, 3, 9, 9, tzinfo=zone)
    next_local_morning = before + timedelta(days=1)
    next_elapsed_day = (before.astimezone(timezone.utc) + timedelta(hours=24)).astimezone(zone)
    first = datetime(2024, 11, 3, 1, 30, tzinfo=zone, fold=0)
    second = first.replace(fold=1)
    # Compare elapsed instants in UTC, not wall-clock subtraction within one zone.
    gap = int((second.astimezone(timezone.utc) - first.astimezone(timezone.utc)).total_seconds())
    start, exclusive_end = date(2024, 4, 8), date(2024, 4, 10)
    included = [start + timedelta(days=i) for i in range((exclusive_end-start).days)]
    assert next_local_morning.hour == 9 and next_elapsed_day.hour == 10
    assert int((next_local_morning.astimezone(timezone.utc)-before.astimezone(timezone.utc)).total_seconds()) == 23*3600
    assert first.isoformat() != second.isoformat() and gap == 3600
    assert included == [date(2024, 4, 8), date(2024, 4, 9)]
    return {
        'scope': 'synthetic arithmetic demonstration, not real host or agent validation',
        'python': sys.version.split()[0],
        'zone': zone.key,
        'timezone_database_version': 'not independently identified; installed data only',
        'same_local_time_next_date': next_local_morning.isoformat(),
        'after_24_elapsed_hours': next_elapsed_day.isoformat(),
        'repeated_local_time': [first.isoformat(), second.isoformat()],
        'repeated_time_elapsed_gap_seconds': gap,
        'all_day_dates_before_exclusive_end': [day.isoformat() for day in included],
        'external_writes': 'none',
    }


if __name__ == '__main__':
    try:
        result = demonstrate()
    except ZoneInfoNotFoundError:
        print(json.dumps({'status': 'blocked', 'reason': 'required installed IANA zone unavailable; no installation attempted'}))
        raise SystemExit(2)
    print(json.dumps(result, indent=2))
