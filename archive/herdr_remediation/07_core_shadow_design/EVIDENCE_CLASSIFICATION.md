# Evidence Classification

- `DISPATCHABLE`: 合法 submission 且状态可派发。
- `NOT_READY`: 合法 submission，但尚不可派发。
- `NOT_SUBMISSION`: 合法 JSON，但不是 submission。
- `MALFORMED`: JSON 或声明的 envelope 非法。
- `UNKNOWN_STATUS`: submission status 不在词表。
- `CONFLICTED`: 身份、绑定或重复冲突。

```text
JSON 可解析？
├─ 否 → MALFORMED
└─ 是
   ├─ 声明为 submission？否 → NOT_SUBMISSION
   └─ 是
      ├─ envelope 合法？否 → MALFORMED
      ├─ status 已知？否 → UNKNOWN_STATUS
      ├─ binding 冲突？是 → CONFLICTED
      ├─ status ready？否 → NOT_READY
      └─ 是 → DISPATCHABLE
```

非 DISPATCHABLE 不得进入评审队列，但必须显示诊断。UNKNOWN_STATUS 不自动降为 NOT_READY。
