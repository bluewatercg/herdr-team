#!/usr/bin/env bash
set -eu

command -v herdr >/dev/null
herdr status >/dev/null 2>&1 || { echo "无法连接当前 Herdr session" >&2; exit 2; }
command -v jq >/dev/null
herdr --version
jq --version
herdr agent --help >/dev/null
echo "OK: Herdr OMP preflight passed"
