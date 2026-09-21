# Artifact-set Digest

复用 MANIFEST.sha256 风格：

1. 路径相对 workspace root 且使用 POSIX 分隔符。
2. 每行 `<lowercase-sha256><two spaces><normalized-path>\n`。
3. 按 normalized path 的 UTF-8 字节序排序。
4. manifest 使用 UTF-8。
5. revision = `sha256:` + SHA-256(manifest bytes)。

不包含 Projection、Acceptance 自身、派生 Dashboard、未显式纳入的运行日志。
