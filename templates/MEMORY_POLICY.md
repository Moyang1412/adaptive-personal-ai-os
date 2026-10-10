# Memory Policy

- Treat current user instructions as higher priority than stale state.
- Separate facts, assumptions, decisions, and unknowns.
- Do not write health, relationship, financial, credential, or other sensitive details to long-term state by default.
- Ask before persisting a new stable preference unless the user has already given explicit standing permission.
- Record source and date for facts that may change.
- Remove or mark stale state instead of silently treating it as current.
