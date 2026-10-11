<div align="center">

# ZhiXu · 智序

**One shared method. Your own context. Multiple agents.**

Adaptive Personal AI OS · **v0.3.0 Preview**

[Get started](#get-started) · [Examples](docs/EXAMPLES.md) · [Private memory](skills/adaptive-personal-ai-os/references/memory.md) · [Validation](docs/VALIDATION.md) · [中文](README.md)

</div>

---

**Describe your goal in ordinary language; let the agent select a suitable workflow.**

ZhiXu is an installable Agent Skill for learning, decisions, task continuity and personal context reuse. The shared core provides methods, individual configuration supplies collaboration preferences, and private files retain authorized context and progress.

It is not a new model, standalone app or always-on life manager.

## Ways to use it

| Goal | Example request | Intended contribution |
|---|---|---|
| Learning | “I want to learn data analysis systematically.” | Adapt practice and feedback to the goal and starting level. |
| Decisions | “Help me compare these options.” | Organize constraints, evidence and tradeoffs. |
| Task continuity | “Read the current status and continue.” | Resume from verified state with less repetition. |
| Personal collaboration | “Use my saved collaboration preferences.” | Reuse relevant configuration and context within permission. |

These are workflow design goals, not guaranteed results on every model. [Examples →](docs/EXAMPLES.md)

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

## Shared methods, individual configuration

```text
Public Skill: shared methods
          +
Private files: your preferences, goals and progress
          +
Host: its actual model, tools and permissions
```

Start without memory. When useful, choose no persistence, confirmation before saving, or explicitly authorized low-risk accumulation. Reuse relevant existing context; do not scrape native histories or require a long questionnaire.

Private files stay in a user-selected directory outside the public package. Individual preferences do not become everyone else's defaults. Another agent may use selected files with permission. A new model service/account does not automatically gain access. Updating public instructions should not overwrite private context.

**This version uses host file tools and Markdown records.** It does not include a memory database, automatic synchronization, native-history importer or code-enforced access controls. [Consent and memory protocol →](skills/adaptive-personal-ai-os/references/memory.md)

Local storage is not local inference: loaded records may be sent to a cloud model provider. Host history and native-memory settings remain separate.

## Learning process and limits

Goal → grounded curriculum → baseline → practice and feedback → independent new task → delayed check → adjustment.

Research-informed practices do not establish product efficacy. No guaranteed optimal paths or claims that assisted completion equals independent mastery. [Protocol and primary research →](skills/adaptive-personal-ai-os/references/learning.md)

## Maintainable by design

A compact core loads references on demand. Personal experience stays personal; project rules stay scoped. Public changes need an explicit maintenance task and regression checks.

[Architecture](ARCHITECTURE.md) · [Upgrading](UPGRADING.md) · [Validation](docs/VALIDATION.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

**MIT licensed. No daemon or built-in telemetry. Not an official OpenAI, Anthropic or DeepSeek product.**
