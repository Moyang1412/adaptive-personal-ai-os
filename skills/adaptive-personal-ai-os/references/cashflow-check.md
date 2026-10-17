# Optional dated cash-flow arithmetic

Reuse an appropriate available calculator or existing budget tool first. If Python
is already available and the user requests checking supplied cash-flow figures,
the bundled [read-only helper](../scripts/check_cashflow.py) can check one explicit
JSON scenario without bank access or a new budgeting database. It is optional;
do not install a runtime or require a financial file for an ordinary question.

Run `python <installed-skill>/scripts/check_cashflow.py --example` to inspect the
fictional input format, or `--input <explicitly-selected-scenario.json>` to calculate.
The placeholder denotes the actual verified installation path, not the current
project directory. Respect host permissions and do not scan for statements.

Inputs: schema_version=1, one currency label, explicit decimal scale (0..3),
as_of/horizon ISO dates, opening_available as a decimal string, and events with
unique id, date, direction (income/expense), amount string, bound (exact/minimum),
certainty (confirmed/uncertain). Only expenses support minimum bounds; a minimum
expense amount may be null when unknown. Uncertain income is excluded, not treated
as cash. Optional expenses belong in separate scenarios. Already received money
must not be counted again in both opening cash and future events. Restricted or
reserved funds are not automatically freely spendable.

The helper uses integer units, rejects silent rounding/mixed-currency fields,
and shows date-specific balances. It assumes listed confirmed future income
arrives; it does not verify that assumption. Same-day expenses are placed before
income to flag timing risk, not assert the real order. Unknown/minimum expenses
make remaining balances upper bounds, not guaranteed money available to spend.
Currency precision, completeness, fees and factual inputs require separate checks.
Output is calculation evidence only, not an affordability decision or financial
advice. The script writes only stdout; a cloud-backed host may still receive the
input/output in its context, so do not promise wholly local private processing.
