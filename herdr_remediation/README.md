# Herdr-team 整改实施包 v1.0

状态：PROPOSAL / NOT_IMPLEMENTATION_BASELINE

本包用于组织两条并行讨论和形成可执行整改方案：

1. Herdr-team 底层工作流、治理与机器验收协议改造。
2. WebUI 与背后 Projection / Reducer / Watch 流程改造。

核心原则：

- 保留 `MASTER_PLAN -> TASK_BOARD -> OMP TODO`、`FILE_SCOPE`、唯一 `WRITE_OWNER`、独立 Reviewer、PM Gate、同 revision 双 Gate、持久账本、幂等通知、Watch、断线恢复和动态角色配置。
- 借鉴参考项目的结构化产物契约、有限修复轮次、接口先冻结和唯一 integration owner 思想，但不复制代码、目录、角色或固定阶段。
- 新增 `DELIVERY_PROFILE + CHANGE_CLASS + RISK_FLAGS`，先决定交付层级，再派生 Agent、测试、文档和 Gate 力度。
- 新增 `herdr-task-acceptance/1.0`，将验收事实机器化。
- 新增 `herdr-dashboard-projection/1.0`，Dashboard 只展示确定性投影。
- Build 是主工作；Trace 是最小结构化副作用；Verify 绑定当前 revision。

## 推荐阅读顺序

1. `01_discussion/00_DISCUSSION_CHARTER.md`
2. `01_discussion/01_CORE_WORKGROUP_BRIEF.md`
3. `01_discussion/02_WEBUI_WORKGROUP_BRIEF.md`
4. `04_rollout/00_MASTER_REMEDIATION_PLAN.md`
5. `02_core/specs/DELIVERY_GOVERNANCE_SPEC.md`
6. `02_core/specs/TASK_ACCEPTANCE_SPEC.md`
7. `03_webui/specs/DASHBOARD_ARCHITECTURE.md`
8. `04_rollout/03_VALIDATION_PLAYBOOK.md`

## 决策闸门

本包不能直接视为已批准基线。组织讨论结束后应形成：

- `DECISION-CORE`
- `DECISION-WEBUI`
- `DECISION-DELIVERY-PROFILE`
- `DECISION-MIGRATION`

只有 PM 明确批准对应 revision 后才进入实现。
