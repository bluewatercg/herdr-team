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

## 文件写入所有权
`FILE_OWNERSHIP.md` 是并发写入控制账本，不是第二套任务状态。PM 为每个任务登记具体 `FILE_SCOPE` 和唯一 `WRITE_OWNER`；`lfa-start` 派单前检查重叠，有冲突就串行或重新切分。一级 Agent 管理本组 pane，只有指定 pane 可写，其他 pane 只读；Review 按实际 diff 检查越界。换 owner 必须先释放原 owner，同一路径禁止两个 `ACTIVE` 写 owner。

## 稳定名称与断线恢复
稳定主角色为 `lfa-start`、`lfa-pm`、`lfa-android`、`lfa-api`、`lfa-ios`、`lfa-review`；辅助交叉评审角色为 `lfa-grok-review`、`lfa-claude-review`。后两者不替代 `lfa-review`，不形成正式 Review Gate，也不写源码或控制账本。Herdr server 保存 pane 和 Agent 进程；`herdr-team/.agent-control/` 保存项目事实。TUI、SSH 或当前 pane 断开后，重新进入 Herdr，在项目目录运行 `./herdr-team/lfa-team.sh` 并选择“恢复 PM 协调”。不要再次启动新一轮覆盖现有状态。

任务派发后，运行入口并选择 `4) 打开 PM 对话窗口` 可直接切换到 `lfa-pm` pane，继续讨论其他项目问题；已派发且无依赖的工作不会因此暂停。

开始新一轮时可为每个角色选择当前项目中已有的空闲 Shell pane；未选择的角色自动创建 workspace。脚本按真实前台进程验证 pane，拒绝当前入口 pane、运行服务的 pane、其他项目 pane、重复分配和已有未命名 Agent。已运行的 `lfa-*` 团队不会被覆盖，使用“恢复 PM 协调”继续。

新一轮的目标、验收和限制已内置当前 DHEA Investor MVP 默认值，三项直接回车即可采用。自定义内容可输入多行，并以单独一行 `.` 结束；pane 输入仅接受列表中的 `w*:p*` ID或空行。

## 自动继续与 watch 恢复
新建团队和“恢复 PM 协调”均调用 `review_dispatch.py ensure-watch`，为当前项目与 Herdr session 保持一个常驻 watch；只有确认进程就绪才返回成功。重复启动复用现有实例，进程退出后重新运行恢复入口即可重建，不终止其他项目或 session 的进程。

当前同一 revision 的独立 Review 与 PM 双 ACCEPTED、证据完整且源文件哈希仍匹配时，现有评审队列持久化通知 `lfa-start`。已确认的通知不会因重复轮询或重启再次发送；总控重新核对授权、依赖与精确文件所有权后继续合格动作，无合格动作则记录具体原因。通知不授予业务、QR G0 或集成权限。

发送中断或结果不明保留 `DELIVERY_UNKNOWN`，不假定成功、不盲目重发。核实实际投递证据后，使用 `python3 herdr-team/review_dispatch.py resolve '<submission-key>' lfa-start SENT '<投递证据>'` 确认已送达，或以 `QUEUED` 和未送达证据允许重试。单 Gate、过期、拒绝、BLOCKED/CONFLICTED 或缺证据不触发继续。专门隔离回归：`python3 herdr-team/review_dispatch.py self-test`；不会向真实业务队列写入验收。

## 模型分工
`lfa-start`、`lfa-pm`、`lfa-review` 使用 `shuaiapi-020/gpt-6-astra`；`lfa-android`、`lfa-api`、`lfa-ios` 使用 `shuaiapi-020/gpt-5.6-sol`。`lfa-grok-review` 使用 Grok CLI 的 `shuai-grok`；`lfa-claude-review` 使用 Claude CLI 的本机默认模型。模型和 kind 记录在 `herdr-team/.agent-control/AGENT_STATUS/`。

OMP 使用 `--auto-approve`，Grok 使用 `--always-approve`，Claude 使用 `--permission-mode auto`。辅助评审角色的 prompt 明确限制为只读第二意见。

Web 面板使用 Python 标准库并仅绑定 `127.0.0.1`，无需安装 Node 或额外依赖。运行日志写入 `.agent-control/dashboard.log`；动态控制账本和日志不纳入静态发行哈希。

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
