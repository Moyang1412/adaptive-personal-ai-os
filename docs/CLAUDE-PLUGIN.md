# 智序的 Claude 插件封装

此封装复用 `skills/adaptive-personal-ai-os/` 中的完整公共核心，插件名为 `zhixu`，Skill 名称仍为 `adaptive-personal-ai-os`，保留 MIT 许可。没有新增 hooks、MCP 服务、额外运行时或权限设置。

## v1.0.1 适配范围

v1.0.1 提供仓库插件市场和插件 ZIP。插件与裸 Skill 共用同一核心，原有 v1.0.0 标签和资产保留。下载入口及检查边界见 [1.0.1 发布记录](RELEASE-1.0.1.md)。清单验证、文件打包与线上发布均不能代替桌面激活或模型行为验收。

公共核心缩短了 frontmatter 的 description，使其适合 Claude 自定义技能文档列出的 200 字符限制，并更新版本元数据；工作方法保持不变。本机已经安装的 Skill 不会被打包操作替换。

## Claude Desktop / Cowork：市场安装

1. 进入 `Customize → Plugins`。
2. 选择 `Add marketplace → Add from a repository`。
3. 填写 `Moyang1412/adaptive-personal-ai-os`。
4. 在 `zhixu-skills` 市场找到 `zhixu`，安装并启用。
5. 新建聊天，在 `/` 菜单确认插件技能，并核对真实加载结果。

实际菜单名称以客户端显示为准。Anthropic 当前将插件功能列为 Pro、Max、Team 和 Enterprise 计划可用，组织策略可以限制安装。安装步骤依据[官方插件说明](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)。本仓库未替用户登录或修改其云端账号，真实桌面端加载仍待验证。

## 插件 ZIP 上传

在 [v1.0.1 Release](https://github.com/Moyang1412/adaptive-personal-ai-os/releases/tag/v1.0.1) 下载 `zhixu-1.0.1-plugin.zip`，进入 `Customize → Plugins` 的 `Add` 或 `+` 菜单，选择上传自定义插件并启用。新建聊天后再检查发现与加载。

单 Skill ZIP `zhixu-1.0.1-skill.zip` 用于直接 Skill 入口，不应上传到插件入口。两个包都不包含个人记忆或聊天记录。

## 本地构建

在仓库根目录执行：

```powershell
python -X utf8 scripts/package_claude_plugin.py --output "$env:USERPROFILE\Downloads\zhixu-1.0.1-plugin.zip"
```

Python 仅用于维护者生成 ZIP，使用者上传插件后不需要自行安装 Python。输出或同名校验报告已存在时脚本停止，不覆盖旧文件；同版本换一个输出名重建时会使用新的编号暂存目录。构建仅纳入显式选择的公共文件，不读取或打包个人资料与仓库评测数据。

插件 ZIP 的根目录结构：

```text
.claude-plugin/plugin.json
skills/adaptive-personal-ai-os/SKILL.md
skills/adaptive-personal-ai-os/VERSION
skills/adaptive-personal-ai-os/LICENSE
skills/adaptive-personal-ai-os/agents/openai.yaml
skills/adaptive-personal-ai-os/references/...
LICENSE
README.md
```

单 Skill ZIP 的顶层目录是 `adaptive-personal-ai-os/`，插件 ZIP 则包含 `.claude-plugin/` 和 `skills/`。上传时选择对应入口。

## Claude Code

在命令行执行：

```text
claude plugin marketplace add Moyang1412/adaptive-personal-ai-os
claude plugin install zhixu@zhixu-skills
```

直接 Skill 的 Claude Code 入口是 `/adaptive-personal-ai-os`，插件入口按命名空间为 `/zhixu:adaptive-personal-ai-os`，以实际发现结果为准。不要在同一宿主并行启用同一核心的裸 Skill 和插件副本。切换前核对用户改动并备份旧副本到扫描目录之外；打包脚本不会自动卸载或替换既有安装。

## 验证与切换边界

文件检查应覆盖 JSON 清单、插件相对路径、Skill frontmatter、全部配套文件、ZIP CRC 和逐文件哈希。

```text
claude plugin validate .claude-plugin/plugin.json --strict --json
claude plugin validate .claude-plugin/marketplace.json --strict --json
```

还需在真实桌面端确认插件被识别、启用及实际加载。可以测试：

> 使用已安装的智序，帮我把每天学习 20 分钟英语变成今天能完成的一步，先不用建立长期档案。

负例：

> 把 Good morning 翻译成中文。

负例应直接翻译，不能被扩展成计划、测评或建档。安装不携带聊天历史或个人记忆，记忆、文件访问、联网与定时能力依赖宿主实际工具和授权。

回退时停用 `zhixu`，恢复扫描目录外备份的裸 Skill，或重新安装 [v1.0.0 Skill](https://github.com/Moyang1412/adaptive-personal-ai-os/tree/v1.0.0/skills/adaptive-personal-ai-os)。不要同时重新启用两个入口，也不要用公共包覆盖私人资料。

插件和市场结构依据[官方插件清单参考](https://code.claude.com/docs/en/plugins-reference)与[官方市场说明](https://code.claude.com/docs/en/plugin-marketplaces)。
