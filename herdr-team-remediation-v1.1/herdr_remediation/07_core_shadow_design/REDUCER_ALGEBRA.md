# Reducer Algebra

## 摄取

```text
同 idempotency_key + 同 SHA-256(JCS(payload)) → DUPLICATE
同 idempotency_key + 不同 digest → IDEMPOTENCY_CONFLICT
```

冲突优先于普通聚合。

## 分区

```text
(task_id, subject_revision, criterion_id)
```

不同 revision 永不直接聚合。

## 修订

只有 `generation` 与 `supersedes_event_id` 可取代旧声明。无显式 supersession 的不同并发声明为 `CONCURRENT_RESULT_CONFLICT`。

## Join

同 revision、criterion、generation 内：

```text
IDEMPOTENCY_CONFLICT > INVALID > STALE > FAIL > UNVERIFIED > PENDING > PASS
```

## 性质

- commutative
- associative
- idempotent
- supersession-preserving
- revision-isolated
- conflict-dominating

禁止 arrival-order fold、last-write-wins、跨 revision global max。
