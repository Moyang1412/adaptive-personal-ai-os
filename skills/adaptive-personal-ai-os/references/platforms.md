# Host adapters

Documentation checked: 2026-10-11. Shared Agent Skills format does not guarantee identical model behavior or tool availability. Provider availability is a separate host check.

| Host | Documented user-level root | Invocation | Evidence status |
|---|---|---|---|
| Codex | `~/.agents/skills/` | `$adaptive-personal-ai-os` | Documentation/file adaptation; live acceptance pending |
| Claude Code | `~/.claude/skills/` | `/adaptive-personal-ai-os` | Documentation/file adaptation; live acceptance pending |
| DSH | `${DSH_AGENTS_HOME:-~/.agents}/skills/` or `${DSH_HOME:-~/.dsh}/skills/` | Select a discovered Skill through the current host interface | Filesystem-provider adaptation; live acceptance pending |
| Other Agent Skills hosts | Their verified configured root | Follow host documentation | Format-level candidate only |

Copy the whole `adaptive-personal-ai-os` directory, not just SKILL.md. Codex and default DSH may share a single `.agents/skills` copy. Do not install duplicate copies automatically. DSH needs its Skill registry/filesystem provider enabled and may override default roots. Preserve existing presets and settings.

Before a first long-term-memory save, ask the host for a capability descriptor or
inspect only the provider paths the user named. Record native memory, installed
tools, enabled configuration, current-session callability and isolated-test
results separately. Skill installation is not provider installation. If a host
cannot expose a capability or permission, mark it unknown and choose no extra
engine rather than guessing.

The old `.codex/skills` install advice is not the current documented default. Inspect existing local, project and legacy copies; resolve conflicts with the user rather than deleting a private Skill. Organization/custom configurations can differ.

Codex's `agents/openai.yaml` is optional UI/invocation metadata, not a universal activation switch or access grant. Preserve Claude Code's CLAUDE.md, settings and native memory. Do not assume DSH has native memory because it can load filesystem Skills.

## Check actual activation

Inspect the available Skill catalog, selected path or loader trace. Reopen the host if needed and explicitly invoke the installed name. Then try a natural learning request and a negative-control one-sentence translation. For provider acceptance, also run synthetic save/read/correct/delete and scope/concurrency checks. Record host/model versions, actual loading evidence, provider storage location and the exact operations verified.

A helpful answer is not activation proof. File presence is not runtime validation. No installation doctor or automated host test is included in this release.

## Capability degradation

Use only the host's real tools and permissions. No web access means no current-source verification claim. No write access means draft-only memory. No independent review tool means self-review. No scheduler means no promise of future delivery. Never weaken host security to make the Skill work.

## Primary sources

- Agent Skills standard: https://agentskills.io/specification
- Codex Skills: https://developers.openai.com/codex/skills/
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code memory: https://code.claude.com/docs/en/memory
- DSH filesystem provider: https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md

These sources support platform conventions, not a claim that ZhiXu passed live acceptance.
