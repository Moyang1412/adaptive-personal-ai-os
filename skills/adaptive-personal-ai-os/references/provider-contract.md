# Memory provider contract

This reference describes a small adapter boundary. It is not a memory engine.
The Skill evaluates a provider, routes an authorized operation and records the
boundary. The selected provider owns storage, search, ranking, synchronization
and deletion semantics.

## Provider descriptor

An adapter reports one descriptor before it is recommended. Values describe the
current host; documentation claims alone do not count as current capability.
The machine-readable shape is [provider-descriptor.schema.json](provider-descriptor.schema.json).

```json
{
  "schema_version": 1,
  "id": "provider-id",
  "name": "Provider name",
  "version": "1.2.3",
  "kind": "installed-tool",
  "location": "local path or service endpoint description",
  "local": true,
  "network_required": false,
  "capabilities": [
    "save", "read", "correct", "delete", "scope",
    "cross_session", "cross_agent", "concurrent_write_guard", "import_export"
  ],
  "storage_location": "user-described path or service",
  "license": "SPDX identifier or unknown",
  "maintenance_status": "active",
  "interface": "memory-provider-v1",
  "source_of_truth": "one stable writer identity",
  "evidence": {
    "documented": true,
    "installed": true,
    "enabled": true,
    "callable": true,
    "isolated_test": true
  },
  "verified_capabilities": ["save", "read", "correct", "delete", "scope", "cross_session"],
  "unverified_capabilities": ["cross_agent", "concurrent_write_guard", "import_export"]
}
```

`documented` means an official description was found. `installed`, `enabled`
and `callable` describe this host and session. `isolated_test` requires a
synthetic save → new-session read → correction → read → deletion → absence
check for the capabilities being claimed. In the example, the six entries in
`verified_capabilities` are the only capabilities treated as tested; the three
entries in `unverified_capabilities` must not be used for routing. Every entry
must also appear in `capabilities`, and an entry cannot appear in both lists.
The JSON Schema checks the allowed names and uniqueness; the adapter must check
these cross-field rules before producing a descriptor.

The adapter should expose operations equivalent to:

```text
describe() -> ProviderDescriptor
save(record, scope, authorization, expected_revision?)
read(query, scope, authorization)
correct(record_id, patch, scope, authorization, expected_revision?)
delete(record_id, scope, authorization, expected_revision?)
export(record_ids, scope, authorization)
import_selected(records, scope, authorization, expected_revision?)
```

An operation must return a blocked/error result when permission, scope,
network or concurrency checks fail. It must not return a successful write just
because a Skill or package is installed. Shared scopes require a single writer
or a verified version/lock guard. If the provider cannot protect competing
writes, do not select it for cross-Agent writes.

## Source and scope rules

- Give each record one source of truth. Do not write it to native memory, the
  public Skill and another provider at the same time.
- Use a project, personal or third-party subject and an explicit scope.
- Read only records relevant to the current task and authorized scope.
- A provider switch is a new authorization event. Migrate only record IDs the
  user selected; never bulk-import history.
- A local path can still enter a cloud model's context when an Agent reads it.

## Selection rule

Evaluate at the first real need for long-term continuity and keep the decision
for the current scope. Reuse the native host memory when it covers the need.
Recommend an installed provider only when a concrete gap exists and the
provider is installed, enabled, callable, licensed, maintained and isolated
tested. Otherwise offer no extra engine. A minimal Markdown file can be an
explicitly chosen fallback, but it is a record format, not a memory engine.

## When several providers qualify

Capability eligibility is not a quality ranking. Compare the actual task gap,
existing selected provider, storage/network conditions and relevant cost evidence.
Use the user's stated priorities; do not invent scores or treat alphabetical
order, repository popularity or installation order as superiority. If the choice
remains materially unresolved, keep extra persistence off and present the small
qualified set with the decision-changing difference. Continue independent useful
work rather than writing to every candidate.


## Retrieval boundaries include relationships

A text search, entity-name prefix or project tag is not an authorization boundary.
Verify that the actual read path is limited to the authorized scope before data
enters the model context. Inspect related-edge endpoints, snippets and metadata
as well as primary records: opening one allowed node may expose names of other
nodes. Do not read an entire mixed-scope store and call later filtering isolation.
If the provider lacks a verified boundary, use an explicitly authorized separate
store/adapter or no extra engine. Do not silently configure either. File locks
coordinate writes; they do not resolve conflicting factual corrections by themselves.
