# Core / Workflow 工作组任务书

## 必答问题

1. Delivery Profile 的权威文件和 revision 如何存储？
2. `/delivery-setup`、`/delivery-change`、`/task-calibrate` 由谁执行？
3. Facts 如何自动收集，哪些 Decisions 必须询问用户？
4. Change Class 如何检测、升级、降级？
5. Effective Policy 如何确定性派生？
6. Task Acceptance 写入哪个持久层？
7. Evidence URI 如何解析及校验？
8. 如何保证 current / subject / reviewer / PM revision 一致？
9. Repair Round 何时递增，何时不递增？
10. 哪些事件是 meaningful activity，哪些只是 documentation activity？
11. 如何阻止 Documentation Loop？
12. 如何处理现有 Legacy Task？

## 最小决策

- `herdr-delivery-profile/1.0`
- `herdr-task-acceptance/1.0`
- `herdr-ledger-event/1.0`
- `herdr-effective-policy/1.0`
- `herdr-dashboard-projection/1.0`

## 明确不做

- 固定十阶段流程
- 硬编码角色
- 新的第四套任务状态系统
- `.pi/games` 运行树
- 文本 done 推进状态
- 将历史任务伪造为 PASS
