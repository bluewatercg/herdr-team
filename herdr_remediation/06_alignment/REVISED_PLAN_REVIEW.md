# 修订版整改方案评审

```text
status: REVIEW_ONLY / NOT_IMPLEMENTATION_BASELINE
review_subject: 六人评审后的修订方案（Core 只读影子切片 + Q1-Q7 决策 + 五类合同 + Slice 0-7）
target_repo: herdr-team/
target_revision: HEAD = 1b8ec5de530ebdb0ce485a514e0c52a02c4274bc
Prepared By: AI-assisted engineering
Reviewed By: NOT_AVAILABLE_AT_CURRENT_STAGE
Approved By: NOT_AVAILABLE_AT_CURRENT_STAGE
Approval Required For Investor MVP: NO
Approval Required Before Production: YES
```

---

## 1. 总判定

```text
方向              ACCEPT
Q1 / Q3 / Q4 / Q5 / Q6   ACCEPT（与上一轮评审一致）
Q2                ACCEPT WITH AMENDMENT（删 const 正确，但新约束有一处过度）
Q7                ACCEPT（且因 Wizard 暂缓，正确做法是只登记不实现）
Slice 0-7 的依赖顺序   ACCEPT
Slice 4 的范围     REDUCE（见 §4，成本最高、可信度最低）
Slice 5 的技术要求   INSUFFICIENT（见 §3，缺构造性确定性保证）
治理登记            MISSING（见 §6，违反 herdr-team 自身 dispatch rule 2/3）
implementation_allowed: false   —— 维持，无异议
```

修订版把上一版的「大规模同时改造」收缩成「先把事实机器化」，方向对，收缩幅度也对。**但有 7 处技术问题、2 处治理缺口，以及 1 个我今天在真实仓库里查出来的活体缺陷**——后者应当插到 Slice 0 之前。

---

## 2. 它正确吸收的部分（确认，不重复论证）

| 上一轮编号 | 修订版处理 | 判定 |
|---|---|---|
| G6 PHASES 扩还是并存 | 并存，新维度归 `verification_projection`，`may_block/advance_legacy_phase: false` | ✅ 正确。dispatch lifecycle 与 verification dimension 确实不是同层 |
| G4 `max_rounds` const 2 | 改为 integer 0..10，语义交 Validator | ✅ 方向正确（但见 §3-C） |
| G3 Criterion Registry | 独立版本化 JSON + `criterion_registry_ref` | ✅ 正确 |
| G8 WebUI 零依赖冲突 | 保持 stdlib，Phase 5 重写为最小只读扩展 | ✅ 正确 |
| G10 `deferred_scope` vs `PARKED` | 不引入第二套停放权威，只存 `park_authority` 引用 | ✅ 正确 |
| G11 `agent_calibration` 改角色名 | 禁止，改为策略键 | ✅ 正确 |
| G7 `core/` 撞名 | 改用 `harness/` + `MACHINE/` | ✅ 正确 |
| E-7 Phase 0 未提脏工作树 / SHA256SUMS | Slice 0 明确隔离 + 复用 | ✅ 正确 |
| E-1 `AGENTS.md` 越界 | 落点改为 `prompts/*` | ✅ 正确 |
| E-2/E-3 命名错误 | 未提（低优先级，不影响决策） | ⚠️ 仍未修正 |

---

## 3. 技术异议

### 3-A（最高）Reducer 缺构造性确定性保证 —— 会直接挂掉自己的「乱序」测试

修订版要求 Pure Reducer 必须通过「乱序 / 重放 / 同键异载荷」。但如果 reducer 写成

```python
for event in events:
    state = apply(state, event)
```

那么「乱序」测试**必然失败**：只要两个事件触碰同一字段，结果就依赖到达顺序。而修订版自己承认「跨 source 无因果关系 → 只能用明确 causation/correlation 或 reducer 规则解释」——**即事件集只有偏序，没有全序**。对偏序集合做 fold，不可能确定性。

**必须写成格（lattice）上的单调 join**，并且顺序已经在包内现成：

> `02_core/specs/TASK_ACCEPTANCE_SPEC.md:51` —— `INVALID > STALE > FAIL > UNVERIFIED > PENDING > PASS`

若每个维度按该全序取 `max()`，则 reducer 天然满足交换律、结合律、幂等律，乱序/重放**按构造成立**，不靠运气。

**补充要求**：`idempotency_key` 同键异载荷是**冲突**，不是 `max` 能表达的。必须明确：冲突先于 join 求值，且冲突结果（`IDEMPOTENCY_CONFLICT`）在格中**支配一切**（高于 `INVALID`）。否则冲突会被 `max` 悄悄吸收掉。

**验收标准建议**：乱序测试不能只测「最终状态相同」，必须断言 reducer 是 `commutative ∧ associative ∧ idempotent`（可用随机置换 + 重复注入做性质测试）。

### 3-B（高）Legacy Adapter 是成本最高、可信度最低的组件 —— 必须拆分

修订版目标 1 是「能把现有文本账本转换成有合法来源的结构化事件」，Slice 4 读 `TASK_BOARD.md` / `REVIEW_QUEUE.md` / evidence JSON / `gate_key`。

问题：上一轮评审已确认 **E1 —— 现有 Gate 判定本身就是子串匹配**（`review_dispatch.py:61`：`'PM_ACCEPTED' in text`）。若 Adapter 从同一批文本派生事件，则「结构化事件」只是把子串匹配换了层皮，**其可信度上限等于被解析散文的可信度**。这构成循环：投影的可靠性由 Adapter 决定，Adapter 无独立校验。

而修订版声称的目标是「不出现已被 Reviewer 发现的伪 PASS」——用散文派生的 PASS 无法证明这一点。

**关键事实：evidence 层其实已经是结构化的，成本远低于修订版假设。**

实测 16 个证据 JSON：

| 结构 | 数量 | 说明 |
|---|---:|---|
| 有 per-task 私有 schema | 4 | `qr-android-01-evidence/1.0`、`qr-e2e-01-evidence/1.0`、`qr-final-01-evidence/1.0`、`qr-pc-01-evidence/1.0` |
| 无 `schema` 字段 | 12 | `QR-GEOMETRY-*`、`QR-PLAN-*`、`RUN-*` |

`QR-FINAL-01-D01.json` 的顶层结构已经是：`plan_id / deliverable_id / task_id / write_owner / status / stage / source_receipt{path,lines,utf8_bytes,sha256} / authority / implementation_files[11] / self_binding{path,sha256,bytes,binding} / behavior / focused_checks / requirement_btw_checks[12] / fixture_disclosure`。

而 `review_dispatch.py:discover_evidence()` 已经能读 `task_id/plan_id/deliverable_id/status/write_owner/implementation_files[{path,sha256}]`。

**结论**：真正要做的不是新建 `herdr-evidence-descriptor/1.0`，而是**把已有的 4 个 per-task schema 收敛成 1 个共享版本化 schema**（保留既有字段语义），否则会造出第三套并行格式，让 Adapter 同时映射两种。

**建议拆分**：

```text
Slice 4a  Evidence JSON → 共享 schema + validator
          成本低、可信度高、可独立验收。建议前移。
Slice 4b  Markdown 账本（TASK_BOARD / REVIEW_QUEUE）
          成本高、可信度上限低。建议降级为「保守分类器」：
          只输出 EXACT | PARTIAL | UNAVAILABLE | CONFLICTED，
          且默认值必须是 UNAVAILABLE，绝不是 PASS。
          散文只作 source_ref，不作事件内容。
```

硬不变量建议写进 spec：**Adapter 在无法确证时只能降级，不得升级。** 没有这条，影子切片会把伪 PASS 从文本搬进 JSON。

### 3-C（中）三个伪 PASS 封堵中，第三处过度约束，且与 §5 自相矛盾

修订版 §4 伪 PASS 3 要求：

```text
EXHAUSTED requires:
  current_round == max_rounds
  max_rounds > 0
  at least one finding_ref
  regression.required == true      ← 问题在这
```

`regression.required == true` 与 repair 是否耗尽**没有逻辑关系**。一个 PATCH 类任务可以不需要回归而把修复轮次用尽。强制它 → 合法输入被判 `CONTRACT_INVALID`。

而修订版 §5 自己刚说过「不能无条件将 UNVERIFIED 阻断所有任务」——即已经意识到过度阻断的问题。同一份文档里一处放松、一处收紧，不自洽。

**建议**：删掉该子句，保留 `current_round == max_rounds ∧ max_rounds > 0 ∧ len(finding_refs) >= 1`。

**另外补两条它漏掉的**：

- `status: NOT_REQUIRED` 时 `finding_refs` 必须为空（非空即 INVALID）。
- `required: false` 时 `result` 必须为 `NOT_REQUIRED`，不得为 `PASS`/`FAIL`。

### 3-D（中）`evidence_refs` 的类型在新旧之间断裂

- 包内 fixture 用 URI 字符串：`"evidence_refs": ["evidence://test/T1"]`。
- 修订版新引入 `herdr-evidence-descriptor/1.0`，其 URI + integrity + binding 都在 descriptor 里。

那么 acceptance 里的 `evidence_refs` **应该是 `evidence_id`（如 `EVD-001`），不是 URI**。否则 acceptance 直接持有 URI，descriptor 的 integrity 层被绕过——而 integrity 正是封堵「伪 PASS 1 / Evidence hash mismatch」的机制。

修订版引入了 descriptor，却没说它**取代** URI 字符串。必须明说，且 4 个 fixture 全部要改。这一点与 §3-C 一起构成「fixtures 必须在语义修正后重新生成」的结论——即 G2 不能按旧语义扩到 C01–C18。

### 3-E（中）`required: false → NOT_REQUIRED` 没有承载字段

修订版 §5 写「required=false → NOT_REQUIRED」。但 `regression.result` 的 enum 是 `["PASS","FAIL","UNVERIFIED"]`，**没有 `NOT_REQUIRED`**。所以这个值没有落点。

而现有 fixture `acceptance-pass.json` 正是 `required: false, result: "UNVERIFIED", reason_code: "NOT_EXECUTED"` —— 按修订版 §5 的规则，它应该表达为 `NOT_REQUIRED`。

**必须二选一并写死**：

```text
方案甲：result enum 增加 NOT_REQUIRED
方案乙：required=false 时忽略 result 字段，由 reducer 派生 NOT_REQUIRED
```

我倾向方案乙（避免一个字段承载两种语义），但无论选哪个，**`UNVERIFIED` 目前被同时用来表示「不需要」和「需要但无法验证」，这是当前设计里最脏的一处**，必须解决。

### 3-F（中）`artifact-set` 的摘要算法未定义 —— 而仓库里已有现成约定

`revision_status` 的 STALE 判定**完全依赖** `artifact-set` 摘要。修订版选了正确的类型（避开不可用的 `git`），但从未定义摘要怎么算：

- 按什么排序？
- 是否包含 acceptance JSON 自身 / evidence / criterion registry？
- 路径相对谁？

不同实现会算出不同摘要 → STALE 误报。

**仓库已有约定，直接用**：

```text
herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-REPAIR-BOUNDARY-manifest.json   (175 KB，已有 artifact-set manifest 先例)
docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/MANIFEST.sha256                  (格式：<sha256>  <相对路径>，按路径排序)
MASTER_PLAN.md:148                                                                       (已用 MANIFEST digest 绑定包 revision：0416b380…)
```

**建议**：`artifact-set.value` = `sha256:` + 对 `<sha256>  <path>\n` 排序清单（同 `MANIFEST.sha256` 格式）再取 sha256。**不要另造摘要方案。**

### 3-G（中）规范化 JSON 哈希未定义 —— 同样已有约定

`Ledger Event` 需要「同 idempotency_key + 同规范 payload digest」，`Evidence Descriptor` 需要 integrity digest。但「规范」是什么？JSON 键序、数字格式、Unicode 转义都会改变字节。

**仓库已有 JCS 约定**：

```text
fixtures/dhea-v3/jcs/metadata.jcs
fixtures/dhea-v3/jcs/product-gate-declaration.jcs
fixtures/dhea-v3/jcs/result-snapshot.jcs
fixtures/dhea-v3/jcs/sha256.json                    ← JCS 哈希清单
EVIDENCE/QR-FINAL-01-D01.json:72                    ← "canonical JCS digest binds persistence and replay"
```

**建议**：显式写「payload digest = SHA-256(JCS(payload))」，并复用 `fixtures/dhea-v3/jcs/sha256.json` 的清单形式。**否则事件幂等性会在跨语言/跨实现时碎掉。**

---

## 4. 我建议重排的 Slice 顺序

修订版的依赖顺序是对的，但有 3 处应调整：

```text
新增 Slice 0.5  证据层静态审计（成本约 1 小时，见 §5）
                → 必须在 Slice 4 之前，否则 Adapter 会忠实复现现有盲区

Slice 4 拆为    4a Evidence JSON 共享 schema（前移，低成本高可信）
                4b Markdown 保守分类器（后移，降级为 UNAVAILABLE 默认）

Slice 6 选谁    建议选 QR-ANDROID-01-D01，不要随便挑
                理由见 §5：它的证据正好是当前被静默丢弃的那个，
                影子输出立刻能演示价值
```

---

## 5. 真实仓库里的活体缺陷（本次新发现，修订版和上一版都没提）

### 16 个证据 JSON，只有 3 个能被派发

`review_dispatch.py:24`：

```python
EVIDENCE_READY = {'IMPLEMENTED_PENDING_REVIEW', 'AUTHOR_COMPLETE', 'REVIEW_PENDING'}
```

`review_dispatch.py:76-77`：

```python
if any(not evidence.get(name) for name in required) or evidence['status'] not in EVIDENCE_READY:
    continue
```

实测结果：

| 证据文件 | 缺必需字段 | status 在 EVIDENCE_READY | 会被派发 |
|---|---|---|:--:|
| `QR-PC-01-D01.json` | — | 是 | ✅ |
| `QR-FINAL-01-D01.json` | — | 是 | ✅ |
| `QR-E2E-01-D01.json` | — | 是 | ✅ |
| **`QR-ANDROID-01-D01.json`** | **无缺失** | **否**（`IMPLEMENTED_DEVICE_EVIDENCE_PENDING`） | ❌ |
| `QR-GEOMETRY-01-G1-*.json` (3) | `write_owner` | 否 | ❌ |
| `QR-PLAN-0{2,3,4}-D01-checks.json` | `write_owner` | 否 | ❌ |
| `QR-SCOPE-05-D01-checks.json` | `status`, `write_owner` | 否 | ❌ |
| `RUN-*` (4) | 多项 | 否 | ❌ |
| `PM-ONBOARD-*.json` | `plan_id`, `deliverable_id`, `write_owner` | 否 | ❌ |

**关键点不是「13 个被丢弃」，而是「丢弃是静默的，且 NOT_READY 与 UNRECOGNIZED 不可区分」。**

`QR-ANDROID-01-D01.json` 五个必需字段齐全、结构完整，仅因 `status` 字符串不在一个 3 元素硬编码集合里就被跳过。系统无法区分：

```text
「这份证据确实还没准备好」      ← 合理跳过
「这份证据的 status 拼错了 / 用了新词表」 ← 静默丢弃，应报警
```

同理，7 个文件缺 `write_owner` 也是静默的。

**这与整改主题直接相关**：影子切片要证明「能把事实机器化」，但如果 Legacy Adapter 复用 `EVIDENCE_READY` 这套词表逻辑，它会**忠实复现同一个盲区**，然后把盲区画进漂亮的 Projection。

**结论**：`status` 词表必须成为 Evidence 共享 schema 的 enum（§3-B 的 Slice 4a），并加一条规则——**status 不在词表内 → 报 `UNKNOWN_EVIDENCE_STATUS`，不得静默跳过**。这是 Slice 0.5 的核心产出。

顺带：`PM-ONBOARD-20260918T043217Z.json` 的 `status` 字段里装的是一整段 git status 文本（多行）。字段无类型纪律，也应在共享 schema 里收紧。

---

## 6. 两处治理缺口（修订版完全没提，但会卡住派发）

### 6-A 未注册 `PARALLEL_WORKSTREAM`

`prompts/start.md:5` + `MASTER_PLAN.md:83-84` 规定：任何非主线工作必须先做影响分析，并登记

```text
WORKSTREAM / MAINLINE_IMPACT / EXECUTION_STATUS / INTEGRATION_STATUS
需求与来源 / owner / 依赖 / 精确读写文件隔离 / Exit / Integration Gate
```

且「未分类或隔离不成立时不得派发，先交 PM 裁定」。

修订版给了一个 `decision_id`，**但没有 workstream 注册**。按其自身规则，Slice 0 就派不出去。

**建议**：

```text
WORKSTREAM: HARNESS-VERIFICATION-SHADOW
MAINLINE_IMPACT:
  Slice 0-6  → NONE      （只新增 harness/ 与 MACHINE/，不改主线运行行为）
  Slice 7    → BOUNDED   （改 dashboard.py，见 6-B）
```

### 6-B 会打破已 ACCEPTED 的 GOV-DOC-01-D01 哈希绑定

`MASTER_PLAN.md:106-107`：

```text
PLAN_ID: GOV-DOC-01
DELIVERABLE_ID: GOV-DOC-01-D01
STATUS: ACCEPTED
ACCEPTED_KEY: RUN-20260918T043217Z-DOC-GOVERNANCE:f348c1da5ea03d3076b867222a3e951b34bd6ee02c42dc270537b3d3eb6b8a2d
ACCEPTANCE_SCOPE: ... subsequent control-record edits change bound source hashes
                  and do not assert current envelope freshness ...
```

而 `GOV-REQ-05` 的授权范围就是 **`review_dispatch.py`**，`GOV-REQ-06` 是 **`dashboard.py`**。

修订版的 Slice 2/3/5 改 `review_dispatch.py` 相邻逻辑、Slice 7 改 `dashboard.py` → **这两个已 ACCEPTED 交付物的绑定哈希会变**。按 `start.md:33`「历史前缀、旧Review及Evidence不改」，不能回头改旧记录，只能追加说明。

**修订版必须补一段**：对 `GOV-DOC-01-D01` 的影响声明（哪些哈希变化、是否需要新的 envelope、是否触发重新绑定）。否则 Slice 7 会在一个 ACCEPTED 交付物上做未经声明的修改。

---

## 7. 决策记录格式不符

包内 `01_discussion/03_DECISION_TEMPLATE.md` 规定字段：

```text
decision_id / decision_revision / status / scope
accepted / rejected / modified
implementation_allowed / required_gates / open_questions
```

修订版 §9 的 `DECISION-CORE-SHADOW-SLICE`：

| 模板要求 | 修订版 | 判定 |
|---|---|---|
| `decision_revision` | 无 | ❌ 缺 |
| `scope`（CORE/WEBUI/…） | 无（改用 decision_id 后缀表达） | ❌ 缺 |
| `required_gates` | 无 | ❌ 缺 |
| `open_questions` | 无（Q1-Q7 写在正文，未结构化） | ❌ 缺 |
| `status: DRAFT\|APPROVED\|REJECTED` | `APPROVED_FOR_DETAILED_DESIGN` | ❌ 枚举外 |
| `implementation_allowed`（布尔） | 对象 `{core_shadow_slice, production_gate_change}` | ⚠️ 结构变了 |

模板存在的意义就是让决策可机器消费。**第一份决策就漂移，等于宣布模板作废。** 建议二选一：改模板（并记录原因），或改决策以符合模板。不要静默不一致。

---

## 8. 未决问题（修订后仍开放）

| # | 问题 | 阻塞 |
|---|---|---|
| Q8 | reducer 是否按「每维度在 `INVALID > STALE > FAIL > UNVERIFIED > PENDING > PASS` 上取 max」实现？（§3-A） | 是（Slice 5） |
| Q9 | `IDEMPOTENCY_CONFLICT` 在格中的支配位置？（§3-A） | 是（Slice 5） |
| Q10 | `artifact-set` 摘要是否采用 `MANIFEST.sha256` 格式？（§3-F） | 是（Slice 1/3） |
| Q11 | payload digest 是否采用 `SHA-256(JCS(payload))`？（§3-G） | 是（Slice 1/3） |
| Q12 | `regression.required=false` 用方案甲还是乙？（§3-E） | 是（Slice 1/2） |
| Q13 | `evidence_refs` 改为 `evidence_id` 后，4 个 fixture 是否全部重生成？（§3-D） | 是（Slice 2） |
| Q14 | Slice 4 是否拆为 4a/4b？（§3-B） | 是（Slice 顺序） |
| Q15 | `HARNESS-VERIFICATION-SHADOW` 的 workstream 注册与 `MAINLINE_IMPACT` 分类？（§6-A） | 是（派发前） |
| Q16 | 对 `GOV-DOC-01-D01` 的影响声明？（§6-B） | 是（Slice 7 前） |

---

## 9. 结论

修订版把我上一轮列出的 8 条缺口和 7 条错误吸收了绝大部分，收缩方向正确，**「先机器化事实 → 再证明 reducer 确定性 → 再影子展示 → 最后谈 Gate 和 UI」这个顺序我完全同意**。

我不同意的是三件事：

1. **reducer 的确定性还停留在愿望层面**（§3-A）。不写成格上的 join，乱序测试过不了。
2. **Legacy Adapter 的定位错了**（§3-B）。evidence 层已经是结构化的，成本被高估；Markdown 层可信度有硬上限，成本被低估。拆分后前移 4a、降级 4b。
3. **Slice 0 之前应该先做一次证据层静态审计**（§5）。因为当前 `EVIDENCE_READY` 已经在静默丢弃 13/16 份证据，而 Adapter 会把同一个盲区复制进 Projection。

另外两处治理缺口（§6）会直接卡住派发，必须在 `implementation_allowed` 置真之前补上。

**当前 `implementation_allowed: false` 应当维持——不仅因为五类 Schema 和 WRITE_OWNER 未冻结，还因为 §6-A 的 workstream 注册和 §6-B 的既有 ACCEPTED 交付物影响声明都还不存在。**

---

## 10. 本次评审边界

- 只做静态阅读、交叉核对与只读脚本统计。**未运行 `dashboard.py`、未运行 `review_dispatch.py`，未修改任何账本或代码。**
- 只读统计脚本见 §3-B / §5 表格；数据源为 `herdr-team/.agent-control/EVIDENCE/*.json` 与 `review_dispatch.py` 常量。
- 未评估 `harness/` 与 `MACHINE/` 目录的 `.gitignore` 策略、`SHA256SUMS.txt` 是否需扩展——属实施细节。
- 本文件是评审，不是决策记录。`DECISION-CORE` / `DECISION-WEBUI` / `DECISION-DELIVERY-PROFILE` / `DECISION-MIGRATION` 仍全部缺失。
