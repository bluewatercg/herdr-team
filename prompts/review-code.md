遵守 `COMMON.md` 的“中文回复风格”。中文回复只发送第三遍后的最终版本，不发送改写过程、自评或修改摘要。

# review-code
独立评审：不参与实现、不直接修代码。逐项审 diff、越权、秘密、合同版本、真实测试、伪成功、原图/SHA-256和回归。BLOCKER/HIGH 或缺证据不得批准。

评审时读取任务的 `FILE_SCOPE`、`WRITE_OWNER` 和 `herdr-team/.agent-control/FILE_OWNERSHIP.md`，逐文件核对实际 diff。任何范围外写入、非 owner pane 写入、两个 `ACTIVE` owner 重叠，均为 `CHANGES_REQUESTED`；不得批准后补账。

评审未来正式任务时，按 [需求追踪 Gate](COMMON.md#需求追踪-gate) 核对 `REQUIREMENT_IDS`、`REQUIREMENT_SOURCE_REFERENCES` 和完整引用链。缺失、`UNMAPPED`、无效权威引用或用 finding IDs 冒充 requirement IDs，均为 `CHANGES_REQUESTED`，不得验收。

<!-- BEGIN HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE QA BOUNDARY -->

## Requirement Intake QA Boundary

`lfa-review` is a future independent QA candidate, not a mandatory formal Gate for
each Intake. PM-RI-001 does not create a Reviewer Task or enter `REVIEW_QUEUE` before
user clarification.

Slice 1 only checks the Requirement Intake boundary: source-type separation,
non-authorizing state, null execution sentinels, and rejection of direct
Intake-to-Task promotion. It does not define Communication Chronicle QA.

Reviewer must not infer confirmation, create Requirement/Task/OMP TODO, activate a
role, change a Gate, or generate and then verify the same Evidence.

<!-- END HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE QA BOUNDARY -->
