# 真实仓库落点

## 现有关键文件

```text
herdr-team/review_dispatch.py
herdr-team/dashboard.py
herdr-team/activate.sh
herdr-team/config.env
herdr-team/prompts/COMMON.md
herdr-team/prompts/start.md
herdr-team/prompts/pm.md
herdr-team/prompts/review-code.md
herdr-team/.agent-control/TASKS/TASK_TEMPLATE.md
herdr-team/.agent-control/EVIDENCE/**
herdr-team/.agent-control/TASK_BOARD.md
herdr-team/.agent-control/REVIEW_QUEUE.md
herdr-team/SHA256SUMS.txt
```

## 新实现路径候选

```text
herdr-team/harness/{contracts,evidence,validation,reducer,projection,adapters}/
herdr-team/.agent-control/MACHINE/{criteria,evidence,events,acceptance,projections}/
```

## 禁止路径

- 项目科学计算 `core/`
- Node/WebUI 组件树
- 项目根 `AGENTS.md`

## 旧生命周期

```text
ACTIVE → AUTHOR_COMPLETE → REVIEW_PENDING → REVIEW_ACCEPTED
→ PM_PENDING → PM_ACCEPTED → CLOSED
```

Shadow 不推进、不阻断、不写回旧生命周期。
