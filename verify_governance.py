#!/usr/bin/env python3
"""Herdr 治理一致性校验器（只读）。

把目前只写在 herdr-team/prompts/*.md 里的硬规则变成可执行检查。脚本不写任何
项目状态、不派发、不授予权限、不修改账本；它只读账本和仓库事实，输出发现。

覆盖的规则来源：
  prompts/start.md   PM 接管 Gate、文件冲突 Gate、Master Plan Gate
  prompts/COMMON.md  计划绑定与 OMP TODO、需求追踪 Gate、文件写入所有权
  prompts/pm.md      项目接管流程、Requirement Intake
  prompts/review-code.md  独立评审边界

退出码：
  0  没有 VIOLATION（可能有 WARNING/INFO）
  1  至少一个 VIOLATION
  2  用法或环境错误
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from checksum_manifest import check_manifest, static_files

SEVERITY_ORDER = {"VIOLATION": 0, "WARNING": 1, "INFO": 2}

PLAN_GATE_STATUSES = {"READY", "CONFLICTED", "BLOCKED"}

# 交付物状态中禁止派发的集合（MASTER_PLAN "Dispatch and update protocol"）
NON_DISPATCHABLE_DELIVERABLE = {"PARKED", "BLOCKED", "ACCEPTED"}

# 任务状态中代表"已验收/已关闭"的标记
ACCEPTED_MARKERS = ("ACCEPTED", "CLOSED")

# 任务状态中代表"可派发/进行中"的标记
DISPATCHABLE_MARKERS = ("READY", "DISPATCH", "IN_PROGRESS", "ACTIVE")

EVIDENCE_REF_RE = re.compile(r"(?:^|[\s;(,])EVIDENCE/([A-Za-z0-9._-]+)")

# FILE_OWNERSHIP 有两种列宽：6 列（path|TASK_ID|SUBTASK_ID|WRITE_OWNER|READERS|status）
# 和 7 列（多插 PLAN_ID|DELIVERABLE_ID）。写 owner 不是只有 lfa-*，还有 shadow-core 等，
# 所以按列位取值，不靠前缀猜。
OWNER_COL_BY_WIDTH = {6: 3, 7: 4}

# 交付物 ID 去掉末段即所属 PLAN_ID（M1-D01→M1、GOV-DOC-01-D01→GOV-DOC-01、QR-GEOMETRY-01-G0→QR-GEOMETRY-01）
DELIVERABLE_SUFFIX_RE = re.compile(r"-(?:D\d+|G\d+|R\d+|S\d+)$")

# 视为"独占写"的状态；RELEASED 等释放态不参与冲突判定
ACTIVE_STATUSES = {"ACTIVE"}
ACTIVE_PREFIXES = ("AUTHORIZED_ACTIVE",)


class Finding:
    __slots__ = ("check", "severity", "message", "evidence")

    def __init__(self, check: str, severity: str, message: str, evidence=None):
        self.check = check
        self.severity = severity
        self.message = message
        self.evidence = evidence or []

    def as_dict(self):
        return {
            "check": self.check,
            "severity": self.severity,
            "message": self.message,
            "evidence": self.evidence,
        }


def cells_of(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(c and set(c) <= set("-: ") for c in cells)


def parse_tables(text: str):
    """返回 [(header, [row_cells, ...]), ...]，覆盖全文所有 markdown 管道表。"""
    tables = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if not lines[i].lstrip().startswith("|"):
            i += 1
            continue
        block = []
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            block.append(lines[i])
            i += 1
        if len(block) < 2:
            continue
        header = cells_of(block[0])
        if not is_separator(cells_of(block[1])):
            continue
        rows = []
        for raw in block[2:]:
            cs = cells_of(raw)
            if not any(cs) or is_separator(cs):
                continue
            rows.append(cs)
        tables.append((header, rows))
    return tables


def row_get(header: list[str], row: list[str], name: str) -> str:
    try:
        idx = header.index(name)
    except ValueError:
        return ""
    return row[idx] if idx < len(row) else ""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")




def token_present(token: str, text: str) -> bool:
    """ID 是否以完整词形式出现在权威文本中。"""
    if not token:
        return False
    return re.search(r"(?<![A-Za-z0-9_-])" + re.escape(token) + r"(?![A-Za-z0-9_-])", text) is not None


def normalize_owner(raw: str) -> str:
    """lfa-start(w15:p1) 与 lfa-start 是同一写 owner，pane 注解不构成冲突。"""
    return re.sub(r"\s*\([^)]*\)\s*$", "", raw.strip())


def owning_plan_of(deliverable_id: str, explicit: dict[str, str]) -> str | None:
    """推导交付物所属 PLAN_ID：显式表映射优先，否则按 ID 末段剥离。"""
    if deliverable_id in explicit:
        return explicit[deliverable_id]
    m = DELIVERABLE_SUFFIX_RE.search(deliverable_id)
    return deliverable_id[: m.start()] if m else None


def git_head(path: Path) -> str | None:
    """返回 path 所在仓库的 HEAD；不是 git 仓库时返回 None。"""
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(path),
                           capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def wsl_to_host(raw: str) -> Path:
    """仅 Windows Python 将 WSL 挂载路径转换为盘符；Linux/WSL 保留原路径。"""
    m = re.match(r"^/mnt/([a-zA-Z])/(.*)$", raw.strip())
    if m and sys.platform == "win32":
        return Path(f"{m.group(1).upper()}:/{m.group(2)}")
    return Path(raw.strip())


def parse_kv_block(text: str) -> dict[str, list[str]]:
    """收集形如 `KEY: value` 的字段，同名键保留全部出现（列表）。

    键名大小写都接受：Requirement Intake 里既有 USER_CONFIRMED 也有
    task_creation_allowed 这类小写字段。
    """
    out: dict[str, list[str]] = {}
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Za-z][A-Za-z0-9_]*):\s*(.*?)\s*$", line)
        if m:
            out.setdefault(m.group(1), []).append(m.group(2))
    return out


def is_nullish(v: str) -> bool:
    return v.strip().lower() in {"null", "~", ""}


def is_false(v: str) -> bool:
    return v.strip().lower() in {"false", "no", "off"}


# --------------------------------------------------------------------------
# 各项检查
# --------------------------------------------------------------------------

def check_pm_gate(root: Path, ctrl: Path, f: list[Finding]):
    gate_path = ctrl / "PM_GATE"
    snap_path = ctrl / "PROJECT_SNAPSHOT.md"
    if not gate_path.exists():
        f.append(Finding("GATE-MISSING", "VIOLATION", "PM_GATE 不存在，lfa-start 不得派单"))
        return
    gate = parse_kv_block(read(gate_path))
    get = lambda k: (gate.get(k) or [""])[0].strip()  # noqa: E731

    status = get("STATUS")
    if status not in PLAN_GATE_STATUSES:
        f.append(Finding("GATE-STATUS-INVALID", "VIOLATION",
                         f"PM_GATE.STATUS={status!r} 不在 {sorted(PLAN_GATE_STATUSES)}",
                         [f"PM_GATE"]))

    if not snap_path.exists():
        f.append(Finding("GATE-SNAPSHOT-MISSING", "VIOLATION",
                         "PROJECT_SNAPSHOT.md 不存在，PM 接管未完成"))
        return
    snap = parse_kv_block(read(snap_path))
    sget = lambda k: (snap.get(k) or [""])[0].strip()  # noqa: E731

    for field, check in (("RUN_ID", "GATE-RUNID-MISMATCH"),
                         ("SNAPSHOT_ID", "GATE-SNAPSHOT-MISMATCH")):
        a, b = get(field), sget(field)
        if a and b and a != b:
            f.append(Finding(check, "VIOLATION",
                             f"PM_GATE.{field} 与 PROJECT_SNAPSHOT.{field} 不一致",
                             [f"PM_GATE            = {a}", f"PROJECT_SNAPSHOT   = {b}"]))

    # start.md「PM 接管 Gate」要求核对快照 GIT_HEAD 等于当前 Git HEAD。
    # 该 HEAD 属于 PROJECT_SNAPSHOT.REPOSITORY_ROOT 指向的项目仓库，不是本 kit 所在仓库。
    gate_head = get("GIT_HEAD") or sget("GIT_HEAD")
    repo_root_raw = sget("REPOSITORY_ROOT")
    repo_root = wsl_to_host(repo_root_raw) if repo_root_raw else root.parent
    actual = git_head(repo_root)
    kit_head = git_head(root)

    if actual is None:
        f.append(Finding("GATE-HEAD-UNVERIFIABLE", "VIOLATION",
                         "PM 接管 Gate 无法执行：绑定的项目仓库在本地不是 git 仓库，HEAD 核对无从进行",
                         [f"REPOSITORY_ROOT = {repo_root_raw or '(未记录)'}",
                          f"解析为本地路径  = {repo_root}",
                          f"账本记录 GIT_HEAD = {gate_head or '(空)'}",
                          f"本 kit 仓库 HEAD  = {kit_head or '(非仓库)'}"]))
    elif gate_head and gate_head != actual:
        f.append(Finding("GATE-HEAD-DRIFT", "VIOLATION",
                         "PM_GATE.GIT_HEAD 与项目仓库当前 HEAD 不一致，PM 接管 Gate 不成立",
                         [f"账本 GIT_HEAD = {gate_head}", f"实际 HEAD     = {actual}"]))


def collect_master_plan(mp_text: str):
    """从 MASTER_PLAN 提取登记事实。

    登记不限于表格：GOV-DOC-01 / QR-PLAN-0x / AUTO-DISPATCH-01 等 workstream 写在
    正文章节里。因此"是否已登记"用全文完整词匹配判断，只有显式 PLAN_ID 与
    DELIVERABLE_ID 同表出现时才建立归属映射。
    返回 (deliverable_plan, deliverable_status)。
    """
    deliverable_plan: dict[str, str] = {}
    deliverable_status: dict[str, str] = {}
    for header, rows in parse_tables(mp_text):
        if "DELIVERABLE_ID" not in header:
            continue
        for r in rows:
            d = row_get(header, r, "DELIVERABLE_ID")
            if not d:
                continue
            if "PLAN_ID" in header:
                p = row_get(header, r, "PLAN_ID")
                if p:
                    deliverable_plan.setdefault(d, p)
            if "Status" in header:
                deliverable_status.setdefault(d, row_get(header, r, "Status"))
    return deliverable_plan, deliverable_status


def local_source_reference(root: Path, ctrl: Path, reference: str) -> tuple[Path, str]:
    """Resolve an exact local file, optionally with a heading or inclusive line range."""
    match = re.fullmatch(r"([^#:\s]+)(?:#([^\s]+)|:(\d+)(?:-(\d+))?)?", reference)
    if not match:
        raise ValueError("来源须为精确相对路径，可附 #heading 或 :起行-止行")
    raw, anchor, start, end = match.groups()
    parts = raw.split("/")
    if (raw.startswith("/") or any(p in {"", ".", ".."} for p in parts)
            or any(c in raw for c in "\\*?[]%")):
        raise ValueError("来源路径不安全或不是精确文件")
    if parts[0] == root.name:
        base, parts = root, parts[1:]
    elif parts[0] in {"docs", "AGENTS.md"}:
        base = root.parent
    else:
        base = ctrl
    path = base
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("来源不能经过符号链接")
    if not path.is_file():
        raise ValueError("来源文件不存在")
    text = read(path)
    lines = text.splitlines()
    if start:
        first, last = int(start), int(end or start)
        if not 1 <= first <= last <= len(lines):
            raise ValueError("来源行号不存在或范围倒置")
        text = "\n".join(lines[first - 1:last])
    elif anchor:
        matches = []
        for i, line in enumerate(lines):
            heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if heading:
                slug = re.sub(r"[^\w\- ]", "", heading[2].lower()).replace(" ", "-")
                if slug == anchor:
                    matches.append((i, len(heading[1])))
        if len(matches) != 1:
            raise ValueError("来源章节不存在或不唯一")
        first, level = matches[0]
        last = next((i for i in range(first + 1, len(lines))
                     if re.match(r"^#{1," + str(level) + r"}\s", lines[i])), len(lines))
        text = "\n".join(lines[first:last])
    return path, text


def historical_authority_sources(root: Path, ctrl: Path) -> list[tuple[str, str]]:
    """Read ownership and PM-owned evidence only; these are candidates, not grants."""
    sources = []
    try:
        _, ownership = local_source_reference(root, ctrl, "FILE_OWNERSHIP.md")
    except (OSError, ValueError):
        return sources
    sources.append(("FILE_OWNERSHIP.md", ownership))
    paths = set()
    for header, rows in parse_tables(ownership):
        for row in rows:
            path = row_get(header, row, "path")
            if (normalize_owner(row_get(header, row, "WRITE_OWNER")) == "lfa-pm"
                    and path.startswith(f"{root.name}/.agent-control/EVIDENCE/")
                    and path.endswith(".md")):
                paths.add(path)
    for reference in sorted(paths):
        try:
            _, text = local_source_reference(root, ctrl, reference)
        except (OSError, ValueError):
            continue
        sources.append((reference, text))
    return sources


def historical_binding_evidence(sources: list[tuple[str, str]], task: str,
                                plan: str, deliverable: str) -> list[str]:
    """Find same-task declarations without interpreting authorization prose."""
    evidence = []
    for reference, text in sources:
        sections = re.split(r"(?m)(?=^#{1,6} )", text)
        line = 1
        for section in sections:
            fields: dict[str, set[str]] = {}
            for key, value in re.findall(
                    r"(?<![\w-])(TASK_ID|PLAN_ID|DELIVERABLE_ID)\s*[:=]\s*([A-Za-z0-9_-]+)", section):
                fields.setdefault(key, set()).add(value)
            if fields.get("TASK_ID") == {task}:
                conflicts = [key for key, expected in (("PLAN_ID", plan), ("DELIVERABLE_ID", deliverable))
                             if key in fields and fields[key] != {expected}]
                if not conflicts:
                    missing = [key for key in ("PLAN_ID", "DELIVERABLE_ID") if key not in fields]
                    evidence.append(f"{reference}:{line}: TASK_ID 精确匹配；"
                                    + ("缺少 " + ", ".join(missing) if missing else "三元组精确匹配")
                                    + "；授权原文、精确 scope/owner/来源及母计划边界须人工核验")
            line += section.count("\n")
    return evidence


def check_task_bindings(root: Path, ctrl: Path, mp_text: str, f: list[Finding]):
    tb_path = ctrl / "TASK_BOARD.md"
    if not tb_path.exists():
        f.append(Finding("BIND-TASKBOARD-MISSING", "VIOLATION", "TASK_BOARD.md 不存在"))
        return
    deliverable_plan, deliverable_status = collect_master_plan(mp_text)

    tb_text = read(tb_path)
    authority_sources = None
    seen_any = False
    for header, rows in parse_tables(tb_text):
        if not {"PLAN_ID", "DELIVERABLE_ID", "TASK_ID"} <= set(header):
            continue
        seen_any = True
        for r in rows:
            plan = row_get(header, r, "PLAN_ID")
            deliv = row_get(header, r, "DELIVERABLE_ID")
            task = row_get(header, r, "TASK_ID")
            reqs = row_get(header, r, "REQUIREMENT_IDS")
            status = row_get(header, r, "Status") or row_get(header, r, "STATUS")

            if not (plan and deliv and task):
                f.append(Finding("BIND-MISSING", "VIOLATION",
                                 "任务行缺少 PLAN_ID / DELIVERABLE_ID / TASK_ID 之一",
                                 [f"row = {r[:6]}"]))
                continue

            if "REQUIREMENT_SOURCE_REFERENCES" in header and not row_get(header, r, "REQUIREMENT_SOURCE_REFERENCES"):
                f.append(Finding("BIND-SOURCE-INVALID", "VIOLATION", "来源引用为空",
                                 [f"TASK_ID={task}"]))
            for reference in filter(None, (part.strip() for part in
                    row_get(header, r, "REQUIREMENT_SOURCE_REFERENCES").split(";"))):
                try:
                    local_source_reference(root, ctrl, reference)
                except (OSError, ValueError) as exc:
                    f.append(Finding("BIND-SOURCE-INVALID", "VIOLATION", str(exc),
                                     [f"TASK_ID={task}", reference]))

            missing_plan = not token_present(plan, mp_text)
            missing_deliverable = not token_present(deliv, mp_text)
            if missing_plan or missing_deliverable:
                if authority_sources is None:
                    authority_sources = historical_authority_sources(root, ctrl)
                candidates = historical_binding_evidence(authority_sources, task, plan, deliv)
                if candidates:
                    f.append(Finding("BIND-AUTHORITY-MANUAL-REVIEW", "VIOLATION",
                                     "MASTER_PLAN 绑定未完整登记；存在同任务历史来源，授权语义尚未机器核验，不能自动放行",
                                     [f"TASK_ID={task}; PLAN_ID={plan}; DELIVERABLE_ID={deliv}", *candidates]))
                else:
                    if missing_plan:
                        f.append(Finding("BIND-PLAN-UNKNOWN", "VIOLATION",
                                         f"PLAN_ID={plan} 未在 MASTER_PLAN 登记",
                                         [f"TASK_ID={task}"]))
                    if missing_deliverable:
                        f.append(Finding("BIND-DELIVERABLE-UNKNOWN", "VIOLATION",
                                         f"DELIVERABLE_ID={deliv} 未在 MASTER_PLAN 登记",
                                         [f"TASK_ID={task}"]))
            if not missing_deliverable:
                owner_plan = owning_plan_of(deliv, deliverable_plan)
                if owner_plan and owner_plan != plan and token_present(owner_plan, mp_text):
                    f.append(Finding("BIND-PLAN-DELIVERABLE-MISMATCH", "VIOLATION",
                                     "PLAN_ID 与 DELIVERABLE_ID 不属于同一 plan",
                                     [f"TASK_ID={task}",
                                      f"任务 PLAN_ID={plan}",
                                      f"交付物所属={owner_plan}"]))

            if "UNMAPPED" in reqs:
                up = status.upper()
                if any(m in up for m in ACCEPTED_MARKERS):
                    f.append(Finding("BIND-UNMAPPED-ACCEPTED", "VIOLATION",
                                     "REQUIREMENT_IDS 含 UNMAPPED 却已验收/关闭（需求追踪 Gate 禁止）",
                                     [f"TASK_ID={task}", f"Status={status}"]))
                elif any(m in up for m in DISPATCHABLE_MARKERS):
                    f.append(Finding("BIND-UNMAPPED-DISPATCHABLE", "WARNING",
                                     "REQUIREMENT_IDS 含 UNMAPPED 且状态为可派发（规则不追溯历史行，需人工确认）",
                                     [f"TASK_ID={task}", f"Status={status}"]))

            dstat = deliverable_status.get(deliv, "")
            if dstat and dstat.upper() in NON_DISPATCHABLE_DELIVERABLE:
                if "PARKED" not in status.upper():
                    f.append(Finding("BIND-DELIVERABLE-NOT-DISPATCHABLE", "WARNING",
                                     f"交付物 {deliv} 状态为 {dstat}，该任务本不应派发",
                                     [f"TASK_ID={task}", f"Status={status}"]))
    if not seen_any:
        f.append(Finding("BIND-TABLE-NOT-FOUND", "WARNING",
                         "TASK_BOARD.md 中未找到含 PLAN_ID/DELIVERABLE_ID/TASK_ID 的任务表"))


def check_file_ownership(root: Path, ctrl: Path, f: list[Finding]):
    fo_path = ctrl / "FILE_OWNERSHIP.md"
    if not fo_path.exists():
        f.append(Finding("OWN-LEDGER-MISSING", "VIOLATION", "FILE_OWNERSHIP.md 不存在"))
        return
    active: dict[str, list[str]] = {}
    rows_seen = 0
    for line in read(fo_path).splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cs = cells_of(line)
        if len(cs) not in OWNER_COL_BY_WIDTH or is_separator(cs):
            continue
        raw_path = cs[0]
        if "/" not in raw_path:
            continue
        path = re.sub(r"\s*\(.*\)\s*$", "", raw_path).strip()
        status = cs[-1].strip()
        owner = cs[OWNER_COL_BY_WIDTH[len(cs)]].strip()
        rows_seen += 1
        is_active = status in ACTIVE_STATUSES or any(status.startswith(p) for p in ACTIVE_PREFIXES)
        if not owner:
            if is_active:
                f.append(Finding("OWN-NO-OWNER", "VIOLATION",
                                 "ACTIVE 所有权行没有 WRITE_OWNER，写权限无人承担",
                                 [f"path={path}", f"status={status}"]))
            continue
        if is_active:
            active.setdefault(path, []).append(normalize_owner(owner))

    for path, owners in sorted(active.items()):
        uniq = sorted(set(owners))
        if len(uniq) > 1:
            f.append(Finding("OWN-MULTI-ACTIVE", "VIOLATION",
                             "同一路径存在多个 ACTIVE 写 owner（COMMON.md 禁止）",
                             [f"path={path}", f"owners={uniq}"]))
    if rows_seen == 0:
        f.append(Finding("OWN-LEDGER-EMPTY", "WARNING", "FILE_OWNERSHIP.md 未解析到所有权行"))


def check_intake(root: Path, ctrl: Path, f: list[Finding]):
    path = ctrl / "PM_REQUIREMENT_INTAKE.md"
    if not path.exists():
        return
    text = read(path)
    sections = re.split(r"^## ", text, flags=re.M)[1:]
    for sec in sections:
        title = sec.splitlines()[0].strip()
        if not re.match(r"^PM-RI-", title):
            continue
        kv = parse_kv_block(sec)
        confirmed = [v for v in kv.get("USER_CONFIRMED", [])]
        intake_ids = kv.get("INTAKE_ID", [])
        confirmed_false = any(is_false(v) for v in confirmed)

        if confirmed_false:
            for key, check in (("REQUIREMENT_MAPPING_ALLOWED", "INTK-MAPPING-ALLOWED"),
                               ("task_creation_allowed", "INTK-TASK-ALLOWED"),
                               ("dispatch_allowed", "INTK-DISPATCH-ALLOWED")):
                vals = kv.get(key, []) + kv.get(key.upper(), [])
                if vals and not all(is_false(v) for v in vals):
                    f.append(Finding(check, "VIOLATION",
                                     f"USER_CONFIRMED=false 时 {key} 必须为 false",
                                     [f"intake={title}", f"{key}={vals}"]))
            for key in ("TASK_ID", "OMP_TODO", "FILE_SCOPE", "WRITE_OWNER"):
                for v in kv.get(key, []):
                    if not is_nullish(v):
                        f.append(Finding("INTK-EXEC-OBJECT", "VIOLATION",
                                         f"USER_CONFIRMED=false 时 {key} 必须为 null 哨兵",
                                         [f"intake={title}", f"{key}={v!r}"]))
                        break

        for iid in intake_ids:
            if is_nullish(iid):
                continue
            for key in ("REQUIREMENT_ID", "TASK_ID"):
                for v in kv.get(key, []):
                    if v.strip() == iid.strip():
                        f.append(Finding("INTK-ID-REUSE", "VIOLATION",
                                         f"INTAKE_ID 被当作 {key} 使用",
                                         [f"intake={title}", f"{key}={v}"]))


def check_integrity(root: Path, ctrl: Path, f: list[Finding]):
    errors = check_manifest(root)
    if errors:
        f.append(Finding("INTG-CHECKSUM-INVALID", "VIOLATION",
                         "静态清单缺失、格式/覆盖错误或文件内容不匹配", errors))


def check_jev(root: Path, ctrl: Path, f: list[Finding]):
    log = ctrl / "JEV_DECISIONS.jsonl"
    blockers = ctrl / "BLOCKERS.md"
    if log.exists():
        return
    referenced = blockers.exists() and "JEV_DECISIONS" in read(blockers)
    if referenced:
        f.append(Finding("JEV-EVENT-MISSING", "WARNING",
                         "存在记录在案的 Jev 授权阻塞：JEV_DECISIONS.jsonl 尚未产生，依赖它的派发不可执行",
                         ["BLOCKERS.md 引用了 JEV_DECISIONS", f"{log} 不存在"]))


def check_evidence_refs(root: Path, ctrl: Path, f: list[Finding]):
    missing = []
    for name in ("TASK_BOARD.md", "REVIEW_QUEUE.md"):
        p = ctrl / name
        if not p.exists():
            continue
        for m in EVIDENCE_REF_RE.finditer(read(p)):
            ref = m.group(1)
            if not (ctrl / "EVIDENCE" / ref).exists():
                missing.append(f"{name}: EVIDENCE/{ref}")
    if missing:
        uniq = sorted(set(missing))
        f.append(Finding("EVID-MISSING-REF", "WARNING",
                         "账本引用了不存在的证据路径",
                         [f"{len(uniq)} 条", *uniq[:8]]))


def check_review_state(root: Path, ctrl: Path, f: list[Finding]):
    p = ctrl / "REVIEW_QUEUE.md"
    if not p.exists():
        return
    m = re.search(r"<!-- review-state -->\s*(\{.*\})", read(p), re.S)
    if not m:
        return
    try:
        state = json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        f.append(Finding("RQ-STATE-INVALID", "VIOLATION",
                         f"review-state JSON 无法解析：{exc}"))
        return
    subs = state.get("submissions", {})
    stale = sum(1 for v in subs.values() if v.get("status") == "STALE")
    if subs and stale == len(subs):
        f.append(Finding("RQ-ALL-STALE", "INFO",
                         "全部评审提交为 STALE。源引用含可变控制账本，属已知性质，不代表篡改",
                         [f"{stale}/{len(subs)} 提交 STALE"]))


def check_agent_status(root: Path, ctrl: Path, f: list[Finding]):
    d = ctrl / "AGENT_STATUS"
    if not d.is_dir():
        return
    gate = parse_kv_block(read(ctrl / "PM_GATE")) if (ctrl / "PM_GATE").exists() else {}
    gate_head = (gate.get("GIT_HEAD") or [""])[0]
    for p in sorted(d.glob("*.json")):
        try:
            rec = json.loads(read(p))
        except json.JSONDecodeError:
            f.append(Finding("AGENT-STATUS-INVALID", "WARNING", f"{p.name} 不是合法 JSON"))
            continue
        gh = rec.get("git_head")
        if gh and gate_head and gh != gate_head:
            f.append(Finding("AGENT-STATUS-DRIFT", "WARNING",
                             "AGENT_STATUS 记录的 git_head 与 PM_GATE 不一致",
                             [f"{p.name}: {gh}", f"PM_GATE: {gate_head}"]))


CHECKS = (
    ("PM Gate 与仓库事实", check_pm_gate),
    ("任务绑定与需求追踪", check_task_bindings),
    ("文件写入所有权", check_file_ownership),
    ("Requirement Intake", check_intake),
    ("受保护文件完整性", check_integrity),
    ("Jev 决策账本", check_jev),
    ("证据引用", check_evidence_refs),
    ("评审队列机器状态", check_review_state),
    ("Agent 状态一致性", check_agent_status),
)


def self_test() -> int:
    """离线自检：只验解析器与判定逻辑，不读取真实账本、不联网。"""
    import tempfile

    failures: list[str] = []

    def expect(cond: bool, label: str):
        if not cond:
            failures.append(label)

    tables = parse_tables("| a | b |\n|---|---|\n| 1 | 2 |\n")
    expect(len(tables) == 1 and tables[0][1] == [["1", "2"]], "parse_tables 基本解析")
    expect(parse_tables("| a | b |\n| 1 | 2 |\n") == [], "缺少分隔行时不应识别为表")

    expect(OWNER_COL_BY_WIDTH == {6: 3, 7: 4}, "owner 列位映射")
    expect(normalize_owner("lfa-start(w15:p1)") == "lfa-start", "pane 注解不应构成 owner 冲突")
    expect(normalize_owner("shadow-core") == "shadow-core", "非 lfa- 前缀 owner 应保留")

    expect(owning_plan_of("M1-D01", {}) == "M1", "交付物归属：M1-D01")
    expect(owning_plan_of("QR-GEOMETRY-01-G0", {}) == "QR-GEOMETRY-01", "交付物归属：G0 后缀")
    expect(owning_plan_of("DELIVERABLE-QIUQIU-01",
                          {"DELIVERABLE-QIUQIU-01": "PLAN-QIUQIU-01"}) == "PLAN-QIUQIU-01",
           "显式表映射优先")
    expect(owning_plan_of("NO-SUFFIX", {}) is None, "无法推导时应返回 None")

    expect(token_present("M1", "见 M1 章节"), "完整词匹配命中")
    expect(not token_present("M1", "M10 与 M1X"), "完整词匹配应拒绝子串")

    from unittest.mock import patch

    for platform, expected in (("win32", "D:/Project/x"), ("linux", "/mnt/d/Project/x")):
        with patch.object(sys, "platform", platform):
            expect(str(wsl_to_host("/mnt/d/Project/x")).replace("\\", "/") == expected,
                   f"WSL 路径映射遵循运行平台 {platform}")
    expect(not token_present("M1", "M1-D01"), "交付物前缀不能冒充 plan 登记")
    expect(not token_present("T1", "T1-OTHER"), "任务前缀不能匹配另一任务")

    with tempfile.TemporaryDirectory() as td:
        root, ctrl = Path(td), Path(td) / ".agent-control"
        ctrl.mkdir()
        board = ("| PLAN_ID | DELIVERABLE_ID | TASK_ID | STATUS |\n|---|---|---|---|\n"
                 "| CONTROL-FAKE | CONTROL-FAKE-D01 | T1 | ACCEPTED_CONTROL_PLANE_ONLY; MAINLINE_IMPACT=NONE |\n")
        (ctrl / "TASK_BOARD.md").write_text(board, encoding="utf-8")
        got = []
        check_task_bindings(root, ctrl, "", got)
        expect({x.check for x in got} == {"BIND-PLAN-UNKNOWN", "BIND-DELIVERABLE-UNKNOWN"},
               "任务登记、control 前缀和 NONE 不构成授权")
        declaration = ("## Bounded history\nTASK_ID=T1; PLAN_ID=CONTROL-FAKE; "
                       "DELIVERABLE_ID=CONTROL-FAKE-D01\nAuthority: explicit user request.\n")
        (ctrl / "FILE_OWNERSHIP.md").write_text(declaration, encoding="utf-8")
        got = []
        check_task_bindings(root, ctrl, "", got)
        expect(len(got) == 1 and got[0].check == "BIND-AUTHORITY-MANUAL-REVIEW"
               and got[0].severity == "VIOLATION", "历史同任务原文只转人工核验，不放行")
        for conflicting in (declaration.replace("TASK_ID=T1;", "TASK_ID=T1-OTHER;"),
                            declaration.replace("PLAN_ID=CONTROL-FAKE;", "PLAN_ID=OTHER;"),
                            declaration.replace("DELIVERABLE_ID=CONTROL-FAKE-D01", "DELIVERABLE_ID=OTHER-D01")):
            (ctrl / "FILE_OWNERSHIP.md").write_text(conflicting, encoding="utf-8")
            got = []
            check_task_bindings(root, ctrl, "", got)
            expect({x.check for x in got} == {"BIND-PLAN-UNKNOWN", "BIND-DELIVERABLE-UNKNOWN"},
                   "其他 task/plan/deliverable 原文不可转用")
        got = []
        check_task_bindings(root, ctrl,
                            "| PLAN_ID | DELIVERABLE_ID |\n|---|---|\n| OTHER | CONTROL-FAKE-D01 |\nCONTROL-FAKE", got)
        expect(any(x.check == "BIND-PLAN-DELIVERABLE-MISMATCH" for x in got),
               "产品任务仍须匹配母计划归属")
        (ctrl / "source.md").write_text("# Source\n## Exact task\nTASK_ID=T1\n## Other\nTASK_ID=T2\n", encoding="utf-8")
        expect(local_source_reference(root, ctrl, "source.md#exact-task")[1]
               == "## Exact task\nTASK_ID=T1", "来源锚点不包含相邻任务")
        expect(local_source_reference(root, ctrl, "source.md:3")[1] == "TASK_ID=T1", "来源行号精确")
        for reference in ("../source.md", "/tmp/source.md", "source*.md", "missing.md",
                          "source.md#absent", "source.md:0", "source.md:3-2", "source.md:999",
                          "source.md%23exact-task", "C:\\source.md"):
            try:
                local_source_reference(root, ctrl, reference)
            except (OSError, ValueError):
                pass
            else:
                expect(False, f"拒绝无效来源 {reference}")
        source_board = board.replace("STATUS |", "STATUS | REQUIREMENT_SOURCE_REFERENCES |")
        source_board = source_board.replace("|---|---|---|---|", "|---|---|---|---|---|")
        source_board = source_board.replace("MAINLINE_IMPACT=NONE |", "MAINLINE_IMPACT=NONE | missing.md |")
        (ctrl / "TASK_BOARD.md").write_text(source_board, encoding="utf-8")
        got = []
        check_task_bindings(root, ctrl, "", got)
        expect(any(x.check == "BIND-SOURCE-INVALID" for x in got), "无效来源传播到绑定检查")

    with tempfile.TemporaryDirectory() as td:
        root, ctrl = Path(td), Path(td) / ".agent-control"
        ctrl.mkdir()
        (ctrl / "PM_REQUIREMENT_INTAKE.md").write_text(
            "## PM-RI-001\n```yaml\nINTAKE_ID: PM-RI-001\nUSER_CONFIRMED: false\n"
            "REQUIREMENT_MAPPING_ALLOWED: true\ntask_creation_allowed: true\n"
            "TASK_ID: T1\n```\n", encoding="utf-8")
        got: list[Finding] = []
        check_intake(root, ctrl, got)
        ids = {x.check for x in got}
        expect("INTK-MAPPING-ALLOWED" in ids, "未确认时禁止 Requirement Mapping")
        expect("INTK-TASK-ALLOWED" in ids, "未确认时禁止建任务（小写字段）")
        expect("INTK-EXEC-OBJECT" in ids, "未确认时执行字段必须为 null")

    with tempfile.TemporaryDirectory() as td:
        root, ctrl = Path(td), Path(td) / ".agent-control"
        ctrl.mkdir()
        digest = hashlib.sha256(b"hello").hexdigest()
        for name in static_files(root):
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"hello")
        (root / "SHA256SUMS.txt").write_text(
            "# BASE_COMMIT: example\n# GENERATED_AT: example\n"
            + "".join(f"{digest}  {name}\n" for name in static_files(root)), encoding="utf-8")
        target = root / "README.md"
        got = []
        check_integrity(root, ctrl, got)
        expect(not got, "一致时不应报错")
        target.write_text("tampered", encoding="utf-8")
        got = []
        check_integrity(root, ctrl, got)
        expect(any(x.severity == "VIOLATION" and "checksum mismatch: README.md" in x.evidence
                   for x in got), "篡改必须被检出")

    if failures:
        print("SELF-TEST FAILED:")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("SELF-TEST PASS")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Herdr 治理一致性校验器（只读）")
    ap.add_argument("--root", default=None,
                    help="herdr-team 目录，默认取脚本所在目录")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--strict", action="store_true", help="WARNING 也导致退出码 1")
    ap.add_argument("--self-test", action="store_true", help="只运行离线自检")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent
    ctrl = root / ".agent-control"
    if not ctrl.is_dir():
        print(f"错误：未找到 {ctrl}", file=sys.stderr)
        return 2

    mp_path = ctrl / "MASTER_PLAN.md"
    mp_text = read(mp_path) if mp_path.exists() else ""

    findings: list[Finding] = []
    for _label, fn in CHECKS:
        try:
            if fn is check_task_bindings:
                fn(root, ctrl, mp_text, findings)
            else:
                fn(root, ctrl, findings)
        except Exception as exc:  # 单条检查失败不应掩盖其他结果
            findings.append(Finding("CHECK-ERROR", "WARNING",
                                    f"检查 {fn.__name__} 执行失败：{type(exc).__name__}: {exc}"))

    findings.sort(key=lambda x: (SEVERITY_ORDER[x.severity], x.check))
    counts = {s: sum(1 for x in findings if x.severity == s) for s in SEVERITY_ORDER}

    if args.json:
        print(json.dumps({
            "root": str(root),
            "counts": counts,
            "findings": [x.as_dict() for x in findings],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"治理校验：{root}")
        print(f"VIOLATION={counts['VIOLATION']}  WARNING={counts['WARNING']}  INFO={counts['INFO']}")
        if not findings:
            print("\n未发现问题。")
        for sev in ("VIOLATION", "WARNING", "INFO"):
            group = [x for x in findings if x.severity == sev]
            if not group:
                continue
            print(f"\n[{sev}]")
            for x in group:
                print(f"  {x.check}: {x.message}")
                for e in x.evidence:
                    print(f"      - {e}")

    if counts["VIOLATION"] or (args.strict and counts["WARNING"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
