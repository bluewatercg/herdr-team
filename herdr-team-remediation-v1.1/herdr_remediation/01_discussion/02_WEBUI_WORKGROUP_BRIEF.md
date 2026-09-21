# WebUI 工作组边界 v1.1

当前暂缓全量 WebUI。

Slice 7 仅允许在现有 `dashboard.py` 增加只读 Shadow Verification 区域，并满足：

- 只读取 versioned Projection。
- 不复制 Reducer。
- 不解析 Markdown/终端得 PASS。
- 不判断或推进 Gate。
- 不引入 Node 或组件工具链。
