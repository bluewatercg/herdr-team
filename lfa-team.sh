#!/usr/bin/env bash
set -eu

KIT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$KIT_DIR")
CONTROL_DIR="$KIT_DIR/.agent-control"
cd "$PROJECT_ROOT"
herdr status >/dev/null 2>&1 || { echo "无法连接当前 Herdr session" >&2; exit 2; }

status() {
  printf '\nPM Gate:\n'
  [ ! -f "$CONTROL_DIR/PM_GATE" ] || cat "$CONTROL_DIR/PM_GATE"
  printf '\nTeam Agents:\n'
  for role in lfa-start lfa-pm lfa-android lfa-api lfa-ios lfa-test lfa-review lfa-grok-review lfa-claude-review; do
    herdr agent get "$role" 2>/dev/null || printf '%s: NOT_RUNNING\n' "$role"
  done
}

reconcile_reviews() {
  python3 "$KIT_DIR/review_dispatch.py" --root "$PROJECT_ROOT" reconcile >/dev/null
}

read_block() {
  prompt=$1
  default=$2
  printf '%s（直接回车使用项目默认值；自定义内容以单独一行 . 结束）:\n' "$prompt" >&2
  IFS= read -r line
  [ -n "$line" ] || { printf '%s' "$default"; return; }
  value=$line
  while IFS= read -r line && [ "$line" != . ]; do
    value="$value
$line"
  done
  printf '%s' "$value"
}

list_available_panes() {
  found=0
  for pane in $(herdr pane list | jq -r --arg root "$PROJECT_ROOT" '.result.panes[] | select(.cwd == $root and (.agent? == null)) | .pane_id'); do
    [ "$pane" = "${HERDR_PANE_ID:-}" ] && continue
    if herdr pane process-info --pane "$pane" | jq -e '.result.process_info.foreground_processes as $p | ($p | length) == 1 and (($p[0].argv // []) | length) == 1 and (($p[0].argv[0] // "") | split("/")[-1] | test("^(ba|z|fi)?sh$"))' >/dev/null; then
      printf '  %s\n' "$pane"
      found=1
    fi
  done
  [ "$found" = 1 ] || echo '  （没有可接入的空闲 Shell pane；回车将自动创建）'
}

choose_panes() {
  assignments=$1
  : > "$assignments"
  echo '可接入的当前项目空闲 Shell pane：'
  list_available_panes
  echo '为每个角色输入 pane ID；直接回车表示自动创建 workspace。'
  for role in lfa-start lfa-pm lfa-android lfa-api lfa-ios lfa-test lfa-review lfa-grok-review lfa-claude-review; do
    while :; do
      printf '%s pane: ' "$role"
      IFS= read -r pane
      [ -z "$pane" ] && break
      case "$pane" in
        w*:p*) printf '%s=%s\n' "$role" "$pane" >> "$assignments"; break;;
        *) echo '请输入列表中的 pane ID（例如 wQ:p4），或直接回车自动创建。' >&2;;
      esac
    done
  done
}

printf '%s\n' \
  '1) 开始新一轮工作' \
  '2) 查看团队状态' \
  '3) 恢复 PM 协调' \
  '4) 打开 PM 对话窗口' \
  '5) 环境预检' \
  '6) 打开团队 Web 面板' \
  '7) 设置 Jev API Key'
printf '请选择 [1-7]: '
IFS= read -r action

case "$action" in
  1)
    default_goal='跑通并验证真实 Android App → 标准 API → Python Core → DHEA 研究结果 → App 结果展示 → Web 诊断证据的 Investor MVP 闭环；先审计现状，再修复当前阻塞项。'
    default_acceptance='指定 Android 手机完成原始 JPEG 不可变保存和 SHA-256；multipart 上传成功；API 持久化原图并生成 request_id；统一调用 DheaRuntime.analyze()；Core 输出正确方向的 256×24 透视校正图、Green profile、T、C、T/C 和研究 4PL 结果或明确拒绝原因；App 展示服务端结果；Web 可按 request_id 查看阶段诊断；真实实验室参考值可绑定时完成绑定；相关构建、测试和运行证据全部落盘。'
    default_constraints='遵守 CONTROLLED_CAPTURE_INVESTOR_MVP；分析物仅 DHEA；原始 JPEG 不得重编码、转 PNG 或修改；缺失值保持 null，不得补 0 或造数据；人工 ROI 必须显式记录；App 只负责采集和展示，API 负责传输和持久化，Core 负责算法；YOLO、iOS 实现、法规和生产泛化属于 POST_FUNDING_GATE，不阻塞当前 P0；不得覆盖现有工作或运行中的服务。'
    goal=$(read_block '本轮要完成什么' "$default_goal")
    acceptance=$(read_block '完成时应看到什么结果' "$default_acceptance")
    constraints=$(read_block '限制、禁区或必须保留的内容' "$default_constraints")
    mkdir -p "$CONTROL_DIR/ROUNDS"
    "$KIT_DIR/preflight.sh"
    round=$(date -u +%Y%m%dT%H%M%S%NZ)
    brief="$CONTROL_DIR/ROUNDS/$round.md"
    assignments="$CONTROL_DIR/ROUNDS/$round.panes"
    choose_panes "$assignments"
    printf '# ROUND_BRIEF\nRUN_ID: %s\nGOAL: %s\nACCEPTANCE: %s\nCONSTRAINTS: %s\nPANE_ASSIGNMENTS: %s\n' \
      "$round" "$goal" "$acceptance" "${constraints:-NONE}" "${assignments#$PROJECT_ROOT/}" > "$brief"
    "$KIT_DIR/activate.sh" "$goal" "$brief" "$assignments"
    reconcile_reviews
    ;;
  2)
    status
    ;;
  3)
    "$KIT_DIR/activate.sh" --recover
    python3 "$KIT_DIR/review_dispatch.py" --root "$PROJECT_ROOT" ensure-watch >/dev/null
    reconcile_reviews
    herdr agent prompt lfa-pm "这是断线恢复，不是首次激活：不要重跑 PM-ONBOARD，不要重建或拆分读取类 TODO。保留已有业务 TODO；用一个原子恢复检查批量读取 MASTER_PLAN.md、FILE_OWNERSHIP.md、PM_GATE、PROJECT_SNAPSHOT.md、TASK_BOARD.md、DECISIONS.md、BLOCKERS.md、REVIEW_QUEUE.md 和 AGENT_STATUS，并核对当前 Git HEAD。只处理自上次状态以来的变化，继续下一项已授权、依赖满足且所有权无冲突的动作；无法推进时记录具体原因。" >/dev/null
    herdr agent prompt lfa-start "这是断线恢复，不是首次激活：不要重跑启动会议，不要重建或拆分读取类 TODO。保留已有业务 TODO；用一个原子恢复检查批量读取 MASTER_PLAN.md、FILE_OWNERSHIP.md、PM_GATE、PROJECT_SNAPSHOT.md、TASK_BOARD.md、DECISIONS.md、BLOCKERS.md、REVIEW_QUEUE.md 和 AGENT_STATUS。只有 PM_GATE=READY、RUN_ID 与 HEAD 匹配时，才重新评估下一项已授权、依赖满足且所有权无冲突的动作；无法推进时记录具体原因。恢复、完成或通知均不授予业务执行或集成权限。" >/dev/null
    echo "恢复完成：review watch 已启动。"
    echo "已通知 lfa-pm：继续现有项目协调。"
    echo "已通知 lfa-start：重新检查 Gate、依赖和可执行动作。"
    echo "现有账本、任务状态和历史记录未重置。"
    ;;
  4)
    herdr agent get lfa-pm >/dev/null 2>&1 || { echo "PM 未运行，请先开始新一轮工作或恢复团队" >&2; exit 2; }
    herdr agent focus lfa-pm
    ;;
  5)
    "$KIT_DIR/preflight.sh"
    ;;
  6)
    if ! curl -fsS http://127.0.0.1:8765/api/status >/dev/null 2>&1; then
      nohup python3 "$KIT_DIR/dashboard.py" > "$CONTROL_DIR/dashboard.log" 2>&1 &
      sleep 1
      curl -fsS http://127.0.0.1:8765/api/status >/dev/null || {
        cat "$CONTROL_DIR/dashboard.log" >&2
        exit 2
      }
    fi
    echo '团队面板: http://127.0.0.1:8765'
    ;;
  7)
    printf '请输入 TYPESAFE_API_KEY（回车取消）: '
    IFS= read -r key
    [ -n "$key" ] || { echo '已取消'; exit 0; }
    if grep -q '^TYPESAFE_API_KEY=' "$KIT_DIR/config.env" 2>/dev/null; then
      sed -i "s|^TYPESAFE_API_KEY=.*|TYPESAFE_API_KEY=$key|" "$KIT_DIR/config.env"
    else
      printf '\nTYPESAFE_API_KEY=%s\n' "$key" >> "$KIT_DIR/config.env"
    fi
    echo "✓ Jev API Key 已保存到 config.env"
    echo "✓ 所有 agents 现在可以自动使用 Jev 语义预检功能"
    ;;
  *)
    echo "无效选择" >&2
    exit 2
    ;;
esac
