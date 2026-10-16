# FSRS：只在确实需要复习排程时复用

检查日期：2026-10-17。固定源码：[open-spaced-repetition/ts-fsrs @ c8ca282](https://github.com/open-spaced-repetition/ts-fsrs/tree/c8ca282edc3fe1cdfa1c24912437938b63a25cb3)。该提交中调度包版本为5.4.2；这是源码快照，不代表当前已安装或最新发行版。

## 结论

智序保留无运行依赖的教学指令核心。需要卡片复习时，优先用本人已经授权、实际可用的复习工具；只有开发明确的卡片排程功能，才考虑接入成熟调度库。FSRS计算复习状态与时间，不替代跨Agent记忆provider、提醒服务、教材路径或独立能力评估。不在普通讲解中自动安装、收集复习日志或建立第二套学习数据库。

## 这次实际读了什么

- 根README、[MIT许可证](https://github.com/open-spaced-repetition/ts-fsrs/blob/c8ca282edc3fe1cdfa1c24912437938b63a25cb3/LICENSE)。
- [调度包说明](https://github.com/open-spaced-repetition/ts-fsrs/blob/c8ca282edc3fe1cdfa1c24912437938b63a25cb3/packages/fsrs/README.md)及package.json：此快照要求Node.js至少20，调度包与参数优化包分开。
- [models.ts](https://github.com/open-spaced-repetition/ts-fsrs/blob/c8ca282edc3fe1cdfa1c24912437938b63a25cb3/packages/fsrs/src/models.ts)、default.ts、convert.ts、abstract_scheduler.ts，以及[fsrs.ts](https://github.com/open-spaced-repetition/ts-fsrs/blob/c8ca282edc3fe1cdfa1c24912437938b63a25cb3/packages/fsrs/src/fsrs.ts)的repeat、next、get_retrievability及相关入口。
- [参数优化包说明](https://github.com/open-spaced-repetition/ts-fsrs/blob/c8ca282edc3fe1cdfa1c24912437938b63a25cb3/packages/binding/README.md)：复习日志转换、训练及浏览器/WASI依赖。没有审查完整Rust实现或训练流程。

没有安装、执行第三方代码、导入个人卡组、训练参数、发通知或验证学习效果。

## 对接时最容易混淆的五件事

| 实际接口或数据 | 智序应如何解释 |
|---|---|
| repeat返回四种评分的候选card/log | 它们是同一次复习的四种可能排程，不能保存成四次真实复习。 |
| next接收一个评分并返回card/log | 返回计算结果不等于已写入应用数据库。先核对实际回答、评分与授权，再由现有工具保存并检查结果。可选afterHandler可能带有调用方行为，不能一概当成无副作用。 |
| due、review、last_review等时间字段 | 到期是安排，不是完成；错过日期不能自动推断遗忘或补记Again。保留真实发生时间、时区及原始日志。 |
| get_retrievability的预测值 | 是模型对卡片回忆的估计，不是某人已掌握课程、考试通过率或知识迁移的证明。 |
| 独立的参数优化包 | 调度器存在不表示个性化训练已发生。优化需要适用、获准的复习历史和另外的执行能力，普通调度不需要默认加入该依赖。 |

README明确要求在应用边界验证外部输入。实际适配还需核对评分枚举、有效日期、卡片ID/所有者、日志去重、并发更新和存储读回；不要把TypeScript类型断言当作运行时验证。所查源码不能证明任意上层应用的权限隔离、持久化或网络行为。

## 采用与不采用

采用“预览与实际记录分开”“计划时间与完成证据分开”的通用约束，写入学习参考；没有复制第三方算法或代码。若以后获准开发适配器，应固定版本、保留许可、用合成卡片验证重复提交和重启恢复，再单独确认实际工具加载及写入范围。

不从默认参数推导每个人都该用同一复习频率，不保证保留率，不将逾期当成错误，不把排程库包装成自动记忆引擎。现有学习协议的自主选择、帮助程度、保持与迁移证据仍适用。
