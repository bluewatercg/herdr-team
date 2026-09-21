# Master Remediation Plan

## Phase 0：冻结整改边界

1. 创建整改分支或隔离 worktree。
2. 记录当前行为基线与现有测试。
3. 冻结不变量和明确不做项。
4. 两工作组完成决策记录。
5. PM 批准后设置 `implementation_allowed: true`。

### 验证

- 决策记录版本化。
- 现有启动、Watch、恢复能力基线通过。
- 无产品代码改动。

## Phase 1：Delivery Governance

1. 加入 Delivery Profile schema。
2. 实现 profile store 与 revision。
3. 实现 Delivery Setup / Change / Task Calibrate。
4. 实现 Effective Policy 计算。
5. 将 Profile 注入 Agent 启动上下文。
6. 加入 Development Readiness。

### 验证

- MVP1 PATCH 产生轻策略。
- MVP1 Contract Change 产生 current-slice Gate。
- Profile 未确认不能激活。
- 降级和升级均产生差异记录。

## Phase 2：Acceptance Contract

1. 修改 Task Template。
2. 加入 JSON Schema 与 validator。
3. 定义 Evidence resolver。
4. 实现 Acceptance reducer。
5. 实现 revision matching。
6. 实现 Repair / Regression 状态机。
7. Reviewer 输出结构化结果。
8. PM Gate 只读结构化结果。

### 验证

运行 Core Matrix C01-C18。

## Phase 3：BTW 与 Doc Loop 防护

1. 冻结 BTW policy。
2. 设置一个 active build TODO。
3. 区分 meaningful / documentation events。
4. 只允许四类文档触发器。
5. 加入 DOC_LOOP_DETECTED。
6. Agent 回复改为 delta。

### 验证

- 文档事件不能推进任务。
- Build TODO 存在时不会生成独立文档主任务。
- 重复 recap 被识别。

## Phase 4：Projection API

1. 定义 Dashboard Projection。
2. 实现确定性 reducer。
3. 幂等重放测试。
4. Attention 去重。
5. last meaningful activity。
6. Legacy 映射。

### 验证

- 相同事件集得到相同 Projection。
- 到达顺序扰动不改变最终状态。
- 重放不增加 repair round。

## Phase 5：WebUI MVP

1. Delivery Profile 页面。
2. Run Overview。
3. Task Detail。
4. Evidence Detail。
5. Needs Attention。
6. Gate Chain。
7. Terminal 移入诊断 Tab。

### 验证

运行 UI Acceptance Scenarios 1-14。

## Phase 6：影子运行

1. 新 Projection 与现有 Dashboard 并行。
2. 不控制生产 Gate。
3. 比较状态差异。
4. 修正 reducer 和数据缺口。
5. PM 明确切换。

## Phase 7：切换与收尾

1. Dashboard 改读 Projection。
2. Gate 改读 Acceptance 与 revision。
3. 保留回滚开关。
4. 旧任务按 Legacy 展示。
5. 输出迁移报告。
