#!/usr/bin/env bash
set -eu

KIT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$KIT_DIR")
CONTROL_DIR="$KIT_DIR/.agent-control"
cd "$KIT_DIR"
herdr status >/dev/null 2>&1 || { echo "无法连接当前 Herdr session" >&2; exit 2; }
command -v jq >/dev/null
. "$KIT_DIR/config.env"

G=${1:-}
BRIEF=${2:-}
ASSIGNMENTS=${3:-}
[ -n "$G" ] || { printf "请输入本轮目标: "; IFS= read -r G; }
[ -n "$G" ]
[ -z "$BRIEF" ] || [ -f "$BRIEF" ]
[ -z "$ASSIGNMENTS" ] || [ -f "$ASSIGNMENTS" ]

for role in lfa-start lfa-pm lfa-android lfa-api lfa-ios lfa-review; do
  if herdr agent get "$role" >/dev/null 2>&1; then
    echo "团队已存在：$role。请运行 ./herdr-team/lfa-team.sh 并选择恢复协调，不要重复启动。" >&2
    exit 2
  fi
done

validate_assignments() {
  [ -z "$ASSIGNMENTS" ] && return
  seen_roles=' '
  seen_panes=' '
  while IFS='=' read -r assigned_role pane; do
    [ -n "$assigned_role" ] && [ -n "$pane" ] || { echo "无效 pane 映射：$assigned_role=$pane" >&2; exit 2; }
    case "$assigned_role" in
      lfa-start|lfa-pm|lfa-android|lfa-api|lfa-ios|lfa-review) ;;
      *) echo "未知团队角色：$assigned_role" >&2; exit 2;;
    esac
    case "$seen_roles" in *" $assigned_role "*) echo "角色重复映射：$assigned_role" >&2; exit 2;; esac
    case "$seen_panes" in *" $pane "*) echo "pane 重复映射：$pane" >&2; exit 2;; esac
    [ "$pane" != "${HERDR_PANE_ID:-}" ] || { echo "不能接管当前入口 pane：$pane" >&2; exit 2; }
    info=$(herdr pane get "$pane") || { echo "pane 不存在：$pane" >&2; exit 2; }
    printf %s "$info" | jq -e --arg root "$PROJECT_ROOT" '.result.pane | .cwd == $root and (.agent? == null)' >/dev/null || {
      echo "pane 不是当前项目的空闲 Shell：$pane" >&2
      exit 2
    }
    herdr pane process-info --pane "$pane" | jq -e '.result.process_info.foreground_processes as $p | ($p | length) == 1 and (($p[0].argv // []) | length) == 1 and (($p[0].argv[0] // "") | split("/")[-1] | test("^(ba|z|fi)?sh$"))' >/dev/null || {
      echo "pane 前台不是空闲交互 Shell：$pane" >&2
      exit 2
    }
    seen_roles="$seen_roles$assigned_role "
    seen_panes="$seen_panes$pane "
  done < "$ASSIGNMENTS"
}

assigned_pane() {
  [ -n "$ASSIGNMENTS" ] || return
  wanted=$1
  while IFS='=' read -r assigned_role pane; do
    [ "$assigned_role" = "$wanted" ] && { printf '%s\n' "$pane"; return; }
  done < "$ASSIGNMENTS"
}

validate_assignments

mkdir -p "$CONTROL_DIR/AGENT_STATUS" "$CONTROL_DIR/EVIDENCE" "$CONTROL_DIR/TASKS"
RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)
printf 'RUN_ID: %s\nSTATUS: PRE_ONBOARD\n' "$RUN_ID" > "$CONTROL_DIR/PM_GATE"

start_role() {
  role=$1
  case "$role" in
    lfa-start) k=$START_KIND; model=$START_MODEL; prompt_file=start;;
    lfa-pm) k=$PM_KIND; model=$PM_MODEL; prompt_file=pm;;
    lfa-android) k=$APP_APK_KIND; model=$APP_APK_MODEL; prompt_file=app-apk;;
    lfa-api) k=$API_KIND; model=$API_MODEL; prompt_file=api;;
    lfa-ios) k=$APP_IOS_KIND; model=$APP_IOS_MODEL; prompt_file=app-ios;;
    lfa-review) k=$REVIEW_CODE_KIND; model=$REVIEW_CODE_MODEL; prompt_file=review-code;;
  esac
  p=$(assigned_pane "$role")
  if [ -z "$p" ]; then
    j=$(herdr workspace create --cwd "$PROJECT_ROOT" --label "$role-$RUN_ID")
    p=$(printf %s "$j" | jq -r '.result.root_pane.pane_id // .result.root_pane.id // empty')
    [ -n "$p" ]
  fi
  herdr agent start "$role" --kind "$k" --pane "$p" -- --model "$model" --auto-approve
  printf '{"role":"%s","model":"%s","pane":"%s","run_id":"%s","status":"STARTED"}\n' "$role" "$model" "$p" "$RUN_ID" > "$CONTROL_DIR/AGENT_STATUS/$role.json"
  prompt=$(cat "$KIT_DIR/prompts/COMMON.md" "$KIT_DIR/prompts/$prompt_file.md")
  brief_text=
  [ -z "$BRIEF" ] || brief_text=$(cat "$BRIEF")
  herdr agent prompt "$role" "$prompt
本轮目标：$G
RUN_ID：$RUN_ID
本轮工作简报：
$brief_text
立即使用 OMP todo_write 建立你的 TODO。PM 先执行 PM-ONBOARD 并生成 herdr-team/.agent-control/PROJECT_SNAPSHOT.md；lfa-start 等待 PM_GATE=READY 且校验快照 HEAD 后再召开正式会议；其他角色只做预检并等待正式 TASK_ID，不得修改业务代码。"
}

for role in lfa-start lfa-pm lfa-android lfa-api lfa-ios lfa-review; do
  start_role "$role" > "$CONTROL_DIR/EVIDENCE/activate-$role.log" 2>&1 &
done
wait
python3 "$KIT_DIR/review_dispatch.py" --root "$PROJECT_ROOT" ensure-watch

echo "OK: OMP agents started; PM gate is PRE_ONBOARD"
echo "等待 PM_GATE=READY 后，lfa-start 才能正式派单"
