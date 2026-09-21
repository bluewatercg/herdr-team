# 整改讨论章程

## 目标

将当前“终端窗格 + 高强度文档治理”模式调整为：

`Delivery Profile -> Task Calibration -> Build -> Acceptance -> Repair -> Regression -> Gates -> Dashboard Projection`

## 分组

### A. Core / Workflow 工作组

负责：

- Delivery Profile 与交互式配置向导
- Change Class / Risk Flags / Effective Policy
- Task Acceptance Contract
- Evidence、Revision、Repair、Regression、双 Gate
- BTW、文档预算、WIP、Doc Loop Kill Switch
- Watch / Ledger / Reducer 输入事件
- 兼容和迁移

### B. WebUI / Projection 工作组

负责：

- Dashboard 信息架构
- Projection schema 和 reducer 输出
- Run Overview / Task Detail / Evidence Detail
- Needs Attention
- Delivery Profile 页面与配置向导
- Terminal 降级为诊断 Tab
- 状态映射、边界状态和 UI 验收

## 共同不变量

- UI 不写权威状态。
- Agent 文本不等于完成。
- `UNVERIFIED` 永不等于 `PASS`。
- 缺字段是 `CONTRACT_INVALID`，不是 `UNVERIFIED`。
- Acceptance、Regression、Reviewer Gate、PM Gate 必须绑定同一 subject revision。
- Reviewer 可发现 NEXT/LATER，但 MVP1 下只有指定阻断类型可拒绝当前交付。
- Documentation 默认不阻塞开发。

## 讨论输出

每组只提交：

1. 采用 / 不采用的决策；
2. 文件级变更清单；
3. Schema / API 差异；
4. 状态机；
5. 测试和 Fixture；
6. 迁移风险；
7. 未决问题；
8. 最小可实现切片。

禁止输出长篇项目历史复述。
