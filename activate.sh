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
RECOVER=0
if [ "$G" = --recover ]; then
  RECOVER=1
  [ -f "$CONTROL_DIR/PM_GATE" ] || { echo "没有可恢复的 PM_GATE" >&2; exit 2; }
  RUN_ID=$(python3 -c 'import pathlib, sys; rows = [line.split(":", 1)[1].strip() for line in pathlib.Path(sys.argv[1]).read_text().splitlines() if line.startswith("RUN_ID:")]; assert len(rows) == 1 and rows[0], "PM_GATE 缺少唯一 RUN_ID"; print(rows[0])' "$CONTROL_DIR/PM_GATE")
fi
[ -n "$G" ] || { printf "请输入本轮目标: "; IFS= read -r G; }
[ -n "$G" ]
[ -z "$BRIEF" ] || [ -f "$BRIEF" ]
[ -z "$ASSIGNMENTS" ] || [ -f "$ASSIGNMENTS" ]
for role in lfa-start lfa-pm lfa-android lfa-api lfa-ios lfa-test lfa-review lfa-grok-review lfa-claude-review; do
  [ "$RECOVER" = 0 ] || break
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
      lfa-start|lfa-pm|lfa-android|lfa-api|lfa-ios|lfa-test|lfa-review|lfa-grok-review|lfa-claude-review) ;;
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
if [ "$RECOVER" = 0 ]; then
  RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)
  printf 'RUN_ID: %s\nSTATUS: PRE_ONBOARD\n' "$RUN_ID" > "$CONTROL_DIR/PM_GATE"
fi

start_role() {
  role=$1
  case "$role" in
    lfa-start) k=$START_KIND; model=$START_MODEL; prompt_file=start;;
    lfa-pm) k=$PM_KIND; model=$PM_MODEL; prompt_file=pm;;
    lfa-android) k=$APP_APK_KIND; model=$APP_APK_MODEL; prompt_file=app-apk;;
    lfa-api) k=$API_KIND; model=$API_MODEL; prompt_file=api;;
    lfa-ios) k=$APP_IOS_KIND; model=$APP_IOS_MODEL; prompt_file=app-ios;;
    lfa-test) k=$TEST_KIND; model=$TEST_MODEL; prompt_file=test;;
    lfa-review) k=$REVIEW_CODE_KIND; model=$REVIEW_CODE_MODEL; prompt_file=review-code;;
    lfa-grok-review) k=$GROK_REVIEW_KIND; model=$GROK_REVIEW_MODEL; prompt_file=review-code;;
    lfa-claude-review) k=$CLAUDE_REVIEW_KIND; model=$CLAUDE_REVIEW_MODEL; prompt_file=review-code;;
  esac
  p=$(assigned_pane "$role")
  if [ -z "$p" ]; then
    j=$(herdr workspace create --cwd "$PROJECT_ROOT" --label "$role-$RUN_ID")
    p=$(printf %s "$j" | jq -r '.result.root_pane.pane_id // .result.root_pane.id // empty')
    [ -n "$p" ]
  fi
  case "$k" in
    grok) herdr agent start "$role" --kind "$k" --pane "$p" -- --model "$model" --always-approve;;
    claude) herdr agent start "$role" --kind "$k" --pane "$p" -- --permission-mode auto;;
    *) herdr agent start "$role" --kind "$k" --pane "$p" -- --model "$model" --auto-approve;;
  esac
  printf '{"role":"%s","model":"%s","pane":"%s","run_id":"%s","status":"STARTED"}\n' "$role" "$model" "$p" "$RUN_ID" > "$CONTROL_DIR/AGENT_STATUS/$role.json"
  prompt=$(cat "$KIT_DIR/prompts/COMMON.md" "$KIT_DIR/prompts/$prompt_file.md")
  if [ "$RECOVER" = 1 ]; then
    herdr agent prompt "$role" "$prompt
恢复模式覆盖首次启动流程：这是既有 RUN_ID=$RUN_ID 的缺失角色重建，不是新一轮。不要执行 PM-ONBOARD、重开启动会议、重置 Gate、重建账本或接管其他角色任务。读取现有 PM_GATE、PROJECT_SNAPSHOT.md、MASTER_PLAN.md、TASK_BOARD.md、FILE_OWNERSHIP.md、BLOCKERS.md 和 REVIEW_QUEUE.md，核对当前 HEAD；向现有 PM 报告恢复情况。在 PM 确认现有授权、依赖和精确文件所有权前只读等待，不修改业务文件。保留所有既有历史；启动本身不授予执行或集成权限。"
    return
  fi
  brief_text=
  [ -z "$BRIEF" ] || brief_text=$(cat "$BRIEF")
  herdr agent prompt "$role" "$prompt
本轮目标：$G
RUN_ID：$RUN_ID
本轮工作简报：
$brief_text
立即使用 OMP todo_write 建立你的 TODO。PM 先执行 PM-ONBOARD 并生成 herdr-team/.agent-control/PROJECT_SNAPSHOT.md；lfa-start 等待 PM_GATE=READY 且校验快照 HEAD 后再召开正式会议；其他角色只做预检并等待正式 TASK_ID，不得修改业务代码。"
}

for role in lfa-start lfa-pm lfa-android lfa-api lfa-ios lfa-test lfa-review lfa-grok-review lfa-claude-review; do
  if [ "$RECOVER" = 1 ]; then
    if info=$(herdr agent get "$role" 2>&1); then
      echo "保留现有 Agent：$role"
      continue
    fi
    printf '%s' "$info" | jq -e '.error.code == "agent_not_found"' >/dev/null || {
      printf '无法检查 %s：%s\n' "$role" "$info" >&2
      exit 2
    }
    start_role "$role" > "$CONTROL_DIR/EVIDENCE/recover-$role.log" 2>&1 || {
      cat "$CONTROL_DIR/EVIDENCE/recover-$role.log" >&2
      exit 1
    }
    continue
  fi
  start_role "$role" > "$CONTROL_DIR/EVIDENCE/activate-$role.log" 2>&1 &
done
wait
python3 "$KIT_DIR/review_dispatch.py" --root "$PROJECT_ROOT" ensure-watch

if [ "$RECOVER" = 1 ]; then
  echo "缺失角色已补起；原有 Agent、RUN_ID 和 PM_GATE 保持不变。"
else
  echo "OK: OMP agents started; PM gate is PRE_ONBOARD"
  echo "等待 PM_GATE=READY 后，lfa-start 才能正式派单"
fi
