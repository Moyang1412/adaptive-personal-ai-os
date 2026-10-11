<div align="center">

# ZhiXu · 智序

**One shared method. Your own context. Multiple agents.**

Adaptive Personal AI OS · **v0.3.0 Preview**

[Get started](#get-started) · [Private memory](skills/adaptive-personal-ai-os/references/memory.md) · [Validation](docs/VALIDATION.md) · [中文](README.md)

</div>

---

**Say what you want to do, not how to write a perfect prompt.**

ZhiXu is an installable Agent Skill for contextual decisions, project continuity, personal planning and learning through practice. It distinguishes getting a result from building a skill, reuses only relevant authorized context, and keeps personal facts separate from public instructions.

It is not a new model, standalone app or always-on life manager.

## What it is designed to do

| Say this | Intended behavior |
|---|---|
| “I want to learn photography.” | Clarify the use, ground a suitable path, start a small exercise. |
| “Continue yesterday's project.” | Read verified state rather than invent progress. |
| “One lifelong personal habit, not a work habit.” | Respect the life/work boundary. |
| “Remember that I prefer concise answers.” | Save within consent, not in the public Skill. |
| “That was my friend's experience.” | Correct attribution instead of treating it as your history. |

These are testable design requirements, not guaranteed results on every model.

## Get started

Use your existing **Codex, Claude Code or DSH**. The instruction core needs no extra server, API key or Python runtime.

Give your agent this request:

```text
Install the ZhiXu Skill from:
https://github.com/Moyang1412/adaptive-personal-ai-os/tree/main/skills/adaptive-personal-ai-os
Check this host's skills root and existing copies first.
Do not overwrite personal configuration, memory or other Skills.
Report the real installation path and verify the host catalog or loader trace.
```

This delegates installation to a host with suitable tools and permissions; it is not a universal executable command. Alternatively download the repository and copy the complete Skill folder manually.

| Host | Documented user skills root | Explicit invocation |
|---|---|---|
| Codex | `~/.agents/skills` | `$adaptive-personal-ai-os` |
| Claude Code | `~/.claude/skills` | `/adaptive-personal-ai-os` |
| DSH | `~/.agents/skills` or a configured DSH skills root | Select through its current Skill interface |

**Format/documentation adaptation is complete; live host acceptance is pending.** Custom configurations and organization policies may differ. [Installation guide →](docs/INSTALL.md)

A plausible answer is not proof of activation. Inspect the actual Skill catalog, installed path or loader trace.

## Personalization without a private fork

```text
Public Skill: shared methods
          +
Private files: your preferences, goals and progress
          +
Host: its actual model, tools and permissions
```

Start without memory. When useful, choose no persistence, confirmation before saving, or explicitly authorized low-risk accumulation. Reuse relevant existing context; do not scrape native histories or require a long questionnaire.

Private files stay in a user-selected directory outside the public package. Another agent may use selected files with permission. A new model service/account does not automatically gain access. Updating public instructions should not overwrite private context.

**This version uses host file tools and Markdown records.** It does not include a memory database, automatic synchronization, native-history importer or code-enforced access controls. [Consent and memory protocol →](skills/adaptive-personal-ai-os/references/memory.md)

Local storage is not local inference: loaded records may be sent to a cloud model provider. Host history and native-memory settings remain separate.

## Learning with evidence

Goal → grounded curriculum → baseline → practice and feedback → independent new task → delayed check → adjustment.

Research-informed practices do not establish product efficacy. No guaranteed optimal paths or claims that assisted completion equals learning. [Protocol and primary research →](skills/adaptive-personal-ai-os/references/learning.md)

## Maintainable by design

A compact core loads references on demand. Personal experience stays personal; project rules stay scoped. Public changes need an explicit maintenance task and regression checks.

[Architecture](ARCHITECTURE.md) · [Upgrading](UPGRADING.md) · [Validation](docs/VALIDATION.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

**MIT licensed. No daemon or built-in telemetry. Not an official OpenAI, Anthropic or DeepSeek product.**
