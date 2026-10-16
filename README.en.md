<div align="center">

# ZhiXu · 智序

**One shared method. Your own context. Multiple agents.**

Adaptive Personal AI OS · **v1.0.1 · Claude plugin support**

[Get started](#get-started) · [Examples](docs/EXAMPLES.md) · [Memory choices](docs/PROVIDERS.en.md) · [Private memory](skills/adaptive-personal-ai-os/references/memory.md) · [Validation](docs/VALIDATION.md) · [中文](README.md)

</div>

---

**Describe your goal in ordinary language; let the agent select a suitable workflow.**

ZhiXu is an installable Agent Skill for learning, planning and decisions, task continuity, everyday life support, personal context reuse and memory-provider choice. The shared core provides methods, individual configuration supplies collaboration preferences, and private files or a selected provider retain authorized context and progress.

It is not a new model, standalone app or always-on life manager.

## Ways to use it

| Goal | Example request | Intended contribution |
|---|---|---|
| Learning | “I want to learn data analysis systematically.” | Adapt practice and feedback to the goal and starting level. |
| Everyday life | “Help me arrange the chores and leave time to rest.” | Support routines, health habits, household money, career exploration and relationships according to the person's own goal. |
| Decisions | “Help me compare these options.” | Organize constraints, evidence and tradeoffs. |
| Task continuity | “Read the current status and continue.” | Resume from verified state with less repetition. |
| Personal collaboration | “Use my saved collaboration preferences.” | Reuse relevant configuration and context within permission. |
| Memory choice | “I need continuity; check what already exists first.” | Use native memory first; assess an installed provider only for a clear gap. |

These are workflow design goals, not guaranteed results on every model. Version 1.0.0 is ZhiXu's first stable release; publication does not establish learning or life outcomes. [Examples →](docs/EXAMPLES.md) · [1.0.0 release and validation record →](docs/RELEASE-1.0.0.md)

## Maintenance candidate

The 2026-10-17 candidate lives on `dot/overnight-improvements-20261017`; it does not replace the v1.0.1 release. See the [reuse and verification record](docs/REUSE-REVIEW-2026-10-17.md) for selected ideas, rejected dependencies and limits. The 42 offline unit checks and 95-case routing schema pass are not evidence of live host activation or improved user outcomes.

## Get started

**For Claude Desktop / Cowork, start with the plugin marketplace:** open `Customize → Plugins → Add marketplace → Add from a repository`, enter `Moyang1412/adaptive-personal-ai-os`, then install `zhixu` from the `zhixu-skills` marketplace. Menu labels, availability and organization policies may differ.

Alternatively, upload `zhixu-1.0.1-plugin.zip` from the [v1.0.1 Release](https://github.com/Moyang1412/adaptive-personal-ai-os/releases/tag/v1.0.1). Actual desktop discovery, enablement and loading still require live verification. [Plugin guide →](docs/CLAUDE-PLUGIN.md) · [1.0.1 changes and limits →](docs/RELEASE-1.0.1.md)

**Use one active entry per host: the plugin or the standalone Skill.** For Codex, DSH or a standalone installation, follow the steps below.

Use your existing **Codex, Claude Code or DSH**. The instruction core needs no extra server, API key or Python runtime and does not create a memory database.

Give your agent this request:

```text
Install the ZhiXu Skill from:
https://github.com/Moyang1412/adaptive-personal-ai-os/tree/v1.0.1/skills/adaptive-personal-ai-os
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

Start without memory. When long-term continuity is first needed, inspect the host's native memory and the user's installed, authorized providers once for that scope. Then choose:

- **A Native memory** when the host already covers the need.
- **B Native memory plus a private profile** for an explicit cross-agent need with scope and version/lock protection.
- **C An installed mature provider** only when it fills a clear gap and its installation, enablement, callability, license, maintenance and isolated test are verified.
- **D No extra long-term memory** when there is no gap, permission or verification, or when the user declines persistence.

Installing this Skill does not install a provider. If no suitable provider exists, choose D; a hand-maintained Markdown file is a minimal record fallback, not a full memory engine. Reuse relevant existing context; do not scrape native histories or require a long questionnaire.

Private files stay in a user-selected directory outside the public package. Individual preferences do not become everyone else's defaults. Another agent may use selected files with permission. A new model service/account does not automatically gain access. Updating public instructions should not overwrite private context.

**The public Skill handles assessment, routing, authorization and boundaries.** The selected provider handles saving, reading, correction, deletion and export. This release includes no memory database, vector search, automatic synchronization, native-history importer or code-enforced access controls. [Memory choices and migration →](docs/PROVIDERS.en.md) · [Consent and memory protocol →](skills/adaptive-personal-ai-os/references/memory.md)

Local storage is not local inference: loaded records may be sent to a cloud model provider. Host history and native-memory settings remain separate.

## Learning process and limits

Version 1.0.0 includes dual-mode learning. Installed copies do not update automatically; check the loaded path and preserve private files when upgrading.

Goal → start learning, or choose a brief diagnostic → practice and feedback → independent new task → delayed retention and transfer checks → adjustment.

Start with useful learning or a real task by default, drawing evidence from the user's own explanations and actions. A brief diagnostic is optional, skippable and interchangeable with learning; do not force a mode choice at every opening. Preserve existing explicit preferences.

Both modes use the same standard: assess specific skills, observed performance and the help required, then reduce redundant teaching where evidence supports it. Work completed by the assistant is not learner mastery; declining a check or replying slowly is not inability. Keep missing evidence unknown and continue helping. Learning cards and long-term saving are optional.

Research-informed methods do not establish product efficacy. Check judgments against later independent performance, retention and transfer; compare efficiency through time and burden at comparable learning outcomes, not fewer questions or faster completion alone. No guaranteed optimal paths. [Protocol and primary research →](skills/adaptive-personal-ai-os/references/learning.md)

## Other workflows

Start from the supplied context and load the relevant reference on demand. Ask only about a gap that changes the next action; a simple request does not require an intake questionnaire.

| Workflow | Methods in this release |
|---|---|
| Planning | Check realistic capacity and dependencies; name a completion condition and a feasible next action. Reduce scope or revise arrangements when capacity is insufficient. |
| Decisions | Separate facts, estimates and preferences; identify the key unknown and conditions that would change the recommendation. |
| Research | Check whether a source supports the specific claim and applies to the people or tasks involved; stop once the needed evidence is sufficient. |
| Memory | Retrieve by authorized scope, source and event time; distinguish plans from outcomes and preserve unresolved conflicts. |
| Continuity | Reconcile a handoff with current files and completion evidence before continuing. |
| Review | Compare intended and actual outcomes, then test one actionable adjustment without presenting a causal guess as fact. |
| Communication | Provide the requested draft, listening or clarification without mandatory disclosure; drafting does not authorize sending. |

Memory still uses native capabilities and already authorized providers, without adding an engine or expanding access. GitHub practices and papers inform design choices; they do not establish this Skill's efficacy. Compare actual outcomes, errors and interaction burden. [Source review and applicability →](docs/RESEARCH-NONLEARNING-2026-10-13.md) · [Behavioral validation and gaps →](docs/VALIDATION-NONLEARNING.md)

The synthetic checks above apply to their recorded candidate snapshots. Release checks for 1.0.0 are recorded separately; earlier results are not acceptance of a current host or real-user outcomes.

## Everyday life support

The person chooses the goal. Rest, enjoying a hobby, caring for family or steadier finances can be complete goals. Start with useful help from the information supplied and ask only about a gap that changes the next action. No compulsory tests, tracking, devices or personality labels; leisure does not automatically become an income project.

| Need | Possible help |
|---|---|
| Routines, chores and leisure | Adjust the environment or task size, offer a feasible step and protect the desired rest and enjoyment. |
| Health habits | Discuss sleep, food and movement within existing conditions; treat symptoms or care needs separately, without personal diagnoses or prescriptions. |
| Household cash flow and purchases | Check amounts, income and payment dates, and essential expenses before comparing a purchase with waiting; no fixed budget ratios. |
| Career exploration | Compare real constraints and role information, then suggest an affordable way to learn or try; the person decides whether to continue. |
| Relationships and emotional support | Listen, clarify or draft as requested, without guessing another person's motives or turning feelings into compulsory exercises. |

Read the [life-support entry point](skills/adaptive-personal-ai-os/references/life.md) as needed, without adding a full intake questionnaire. Specific medical, financial or legal judgments require current reliable sources and relevant local conditions. Sensitive reads, writes, sharing between services and outside contact retain existing authorization requirements; asking for advice does not automatically authorize account access, saving intimate details, sending messages or purchases.

Research informs some methods; it does not establish that this Skill improves health, finances, relationships or quality of life. All four single-run anonymous life-support comparisons tied; they do not establish overall efficiency gains. [Life-domain source review →](docs/RESEARCH-LIFE-2026-10-13.md) · [Candidate validation scope and gaps →](docs/VALIDATION-LIFE.md) · [1.0.0 release record →](docs/RELEASE-1.0.0.md)

## Maintainable by design

A compact core loads references on demand. Personal experience stays personal; project rules stay scoped. Public changes need an explicit maintenance task and regression checks.

[Architecture](ARCHITECTURE.md) · [Memory providers](docs/PROVIDERS.en.md) · [Upgrading](UPGRADING.md) · [Validation](docs/VALIDATION.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

**MIT licensed. No daemon or built-in telemetry. Not an official OpenAI, Anthropic or DeepSeek product.**
