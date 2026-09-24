# Herdr 多 Agent 自动激活包
默认团队包含六个 OMP 主角色，以及 Grok、Claude 两个只读交叉评审角色。

```bash
cd /你的项目
# 在 Herdr 的空闲 Shell pane 内，只执行这一个公开入口
./herdr-team/lfa-team.sh
```

查看实时状态时仍运行同一入口，选择 `6) 打开团队 Web 面板`，然后访问 `http://127.0.0.1:8765`。面板每 5 秒只读刷新 Herdr Agent、母计划位置、PM Gate、任务板、阻塞项和最近终端输出；支持只读筛选、节点深链接和证据定位，不提供命令发送、审批或文件修改能力。

三层状态：`MASTER_PLAN.md` 是项目阶段、依赖、下一 Gate 和停放工作的唯一权威；`TASK_BOARD.md` 是当前可执行任务权威；OMP TODO 是每个 Agent 会话执行权威。不会绕过登录、授权或审批。iOS 真构建仍需 macOS/Xcode。

## PM 项目接管
PM 激活后先读取 `herdr-team/.agent-control/MASTER_PLAN.md`，再扫描仓库、Git、活动任务、合同、阻塞、证据和 Agent 状态，生成 `PROJECT_SNAPSHOT.md`。每个任务必须绑定 `PLAN_ID`、`DELIVERABLE_ID` 和 `TASK_ID`；无完整绑定任务不得派发。`lfa-start` 读取快照并通过 PM Gate 后才进入正式会议与派单。OMP TODO 仅表示单 Agent 执行进度，不等于项目任务关闭。

未来正式任务还必须填写 `REQUIREMENT_IDS`、`REQUIREMENT_SOURCE_REFERENCES`，遵循 [需求追踪 Gate](prompts/COMMON.md#需求追踪-gate) 的唯一引用链。`UNMAPPED` 阻止派发和验收，直至 PM 核实映射；finding IDs 不得冒充 requirement IDs。模板、任务板、证据和 Dashboard 只引用权威 ID/来源，不复制需求正文。

## Jev 决策与 START 授权回执
Jev 只提供建议，不能单独改变 Intake、Task、Review、Gate、ownership 或派发状态。只有同时存在真实 Jev 输出、明确的 PM 裁决、完整任务绑定和唯一 `WRITE_OWNER` 时，才允许持久化授权事件。

受控 writer 为 `jev_decide.py`，只接受 `actor=lfa-pm` 且明确授予 `lfa-start` 的事件：

```bash
python3 herdr-team/jev_decide.py --input /path/to/real-pm-decision.json
python3 herdr-team/jev_decide.py --self-test
```

事件追加到 `.agent-control/JEV_DECISIONS.jsonl`，使用排他锁、`fsync` 和相同 `decision_id` 幂等检查；损坏日志、冲突重复 ID、缺少 `PLAN_ID`、`DELIVERABLE_ID`、`TASK_ID`、`FILE_SCOPE` 或授权字段时拒绝追加。不存在真实事件时，不创建示例记录，也不把用户文字、prompt transport ACK 或 Jev 建议当作授权。

`lfa-start` 必须读取原始 JSONL，重新核对精确绑定、文件范围、唯一 active owner 和是否存在 superseding event，然后在自己的控制账本中记录 acknowledgement。writer 成功、prompt 发送成功或 Jev 推荐本身都不等于 START 接受、任务派发、执行开始或 Gate 通过。

控制链路变更后可运行：

```bash
python3 -B herdr-team/dashboard.py --check
```

该检查只验证当前真实账本和 Dashboard 投影，不会生成决策、派发任务或修改业务状态。

## 文件写入所有权
`FILE_OWNERSHIP.md` 是并发写入控制账本，不是第二套任务状态。PM 为每个任务登记具体 `FILE_SCOPE` 和唯一 `WRITE_OWNER`；`lfa-start` 派单前检查重叠，有冲突就串行或重新切分。一级 Agent 管理本组 pane，只有指定 pane 可写，其他 pane 只读；Review 按实际 diff 检查越界。换 owner 必须先释放原 owner，同一路径禁止两个 `ACTIVE` 写 owner。

## 稳定名称与断线恢复
稳定主角色为 `lfa-start`、`lfa-pm`、`lfa-android`、`lfa-api`、`lfa-ios`、`lfa-review`；辅助交叉评审角色为 `lfa-grok-review`、`lfa-claude-review`。后两者不替代 `lfa-review`，不形成正式 Review Gate，也不写源码或控制账本。Herdr server 保存 pane 和 Agent 进程；`herdr-team/.agent-control/` 保存项目事实。TUI、SSH 或当前 pane 断开后，重新进入 Herdr，在项目目录运行 `./herdr-team/lfa-team.sh` 并选择“恢复 PM 协调”。不要再次启动新一轮覆盖现有状态。

任务派发后，运行入口并选择 `4) 打开 PM 对话窗口` 可直接切换到 `lfa-pm` pane，继续讨论其他项目问题；已派发且无依赖的工作不会因此暂停。

开始新一轮时可为每个角色选择当前项目中已有的空闲 Shell pane；未选择的角色自动创建 workspace。脚本按真实前台进程验证 pane，拒绝当前入口 pane、运行服务的 pane、其他项目 pane、重复分配和已有未命名 Agent。已运行的 `lfa-*` 团队不会被覆盖，使用“恢复 PM 协调”继续。

新一轮的目标、验收和限制已内置当前 DHEA Investor MVP 默认值，三项直接回车即可采用。自定义内容可输入多行，并以单独一行 `.` 结束；pane 输入仅接受列表中的 `w*:p*` ID或空行。

## 自动继续与 watch 恢复
新建团队和“恢复 PM 协调”均调用 `review_dispatch.py ensure-watch`，为当前项目与 Herdr session 保持一个常驻 watch；只有确认进程就绪才返回成功。重复启动复用现有实例，进程退出后重新运行恢复入口即可重建，不终止其他项目或 session 的进程。

### Agent 每日日记与统一日报

`daily_memory.py watch` 是统一入口：扫描所有命名 Agent 的会话记录，将每个 pane（包括 `lfa-test`）写入同一日期目录的 `events.jsonl`，并生成 `daily-report.md`。日报输入包含工作、测试结果、阻塞、TASK_ID、revision 和证据引用；测试 PASS 仍只是测试证据，不等同 Review 或 PM 验收。

长期记忆与日报分离：`lfa-test` 的操作和测试结果只进入日报事件投影，不写入 `records`、`summary.md` 或 `CURRENT.md`。其他 pane 继续进入原有记忆摘要。开始采集：

```bash
cd /mnt/d/Project/Aventura/java_developer/AIPoweredHealthManager-lfa-reader/herdr-team
HERDR_ENV=1 python3 daily_memory.py watch
```

同一时间只运行一个 watcher；重复启动会因 `writer.lock` 返回 `Resource temporarily unavailable`。检查已有实例：

```bash
pgrep -af 'daily_memory.py watch'
```

日报与原始事件位于 `~/.local/share/lfa-team-memory/YYYY-MM-DD/`：

```bash
cat ~/.local/share/lfa-team-memory/2026-09-23/daily-report.md
less ~/.local/share/lfa-team-memory/2026-09-23/events.jsonl
grep '"agent": "lfa-test"' ~/.local/share/lfa-team-memory/2026-09-23/events.jsonl
```

验证 `lfa-test` 不进入长期记忆：

```bash
python3 - <<'PY'
import sqlite3
db = sqlite3.connect('/root/.local/share/lfa-team-memory/records.sqlite')
print(db.execute("SELECT day, agent, count(*) FROM report_events WHERE agent='lfa-test' GROUP BY day, agent").fetchall())
print(db.execute("SELECT day, agent, count(*) FROM records WHERE agent='lfa-test' GROUP BY day, agent").fetchall())
PY
```

预期第二行为空。测试事件进入 `report_events` 和日报，不进入 `records`、`summary.md` 或 `CURRENT.md`。

### 如何 Review 日报

日报不是代码验收。Review 时依次核对：

1. `daily-report.md`：查看所有 pane 的工作、测试结果和阻塞。
2. `events.jsonl`：回看原始事件，不只看模型生成的摘要。
3. `TASK_ID`、`PLAN_ID`、`DELIVERABLE_ID`：确认测试和实现属于同一任务链路。
4. 测试使用的 Git revision、命令、退出码和证据路径。
5. `lfa-review` 的独立 Review 结果。
6. `lfa-pm` 的 PM 验收结论。

`lfa-test` 的 `PASS` 只证明指定 revision 上的测试结果，不自动等于 `CODE_REVIEW_ACCEPTED`、`PM_ACCEPTED` 或任务关闭。正式流程仍为：`lfa-test` 提供测试证据，`lfa-review` 独立 Review，`lfa-pm` 验收，`lfa-start` 同步账本与 Gate。

原有 `summary.md`/`CURRENT.md` 仍是非权威派生视图，控制账本和任务状态不由日报入口修改。

## 模型分工
`lfa-start`、`lfa-pm` 使用 `shuaiapi-020/gpt-6-astra`；`lfa-android`、`lfa-api`、`lfa-ios` 使用 `shuaiapi-020/gpt-5.6-sol`；独立测试/脚本角色 `lfa-test` 使用 `aliyun/qwen3.7-plus`，独立评审仍使用各自现有配置。PM 负责协调；测试/脚本任务派给 `lfa-test`，代码任务派给对应实现 Agent。正式任务与回报继续绑定同一 `TASK_ID`；该分工不绕过既有 Gate、owner 和授权要求。实际模型和 kind 记录在 `.agent-control/AGENT_STATUS/`。

OMP 使用 `--auto-approve`，Grok 使用 `--always-approve`，Claude 使用 `--permission-mode auto`。辅助评审角色的 prompt 明确限制为只读第二意见。

Web 面板使用 Python 标准库并仅绑定 `127.0.0.1`，无需安装 Node 或额外依赖。运行日志写入 `.agent-control/dashboard.log`；动态控制账本和日志不纳入静态发行哈希。

## 静态清单校验与冻结

`python3 herdr-team/checksum_manifest.py` 只读校验；`--self-test` 检查注释、损坏清单、路径越界、符号链接和缺文件时保留旧清单。`verify_governance.py` 使用同一校验实现。清单错误、缺文件、漏覆盖或摘要不符均失败，不会把 Git 失败自动降级成摘要通过。

每批受保护变更冻结后、提交评审前，由有写入授权且无 ACTIVE 冲突的 owner 执行 `python3 herdr-team/checksum_manifest.py --refresh`，再运行 `sha256sum -c SHA256SUMS.txt`。逐任务更新也必须在该批文件冻结后进行。生成器先读取所有必需文件，缺失即失败，写入前复核内容并原子替换；冻结期间不得并发修改受保护文件。

保护范围由 `checksum_manifest.py` 的 `STATIC_FILES` 与全部 `prompts/*.md` 定义，涵盖运行脚本、治理/Jev/harness 实现和校验器、README/config、任务模板。动态账本、日志、历史 Evidence、独立 remediation/package 发行包及设计文档不纳入本清单；独立包保留自己的清单。此范围不同于 Jev 深度触发集，后者还含动态治理账本。扩大保护范围须评审，不代表当前 Gate 已通过。

清单头的 `BASE_COMMIT` 仅记录生成时 HEAD，`CONTENT_SOURCE: WORKTREE` 明确摘要来自工作树，可能包含未提交修改；时间与提交号不证明内容获批或未被篡改。工具通过不替代同 revision 的非作者 Review 和独立 PM Gate，也不继承历史 ACCEPTED。

治理检查器将母计划之外、在 `FILE_OWNERSHIP.md` 或其登记的 PM-owned Evidence 中找到同任务声明的记录列为 `BIND-AUTHORITY-MANUAL-REVIEW`。这仍是违规，不是授权通过；须核验相同任务三元组、原始授权、精确 scope/owner、需求与 Exit。TASK_BOARD 自填行、命名前缀及 `CONTROL_PLANE_ONLY` / `MAINLINE_IMPACT=NONE` 不授予权限，不追溯回填历史 MASTER_PLAN 或改写 ACCEPTED。COMMON 的现行派发规则和独立双 Gate 继续适用。

显式 `REQUIREMENT_SOURCE_REFERENCES` 列使用分号分隔本地文件引用，可附 `#heading` 或 `:起行-止行`。校验只证明引用可定位，拒绝越界、符号链接或不存在的来源，不证明授权内容真实有效。

## Jev 任务深度观察
`jev_task_depth.py` 是 PM 语义传感器，不是授权或派发器；其 `authority` 全部为 `false`，`authority_effect` 固定为 `NONE`。CLI 接受位置参数 `user_verbatim`，以及 `--pm-interpretation`、`--candidate-action`、`--source-type`、`--files`、`--domains`、`--real-device`、`--no-jev`；来源类型必须区分 `USER_VERBATIM`、`PM_INTERPRETATION`、`AGENT_SUGGESTION`、`OPEN_QUESTION`。

```bash
python3 herdr-team/jev_task_depth.py "用户原始表达" \
  --pm-interpretation "PM 解释" --candidate-action "候选动作" \
  --source-type USER_VERBATIM --no-jev
```

输出状态为 `AVAILABLE`、`UNAVAILABLE`、`INVALID_RESPONSE` 或 `INVALID_INPUT`，包含 `input_sha256`/`input_digest`、模型、建议路径、授权/范围分数、硬/建议触发器和确定性覆盖。`prompts/`、关键 `.agent-control` 控制文件、`activate.sh`、`review_dispatch.py`、真机证据、跨领域或结构化高风险变更强制 `DEEP`；`.agent-control/REVIEW_QUEUE.md` 等元数据时间戳变化不触发硬规则。硬触发时 `propose_process_path()` 只能给出 `DEEP`，最终由 PM 通过 `record_pm_process_decision()` 记录选择；Jev 不创建任务、改变 Gate 或授权。

完整字段和 PM 操作顺序见 [`prompts/pm.md`](prompts/pm.md#jev-任务深度观察pm-语义传感器)。

`preflight.sh` 和 `activate.sh` 是 `lfa-team.sh` 调用的内部脚本，不作为日常入口。

<!-- BEGIN HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE OVERVIEW -->

## Requirement Intake

`herdr-team/.agent-control/PM_REQUIREMENT_INTAKE.md` is the single non-executable
register before Requirement Mapping.

```text
User / PM discussion
→ PM Requirement Intake
→ explicit user confirmation
→ Requirement Mapping
→ current Deliverable Exit
→ TASK_BOARD
→ lfa-start Dispatch Gate
→ OMP TODO
```

An Intake is not a Requirement, Task, Gate, Blocker, OMP TODO, or implementation
authorization. `INTAKE_ID` cannot replace `REQUIREMENT_ID` or `TASK_ID`. Execution
sentinel fields may be present for non-regression checks, but must remain null.

Slice 1 Revision 2 does not add a runtime role, seventh pane, Chronicle implementation,
mandatory Intake Reviewer Gate, automatic dispatch, or decision-aid authority.

<!-- END HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE OVERVIEW -->
