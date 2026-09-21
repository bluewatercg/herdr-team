# Validation Playbook

## A. Schema

使用 JSON Schema validator 验证所有 fixtures。正例必须通过，非法 PASS 无 evidence 必须失败。

## B. Reducer

- 同一事件集重复运行，输出 byte-equivalent projection。
- idempotency key 重放无副作用。
- current revision 改变后旧 PASS 变 STALE。
- evidence 失效后 declared 不变、effective 变 INVALID。

## C. Repair

- 基础设施失败不加 round。
- 正式 reviewer fail 才可能加 round。
- max 后为 EXHAUSTED，不自动 FAILED。

## D. Delivery Calibration

- Quick Start 不超过六个用户决策。
- Repository facts 不询问用户。
- Profile 必须 CONFIRM 后激活。
- PATCH 可降级，不继承父任务全部 Gate。

## E. BTW

- active Build 存在时无文档主任务。
- Trace 只写结构化 event。
- 文档事件不更新 meaningful activity。
- Doc Loop 触发后回到 Build。

## F. UI

- UI 不允许直接写状态。
- 状态有文字和 reason code。
- Terminal 默认不是首页。
- 对所有阻断显示明确下一动作。

## G. 端到端演练

1. 建立 MVP1 Delivery Profile。
2. 创建 PATCH Task。
3. 记录 revision。
4. Reviewer 记录 UNVERIFIED。
5. Dashboard 显示 BLOCKED。
6. 新 Evidence 后记录 PASS。
7. Reviewer PASS。
8. PM PASS。
9. Dashboard PASSED。
10. 再产生新 revision，旧结果 STALE。
