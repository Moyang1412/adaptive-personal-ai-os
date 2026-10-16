# 教学Skill：选取有用机制，不整套照搬

2026-10-17补充检索了GitHub上的tutor agent skills、teaching skills和spaced repetition scheduling。搜索不是穷尽全站，也不把搜索排名当作质量证据。以下两项实际读取了相应指令与许可证，没有安装或运行其脚本。

## Feynman Tutor

快照 `9e9ec6fa08bd2242b7aea1cf3419e28ea2e70664`；读了SKILL.md、README和MIT许可证。

有用的区分是：学习者缺少一个事实/约定时应先说明，不该一直要求他猜；需要推理的部分才考虑适当提示。智序据此补充一个原创、可选参与的说明规则，并保持直接帮助和跳过选择。

不整体引入其默认熟悉学习者、每次读取一组私人笔记、按固定邻居预算扩展检索、指定提取脚本及可视化工具的流程。这些需要真实历史、明确范围与当前宿主能力。附带提取/OCR脚本本轮未审查或运行，不能声称它们优于现有浏览工具。也不采用“代码一律不能类比”的普遍规则：类比应回到实际机制并说明边界，是否有用取决于任务。

- [Skill](https://github.com/koukekoukej-glitch/feynman-tutor/blob/9e9ec6fa08bd2242b7aea1cf3419e28ea2e70664/SKILL.md)
- [README](https://github.com/koukekoukej-glitch/feynman-tutor/blob/9e9ec6fa08bd2242b7aea1cf3419e28ea2e70664/README.md)
- [MIT许可](https://github.com/koukekoukej-glitch/feynman-tutor/blob/9e9ec6fa08bd2242b7aea1cf3419e28ea2e70664/LICENSE)

## Claude Language Tutor

快照 `6a980667c276f0f704e98b6862047b1ba12969fd`；读了README、GPL-3.0许可证，并只读解包langtutor-assessor.skill中的SKILL.md，未执行/安装压缩包内容。

它提供多方面能力记录与分模块教学思路；其评估检查单也允许注明某些能力未测，不能据此说它完全忽略测量限制。但开始前的固定资料采集、自动建档、五模块协作以及固定额度恢复时间，都不能直接作为智序跨宿主默认行为。

课程从某个初级单元开始，不等于已经证实学习者达到该能力级别；智序补充了这个区分。听说读写的证据仍分开，未测试就留未知。固定学习时长和熟练度宣传不能作为个体效果保证。不会把GPL指令或压缩包合并进MIT公共核心；这里只做原创分析与一般方法判断。

- [README](https://github.com/gislio/claude-language-tutor/blob/6a980667c276f0f704e98b6862047b1ba12969fd/README.md)
- [实际读取的评估包](https://github.com/gislio/claude-language-tutor/blob/6a980667c276f0f704e98b6862047b1ba12969fd/langtutor-assessor.skill)
- [GPL-3.0许可](https://github.com/gislio/claude-language-tutor/blob/6a980667c276f0f704e98b6862047b1ba12969fd/LICENSE)

## 本轮结果与证据边界

智序只增加了“先补事实再推理、类比回到实际任务、课程起点不等于能力”的短规则及两个独立合成用例。没有新增依赖、读取私人学习档案、安排提醒或调用其他代理。用例仅进行结构检查，不是模型行为、教学效果或真人学习试验。

English: inspected two pinned teaching instruction sources and their licenses. Adopted narrowly scoped original guidance about missing factual premises and course placement versus demonstrated capability. Did not copy prompts, install scripts, assume prior learner history, import private notes or adopt fixed quota-reset promises. Schema checks are not learning-effect evidence.
