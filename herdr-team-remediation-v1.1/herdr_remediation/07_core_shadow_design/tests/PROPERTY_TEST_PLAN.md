# Property Test Plan

1. Commutative: 输入排列不改变 Projection。
2. Associative: 分批 reduce 后 join 与一次 reduce 一致。
3. Idempotent: 重复注入同事件无变化。
4. Revision isolated: 旧 revision FAIL 不进入新 revision。
5. Supersession preserving: 显式 supersedes 可产生新有效结果。
6. Conflict dominating: 同幂等键异载荷固定冲突。
7. Conservative Markdown: Markdown 永不独立产生 PASS。

场景：QR-ANDROID 未知 status；required=false regression；duplicate/unknown/missing criterion；hash mismatch；stale revision；基础设施 retry 不增加 repair round。
