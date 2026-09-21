# Role Responsibility Matrix v2

> **评审状态：DRAFT**  
> **实施状态：NOT_IMPLEMENTATION_BASELINE**  
> **`implementation_allowed: false`**

本文件用于 `herdr-team/herdr_remediation/` 设计评审，重点关闭以下三类职责问题：

1. 明确 `lfa-core` 的科学计算职责与权限边界；
2. 切断 `lfa-api` 与 Scientific Core 的职责混合；
3. 固定 PM、Orchestrator、各实现 Owner 与 Independent Reviewer 之间的权威边界。

现有执行治理继续遵循：

```text
MASTER_PLAN.md
→ 项目阶段、依赖、下一 Gate、PARKED 范围权威

TASK_BOARD.md
→ 当前可执行任务权威

OMP TODO
→ 单个 Agent 会话执行权威
```

任何正式任务仍必须具备：

```text
PLAN_ID
DELIVERABLE_ID
TASK_ID
REQUIREMENT_IDS
REQUIREMENT_SOURCE_REFERENCES
```

因此，`lfa-core` 必须作为独立角色合同变更接受评审，不得静默加入现有启动链。

---

## 0. 文档元数据

```yaml
document_id: ROLE-RESPONSIBILITY-MATRIX-V2
document_revision: "0.1"
status: DRAFT
implementation_allowed: false

target_repository:
  name: bluewatercg/herdr-team
  branch: main

scope:
  - existing stable role names
  - human-readable display names
  - role responsibility boundaries
  - Requirement Intake ownership
  - Communication Chronicle ownership
  - Scientific Core ownership
  - dispatch and review separation
  - lfa-core role candidate
  - lfa-core / lfa-api / lfa-pm / lfa-review RACI boundaries

non_goals:
  - modify runtime role whitelist
  - modify activate.sh
  - modify config.env
  - create a seventh active pane
  - migrate existing evidence identities
  - modify production Gate or PHASES
  - authorize implementation
```

---

# 1. 决策摘要

```yaml
existing_role_ids:
  action: KEEP

display_names:
  action: UPDATE

responsibility_contracts:
  action: REVISE

new_role:
  role_id: lfa-core
  decision: APPROVE_FOR_DETAILED_DESIGN
  implementation_allowed: false

not_new_roles:
  - lfa-scribe
  - lfa-requirements
  - lfa-data

_deferred_roles:
  - lfa-qa

capabilities:
  requirement_intake:
    owner: lfa-pm

  communication_chronicle:
    owner: lfa-pm
    review_check: lfa-review

  dispatch_and_recovery:
    owner: lfa-start

  scientific_core:
    owner_candidate: lfa-core
```

核心判断：

```text
现有角色名称需要更新展示语义。
PM 与 Orchestrator 的职责边界需要写死。
API 与 Scientific Core 之间存在明确职责空洞。
Requirement Intake 和 Communication Chronicle 是能力，不是新常驻角色。
lfa-core 是当前唯一确认存在的新增角色缺口。
```

---

# 2. 更新后的角色名称

| 稳定 Role ID | 推荐展示名称 | 中文名称 | 状态 |
|---|---|---|---|
| `lfa-start` | LFA Orchestrator | LFA 总控协调器 | 保留 ID，更新展示名 |
| `lfa-pm` | LFA Product & Delivery Manager | LFA 产品与交付经理 | 保留 ID，扩充 Requirement Intake 职责 |
| `lfa-android` | LFA Android Owner | LFA Android 负责人 | 保留 |
| `lfa-api` | LFA API & Gateway Owner | LFA API 与网关负责人 | 保留，收窄至 API/Gateway 边界 |
| `lfa-ios` | LFA iOS Owner | LFA iOS 负责人 | 保留 |
| `lfa-review` | LFA Independent Reviewer | LFA 独立评审员 | 保留，明确独立性 |
| `lfa-core` | LFA Scientific Core Owner | LFA 科学计算 Core 负责人 | 新角色候选 |

现有实现角色的职责基线应保持：

- Android 负责 Kotlin、Gradle、UI、采集、API Client 和测试；不得假设拍摄边缘、光照、角度、距离、裁切或背景稳定。
- API 负责服务、Schema、验证、错误、日志和测试；Schema 必须版本化，并核对 SHA-256。
- iOS 负责 Swift、Xcode、采集、网络和测试；不得以 Linux 或模拟器结果冒充真实 Xcode 或真机验证。
- Reviewer 必须独立评审，不参与实现、不直接修代码，并核对实际 diff、`FILE_SCOPE`、`WRITE_OWNER`、Evidence 和 Requirement Mapping。

---

# 3. `lfa-core` 角色合同

## 3.1 角色身份

```yaml
role_id: lfa-core
display_name: LFA Scientific Core Owner
chinese_name: LFA 科学计算 Core 负责人

role_class:
  - IMPLEMENTATION_OWNER
  - SCIENTIFIC_MEASUREMENT_OWNER
  - CORE_CONTRACT_OWNER

authority:
  requirement_authority: false
  product_scope_authority: false
  dispatch_authority: false
  pm_acceptance_authority: false
  independent_review_authority: false

  scientific_algorithm_implementation_authority: true
  core_contract_proposal_authority: true
  scientific_evidence_production_authority: true
```

## 3.2 核心使命

`lfa-core` 负责将完整原始图像和版本化产品合同转换为可验证、可诊断、可追溯的科学测量结果。

`lfa-core` 对以下内容负责：

- 图像可测量性；
- 正式 ROI；
- C/T 信号提取；
- T/C 比值；
- DHEA 4PL 反演；
- 科学拒绝原因；
- 算法版本；
- 质量策略版本；
- 科学 Evidence 与诊断 Artifact。

`lfa-core` 不拥有：

- 用户需求解释权；
- 产品范围决定权；
- Requirement 创建权；
- 任务派发权；
- 外部 Gateway 权限；
- 自身实现的独立验收权；
- PM Acceptance 权限。

---

# 4. `lfa-core` In Scope

## 4.1 输入完整性与图像解码

`lfa-core` 负责：

- 完整原始 JPEG 解码；
- 输入像素维度检查；
- 颜色通道检查；
- 输入图像 SHA-256 引用核对；
- Core 输入 Schema 版本检查；
- 产品、试纸和算法配置引用检查。

边界：

```text
Core 可以拒绝不可解码或不满足输入合同的图像。
Core 不负责网络上传重试。
Core 不负责 App 相机 API。
Core 不负责 Gateway 身份认证。
```

## 4.2 正式定位与测量 ROI

`lfa-core` 负责：

- 消费试纸方向证据；
- 观察窗口定位；
- 正式测量 ROI 生成；
- ROI 完整性检查；
- ROI 越界和裁切检查；
- ROI 映射诊断 Artifact。

关键约束：

```text
二维码可作为产品识别、协议验证、方向证据和粗搜索指导。
二维码不得默认充当精确几何锚点。
不能假设用户图像边缘、角度、距离、裁切或背景天然稳定。
```

## 4.3 图像可测量性判定

候选检查维度包括：

- 正式 ROI 清晰度；
- Laplacian 或梯度候选指标；
- 运动模糊候选指标；
- 局部过曝和饱和；
- 局部反光；
- C/T 区域边缘宽度；
- Green profile 明确性；
- C 线是否可以可靠测量；
- T 区是否有资格进入定量。

权威边界：

```yaml
app_preview_guidance:
  authority: advisory_only

core_measurement_eligibility:
  authority: authoritative
```

如果 Core 判定图像不可测：

```yaml
tc_ratio: null
concentration: null
```

禁止：

```yaml
tc_ratio: 0
concentration: 0
```

## 4.4 C/T 信号和定量计算

`lfa-core` 负责：

- Green channel 或已批准通道的提取；
- 一维 profile 生成；
- 局部背景估计；
- C/T 候选线定位；
- 线区域积分或批准的信号统计；
- C signal；
- T signal；
- T/C ratio；
- 结果稳定性和可重复性诊断。

必须区分：

```text
研究候选指标
实现基线指标
生产批准指标
```

任何未验证的 Magic Wand、颜色候选、自适应阈值、边缘候选或新 profile 定义，必须标记：

```text
RESEARCH_CANDIDATE
UNVALIDATED
NOT_IMPLEMENTATION_BASELINE
```

## 4.5 DHEA 4PL 与浓度反演

当前实验分析物为 **DHEA**；皮质醇属于后续阶段。

`lfa-core` 负责：

- 读取版本化 DHEA 4PL 参数；
- T/C 到浓度反演；
- 适用范围检查；
- 超出曲线范围处理；
- 数值异常检查；
- 单位输出；
- Curve version 记录。

`lfa-core` 不得：

- 在无批准曲线时生成浓度；
- 用默认曲线替代缺失配置；
- 把失败结果补成 `0`；
- 静默外推到未经验证范围；
- 把 DHEA 配置替换为皮质醇配置。

## 4.6 科学策略与版本化

`lfa-core` 是以下机器合同的技术 Owner：

```text
Core image input contract
Core measurement eligibility output
Core diagnostic metrics
T/C result contract
4PL input and result contract
Image quality policy
Algorithm version
Curve version
```

技术 Owner 不等于可单方面批准。

冻结流程：

```text
lfa-core
→ 提出合同和策略候选

lfa-api
→ 评估传输和外部 Schema 兼容

lfa-android / lfa-ios
→ 评估客户端消费兼容

lfa-pm
→ 核对产品语义、Requirement 和交付范围

lfa-review
→ 独立评审

PM Gate
→ 最终允许实施或发布
```

## 4.7 Core Evidence 和诊断 Artifact

每个重要处理阶段应输出可追溯诊断：

- 输入图像引用；
- 图像 SHA-256；
- 方向诊断；
- ROI Overlay；
- C 区 Overlay；
- T 区 Overlay；
- Green profile；
- 候选线位置；
- 背景估计；
- 质量指标；
- 拒绝原因；
- 算法版本；
- 策略版本；
- 曲线版本；
- 结果 JSON。

失败也必须输出：

- 失败阶段；
- 明确 reason code；
- 可用的诊断 Artifact；
- `subject_revision`；
- 输入 Evidence 引用。

禁止：

```text
只有最终 PASS/FAIL
无失败原因
无 ROI 可视证据
无版本信息
无原图绑定
```

---

# 5. `lfa-core` Out of Scope

## 5.1 不负责 App

```text
Android CameraX 或相机生命周期
Android UI
预览引导动画
Android 权限
APK 构建
iOS AVFoundation
客户端网络重试
客户端结果渲染
```

App 的预览指标可以由 Android/iOS 计算，但只用于指导，不得替代 Core 最终裁决。

## 5.2 不负责外部 API Gateway

```text
HTTP 路由
认证授权
上传会话
网络重试
API Rate Limit
外部请求日志策略
客户端兼容层
```

以上职责归 `lfa-api`。

## 5.3 不负责产品需求和优先级

```text
不决定现在是否支持多设备
不决定 Investor MVP 范围
不决定用户体验文案
不决定是否锁快门
不决定需求是否进入当前主线
不创建权威 Requirement ID
```

以上职责归 `lfa-pm` 和正式 Requirement Mapping。

## 5.4 不负责派发

```text
不创建 OMP TODO
不启动其他 Agent
不调整其他角色 Owner
不修改任务范围
不绕过 lfa-start
```

## 5.5 不负责独立批准自身实现

```text
lfa-core 不能 Review 自己。
lfa-core 不能为自己的 Evidence 给出独立 PASS。
lfa-core 不能代替 PM Acceptance。
```

独立评审归 `lfa-review`。

---

# 6. `lfa-core` 必须遵守的失败语义

```yaml
decode_failed:
  result_status: REJECTED
  tc_ratio: null
  concentration: null

roi_unavailable:
  result_status: REJECTED
  tc_ratio: null
  concentration: null

c_line_unmeasurable:
  result_status: REJECTED
  tc_ratio: null
  concentration: null

quality_unverified:
  result_status: UNVERIFIED
  tc_ratio: null
  concentration: null

measurement_passed:
  result_status: PASS
  tc_ratio: number
  concentration:
    value: number
    analyte: DHEA
    unit: versioned_unit
```

建议的最小 reason code：

```text
CORE_IMAGE_DECODE_FAILED
CORE_IMAGE_INTEGRITY_MISMATCH
CORE_OBSERVATION_ROI_NOT_FOUND
CORE_OBSERVATION_ROI_INCOMPLETE
CORE_ORIENTATION_UNRESOLVED
CORE_IMAGE_BLUR_EXCESSIVE
CORE_MOTION_BLUR_DETECTED
CORE_ROI_OVEREXPOSED
CORE_SPECULAR_GLARE_INTERFERENCE
CORE_C_LINE_NOT_FOUND
CORE_C_LINE_UNMEASURABLE
CORE_C_LINE_AMBIGUOUS
CORE_T_ZONE_UNMEASURABLE
CORE_GREEN_PROFILE_AMBIGUOUS
CORE_MEASURABILITY_UNVERIFIED
CORE_CURVE_VERSION_UNAVAILABLE
CORE_RESULT_OUT_OF_VALIDATED_RANGE
```

---

# 7. RACI 定义

| 缩写 | 含义 |
|---|---|
| `A` | Accountable，最终责任 |
| `R` | Responsible，直接执行 |
| `C` | Consulted，必须协商 |
| `V` | Independent Verifier，独立验证 |
| `I` | Informed，知会 |
| `-` | 无职责 |

附加规则：

1. 每个工作项原则上只能有一个 `A`；
2. `A` 不等于可以绕过 Requirement、Review 或 Gate；
3. `V` 必须独立于 `R`；
4. 同一角色不能在同一交付 revision 上同时是 `R` 和 `V`；
5. PM Acceptance 与 Independent Review 是两个不同 Gate；
6. 科学技术权威不等于产品范围权威；
7. 外部 API Schema 权威不等于科学结果权威。

---

# 8. 完整 Role Responsibility Matrix v2

| 工作项 | Orchestrator | PM | Android | API/Gateway | Scientific Core | iOS | Reviewer |
|---|---:|---:|---:|---:|---:|---:|---:|
| 用户需求澄清 | I | A/R | C | C | C | C | - |
| Requirement Intake | I | A/R | C | C | C | C | V |
| Communication Chronicle 来源归档 | I | A/R | - | - | - | - | V |
| Requirement ID 和 Mapping | V | A/R | I | I | I | I | V |
| MASTER_PLAN / Deliverable / Exit | I | A/R | C | C | C | C | V |
| 可验收任务定义 | V | A/R | C | C | C | C | V |
| PM Gate 输入 | V | A/R | I | I | I | I | V |
| Dispatch Gate | A/R | C | I | I | I | I | I |
| WIP 和并发协调 | A/R | C | I | I | I | I | I |
| FILE_SCOPE 定义 | V | A | C | C | C | C | V |
| WRITE_OWNER 登记 | V | A/R | I | I | I | I | V |
| 写入范围冲突检查 | A/R | C | I | I | I | I | V |
| Android Camera Preview | I | C | A/R | C | C | - | V |
| Android 原始 JPEG Capture | I | C | A/R | C | C | - | V |
| iOS Capture | I | C | - | C | C | A/R | V |
| API 上传与传输完整性 | I | C | C | A/R | C | C | V |
| 外部 API Schema | I | C | C | A/R | C | C | V |
| Core 输入 Schema | I | C | C | C | A/R | C | V |
| JPEG 解码 | I | I | - | C | A/R | - | V |
| 正式 ROI 定位 | I | C | C | - | A/R | C | V |
| 图像可测量性判定 | I | C | C | C | A/R | C | V |
| C/T 线检测 | I | I | - | - | A/R | - | V |
| T/C 计算 | I | I | - | - | A/R | - | V |
| DHEA 4PL 反演 | I | C | - | C | A/R | - | V |
| Threshold 实验设计 | I | A | C | C | R | C | V |
| Threshold 候选实现 | I | C | - | - | A/R | - | V |
| Threshold 正式冻结 | I | A | C | C | R | C | V |
| Core 诊断 Artifact | I | I | - | C | A/R | - | V |
| 错误码定义 | I | A | C | R | R | C | V |
| `null` 结果生成 | I | I | - | C | A/R | - | V |
| `null` 传输保真 | I | C | C | A/R | C | C | V |
| Android 真机测试 | I | C | A/R | C | C | - | V |
| iOS 真机测试 | I | C | - | C | C | A/R | V |
| Core 科学测试 | I | C | - | C | A/R | - | V |
| 回归范围批准 | I | A | C | C | C | C | V |
| 独立代码 Review | I | I | - | - | - | - | A/R |
| 独立 Evidence Review | I | C | - | - | - | - | A/R |
| PM Acceptance | I | A/R | I | I | I | I | V |
| Agent 恢复协调 | A/R | C | I | I | I | I | I |
| 正式 Gate 切换 | V | A | C | C | C | C | V |

---

# 9. 四类权威的唯一归属

## 9.1 产品与需求权威

```yaml
authority: PRODUCT_AND_REQUIREMENT
accountable: lfa-pm
```

`lfa-pm` 负责：

- 用户问题定义；
- 当前是否需要解决；
- 是否属于当前 Investor MVP；
- Requirement ID 与来源；
- Requirement Mapping；
- Deliverable 与 Exit；
- Acceptance Criteria；
- 必须提交的 Evidence 类别；
- 优先级与 PARKED 处理；
- PM Acceptance。

`lfa-core`、`lfa-api` 和 `lfa-review` 可以提出缺口或变更建议，但不能自行扩大用户需求、当前范围或 Delivery Gate。

## 9.2 科学测量权威

```yaml
authority: SCIENTIFIC_MEASUREMENT
accountable: lfa-core
```

`lfa-core` 对以下技术输出负责：

- 完整 JPEG 解码；
- 正式 ROI；
- 图像可测量性；
- C 线测量资格；
- T 区测量资格；
- Green profile；
- C/T 信号；
- T/C ratio；
- DHEA 4PL 反演；
- 科学拒绝码来源；
- 算法版本；
- 质量策略版本；
- 曲线版本；
- 科学诊断 Artifact。

`lfa-core` 只能在已批准 Requirement、合同和策略范围内拥有技术权威，不能凭算法便利性改变产品需求。

## 9.3 接口与传输权威

```yaml
authority: API_AND_GATEWAY
accountable: lfa-api
```

`lfa-api` 负责：

- 外部 API Schema；
- 请求与响应结构；
- 原始 JPEG 传输完整性；
- 上传和会话协议；
- SHA-256 传输校验；
- Core 调用适配；
- Error/Reason Code 透传；
- `null` 保真；
- 服务日志；
- 接口兼容；
- API 测试。

`lfa-api` 不得重新解释 `lfa-core` 的科学结果。

## 9.4 独立验证权威

```yaml
authority: INDEPENDENT_VERIFICATION
accountable: lfa-review
```

`lfa-review` 独立验证：

- 实现是否符合 Requirement；
- 科学实现是否符合批准基线；
- Schema 是否一致；
- Evidence 是否真实；
- 原始 JPEG 与结果是否绑定；
- SHA-256 是否匹配；
- 拒绝链是否保持 `null`；
- 是否存在伪 PASS；
- 是否越出 `FILE_SCOPE`；
- 是否违反 `WRITE_OWNER`；
- 回归是否满足任务要求；
- Requirement Source 是否完整。

---

# 10. `lfa-core`、PM、API、Reviewer 精简 RACI

| 工作项 | `lfa-pm` | `lfa-core` | `lfa-api` | `lfa-review` |
|---|---:|---:|---:|---:|
| 用户需求澄清 | A/R | C | C | I |
| Requirement Intake | A/R | C | C | V |
| Requirement ID 与来源映射 | A/R | I | I | V |
| Investor MVP 范围 | A/R | C | C | V |
| Deliverable 与 Exit | A/R | C | C | V |
| Acceptance Criteria | A | C/R | C/R | V |
| Evidence 要求 | A | C/R | C/R | V |
| Core 技术设计 | C | A/R | C | V |
| 外部 API 技术设计 | C | C | A/R | V |
| API 与 Core 边界设计 | A | R | R | V |
| Core 输入 Schema | C | A/R | C | V |
| Core 输出 Schema | C | A/R | C | V |
| 外部 API 请求 Schema | C | C | A/R | V |
| 外部 API 响应 Schema | C | C | A/R | V |
| Error/Reason Code 分类 | A | R | R | V |
| JPEG 传输完整性 | I | C | A/R | V |
| JPEG 内容解码 | I | A/R | C | V |
| 正式 ROI | C | A/R | I | V |
| 图像可测量性判定 | C | A/R | C | V |
| C/T 检测 | I | A/R | I | V |
| T/C 计算 | I | A/R | I | V |
| DHEA 4PL 反演 | C | A/R | C | V |
| 图像质量指标研究 | A | R | C | V |
| 阈值候选提出 | C | A/R | I | V |
| 阈值正式冻结 | A | R | C | V |
| 算法版本管理 | C | A/R | I | V |
| API 版本管理 | C | C | A/R | V |
| Curve 版本管理 | A | R | C | V |
| Core 诊断 Artifact | I | A/R | C | V |
| API 日志与审计字段 | C | C | A/R | V |
| `null` 结果生成 | I | A/R | C | V |
| `null` 传输保真 | I | C | A/R | V |
| Core 单元测试 | I | A/R | C | V |
| API 单元与集成测试 | I | C | A/R | V |
| App/API/Core E2E 测试定义 | A | R | R | V |
| 独立代码评审 | I | I | I | A/R |
| 独立 Evidence 评审 | C | I | I | A/R |
| PM Acceptance | A/R | I | I | V |
| 正式 Gate 变更建议 | A | C | C | V |
| 生产发布授权 | A | C | C | V |

---

# 11. 关键边界

## 11.1 PM 与 `lfa-core`

PM 决定：

- 要解决什么用户问题；
- 是否属于当前范围；
- 怎样算产品层完成；
- 需要哪些 Evidence；
- 何时进入实现基线。

Core 决定：

- 在批准合同内如何实现科学计算；
- 某张图是否满足已批准的可测量性规则；
- 如何产生诊断指标和科学 Evidence。

禁止：

```text
Core 不得把“算法方便”改写为“产品需求”。
PM 不得在没有 Core Evidence 时凭经验冻结科学阈值。
```

## 11.2 `lfa-api` 与 `lfa-core`

```text
lfa-api 负责“可靠地传什么”。
lfa-core 负责“科学地算什么，以及能不能算”。
```

API owns：

- 外部 API；
- 上传协议；
- Schema transport；
- SHA-256 transport validation；
- Error/Reason Code 透传；
- `null` 保真；
- 日志和 Gateway。

Core owns：

- 图像解码；
- 正式 ROI；
- 测量资格；
- C/T；
- T/C；
- 4PL；
- 科学 reason code 来源。

接口原则：

```text
Core 生成科学结论和科学 reason code。
API 按合同传输，不重新解释。
```

绝对禁止：

```text
API 对 Core REJECTED 改成 SUCCESS。
API 对 null 改成 0。
API 自行计算浓度。
Core 自行实现外部 HTTP Gateway。
```

## 11.3 Android 与 `lfa-core`

Android 负责：

- 预览指导；
- 完整 JPEG Capture；
- 上传；
- 客户端诊断；
- 结果展示。

Core 负责：

- 最终测量资格；
- 正式 ROI；
- C/T 与浓度。

冻结句：

> Android 的 `READY_FOR_CAPTURE` 只表示适合尝试拍摄，不保证 Core 接受。Core 对完整原始 JPEG 的正式 ROI 和 C 线可测量性拥有最终裁决权。

## 11.4 Reviewer 与 `lfa-core`

Reviewer 检查：

- Core 是否符合 Requirement；
- 算法是否与批准基线一致；
- 输入输出 Schema 是否一致；
- 拒绝链是否保持 `null`；
- Evidence 是否绑定原始 JPEG；
- 测试是否真实；
- 诊断 Artifact 是否可复核；
- 是否存在伪 PASS；
- 是否越出 `FILE_SCOPE`。

Reviewer 不负责：

- 替 Core 修算法；
- 替 Core 选择阈值；
- 替 PM 决定产品范围。

---

# 12. 科学阈值的联合责任

| 阶段 | PM | Core | API | Reviewer |
|---|---:|---:|---:|---:|
| 定义实验要回答的产品问题 | A/R | C | I | V |
| 定义候选指标 | C | A/R | I | V |
| 设计指标采集输出 | C | A/R | C | V |
| 实施实验计算 | I | A/R | I | V |
| 形成阈值候选 | C | A/R | I | V |
| 检查外部合同影响 | A | C | R | V |
| 阈值 Evidence Review | C | I | I | A/R |
| 批准为实现基线 | A/R | C | C | V |

关键规则：

```text
Core 可以证明候选阈值。
Reviewer 可以独立判断 Evidence 是否充分。
PM 决定候选是否满足当前产品和交付 Gate。
任何一方都不能单独完成全链批准。
```

---

# 13. Core Review Submission 最小包

```yaml
CORE_REVIEW_SUBMISSION:
  task_id:
  subject_revision:

  requirement_ids: []
  requirement_source_references: []

  applicable_contract_versions:
    core_input:
    core_output:
    quality_policy:
    algorithm:
    curve:

  file_scope: []
  write_owner:

  implementation_files: []

  tests:
    unit: []
    integration: []
    fixture: []
    regression: []

  evidence:
    input_image_refs: []
    input_sha256: []
    roi_overlays: []
    profiles: []
    metrics: []
    result_json: []
    rejection_examples: []

  known_limitations: []
```

Requirement Mapping 缺失、为 `UNMAPPED` 或使用无效权威引用时，必须返回：

```text
CHANGES_REQUESTED
```

## Reviewer 必须检查

- Requirement 和 Core 行为是否一致；
- 变更是否在 `FILE_SCOPE` 内；
- 实际写入者是否为 `WRITE_OWNER`；
- 算法版本是否明确；
- 策略版本是否明确；
- 曲线版本是否明确；
- 原始 JPEG SHA-256 是否可核对；
- ROI Overlay 是否对应原图；
- 指标与拒绝码是否一致；
- 失败是否保持 T/C 和浓度为 `null`；
- PASS 是否有充分 Evidence；
- 测试是否真实执行；
- 回归是否覆盖受影响路径；
- 是否存在硬编码伪成功；
- 是否将研究候选写入生产路径。

## Reviewer 禁止行为

- 不得直接修改 Core 代码；
- 不得替 Core 补测试；
- 不得替 Core 生成 Evidence；
- 不得替 Core 选择阈值；
- 不得要求实现者接受未经 Requirement 支持的新范围；
- 不得把个人技术偏好当成 `CHANGES_REQUESTED`；
- 不得执行 PM Acceptance。

## Core 对 Review Finding 的处理

```text
BLOCKER/HIGH
→ 必须进入修复或明确拒绝该 revision

MEDIUM/LOW
→ PM 判断是否属于当前 Deliverable

Requirement Change
→ 返回 PM，不得由 Core 与 Reviewer 私下扩大范围

Contract Ambiguity
→ API、Core、PM 联合关闭，Reviewer 保持独立验证
```

Core 不得通过修改 Review 文本或补一段说明绕过真实代码和 Evidence 修复。

---

# 14. 合同所有权矩阵

| 合同 | Accountable | Responsible | Consulted | Independent Verifier |
|---|---|---|---|---|
| Requirement Contract | PM | PM | Core、API | Reviewer |
| Capture Contract | PM | Android/iOS | API、Core | Reviewer |
| External Upload API | API | API | Android/iOS、Core、PM | Reviewer |
| Core Input Contract | Core | Core | API、PM | Reviewer |
| Measurement Eligibility Contract | Core | Core | PM、API | Reviewer |
| T/C Result Contract | Core | Core | API、PM | Reviewer |
| DHEA Concentration Contract | Core | Core | PM、API | Reviewer |
| External Result API | API | API | Core、PM、客户端 | Reviewer |
| Error Code Taxonomy | PM | API、Core | 客户端 | Reviewer |
| Image Quality Policy | PM | Core | API、客户端 | Reviewer |
| Diagnostic Artifact Contract | Core | Core | API、PM | Reviewer |
| Acceptance Contract | PM | PM | Core、API | Reviewer |
| Review Evidence Requirements | PM | PM | Core、API | Reviewer |
| Review Evidence Sufficiency Decision | Reviewer | Reviewer | PM | Reviewer |

说明：

- PM 确保任务定义中写清需要哪些 Evidence；
- Core 和 API 负责产生自身范围内的 Evidence；
- Reviewer 对实际 Evidence 是否充分拥有独立判断权；
- Reviewer 不能参与产生被评审 Evidence。

---

# 15. 变更请求路由规则

## 15.1 Core 发现产品需求不完整

```text
Core
→ TECHNICAL_REQUIREMENT_GAP
→ PM Requirement Intake
→ 用户或 PM 决策
```

Core 不得自行补全。

## 15.2 API 发现 Core Schema 不可传输

```text
API
→ CONTRACT_COMPATIBILITY_FINDING
→ Core + PM 协商
→ Reviewer 独立验证最终 revision
```

API 不得静默删字段。

## 15.3 Reviewer 发现科学 Evidence 不足

```text
Reviewer
→ CHANGES_REQUESTED
→ Core 修订实现或 Evidence
→ 新 subject revision
→ 重新独立 Review
```

Reviewer 不得直接修代码。

## 15.4 PM 发现实现不符合用户意图

```text
PM
→ PM_REJECTED
→ 返回 Requirement、Acceptance 或 Scope 修订
```

如果 Requirement 改变：

```text
产生新 Requirement revision
旧实现不得直接补账接受
```

---

# 16. 禁止的职责组合

以下组合必须视为治理违规：

```yaml
- role: lfa-core
  prohibited_combination:
    - 实现算法
    - 独立批准算法

- role: lfa-api
  prohibited_combination:
    - 修改 Core scientific result
    - 对外声明科学结果未改变

- role: lfa-pm
  prohibited_combination:
    - 凭经验冻结阈值
    - 跳过 Evidence Review

- role: lfa-review
  prohibited_combination:
    - 直接修改 Core 代码
    - 审批修改后的同一 revision

- role: lfa-core
  prohibited_combination:
    - 创建 Requirement
    - 实现 Requirement

- role: lfa-api
  prohibited_combination:
    - 将 null 替换为 0
    - 返回 SUCCESS

- role: lfa-pm
  prohibited_combination:
    - 把研究候选直接写入当前实现任务
    - 跳过 Requirement Mapping
```

---

# 17. Gate 定义

## 17.1 API/Core Contract Gate

```yaml
gate: API_CORE_CONTRACT_GATE

required:
  - versioned Core input schema
  - versioned Core output schema
  - null preservation rule
  - reason-code ownership
  - SHA-256 reference behavior
  - compatibility fixtures

accountable: lfa-pm
responsible:
  - lfa-api
  - lfa-core
verifier: lfa-review
```

## 17.2 Scientific Evidence Gate

```yaml
gate: CORE_SCIENTIFIC_EVIDENCE_GATE

required:
  - input image references
  - source SHA-256
  - ROI overlay
  - diagnostic metrics
  - result or rejection JSON
  - algorithm version
  - policy version
  - regression evidence

accountable: lfa-pm
responsible: lfa-core
verifier: lfa-review
```

## 17.3 External Result Integrity Gate

```yaml
gate: RESULT_INTEGRITY_GATE

required:
  - Core result preserved by API
  - null preserved
  - reason codes preserved
  - policy and algorithm versions preserved
  - no synthetic success
  - no zero substitution

accountable: lfa-api
consulted:
  - lfa-core
  - lfa-pm
verifier: lfa-review
```

---

# 18. 是否缺少其他新角色

## 18.1 `lfa-scribe`

```yaml
decision: NOT_NEEDED_NOW
```

理由：

- Communication Chronicle 是 PM 的来源归档能力；
- 不需要新的权力中心；
- 不应产生第七个常驻记录 Agent。

## 18.2 `lfa-requirements`

```yaml
decision: NOT_NEEDED
```

理由：

- Requirement Intake、Mapping、范围和 Acceptance 是 PM 核心职责；
- 新增角色会造成需求解释权重复。

## 18.3 `lfa-qa`

```yaml
decision: DEFER
```

当前由实现 Owner 负责测试执行，Reviewer 负责独立验证。只有未来出现独立测试环境、设备矩阵和专职测试执行需求时，再评估。

## 18.4 `lfa-data`

```yaml
decision: NOT_NEEDED_NOW
```

当前实验数据、指标分析和阈值 Evidence 可由 `lfa-core` 在受限任务范围内负责。

## 18.5 `lfa-core`

```yaml
decision: ROLE_GAP_CONFIRMED
recommendation: ADD_AFTER_CONTRACT_REVIEW
```

`lfa-core` 是当前唯一明确的新角色缺口。

---

# 19. `lfa-core` 启用前 Gate

```text
G0  Role Responsibility Matrix v2 批准
G1  lfa-core Prompt 冻结
G2  lfa-api 与 lfa-core 接口边界冻结
G3  Android/API/Core Schema Owner 冻结
G4  FILE_SCOPE 范围冻结
G5  稳定 Role ID 和恢复语义冻结
G6  activate.sh 与 config.env 变更独立 Review
G7  Dashboard display mapping 更新
G8  历史任务和 Evidence 兼容策略确认
G9  Reviewer 独立评审
G10 PM 批准角色启用
```

在 Gate 完成前：

```yaml
lfa_core:
  role_status: DESIGN_CANDIDATE
  implementation_allowed: false
  stable_agent_start_allowed: false
```

---

# 20. 推荐文件变更

## 第一批：仅设计文档

```text
herdr-team/herdr_remediation/role-model-v2/
  ROLE_RESPONSIBILITY_MATRIX_V2.md
  LFA_CORE_ROLE_SPEC.md
  ROLE_OVERLAP_REVIEW.md
  DECISION-ROLE-MODEL-V2.yaml
```

## 第二批：批准后更新 Prompt

```text
prompts/start.md
prompts/pm.md
prompts/app-apk.md
prompts/api.md
prompts/app-ios.md
prompts/review-code.md
prompts/core.md
README.md
```

## 第三批：单独启用角色

```text
activate.sh
config.env
dashboard.py
AGENT_STATUS handling
role recovery rules
SHA256SUMS.txt
```

三批不得合并为一次修改。

---

# 21. Prompt 可直接采用的冻结文本

## 21.1 `lfa-core`

> `lfa-core` 是科学计算 Core 的实现和技术合同 Owner。`lfa-core` 负责完整 JPEG 解码、正式 ROI、图像可测量性、C/T 信号、T/C、DHEA 4PL、科学拒绝码、算法版本和诊断 Evidence。`lfa-core` 不负责外部 Gateway、客户端实现、产品范围、Requirement 创建、任务派发、独立 Review 或 PM Acceptance。不可测量、拒绝或未验证时，T/C 与浓度必须为 `null`，不得补 `0`。

## 21.2 `lfa-api`

> `lfa-api` 是 API 与 Gateway 的实现和外部合同 Owner。`lfa-api` 负责上传协议、外部 Schema、传输校验、SHA-256、Core 调用适配、错误透传、日志和 `null` 保真。`lfa-api` 不得重新解释科学结果、计算 T/C 或浓度、选择科学阈值、将 Core 拒绝转换为成功，或用 `0` 替代 `null`。

## 21.3 `lfa-pm`

> `lfa-pm` 对用户需求、范围、Requirement Mapping、Deliverable、Acceptance、Evidence 要求和 PM Acceptance 负责。`lfa-pm` 不得凭经验冻结科学阈值，不得要求 Core 为不可测图像生成数值，不得将研究候选直接视为实现基线。科学策略必须由 Core 提供 Evidence，经独立 Reviewer 验证后，再由 PM 判断是否满足当前交付 Gate。

## 21.4 `lfa-review`

> `lfa-review` 对 Core/API 变更执行独立验证，不参与实现、不直接修代码。`lfa-review` 核对 Requirement Mapping、合同版本、`FILE_SCOPE`、`WRITE_OWNER`、实际 diff、真实测试、原图与 SHA-256、诊断 Artifact、`null` 拒绝链和回归。缺少 Evidence、存在伪 PASS、越权写入或 Requirement 引用无效时，必须返回 `CHANGES_REQUESTED`。

---

# 22. Decision 草案

```yaml
decision_id: DECISION-ROLE-MODEL-V2
decision_revision: "1"
status: DRAFT
scope: ROLE_GOVERNANCE

accepted:
  - keep existing stable role IDs
  - adopt role display names
  - define lfa-start as LFA Orchestrator
  - define lfa-pm as LFA Product & Delivery Manager
  - keep Requirement Intake under lfa-pm
  - keep Communication Chronicle as a capability
  - narrow lfa-api to API and Gateway
  - preserve independent reviewer authority

modified:
  - item: Scientific Core ownership
    from: implicit or mixed with API
    to: dedicated lfa-core candidate

new_role_candidates:
  - role_id: lfa-core
    display_name: LFA Scientific Core Owner
    status: APPROVED_FOR_DETAILED_DESIGN
    implementation_allowed: false

rejected_new_roles:
  - lfa-scribe
  - lfa-requirements
  - lfa-data

deferred_new_roles:
  - lfa-qa

implementation_allowed: false

required_gates:
  - ROLE_RESPONSIBILITY_REVIEW
  - API_CORE_BOUNDARY_REVIEW
  - CORE_PROMPT_REVIEW
  - ACTIVATION_COMPATIBILITY_REVIEW
  - RECOVERY_COMPATIBILITY_REVIEW
  - FILE_SCOPE_REVIEW
  - INDEPENDENT_REVIEW
  - PM_ACCEPTANCE

open_questions:
  - exact lfa-core stable pane and recovery identity
  - temporary ownership of current Core tasks before activation
  - Core contract source-of-truth location
  - migration of existing API-owned Core references
```

---

# 23. 决策总结

```yaml
role_model_v2:
  existing_roles: KEEP_WITH_REVISED_DISPLAY_NAMES
  responsibility_overlap: REQUIRES_BOUNDARY_UPDATE

confirmed_missing_role:
  role_id: lfa-core
  name: LFA Scientific Core Owner
  action: ADD_AFTER_GATES

new_capabilities_without_new_roles:
  requirement_intake: lfa-pm
  communication_chronicle: lfa-pm
  dispatch_recovery_gate: lfa-start

not_needed_now:
  - lfa-scribe
  - lfa-requirements
  - lfa-data

deferred:
  - lfa-qa

core_pm_boundary:
  pm_owns:
    - user intent
    - scope
    - requirement
    - acceptance
    - delivery gate
  core_owns:
    - scientific implementation
    - measurement eligibility
    - diagnostic evidence

core_api_boundary:
  api_owns:
    - transport
    - external schema
    - gateway
    - null preservation
  core_owns:
    - scientific result
    - scientific reason codes
    - measurement contracts

core_reviewer_boundary:
  core_owns:
    - implementation
    - tests
    - evidence production
  reviewer_owns:
    - independent verification
    - changes requested
    - review acceptance

non_negotiable:
  - Core cannot approve itself
  - API cannot reinterpret Core
  - PM cannot invent scientific thresholds
  - Reviewer cannot repair implementation
  - rejected or unverified results keep T/C and concentration null
```

---

# 24. 核心冻结句

> **`lfa-core` 对版本化科学计算链负责，包括完整 JPEG 解码、正式 ROI、图像可测量性、C/T 信号、T/C、DHEA 4PL、科学拒绝码和诊断 Evidence。`lfa-core` 不定义产品需求、不控制派发、不承担外部 Gateway、不修改客户端、不批准自身实现。所有 Core 工作仍必须经过 Requirement Mapping、任务派发 Gate、独立 Review 和 PM Acceptance。**

---

# 25. 本版本主要改进

- **职责唯一化**：产品、科学、接口和独立验证分别设置唯一权威；
- **结果完整性**：Core 产生科学结论，API 只能保真传输；
- **科学治理**：阈值由 Core 提证，Reviewer 独立验证，PM 作交付批准；
- **审查独立性**：禁止 Core 自批、Reviewer 直接修复、PM 以经验替代 Evidence；
- **失败语义**：拒绝和未验证状态下，`T/C = null`、`concentration = null`；
- **新增角色控制**：`lfa-core` 仅批准进入详细设计，不批准启动或实现；
- **能力与角色分离**：Requirement Intake、Communication Chronicle 不新增独立常驻角色。
