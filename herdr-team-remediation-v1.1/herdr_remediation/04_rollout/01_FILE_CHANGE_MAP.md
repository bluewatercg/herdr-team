# 真实文件映射 v1.1

设计阶段写：`herdr-team/herdr_remediation/07_core_shadow_design/**`

未来实现候选：

```text
herdr-team/harness/{contracts,evidence,validation,reducer,projection,adapters}/**
herdr-team/.agent-control/MACHINE/**
```

只读输入：

```text
herdr-team/.agent-control/EVIDENCE/**
herdr-team/.agent-control/TASK_BOARD.md
herdr-team/.agent-control/REVIEW_QUEUE.md
herdr-team/review_dispatch.py
herdr-team/dashboard.py
herdr-team/SHA256SUMS.txt
```

Slice 7 才能修改 `dashboard.py`。正式 Gate 集成前禁止修改 `review_dispatch.py`。

永不写：项目根 AGENTS.md、科学计算 core/**、已有 Accepted Evidence、产品应用代码。
