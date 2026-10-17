# Calendar semantics review · 2026-10-17

The earlier practical-life reference requested date/time-zone checks but did not explain recurrence intent, occurrence-versus-series scope or date-only boundaries. The conditional practical reference now names those checks without imposing them on simple questions.

## Sources and adopted scope

- [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545): inspected DATE-TIME, recurrence and VEVENT boundary sections. Calendar serialization rules inform careful interpretation; they are not universal booking-provider behavior or permission to choose an ambiguous user intent.
- [Python zoneinfo documentation](https://docs.python.org/3/library/zoneinfo.html): inspected offset transitions, fold and data availability. Use installed authoritative tooling; do not add a custom timezone database or silently install dependencies.

## Executed evidence

[Offline arithmetic demonstration](../evals/fixtures/calendar_semantics_demo.py), Python 3.12.14 and the installed IANA data:

- New York 2024-03-09 09:00 to the next local 09:00 spans 23 elapsed hours; adding 24 elapsed hours arrives at 10:00.
- New York 2024-11-03 01:30 has two represented instants one hour apart.
- A synthetic date interval April 8 up to April 10 contains April 8 and 9.

The demonstration uses UTC for elapsed differences and reports database-version uncertainty. It is not an ICS parser, recurrence engine, old/new agent comparison or real booking test. Missing zone data produces a blocked result, not an installation. Six authored scenarios cover recurrence intent, ambiguity, all-day interpretation, missing monthly dates, single-occurrence scope and a direct-answer negative control. Their schema validation does not execute an agent.

No calendars accessed, reminders created, invitations sent or bookings changed. Existing host permissions and documented service behavior still govern any real action.
