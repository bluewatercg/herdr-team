# Workstream Draft

本文件尚未写入正式控制账本，因此不生效。

```yaml
WORKSTREAM: HARNESS-VERIFICATION-SHADOW
MAINLINE_IMPACT:
  slice_0_to_6: NONE
  slice_7: BOUNDED
DESIGN_BASELINE:
  - herdr-team/herdr_remediation/07_core_shadow_design/**
FUTURE_IMPLEMENTATION_SCOPE:
  - herdr-team/harness/**
  - herdr-team/.agent-control/MACHINE/**
FORBIDDEN_WRITE_SCOPE:
  - herdr-team/review_dispatch.py
  - herdr-team/dashboard.py
  - existing accepted evidence
  - product code
```

ZIP 仅为 review package。批准后，将选定设计安装到正式设计路径，ZIP 目录不得成为第二权威。
