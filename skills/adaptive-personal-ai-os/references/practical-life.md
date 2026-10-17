# Practical household, travel and digital coordination

Use these only for the requested task, not as a requirement to maintain a household
database. Reuse an existing list or system before suggesting another app.

- **Meals and supplies:** distinguish what is actually on hand, reserved for a
  plan, on a shopping list, ordered and received. Check meaningful quantities,
  units, storage and preparation constraints before making a shopping list. A
  recorded date or inventory entry does not establish food safety; use appropriate
  current guidance for that question. Do not equate a missed inventory update
  with zero stock or count the same ingredient for two incompatible plans.
- **Housing, appointments and errands:** work backward from the actual deadline,
  required documents and dependencies. Distinguish a draft, a submitted request,
  a confirmed appointment and a completed outcome. Check the current local
  provider or authority for eligibility, fees and required originals; a checklist
  from another place is not local law. Preserve an existing booking until a
  replacement and any cancellation consequences are verified and authorized.
- **Travel and outings:** check dates, local time zones, door-to-door travel,
  accessibility and relevant opening/booking constraints. Leave a practical
  fallback for a fragile connection or weather-dependent activity; do not treat
  a search result as confirmed availability. Match structure to the desired
  relaxation or exploration, rather than fill all free time.
- **Digital upkeep:** separate a local file, a synced copy and a tested backup.
  Before cleanup or migration, identify the intended copy and a recovery path;
  deleting a synced item may propagate. A backup job reporting success is not
  evidence that a restore was tested. Do not collect credentials, broaden access
  or delete personal data merely to simplify an organisation plan.

When using a household tool, inspect coupled effects before recording an action:
marking a chore may also consume stock, advance a schedule or assign someone.
Consent to a record is not automatically consent to those additional effects.
Represent skipped, undone and completed actions distinctly and verify the actual
update before relying on the next calculated state.

## Calendar details when they change the result

For a real appointment, recurring reminder or imported event, preserve its date,
zone and intended recurrence. A named zone can change offset; every local morning
is not always every 24 elapsed hours. Resolve repeated/missing local times before
an authorized write, using the actual service's semantics. Keep all-day dates as
dates; iCalendar VEVENT DTEND is exclusive, not an extra occupied day. Do not
silently convert a missing monthly date into month-end. Check exceptions and
whether an edit affects one occurrence or a series. A free/busy lookup does not
reserve the slot or establish another person's agreement.

Use available calendar tools and current zone data rather than build a new engine.
For an ordinary relative-time question with enough context, answer directly; do
not demand calendar access or a recurrence questionnaire.

## Evidence boundary

These are task-coordination safeguards, not a validated life intervention or local legal/medical advice. Verify actual providers, location, dates and permissions for the user's task.

- [Grocy chore implementation, pinned source](https://github.com/grocy/grocy/blob/41206cb90154e0d17d3e108cc1f182b94fdb465d/services/ChoresService.php): the inspected code distinguishes tracked/skipped/undone states and exposes coupled stock/assignment effects. This informs side-effect checks, not a recommendation to install it or adopt its assignment algorithm.

- [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545), sections 3.3.5, 3.3.10 and 3.6.1; [Python zoneinfo](https://docs.python.org/3/library/zoneinfo.html): temporal distinctions, not proof of a particular calendar provider’s behavior.

For capacity or conflicting priorities, use only the relevant part of [planning](planning-decisions.md); for actual health needs use [health](health-habits.md). A request for a simple shopping-list rewrite needs no full protocol.
