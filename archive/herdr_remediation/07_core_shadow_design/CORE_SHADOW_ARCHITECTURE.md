# Core Verification Shadow Architecture

```text
Evidence files
→ classify
→ validate dispatchable envelope
→ resolve integrity and bindings
→ emit immutable events
→ validate acceptance semantics
→ partition by revision and criterion
→ select current generation
→ join concurrent states
→ output versioned projection
```

```yaml
may_advance_legacy_phase: false
may_block_legacy_phase: false
may_write_legacy_ledger: false
may_dispatch_agent: false
may_modify_evidence: false
```

Markdown Adapter 只能输出：

```text
EXACT | PARTIAL | UNAVAILABLE | CONFLICTED
```

默认 UNAVAILABLE，不能产生 PASS。
