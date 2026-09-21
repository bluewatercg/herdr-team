# JCS Event Payload Digest

```text
payload_digest = SHA-256(JCS(payload))
```

Event 保存 canonicalization、digest algorithm 和 digest。JCS 失败时为 `INVALID_PAYLOAD`，禁止回退普通 JSON dump。
