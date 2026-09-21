# In-memory Evidence Index

Reducer 每次运行扫描 Envelope 并建立：

```python
dict[evidence_id, canonical_envelope]
```

该 Index 不持久化、不是权威账本、可由文件完全重建。

重复 ID：相同 JCS bytes 去重；不同 JCS bytes 标记 EVIDENCE_ID_CONFLICT，相关 Acceptance 不得 PASS。
