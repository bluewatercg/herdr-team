# 变更记录 / 2026-09-24

**外部助手干预登记。本文件不是控制账本，不参与任何 Gate、Review 或授权判定。**

## 授权来源

- **指示**：用户明确指示「开始动」。
- **实质授权**：`PM-LEDGER-REQ-01` 已于 `MASTER_PLAN.md`（PM control-ledger governance registration 节）与 `TASK_BOARD.md`（行 PM-GOV-01）登记，但登记时带 `IMPLEMENTATION_AUTHORIZED: false`，从未应用到 `prompts/*.md`。
- **执行者**：外部助手（Lumen），**不是** `lfa-pm`、`lfa-start` 或任何已注册角色。
- **登记目的**：让这次干预可复核，而不是隐藏。

## 本次变更要解决的问题

PM 在 `MASTER_PLAN.md:1104` 登记自己是控制账本唯一 writer，`TASK_BOARD.md` 也把它标为 `REGISTERED`。但运行时行为的唯一来源 `prompts/*.md` 从未改过：

- `prompts/start.md` 两处（`:25`、`:84`/`:87`）宣称 START 是唯一 writer；
- `prompts/pm.md` 四处（`:33`、`:50`、`:75`、`:105`）禁止 PM 写账本。

结果 PM 声明自己是 writer，自己的 prompt 却禁止它写。`verify_governance.py` 原有 9 条检查全部比对绑定与 owner 唯一性，从不比对 writer 身份，因此这个矛盾无法被任何检查发现。这就是用户描述的派单堵塞的机制性成因。

## 改动清单

| 文件 | 前 SHA256 | 后 SHA256 | 大小 |
|---|---|---|---|
| `prompts/start.md` | `c9aa9c5f1d5088bb…` | `d8fac0f44d077150db78f3b4cf47e9e9bf708e5223dcd59ecb3f4be2ee849ecb` | 12,103 → 12,887 B |
| `prompts/pm.md` | `f1de42333405c663…` | `fad04c09be96fa7644e31054708f7bdae64756516b7a9ad0fa26a9867152c2be` | 21,140 → 22,371 B |
| `verify_governance.py` | `e2017a5668313224…` | `54cb4caa364508c3d59b83a3e1234ef075195441def4c5eb622deb4f2fc17cfb` | 36,516 → 44,138 B |
| `.agent-control/DECISIONS.md` | `218066cec869eea3…` | `7f4760eb9c19626e394cd6dc7a7d45b3ac1d943b8136f513fe7cbbbd1a0931f9` | 13,788 → 15,931 B |
| `.agent-control/TASK_BOARD.md` | `9964552e53f6e474…`（备份时）→ `346004fe7f2d107f…`（迁出前） | `647ce70ef47ec07d557fb47c0245baf8707f79e22db8396920905d50d1d49988` | 570,272 → 572,059 → 349,206 B |
| `.agent-control/archive/AGENT_TODO_SNAPSHOTS.md` | 新建 | `f975cf244eb842b054bbc3f93cb736ef63f855af6822479c0e71a50b6367ecfd` | → 224,825 B |

> `TASK_BOARD.md` 本次会话改了两步：先追加 PM-GOV-01 实施回执（570,272 → 572,059 B），再迁出快照（572,059 → 349,206 B）。`346004fe…` 是迁出前的即时哈希。

### 1. `prompts/start.md` — 控制账本写入边界

- 新增 `## 控制账本写入边界` 节，声明 `lfa-pm` 是唯一 writer，START 是执行与回执角色。
- 删除 `:84-85` 与 `:87-93` 的截断重复 sole-writer 段，替换为单一正确表述。
- `:25`「START作为现有唯一writer把PM提供的事实归因记录并回执」改为 PM 落盘、START 只提交事实。
- `:39`/`:40`/`:48` 快照区规则改为**不写入控制账本**，改追加到归档文件。
- `:21`、`:27`、`:33`、`:35` 残留的 START 写账本表述改为 PM 记录。
- `:42-44` 与 `COMMON.md` 重复的中文回复段压缩为指针。

### 2. `prompts/pm.md` — 控制账本唯一 writer

- 新增 `## 控制账本唯一 writer` 节，含三条边界（证据不得作者自写、append-only + 链式哈希、账本实质变更仍需非作者 Review 与单独 PM Gate）。
- 反向断言改为正向：`:33`、`:50`、`:75`、`:105`，以及 `:40`、`:43`、`:51`、`:74`。
- 修复章节错位：`## PM Review 输出` 原本是空标题，其正文（`TASK_ID:` 等 10 个字段）被 `## Machine-readable PM gate` 的 code fence 切断，落在 fence 之外。现已归位并加 fence。
- 补 `PM_GATE.STATUS` 只取 `READY|CONFLICTED|BLOCKED` 三值的说明，任务级结论写 `PM_GATE_DECISION.RESULT`。

### 3. `verify_governance.py` — 新增三条检查

| 检查 | 严重级 | 作用 |
|---|---|---|
| `WRITER-BOUNDARY` | VIOLATION | 扫描 `prompts/*.md`，非 `lfa-pm` 角色自称控制账本 writer 即报错 |
| `SECTION-DUPLICATE` | VIOLATION | 同一账本内 `## ` 标题重复即报错（原规则被违反 8 次且无检查能发现） |
| `LEDGER-SIZE` | WARNING/VIOLATION | 账本 token 估算，>60K 警告、>150K 视为不可恢复 |

另把 `check_agent_status` 的失效状态显式化：该检查找 `git_head` 字段，而 9 个 `AGENT_STATUS` 文件中 0 个有此字段，检查**永远不报任何问题**。现加 `AGENT-STATUS-INERT`（INFO）暴露这一点。

`WRITER_BOUNDARY` 的判定形状为「角色紧邻 writer 断言」，因此合法描述（如 `start.md` 里说明 `lfa-pm` 是唯一 writer）不会被误判。已用改动前的备份验证该检查有牙齿：改动前抓到 2 处越界，改动后 0 处。

### 4. `.agent-control/TASK_BOARD.md` — 快照迁出

迁出 237 行 / 223,379 B：8 个重复 `##` 标题 + 55 个 `### <role>-OP-NNNN` 快照小节标题 + 9 行 `CURRENT_PM_OPERATIONAL_REVISION:` + 55 个 json 快照 fence 块。原文逐字移入 `.agent-control/archive/AGENT_TODO_SNAPSHOTS.md`，原位留指针。

**无损性校验**：多重集重构一致；markdown 表格行 121 → 121（零丢失）；归档缺失行数 0。

> 第一次尝试用的规则是「切 old line 577–1852」，把该区间内的真实账本记录（BTW-CHECK 回执、任务登记表、ownership 表）一起搬走，丢掉 `PM-PATROL-01-D01` 登记行。已从备份逐字节回滚，改用上述外科式规则重做。回滚与损坏态证据见 `.workbuddy-ai/backups/2026-09-24-0303/`。

### 5. `.agent-control/DECISIONS.md` — supersede 记录

追加一节，supersede `GOV-MGMT-01` 节里的「START是八文件唯一writer」。GOV-MGMT-01 的记录流程本身（issue 字段、recurrence_count、release_conditions、历史不改写）继续有效，只改 writer 身份。

## 未做的事

- 未改任何业务代码、`MASTER_PLAN.md`、`FILE_OWNERSHIP.md`、`PM_GATE`、`PROJECT_SNAPSHOT.md`。
- 未做接受判定。`PM-GOV-01` 仍为 `IMPLEMENTED_PENDING_NONAUTHOR_REVIEW_AND_SEPARATE_PM_GATE`，需非作者 Review 与单独 PM Gate 才能关闭。
- 账本仍约 250K tokens，超出单窗口。进一步压缩需要 PM 决定「热/冷分界」（按时间归档旧回执），本次未做，因为那会改变 START 能读到的范围，属实质规则变更。

## 量化效果（对备份逐项实测，复现脚本 `.workbuddy-ai/scripts/before_after.py`）

### 体量

| 指标 | 前 | 后 | 变化 |
|---|---|---|---|
| 账本 6 文件 token | 290,826 | 234,344 | **-19.4%** |
| 账本 6 文件字节 | 1,114,843 B | 895,920 B | -19.6% |
| `TASK_BOARD.md` | 570,272 B / 148,316 tok | 349,206 B / 91,350 tok | **-39.0%** |
| 占 128K 窗口 | 227% | 183% | 仍装不下 |

### 缺陷清零

| 项 | 前 | 后 |
|---|---|---|
| `TASK_BOARD` 重复 `##` 标题 | 2 类 × 4 次（多出 6 份） | **0** |
| prompt 越界 writer 宣称 | 2 处（`start.md`） | **0** |
| `pm.md` 章节错位 | `## PM Review 输出` 正文被 fence 切断 | 已归位 |
| `start.md` 截断重复段 | 存在 | 已删 |

### 新增检出能力（原先完全不可见）

| 检查 | 严重级 | 此前状态 |
|---|---|---|
| `WRITER-BOUNDARY` | VIOLATION | 无任何检查比对 writer 身份 |
| `SECTION-DUPLICATE` | VIOLATION | 规则被违反 8 次，无检查能发现 |
| `LEDGER-SIZE` | WARNING / VIOLATION | 账本 8.5 小时 +952 行，静默增长 |
| `AGENT-STATUS-INERT` | INFO | `check_agent_status` 永远不报问题，伪装成"已通过" |

### 治理校验

`verify_governance.py`：VIOLATION **7 → 4**（`INTG-CHECKSUM-INVALID`、`SECTION-DUPLICATE`×2 消失），WARNING 0。

## 未提升的（如实记录）

- **账本仍 234,344 tokens = 128K 窗口的 183%，断线恢复依然装不下。** 本次只降 19.4%，未解决。
- `COMMON.md:25` 的「中文回复内部三遍处理」让生成成本至少 ×3，未动。
- `OWN-MULTI-ACTIVE` ×2（`docs/QiuQiu_…v1.7…md` 双 owner、`docs/requirements/DHEA_MVP_完整需求.md` 双 owner）为预存在真冲突，未处理。
- `pm.md` 中 Jev 内容占 52%，未压缩。
- 历史 `PM_GATE` 里的 `PM_GATE_ACCEPTED_DOCUMENTARY_ONLY` 类非枚举值未清理。

## 可回滚性

`.workbuddy-ai/backups/2026-09-24-0303/` 保存改动前的 `prompts/`、`verify_governance.py`、`jev_decide.py`、`SHA256SUMS.txt` 与全部 `.agent-control/`，附 `BACKUP_MANIFEST.sha256`。另存 `TASK_BOARD.pre-migration-2-20260924.md` 与 `TASK_BOARD.migrated-broken-20260924.md`。
