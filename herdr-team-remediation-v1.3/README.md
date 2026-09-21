# Herdr-team Remediation v1.3

状态：`PROPOSAL / NOT_IMPLEMENTATION_BASELINE`

```yaml
implementation_allowed: false
```

v1.3 采用最小平台原则：保留文件式、Python stdlib、只读 Shadow，不建设持久化 Evidence Registry、数据库、消息总线、通用事件平台或第二套 Gate。

## 最小架构

```text
5 个 Schema
+ 2 个确定性摘要算法
+ 1 个进程内 Evidence Index
+ 2 个 Typed Event
+ 1 个 Revision-scoped Reducer
+ 1 个 Criterion-level Projection
```

## 当前允许

- Slice 0 正式治理材料准备
- Slice 0.5 Legacy submission/status 静态审计
- Slice 1 五个机器合同与 fixtures 独立评审

## 当前禁止

- `herdr-team/harness/**` 实现
- `herdr-team/.agent-control/MACHINE/**` 写入
- `dashboard.py` 修改
- `review_dispatch.py` 修改
- 旧 PHASES/Gate 修改
- 自动派发、自动 Repair、生产切换

## 阅读顺序

1. `00_governance/DECISION-CORE-SHADOW-SLICE.yaml`
2. `00_governance/WORKSTREAM_DRAFT.md`
3. `03_semantics/LEGACY_SUBMISSION_AND_STATUS.md`
4. `03_semantics/SEMANTIC_VALIDATION.md`
5. `02_algorithms/SUPERSESSION_AND_REDUCER.md`
6. `01_contracts/`
7. `04_fixtures/SCENARIO_INDEX.md`
8. `06_rollout/SLICE_PLAN.md`
