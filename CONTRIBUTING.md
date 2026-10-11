# Contributing

[Home](README.md) · [Validation](docs/VALIDATION.md)

Keep the shared core concise, portable and grounded in the actual goal. Personal facts stay in private files; public examples and tests should be independently constructed synthetic scenarios, not copied or lightly paraphrased private conversations.

## Before changing behavior

Read the affected reference and existing cases. Distinguish individual preferences from project rules and general improvements. A preference can guide that user's authorized configuration without becoming a universal default. A report can reveal a mechanism defect, but the proposed general rule still needs an independent rationale, clear scope and checks beyond the original situation.

Add a positive case, a neighboring negative case and an ambiguity/authority boundary when behavior changes. Do not convert two anecdotal failures into automatic global rules.

## Public documentation

Explain reusable capabilities, setup, limitations and representative uses. Do not present individual support incidents, personal requirements or conversation-specific fixes as product features. Examples should illustrate a workflow rather than reenact a private exchange. Removing a name alone does not make a personal narrative suitable for publication.

Keep individual customization in user-owned files with permission. Public regression cases should test an abstract mechanism with newly constructed inputs; a private incident is not automatically an authorized public fixture. Documentation changes need not add new behavioral rules.

## Checks

The existing validator is still available:

```text
python evals/validate_routing_cases.py
```

It validates case schema only. It does not call a model, run a host or prove memory/teaching behavior. Inspect frontmatter, relative links, source references, package completeness and private information separately. Record exact commands and actual results.

For host acceptance, record version, model/provider, loaded Skill path/trace, prompt, output, tool effects and reviewer judgment. Do not publish real memories, credentials, personal screenshots or raw private conversations.

## Pull requests

Explain the general problem, changed behavior, scope, risks, evidence and rollback. Update CHANGELOG.md and migration notes for changes to defaults. No unsupported claims of scientific efficacy, automatic persistence or universal host compatibility.

Ordinary Skill use must not rewrite or publish this repository. Public maintenance is an explicit task. Local prototype tests cannot be reported as validation of unpublished or different release files.
