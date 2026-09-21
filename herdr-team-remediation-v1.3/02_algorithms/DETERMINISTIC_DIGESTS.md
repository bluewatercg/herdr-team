# Deterministic Digests

1. Event payload digest：`SHA-256(JCS(payload))`，Event Envelope 不参与该摘要。
2. Evidence duplicate digest：`SHA-256(JCS(envelope))`。
3. Artifact-set revision：按 normalized POSIX path 排序的 `<sha256><two spaces><path>\n` UTF-8 manifest 再 SHA-256。
4. Projection event digest：当前 revision 实际参与 Projection 的 `<event_id><two spaces><payload_digest>\n` 按 event_id UTF-8 排序后 SHA-256。
