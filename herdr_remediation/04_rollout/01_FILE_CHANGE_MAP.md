# 文件级变更映射

以下为建议路径，实施前需对真实仓库结构做路径映射。

## 修改

- `.agent-control/TASKS/TASK_TEMPLATE.md`
- `AGENTS.md` 或对应公共执行策略
- `prompts/COMMON.md`
- `prompts/pm.md`
- `prompts/start.md`
- `prompts/review-code.md`
- Watch 事件解析器
- Ledger reducer
- PM / Reviewer Gate 执行器
- WebUI routing、store、API client、Task components

## 新增

```text
.agent-control/contracts/
  herdr-delivery-profile.schema.json
  herdr-task-acceptance.schema.json
  herdr-ledger-event.schema.json
  herdr-dashboard-projection.schema.json

.agent-control/contracts/fixtures/
.agent-control/delivery-profiles/
.agent-control/acceptance/
.agent-control/projections/

core/delivery/
core/acceptance/
core/evidence/
core/projection/

webui/pages/DeliveryProfile/
webui/pages/RunOverview/
webui/pages/TaskDetail/
webui/pages/EvidenceDetail/
webui/components/Acceptance/
webui/components/Gates/
webui/components/Attention/
```

## 不修改

- 原三层状态体系语义
- 现有 Herdr 启动与恢复入口
- 动态角色机制
- 产品业务仓库文件，除非对应任务明确授权
