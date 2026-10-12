# Memory provider integration and migration

[Home](../README.en.md) · [Chinese guide](PROVIDERS.md) · [Provider contract](../skills/adaptive-personal-ai-os/references/provider-contract.md)

ZhiXu starts with the host's native memory and the user's existing authorized
tools. It evaluates a provider once, when long-term continuity is first needed
for a scope. It does not scan all history or install a new engine because a
Skill is present.

## Four choices

| Choice | Use when | Behavior |
|---|---|---|
| A Native memory | Native memory covers the requested scope | Keep the host as the source of truth |
| B Native + private profile | Cross-agent access is explicit and the profile has scope plus revision/lock protection | Share only selected records |
| C Installed mature provider | A clear gap exists and installation, enablement, callability, license, maintenance and isolated tests are verified | Route authorized operations to that provider |
| D No extra memory | There is no gap, permission or verification, or the user declines persistence | Do not create or call an extra engine |

## Adapter checklist

Report the provider name, version, location, local/network status, capabilities,
storage location, license, maintenance state, interface, source of truth and
evidence. Keep official documentation claims separate from installed, enabled,
callable and isolated-test states. The contract is in
[provider-contract.md](../skills/adaptive-personal-ai-os/references/provider-contract.md).

Before recommendation, use fictional records to verify save, new-session read,
correction, read again, deletion and absence. Also verify project scope,
unrelated-request routing, permission failures and a revision/lock guard for
shared writes. If a provider cannot protect competing writes, do not use it for
cross-agent writes.

## Switching and privacy

Stop writes to the old provider before switching. Ask the user to select record
IDs, subject, scope, destination and target account. Migrate only those records,
then verify reads from the new provider and that the old provider no longer
writes. Never bulk-import history or silently copy native memory.

Users can ask to view the current choice, provider version, storage location,
saved records and sharing scope; correct or delete one or all records; disable
an extra provider; export and migrate selected records; and revoke cross-agent
sharing. Each operation must report its actual result. Missing permission means
not executed, never an implied success.

Local storage is not local inference. If an Agent adds a record to a cloud
model's context, the relevant content may be sent to that model provider. Old
conversations, backups and content already in a model context need separate
handling when a record is deleted or sharing is revoked.

This repository provides assessment, routing, authorization and boundaries. It
does not provide a database, vector search, automatic importer, synchronizer or
background memory service. A Markdown file is a minimal manual fallback, not a
complete memory engine.
