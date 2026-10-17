# 安装与排错 · Install

[中文首页](../README.md) · [记忆方案接入](PROVIDERS.md) · [English](../README.en.md)

## Claude 插件方式

Claude Desktop / Cowork 首选在 `Customize → Plugins → Add marketplace → Add from a repository` 添加 `Moyang1412/adaptive-personal-ai-os`，再从 `zhixu-skills` 市场安装 `zhixu`。实际菜单名称和可用性以客户端及组织策略为准。

也可上传 [v1.0.1 Release](https://github.com/Moyang1412/adaptive-personal-ai-os/releases/tag/v1.0.1) 中的 `zhixu-1.0.1-plugin.zip`。Claude Code 也支持插件安装；完整命令、切换与验证见[Claude 插件指南](CLAUDE-PLUGIN.md)。

插件与直接 Skill 复用同一核心。**同一宿主只启用一种入口**；已有裸 Skill 时，先备份到扫描目录外，再切换。文件或清单检查不表示真实桌面端已经激活。

## 正式版与开发候选不要混淆

首页默认安装链接指向正式v1.0.1。若明确希望试用本轮优化，请选择[开发候选的完整Skill目录](https://github.com/Moyang1412/adaptive-personal-ai-os/tree/dot/overnight-improvements-20261017/skills/adaptive-personal-ai-os)，让Agent记录实际取到的提交SHA。该分支持续变化，不是新Release；不能只比较VERSION文件就认定内容相同。

可交给有相应权限的Agent：

```text
我选择智序的开发候选 dot/overnight-improvements-20261017。
请核对当前宿主实际加载路径，以及该分支当前提交。
先比较已有公共文件与候选，保留我的私人资料、配置和本地改动。
不要覆盖有冲突的文件，也不要自动启用记忆服务或安装额外依赖。
在宿主允许的权限内更新无冲突的公共文件；需要确认的步骤按宿主流程处理。
完成后报告实际更新的文件、来源提交和加载证据；没有加载证据就明确说明。
```

有本地改动时使用下方只读比较工具辅助判断。它不会替代授权、备份或实际宿主加载检查，也不会自动将候选提升为正式版。

## 最短路径

已有 Agent 的用户，可以把首页的安装请求与 Skill 文件夹地址交给它，让它先核对自己的加载目录，再安装并报告证据。也可以通过 GitHub 的 Code → Download ZIP 下载仓库，打开 `skills/adaptive-personal-ai-os/`。

**只需把整个 `adaptive-personal-ai-os` 文件夹复制到当前宿主实际扫描的 Skills 根目录。** 保留 SKILL.md、references、agents、LICENSE 和 VERSION；不需要复制根目录文档或 evals。

| Host | 常见用户级根目录 |
|---|---|
| Codex | `~/.agents/skills` |
| Claude Code | `~/.claude/skills` |
| DSH | `~/.agents/skills` 或 `~/.dsh/skills`，以启用的提供方与配置为准 |

`~` 指当前用户目录；Windows 用户可从自己的主目录进入对应隐藏目录。自定义环境、云端环境和组织策略可能不同，必须查看宿主实际配置。安装在一台电脑上，不会安装到另一台电脑或云端。

正式v1.0.1及候选的指令核心不需要额外运行环境。当前开发候选另含可选现金流算术工具，仅在已有Python 3且明确需要计算时使用；没有Python仍可用指令核心。**没有 `install.py`、自动记忆脚本、安装诊断器或自动回滚工具。** 不要运行旧预览里提到但仓库不存在的命令。

安装 Skill 不会安装记忆 provider。首次需要长期记忆时，先检查宿主原生记忆和用户已经安装、授权的工具，再按 [记忆方案接入](PROVIDERS.md) 记录证据和选择 A/B/C/D。没有明确缺口或隔离验证时，选择 D，不要临时建立数据库。

## 先保护已有配置

已有同名文件夹时，先检查它是否被用户修改，不直接覆盖。把旧副本备份到宿主不扫描的目录，再人工比较和替换公共文件。不要把备份留在 Skills 扫描目录造成重复发现。

安装不需要改写 AGENTS.md、CLAUDE.md、原生记忆、凭据、模型配置或启动项。不要为了安装降低安全设置。私人资料始终放在独立目录。

## 两层验证

**文件层：**确认最终路径是 `<skills-root>/adaptive-personal-ai-os/SKILL.md`，frontmatter 的 name 正确，references 相对链接完整。

**宿主层：**在技能列表或加载记录里找到同名 Skill，检查真实路径，显式调用，再测试自然语言请求和一条不应触发的简单翻译。没有宿主层证据，只能说文件安装完成。记忆 provider 还必须单独核对安装、启用、可调用和隔离测试状态，不能把 Skill 加载当成 provider 验证。

Codex 显式调用 `$adaptive-personal-ai-os`；Claude Code 使用 `/adaptive-personal-ai-os`；DSH 在其当前 Skill 入口选择。版本差异详见[平台适配](../skills/adaptive-personal-ai-os/references/platforms.md)。

## DSH：避免多套一层目录

文件系统提供方只发现根目录下一层的技能包。正确形式是 `<实际根目录>/adaptive-personal-ai-os/SKILL.md`，不是把整个仓库再套进一层目录。列表缺失时先查给定目录和警告；项目级同名包可能优先于用户级包。改文件不等于旧对话已重新加载，必要时从当前宿主入口重新调用。此处是官方实现文档核对，不是实机安装结果。

## 常见问题

| 现象 | 优先检查 |
|---|---|
| 列表中没有 | 大小写、实际扫描目录、提供方是否启用、是否需要新会话 |
| 加载了旧版本 | 项目级、用户级、旧目录或同步来源中是否存在同名副本 |
| 不能读取私人档案 | 是否授权了确切目录、当前服务与账号、文件系统是否可访问 |
| 新对话失去进度 | 是否实际写入了状态，新的 Agent 是否被明确允许读取 |
| 不停输出长报告 | 用“简短一点”反馈；检查是否加载了旧核心或冲突规则 |
| 回答正确但不见加载记录 | 不宣布激活成功，继续核对宿主证据 |
| provider 看似已安装 | 检查 enabled、callable、许可证、维护状态和隔离测试；未知就标记未知 |
| 更换 provider 后仍有旧写入 | 先停旧 provider，核对唯一 source of truth 和实际写入日志 |

## English quick reference

For Claude Desktop / Cowork, add the repository marketplace and install `zhixu`, or upload the plugin ZIP. Use only one active plugin or standalone Skill entry per host; desktop activation still needs live verification.

Download the repository or delegate installation to your agent. Copy the entire Skill folder to the host's verified skills root. No Python or additional service is required for the instruction core. The current candidate additionally includes an optional cash-flow arithmetic helper that needs existing Python 3; skip it when unavailable. Review existing copies before replacing them, keep backups outside discovery roots, and never overwrite private context or host settings.

Verify both the files and the host catalog/loader trace. Explicit invocation differs by host. There is no installer, automatic memory engine or runtime doctor in this release. Provider selection is an evidence and authorization step; it does not create a database.

## 候选维护工具：升级前只读比较

优化分支新增 `scripts/compare_skill_bundle.py`，不属于已发布 v1.0.1 的运行时包，也不是宿主诊断器。需要本机 Python，仅在主动执行时读取你指定的一个 Skill 目录与可信版本清单。它不会搜索主目录、读取清单外的私人文件、安装、覆盖或删除文件。

从已经核对来源的同一版本下载独立 Skill 清单（`kind: skill`），在仓库根目录运行：

```sh
python scripts/compare_skill_bundle.py --bundle "/明确指定的/adaptive-personal-ai-os" --manifest "/下载目录/zhixu-1.0.1-manifest.json"
```

- `matching`：列出的公共文件与该清单一致。
- `different`：内容不同，可能是旧版、个人修改或其他原因；不自动判断应覆盖。
- `missing` / `unreadable`：缺失，或符号链接、非普通文件、过大文件等未读取情况。
- 返回码 0 表示清单内文件全部相同，1 表示存在差异，2 表示输入或清单不合法。

哈希一致不能验证清单来源、额外文件、宿主实际加载路径或模型行为；清单需自行来自可信发行来源。此工具不适合作为对抗并发恶意文件替换的安全边界。比较期间保持目标目录不变。

升级时先对照当前版本清单识别个人修改，再对照目标版本看变更范围。备份放到宿主扫描目录之外，只替换已核对的公共文件；有修改的文件应先比较合并。私人记忆、宿主配置和未列出的文件保持独立。最后重新加载技能并报告实际加载证据，不把文件相同说成已激活。

English: this candidate read-only helper compares only manifest-listed public files in one explicitly selected bundle. It does not install, scan extra files, authenticate the manifest, detect the active host path, or prove activation. Preserve local edits and private context before any separate authorized upgrade.

### 区分上游更新与自己的修改

如果还保存着当前安装版本的可信清单，可以同时提供旧、新两个清单，生成只读的三方比较报告：

```sh
python scripts/compare_skill_bundle.py --bundle "/明确指定的/adaptive-personal-ai-os" --baseline-manifest "/下载目录/旧版-manifest.json" --manifest "/下载目录/目标版-manifest.json"
```

- replacement_candidates：本地仍与旧版一致、上游已改变的公共文件，是待核对的替换候选。
- already_target / unchanged：已与目标一致，或三方一致，不需要重复覆盖。
- local_only_changes：上游没改、本地有改动；保留个人修改。
- conflicts：本地和上游都改了；需逐项比较，不直接覆盖。
- new_file_collisions：目标新增路径在本地已有不同内容；不能把它当成空位置。
- retired_unmodified / retired_local_changes：目标清单不再列出该文件；只是提示，不授权删除。
- missing / unreadable：文件缺失或无法安全读取，不能当作升级完成。

计划模式只读取两个清单覆盖的路径，每个路径一次；不枚举其他文件。比较期间保持目录不变，不宣称原子快照或并发防护。返回码0表示没有待处理差异，1表示报告里仍有差异/待核对项，2表示输入错误；所有模式均不执行替换、删除、合并或安装。需要先核对清单来源，比较结果也不能证明宿主已经加载。

English: add --baseline-manifest for a read-only three-way classification of upstream changes, local edits, conflicts and newly occupied paths. Exit 1 means the report contains changes needing review, not that any update was applied. No files are replaced or removed.

## 维护者：明确标记未发布候选包

在优化分支构建供核对的候选包时，先记录已核对的源提交，再使用：

```sh
python scripts/package_release.py --candidate --output-dir /新的候选输出目录 --source-ref 已核对的提交SHA
```

文件名带 `-candidate`，清单的 `build_channel` 为 `candidate`、`tag` 为 null。已有输出目录不会被覆盖。省略该参数保留原有发行构建命名，但两种模式都只生成本地文件，不创建 Git 标签、不发布 Release、不安装、不证明宿主已加载。`source_ref` 是调用者提供的溯源标签，脚本不会自动验证工作区与该提交一致；构建前需检查提交与工作区。

English: --candidate marks local artifacts and manifests as a candidate without changing VERSION. It does not publish, install or verify the caller-supplied source reference. Verify the intended commit and clean worktree before building.

### Windows与换行差异

候选仓库的公共说明、版本及清单采用LF检出规则，减少不同电脑的无意义换行差异。已有副本可能仍保留CRLF；打包器会把公共文本统一为LF，升级比较工具则严格比较文件字节。若比较报告提示不同，先检查是否仅换行不同，不把它直接当作内容修改或授权覆盖。仓库规则不会迁移或重写已安装的私人目录。
