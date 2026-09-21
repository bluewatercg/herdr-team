# 整改包 × 真实仓库 对齐评审

```text
status: REVIEW_ONLY / NOT_IMPLEMENTATION_BASELINE
review_scope: herdr_remediation 全部 34 个文件 vs 真实 herdr-team 仓库
target_repo: herdr-team/  (独立 git 仓库)
target_revision: HEAD = 1b8ec5de530ebdb0ce485a514e0c52a02c4274bc
target_worktree: DIRTY（见 §2.3）
Prepared By: AI-assisted engineering
Reviewed By: NOT_AVAILABLE_AT_CURRENT_STAGE
Approved By: NOT_AVAILABLE_AT_CURRENT_STAGE
Approval Required For Investor MVP: NO
Approval Required Before Production: YES
```

本文件**不修改任何代码**，只回答一个问题：整改包里的每一条声明，落在真实仓库的哪个文件、哪个函数上；哪些能映射、哪些必须改写、哪些在真实仓库里根本不存在。

---

## 1. 结论摘要

| 维度 | 判定 |
|---|---|
| 问题诊断 | **成立**，且真实证据比包内描述更严重（见 §3） |
| 架构方向 | **成立**，值得做 |
| 可直接执行性 | **不成立**。缺 3 个契约、14 条用例数据、1 份真实文件映射、1 个架构决策 |
| 文件级变更清单 | **不可用**。包内 `01_FILE_CHANGE_MAP.md` 的路径是想象架构（见 §5） |
| 范围建议 | 包内 7 个 Phase 中，**Phase 2 / Phase 3 建议全做；Phase 1 建议砍到两维；Phase 5 建议不按包内做；Phase 6 在现有实现下无意义**（见 §7） |

---

## 2. 真实仓库事实基线

### 2.1 规模（`git ls-files`，55 个受控文件）

```text
harness 代码 + prompts + 配置      ≈ 120.6 KB   ( 6.9%)   16 个文件
.agent-control/ 账本 + 证据         ≈ 1 619 KB   (93.1%)   39 个文件
总计                                1 739 KB
```

`.agent-control/` 内需要被 harness 解析的人工可读账本：

| 文件 | 字节 | 行数 |
|---|---:|---:|
| `TASK_BOARD.md` | 323 904 | 910 |
| `MASTER_PLAN.md` | 77 356 | 387 |
| `FILE_OWNERSHIP.md` | 54 397 | 297 |
| `REVIEW_QUEUE.md` | 52 438 | 608 |
| `BLOCKERS.md` | 46 922 | 222 |
| `PROJECT_SNAPSHOT.md` | 13 507 | 117 |
| `DECISIONS.md` | 7 935 | 47 |
| 其余（`PM_GATE` / `PROJECT_SCOPE` / `INTERFACE_CONTRACT` / `TASK_TEMPLATE`） | 2 794 | 35 |
| **小计** | **579 253** | **2 623** |

单文件最大者：`ROUNDS/20260918T043217Z-meeting.md` = 254 767 字节 / 3 683 行（一次会议记录）。

**结论**：93% 的受控体积是状态文本，6.9% 是能执行的代码。这正是包内「高强度文档治理」诊断的量化形式。

### 2.2 真实 harness 组成

```text
dashboard.py        401 行 / 45.8 KB   单文件 Web 面板：PAGE(19) 内联 HTML + Handler(326) stdlib HTTP
review_dispatch.py  679 行 / 31.7 KB   评审队列、双 Gate 状态机、watch 常驻
activate.sh         104 行 /  4.5 KB   角色启动、pane 校验、prompt 注入
lfa-team.sh         133 行 /  6.7 KB   唯一公开入口（菜单 1-6）
preflight.sh         10 行             herdr / jq 预检
config.env           13 行             ROLE_KIND / ROLE_MODEL 映射
prompts/            COMMON.md 23 行、start.md 44 行、pm.md 90 行、review-code.md 6 行、api/app-apk/app-ios 各 4 行
```

### 2.3 基线完整性

- 12 个 harness 文件的 sha256 **与 `SHA256SUMS.txt` 逐字节一致** → 静态发行基线完好。
- 但工作树是脏的：5 个 modified（`TASK_BOARD.md` / `MASTER_PLAN.md` / `FILE_OWNERSHIP.md` / `REVIEW_QUEUE.md` / `QR-ANDROID-01-D01.json`）+ 2 个 untracked（`QR-E2E-01-D01.json`、`herdr_remediation/`）。
- ⚠️ 因此包内 Phase 0 第 2 步「记录当前行为基线与现有测试」**不能直接执行**——当前不构成干净基线，必须先提交或隔离。且包内**完全没提 `SHA256SUMS.txt` 这个现成机制**，应当复用而不是另造一套。

### 2.4 真实状态机（关键）

`review_dispatch.py`：

```python
PHASES = ('ACTIVE', 'AUTHOR_COMPLETE', 'REVIEW_PENDING', 'REVIEW_ACCEPTED',
          'PM_PENDING', 'PM_ACCEPTED', 'CLOSED')            # L23
EVIDENCE_READY = {'IMPLEMENTED_PENDING_REVIEW','AUTHOR_COMPLETE','REVIEW_PENDING'}  # L24
def transition(row, phase):                                 # L32  强制逐级推进，跳级抛异常
def gate_key(task_id, sha256, size, gate_type='REVIEW')     # L28  task_id:sha256:size:type
def task_rows(root)                                         # L40  正则扫 TASK_BOARD.md 半结构化行
def legacy_gate_complete(root, task_id, sha256, size)       # L61  子串匹配 REVIEW_QUEUE.md 判定 Gate
```

这就是现有任务状态系统：**7 阶段线性状态机 + 内容哈希身份 + 文本子串判 Gate**。

---

## 3. 诊断成立的真实证据

包内没给出证据，这里补上——三条都是硬证据：

### E1 Gate 判定靠子串匹配

```python
# review_dispatch.py:61
token  = f'{sha256}/{size}bytes'
spaced = f'{sha256} / {size} bytes'
return task_id in text and (token in text or spaced in text) \
       and 'CODE_REVIEW_ACCEPTED' in text and 'PM_ACCEPTED' in text
```

Gate 是否通过，取决于 52 KB 的 `REVIEW_QUEUE.md` 里是否**碰巧出现了这几个字符串**。不是结构判定。

### E2 投影不是 reducer，是单次运行的定制渲染器

```python
# dashboard.py:153 execution_projection()
node1_tasks = evidence_tasks("QR-PC-01-D01.json")     # 硬编码证据文件名
node3_review_accepted = "QR-FINAL-01 repaired revision independent Review accepted" in review_text \
    and "c99cfa6d411f3181fe0453f0b34c786bf4ce44287e6c795e66b964369ee3a538" in review_text   # 硬编码 sha256
node3_pm_accepted = ... and "15214bytes" in review_text                                       # 硬编码字节数
```

node id、证据文件名、内容哈希、字节数全部写死在函数体内。**再来一个任务就废**。这直接决定了包内 Phase 6「影子运行比较状态差异」在现有实现下做不出有意义对照——现有投影本身就不是从账本推出来的。

### E3 任务解析只看得到第一张表

```python
# dashboard.py:109 parse_tasks()
if in_task_table and line.strip():
    break          # 任务表后第一个非空非表格行 → 直接停止
```

`TASK_BOARD.md` 有 910 行、323 KB，`parse_tasks()` 只会读到第一张表。

### E4 有内容哈希，没有 revision 概念

`gate_key` 绑定的是 `sha256 + size`。**全仓库无 git revision 概念**（`PM_GATE` 里的 `GIT_HEAD` 只用于 PM 接管校验）。所以包内 Core Matrix 的 C10（`current revision 改变 → STALE`）不是「待实现」，是**当前架构下不存在的能力**。

---

## 4. 逐 Phase 对齐

| Phase | 真实落点 | 判定 |
|---|---|---|
| **0 冻结边界** | `SHA256SUMS.txt`(15 项) + `herdr-team/.git`（单 commit） | ⚠️ 可做但**前提不成立**：工作树脏（§2.3）。且应复用 `SHA256SUMS.txt`，包内未提 |
| **1 Delivery Governance** | `config.env`(13 行 role→model) / `activate.sh:68 start_role()`（prompt 注入点）/ `prompts/COMMON.md` | 需新建。**但 `config.env` 是 shell env 格式，不是版本化 JSON**；「Profile 注入启动上下文」的真实注入点是 `start_role()`，包内未定位 |
| **2 Acceptance Contract** | `.agent-control/TASKS/TASK_TEMPLATE.md`(29 行) + `review_dispatch.py` | ✅ 落点清晰。**但现有模板的 `ACCEPTANCE_CRITERIA`/`REQUIRED_TESTS`/`REQUIRED_EVIDENCE` 是无 `criterion_id` 的自由文本**，C06/C07/C08 无处校验 |
| **3 BTW / Doc Loop** | `review_dispatch.py:watchdog(403)`（唯一常驻检测器） | ⚠️ **一半已存在但被违反**：`start.md:8` 已写「总控不得在 MASTER_PLAN/DECISIONS/TASK_BOARD 之外维护第二份项目阶段状态」，`start.md:23` 已写「不另建账本或任务状态系统」。缺的不是规则，是**检测与执行** |
| **4 Projection API** | `dashboard.py:execution_projection(153)` / `status_payload(299)` | ✅ 落点清晰，替换目标明确（见 E2） |
| **5 WebUI MVP** | `dashboard.py:PAGE(19)` 内联 HTML | ❌ **与包内自身约束冲突**（§5.3） |
| **6 影子运行** | — | ❌ 见 E2：现有投影无法作为有意义的对照基线 |
| **7 切换** | `review_dispatch.py:PHASES(23)` / `transition(32)` | ⚠️ **需要包内未给出的架构决策**：新状态（`REPAIRING`/`REPAIR_EXHAUSTED`/`READY_FOR_PM_GATE`/`BLOCKED`）与现有 7 阶段**部分重叠但不相等**。是扩 `PHASES` 还是并存？包内不变量说「不创建第四套任务状态系统」，但没说怎么合 |

---

## 5. `01_FILE_CHANGE_MAP.md` 逐条核对

### 5.1 修改类

| 包内声明路径 | 真实对应 | 判定 |
|---|---|---|
| `.agent-control/TASKS/TASK_TEMPLATE.md` | ✅ 存在，29 行 | 可映射 |
| `AGENTS.md` | ❌ herdr-team 内不存在；**项目根 `AGENTS.md` 是 LFA 项目执行策略** | **越界**。应改为 `prompts/COMMON.md` |
| `prompts/COMMON.md` | ✅ 23 行 | 可映射 |
| `prompts/pm.md` | ✅ 90 行 | 可映射 |
| `prompts/start.md` | ✅ 44 行 | 可映射 |
| `prompts/review-code.md` | ✅ 6 行 | 可映射 |
| Watch 事件解析器 | ≈ `watch_loop(505)` / `ensure_watch(486)` / `watchdog(403)` | ⚠️ 语义不同：现为「评审队列轮询 + 300s 超时看门狗」，**不是通用事件解析器** |
| Ledger reducer | ❌ 不存在 | 新建 |
| PM / Reviewer Gate 执行器 | ≈ `decision(364)` / `submit(212)` / `reconcile(320)` / `continue_accepted(295)` | ⚠️ 存在，但是 7 阶段线性机（§2.4） |
| WebUI routing/store/API client/Task components | ❌ 不存在 | 见 §5.3 |

### 5.2 新增类——路径冲突

```text
包内建议                        真实情况
core/delivery/                  ❌ 项目根 core/ 是 Python Core 分析引擎（12 个 .py）
core/acceptance/                   herdr-team/core/ 会造成同名混淆，
core/evidence/                     且包内写的是无前缀的 core/，
core/projection/                   若落在仓库根会直接撞上真实 core/
```

**必须换名**，例如 `herdr-team/harness/delivery/`。这是包内完全没意识到的问题。

### 5.3 WebUI 与零依赖承诺冲突

- 包内 `README.md` 与 `04_rollout/01` 同时声称：保留零依赖 + 新增 `webui/pages/*`、`webui/components/*` 组件树。
- 真实 `dashboard.py` 是 401 行单文件、`PAGE` 内联 HTML、仅 stdlib。
- 二者**不能同时成立**。若真要组件化，必须同步改 `herdr-team/README.md` 第 43 行（「无需安装 Node 或额外依赖」）——包内未列为修改项。

### 5.4 包内自述与自身清单矛盾

- `README.md` 第 13 行：「**不复制代码、目录、角色或固定阶段**」。
- 但 `01_FILE_CHANGE_MAP.md` 第 32-44 行直接给出 `core/delivery/`、`webui/pages/`、`webui/components/` 整套目录树。
- 且 `README.md` 第 12 行声称保留「动态角色配置」，但变更清单**未涉及** `config.env` / `activate.sh` 这两个角色配置的真实落点。

---

## 6. 缺口清单（实施前必须补齐）

| ID | 缺口 | 证据 | 阻塞级别 |
|---|---|---|---|
| **G1** | 5 个自封「最小决策」中 3 个无 schema / 无 fixture：`herdr-ledger-event/1.0`、`herdr-effective-policy/1.0`、`herdr-dashboard-projection/1.0` | `02_core/contracts/` 只有 2 个 schema | 阻塞 Phase 2/4 |
| **G2** | Core Matrix 18 条里 C09–C18 **一条测试数据都没有**；fixtures 仅 4 个且全是 schema 级 | `contracts/fixtures/` 4 文件 | 阻塞验收 |
| **G3** | **criterion registry 缺失**。C06/C07/C08（缺/未知/重复 criterion）光靠 `herdr-task-acceptance.schema.json` 判不出来，需要任务侧 criterion 清单契约 | schema 无 criterion 定义源 | 阻塞 Phase 2 |
| **G4** | schema 把 `max_rounds` 写成 `const: 2`，与「Effective Policy = Profile × Class × Risk」矛盾——`REGULATED_RELEASE` 无法调轮次 | `herdr-task-acceptance.schema.json:39` | 阻塞 Phase 1 |
| **G5** | 无真实仓库文件映射 | 本文件 §5 | 已由本文件补齐 |
| **G6** | **`PHASES` 合并决策缺失**（扩还是并存） | §4 Phase 7 | 阻塞 Phase 2 |
| **G7** | `core/` 目录名冲突 | §5.2 | 阻塞 Phase 1 |
| **G8** | `webui/` 与零依赖承诺冲突，README 未列为修改项 | §5.3 | 阻塞 Phase 5 |
| **G9** | Evidence URI 解析规则未定；fixtures 用 `evidence://test/T1` 占位 | `acceptance-pass.json` | 阻塞 C09 |
| **G10** | `deferred_scope` 与 `MASTER_PLAN.md` 的 `PARKED` 可能形成第二套停放权威，与「不创建第四套任务状态系统」冲突 | `PROJECT_SCOPE.md` / `MASTER_PLAN.md` 现状 | 需决策 |
| **G11** | `agent_calibration` 与「稳定角色名用于 pane 断线恢复」有张力，包内未约束其不得改稳定角色名 | `prompts/COMMON.md:19` 稳定名清单 | 需约束 |
| **G12** | 命名 / 引用错误 | 见 §7 | 低 |

---

## 7. 包内具体错误

| # | 位置 | 问题 |
|---|---|---|
| E-1 | `04_rollout/01_FILE_CHANGE_MAP.md:8` | 把 `AGENTS.md` 列为修改项——那是项目根 LFA 执行策略，动它会违反项目规则 |
| E-2 | `03_webui/tests/UI_ACCEPTANCE_SCENARIOS.md:12` | 「有 Build TODO 无 owner → `NO_ACTIVE_BUILD`」语义反了，`NO_ACTIVE_BUILD` 应指无 build TODO；无 owner 是 `UNOWNED_BUILD` |
| E-3 | `03_webui/tests/UI_ACCEPTANCE_SCENARIOS.md:15` | 引用「R5 类 PATCH」，**包内全文无 `R5` 定义** |
| E-4 | `README.md:13` vs `01_FILE_CHANGE_MAP.md:20-44` | 「不复制目录」vs 直接给出目录树 |
| E-5 | `README.md:12` vs `01_FILE_CHANGE_MAP.md` | 「保留动态角色配置」vs 清单未涉及 `config.env` / `activate.sh` |
| E-6 | `02_core/specs/TASK_ACCEPTANCE_SPEC.md:8` | `subject_revision.type: git` 但真实仓库无 revision 概念（E4），`artifact-set` 才是当前唯一可用的类型 |
| E-7 | `04_rollout/00_MASTER_REMEDIATION_PLAN.md:6` | Phase 0 要求「记录当前行为基线与现有测试」，未提及工作树已脏、也未提及复用 `SHA256SUMS.txt` |

---

## 8. 范围建议（有立场）

包内 7 个 Phase 不是同价值的。按「收益 ÷ 风险」排序：

### 建议全做

- **Phase 2 Acceptance Contract** — 直接消灭 E1（子串判 Gate）。收益最高，且落点（`TASK_TEMPLATE.md` + `review_dispatch.py`）清晰。
- **Phase 3 BTW / Doc Loop** — 规则已在 `start.md` 存在但被违反，缺的只是检测器。挂在现成的 `watchdog(403)` 上成本很低。**这是本次整改最划算的一块。**

### 建议砍

- **Phase 1 Delivery Governance** — `4 mode × 5 change class × 9 risk flag` 的组合爆炸，对当前单人 + 6 agent 的 MVP 阶段是过度设计。建议**只做 `delivery_mode` + `change_class` 两维**，`risk_flags` 降级为可选自由标注，等真出现跨档需求再展开。

### 建议不按包内做

- **Phase 5 WebUI** — 保持 stdlib 单文件，只把 `execution_projection()` 换成真 reducer。收益 90%，成本 10%。按包内的 `webui/pages/*` 组件树做，等于引入前端工具链 + 推翻「零依赖」承诺，收益增量远小于成本。

### 当前无意义

- **Phase 6 影子运行** — 见 E2，现有投影不是从账本推出来的，影子期没有可对照的旧基线。要么先补一个最小可用的旧投影，要么接受它退化为人工核对。

### 前置（必须先做）

1. 补 **G3 criterion registry** + **G2 扩展到 C01–C18 的 fixtures** —— 否则 Phase 2 无法验收。
2. 用 `SHA256SUMS.txt` 机制完成 Phase 0 基线冻结（含处理当前 5 个 modified）。
3. 就 **G6（`PHASES` 扩还是并存）** 出决策 —— 这是整套整改里唯一的真架构决策，其余都是工程活。

---

## 9. 未决问题

| # | 问题 | 阻塞实施 |
|---|---|---|
| Q1 | `PHASES` 扩还是并存？（G6） | 是 |
| Q2 | `max_rounds` 由 Effective Policy 派生还是 schema 常量？（G4） | 是 |
| Q3 | criterion registry 落在任务模板还是独立契约？（G3） | 是 |
| Q4 | WebUI 保持 stdlib 还是引入工具链？（G8） | 是（Phase 5） |
| Q5 | `deferred_scope` 与 `PARKED` 的权威关系？（G10） | 否 |
| Q6 | `agent_calibration` 是否允许改稳定角色名？（G11） | 否 |
| Q7 | `/delivery-setup` 由哪个角色执行？（包内 `01_CORE_WORKGROUP_BRIEF.md:6` 自列为待答） | 否 |

---

## 10. 本次评审的边界

- 只做静态阅读与交叉核对。**未运行 `dashboard.py`、未运行 `review_dispatch.py self-test`、未启动任何 Herdr agent**。
- 未修改任何代码、账本或既有包内文件；本文件为新增。
- 未评估包内提议的**科学/统计**有效性——不在范围内。
- 本文件是评审，不是决策记录。包内要求的 `DECISION-CORE` / `DECISION-WEBUI` / `DECISION-DELIVERY-PROFILE` / `DECISION-MIGRATION` **仍然全部缺失**，`implementation_allowed` 仍为 `false`。
