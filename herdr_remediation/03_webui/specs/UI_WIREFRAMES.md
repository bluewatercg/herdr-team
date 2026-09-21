# UI Wireframes

## Run Overview

```text
+------------------------------------------------------------------+
| Project / Run / Mode: MVP1_PROOF                  RUNNING         |
| First visible goal | current branch | authoritative update       |
+------------------------------------------------------------------+
| Tasks | Blocked | Repairing | Review Ready | PM Ready | Passed   |
+-------------------------------+----------------------------------+
| Needs Attention               | Pipeline                         |
| BLOCKING TASK-017             | Plan PASS                        |
| AC-002 UNVERIFIED             | Build ACTIVE                     |
| DOC_LOOP_DETECTED TASK-021    | Review BLOCKED                   |
+-------------------------------+----------------------------------+
| Task | Revision | Acceptance | Repair | Regression | Gates       |
+------------------------------------------------------------------+
```

## Task Detail

```text
+------------------------------------------------------------------+
| TASK-017                                         BLOCKED          |
| Current a182e91 | Subject a182e91 | Owner worker-02              |
+------------------------------------------------------------------+
| MATCHED | UNVERIFIED | 1/2 REVIEW | UNVERIFIED | BLOCK | WAIT    |
+----------------------------------+-------------------------------+
| Acceptance                       | Needs Attention               |
| AC-001 PASS                      | BLOCKING AC-002               |
| AC-002 UNVERIFIED                | ENVIRONMENT_UNAVAILABLE       |
+----------------------------------+-------------------------------+
| Repair                            | Regression                    |
+------------------------------------------------------------------+
| Gate chain: artifact -> acceptance -> reviewer -> PM             |
+------------------------------------------------------------------+
| Activity | Evidence | Diff | Tests | Events | Terminal           |
+------------------------------------------------------------------+
```
