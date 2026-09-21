#!/usr/bin/env bash
set -eu

command -v herdr >/dev/null
herdr status >/dev/null 2>&1 || { echo "无法连接当前 Herdr session" >&2; exit 2; }
command -v jq >/dev/null
command -v grok >/dev/null || { echo "缺少 Grok CLI" >&2; exit 2; }
command -v claude >/dev/null || { echo "缺少 Claude CLI" >&2; exit 2; }
herdr --version
jq --version
herdr agent --help >/dev/null
grok --version
claude --version
echo "OK: Herdr agent CLI preflight passed"
