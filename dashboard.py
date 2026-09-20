#!/usr/bin/env python3
"""Local read-only execution dashboard for the LFA Herdr team."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

TEAM = ("lfa-start", "lfa-pm", "lfa-android", "lfa-api", "lfa-ios", "lfa-review")
ROOT = Path(__file__).resolve().parent
CONTROL = ROOT / ".agent-control"

PAGE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LFA 项目时间轴</title>
<style>
:root{color-scheme:dark;--bg:#090c0f;--panel:#11161b;--panel2:#171d23;--line:#34404b;--text:#eef3f7;--muted:#aab5bf;--blue:#78aaff;--green:#54d69b;--amber:#ffd166;--red:#ff8585;--focus:#fff}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:0}button{font:inherit}.shell{max-width:1700px;margin:auto;padding:16px}.skip{position:absolute;top:-60px;left:12px;background:var(--blue);color:#07111d;padding:10px 12px;z-index:20}.skip:focus{top:10px}.top,.controls,.summary,.project-head,.node-top,.drawer-head,.agent-line{display:flex;align-items:center}.top{justify-content:space-between;gap:16px;margin-bottom:12px}.brand h1{font-size:22px;margin:0}.brand p,.muted{color:var(--muted);margin:2px 0 0}.controls{gap:8px}.stamp{color:var(--muted);font-variant-numeric:tabular-nums}.icon{width:44px;height:44px;border:1px solid var(--line);border-radius:5px;background:var(--panel);color:var(--text);cursor:pointer}.icon svg{display:block;width:18px;height:18px;margin:auto;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.icon:hover,.icon[aria-pressed=true]{border-color:var(--blue);background:#172338}button:focus-visible,summary:focus-visible{outline:3px solid var(--focus);outline-offset:2px}.summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-bottom:12px}.metric,.board,.project{border:1px solid var(--line);background:var(--panel);border-radius:6px}.metric{padding:9px 12px;min-width:0}.metric b{display:block;font-size:18px;overflow-wrap:anywhere}.metric span{color:var(--muted);font-size:12px}.board{overflow:hidden}.board-title{padding:11px 13px;border-bottom:1px solid var(--line)}.board-title h2{font-size:16px;margin:0}.project{margin:10px;background:var(--panel2);overflow:hidden}.project-head{justify-content:space-between;gap:12px;padding:9px 11px;border-bottom:1px solid var(--line)}.project-head strong{font-size:15px}.project-head code{color:var(--muted);overflow-wrap:anywhere}.track-wrap{overflow-x:auto;padding:14px}.track{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(190px,1fr);align-items:stretch;gap:30px;min-width:max-content}.stage{position:relative;display:grid;gap:8px;align-content:center}.stage:not(:last-child)::after{content:"";position:absolute;left:100%;top:50%;width:30px;border-top:2px solid var(--line)}.stage:not(:last-child)::before{content:"";position:absolute;right:-30px;top:calc(50% - 4px);border:4px solid transparent;border-left-color:var(--line)}.node{position:relative;width:100%;min-height:112px;text-align:left;border:1px solid var(--line);border-left:4px solid var(--muted);border-radius:5px;background:#0f1419;color:var(--text);padding:10px;cursor:pointer}.node:hover{border-color:var(--blue);transform:translateY(-1px)}.node.accepted{border-left-color:var(--green)}.node.active,.node.running{border-left-color:var(--blue)}.node.warning,.node.repair{border-left-color:var(--amber)}.node.blocked,.node.error{border-left-color:var(--red)}.node-top{justify-content:space-between;gap:8px}.node-id{font:11px ui-monospace,monospace;color:var(--muted);overflow-wrap:anywhere}.node-name{display:block;font-weight:700;margin:5px 0}.node-meta{color:var(--muted);font-size:12px}.badge{display:inline-flex;align-items:center;min-height:23px;padding:2px 7px;border:1px solid var(--line);border-radius:999px;font-size:11px;line-height:1.3;overflow-wrap:anywhere}.accepted{color:var(--green);border-color:#287b5c}.active,.running{color:#b8d2ff;border-color:#416ea9}.warning,.repair{color:var(--amber);border-color:#806826}.blocked,.error{color:var(--red);border-color:#914545}.pending,.idle{color:var(--muted)}.drawer{width:min(620px,calc(100vw - 24px));height:100dvh;max-height:none;margin:0 0 0 auto;border:0;border-left:1px solid var(--line);background:var(--panel);color:var(--text);padding:0}.drawer::backdrop{background:#0009}.drawer-head{position:sticky;top:0;z-index:2;justify-content:space-between;gap:12px;padding:14px 16px;border-bottom:1px solid var(--line);background:var(--panel)}.drawer-head h2{font-size:18px;margin:0}.drawer-body{padding:16px}.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.detail{padding:10px;border:1px solid var(--line);border-radius:5px;background:var(--panel2);min-width:0;overflow-wrap:anywhere}.detail.wide{grid-column:1/-1}.detail h3{font-size:12px;color:var(--muted);margin:0 0 5px}.detail p{margin:0}.checks{list-style:none;padding:0;margin:0}.checks li{padding:7px 0;border-bottom:1px solid var(--line)}.checks li:last-child{border:0}.task-state{display:inline-block;width:16px;color:var(--green)}.agent-line{gap:8px;flex-wrap:wrap}.source-alert{margin:10px;padding:9px 12px;border:1px solid #806826;background:#2a2515;color:#ffe7a1;border-radius:5px}.diagnostics{margin:10px}.diagnostics summary{cursor:pointer;padding:10px;border:1px solid var(--line);border-radius:5px}.diagnostics-body{padding:10px;color:var(--muted)}@media(max-width:650px){body{font-size:16px}.shell{padding:10px}.top{align-items:flex-start;flex-direction:column}.controls{width:100%}.stamp{margin-right:auto;font-size:12px}.summary{grid-template-columns:repeat(2,minmax(0,1fr))}.project{margin:8px}.project-head{align-items:flex-start;flex-direction:column}.track{grid-auto-columns:minmax(235px,78vw)}.detail-grid{grid-template-columns:1fr}.detail.wide{grid-column:auto}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}.node:hover{transform:none}}
</style></head>
<body><a class="skip" href="#portfolio">跳到项目时间轴</a><main class="shell">
<header class="top"><div class="brand"><h1>LFA 项目时间轴</h1><p>项目 → 里程碑节点 → 执行任务 → Agent / Gate</p></div><div class="controls"><span id="stamp" class="stamp">加载中</span><button id="pause" class="icon" title="暂停自动刷新" aria-label="暂停自动刷新" aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg></button><button id="refresh" class="icon" title="立即刷新" aria-label="立即刷新"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11a8.1 8.1 0 0 0-15.5-2M4 4v5h5M4 13a8.1 8.1 0 0 0 15.5 2M20 20v-5h-5"/></svg></button></div></header>
<section class="summary" aria-label="项目摘要"><div class="metric"><b id="projectCount">-</b><span>项目</span></div><div class="metric"><b id="milestoneCount">-</b><span>里程碑节点</span></div><div class="metric"><b id="runningCount">-</b><span>执行中</span></div><div class="metric"><b id="blockedCount">-</b><span>等待 / 阻塞</span></div></section>
<section class="board" aria-labelledby="pmPlanTitle"><div class="board-title"><h2 id="pmPlanTitle">PM 当前执行清单</h2><p class="muted">PM 执行视图及调整记录，不替代 MASTER_PLAN 或任务 Gate。</p></div><div id="pmPlan" class="diagnostics-body">加载中</div></section>
<section id="portfolio" class="board"><div class="board-title"><h2>项目与里程碑</h2><p class="muted">横向按依赖推进；并行节点上下排列。点击任一节点查看唯一详情面板。</p></div><div id="sourceAlert" class="source-alert" role="status" hidden></div><div id="projects"></div><details class="diagnostics"><summary>来源与历史诊断</summary><div id="diagnostics" class="diagnostics-body"></div></details></section>
<style>#pmPlan li{margin:12px 0;overflow-wrap:anywhere}#pmPlan p,#pmHistory p{overflow-wrap:anywhere}</style>
</main><dialog id="drawer" class="drawer" aria-labelledby="drawerTitle"><div class="drawer-head"><h2 id="drawerTitle">节点详情</h2><button id="closeDrawer" class="icon" aria-label="关闭详情"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div><div id="drawerBody" class="drawer-body"></div></dialog>
<script>
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const fmt=t=>t?new Date(t*1000).toLocaleString():'未记录';const badge=(t,k='pending')=>`<span class="badge ${esc(k)}">${esc(t)}</span>`;let paused=false,timer,data,nodeIndex={};
function renderPM(p,agents){
  const root=document.querySelector('#pmPlan'),opened=new Set([...root.querySelectorAll('details[open]')].map(e=>e.dataset.key)),current=p.current;
  const describe=x=>esc(typeof x==='object'&&x!==null?JSON.stringify(x):x??'未映射');
  const revision=r=>`<p><b>${esc(r.revision||r.agent_revision)}</b> · ${esc(r.recorded_at)} · ${r.items.length} 项<br>${esc(r.reason)}<br>previous_revision: ${esc(r.previous_revision??'未提供')} · 发送原文摘要: ${esc(r.previous_submission_sha256??'未提供')}</p>`;
  const agentView=(name,id)=>{const a=agents.current[name],key=id+':'+name;return `<details data-key="${esc(key)}" ${opened.has(key)?'open':''}><summary>${esc(name)} · ${a?esc(a.agent_revision)+' · '+a.items.length+' 项':'PENDING · 缺失真实快照'}</summary>${a?revision(a)+`<p>上游 ${esc(a.parent_pm_revision)} · ${esc(a.parent_pm_todo_ids.join(', '))}</p><p class="muted">以下为该角色完整执行清单，不推断每项与当前 PM-TODO 一对一对应。</p><ol>${a.items.map(t=>`<li><code>${esc(t.id)}</code> ${badge(t.status)} ${esc(t.title)}<br>关联 ${describe(t.related_task_or_deliverable)}</li>`).join('')}</ol>`:''}</details>`};
  const h=current?.hierarchy||{};
  root.innerHTML=current?`<p>整体大计划：${esc(h.overall_goal??'未登记')}</p><p>当前计划：${esc(h.current_plan_section??'未登记')}<br>${describe(h.current_plan_reference??current.base_plan_version)}<br>${esc((h.registered_plans||[]).join(' → '))}</p><p>当前任务：${esc((h.registered_tasks||[]).join(' / '))}</p>${revision(current)}<ol class="pm-items">${current.items.map(i=>`<li><details data-key="${esc(i.id)}" ${opened.has(i.id)?'open':''}><summary><code>${esc(i.id)}</code> ${badge(i.status)} ${esc(i.title)}</summary><p>parent: ${describe(i.parent_task_or_deliverable)} · 关联 ${describe(i.related_task_or_deliverable)}</p>${current.blocked_reason?.[i.id]?`<p>${esc(current.blocked_reason[i.id])}</p>`:''}<p>participants: ${esc((i.participants||[]).join(', ')||'未登记')}</p>${(i.participants||[]).map(a=>agentView(a,i.id)).join('')}</details></li>`).join('')}</ol>`:'尚无 PM 完整快照';
  let history=document.querySelector('#pmHistory');if(!history){history=document.createElement('section');history.id='pmHistory';document.querySelector('.diagnostics').append(history)}
  history.innerHTML=`<h3>PM 执行清单 revision 历史</h3>${p.history.map(revision).join('')}<h3>Agent 完整快照历史</h3>${agents.history.map(revision).join('')}<p>缺失快照：${esc(agents.missing.join(', ')||'无')}</p><p class="error">${esc([...p.errors,...agents.errors].join('; '))}</p><p class="muted">发送原文摘要不是账本hash，不代表防篡改。TODO完成不等于业务Gate通过。</p>`;
}
function normalize(d){const qr=d.execution.workstream.nodes.map((n,i)=>({...n,kind:'当前执行节点',stage:i===0?0:i<3?1:i-1,subtasks:n.subtasks||[]}));const program=d.plan.milestones.map((m,i)=>({node_id:m.id,name:m.name,execution_status:m.status,tone:m.status==='ACCEPTED'?'accepted':m.status==='IN_PROGRESS'?'active':'pending',owner:'PROJECT_LEAD',dependencies:i?[d.plan.milestones[i-1].id]:[],stage:i,kind:'总体里程碑',subtasks:d.tasks.filter(t=>t.plan_id===m.id).map(t=>({id:t.id,title:t.deliverable_id,status:t.status,owner:t.owner}))}));const grouped={};d.tasks.forEach(t=>(grouped[t.plan_id]??=[]).push(t));const registered=Object.entries(grouped).filter(([id])=>!id.startsWith('M')).map(([id,ts])=>({id,name:id,status:ts.some(t=>/ACTIVE|IN_PROGRESS/.test(t.status))?'ACTIVE':'RECORDED',nodes:ts.map((t,i)=>({node_id:t.deliverable_id||t.id,name:t.id,task_id:t.id,owner:t.owner,execution_status:t.status,tone:/ACTIVE|IN_PROGRESS/.test(t.status)?'active':/BLOCK/.test(t.status)?'blocked':'pending',dependencies:i?[ts[i-1].deliverable_id||ts[i-1].id]:[],stage:i,kind:'登记任务',subtasks:[{id:t.id,title:t.deliverable_id,status:t.status,owner:t.owner}]}))}));return[{id:d.execution.goal.goal_id,name:d.execution.goal.name,status:d.execution.goal.status,nodes:qr},{id:'PROGRAM_MILESTONES',name:'Investor MVP 总体里程碑',status:d.plan.current_milestone,nodes:program},...registered.map(p=>({...p,nodes:p.nodes.map(n=>qr.find(q=>q.node_id===n.node_id)||n)}))]}
function nodeButton(n){nodeIndex[n.node_id]=n;return `<button class="node ${esc(n.tone)}" data-node="${esc(n.node_id)}"><span class="node-top"><span class="node-id">${esc(n.node_id)}</span>${badge(n.execution_status,n.tone)}</span><span class="node-name">${esc(n.name)}</span><span class="node-meta">${esc(n.owner||'未分配')} · ${n.subtasks.length} 项任务</span></button>`}
function renderProject(p){const stages={};p.nodes.forEach(n=>(stages[n.stage]??=[]).push(n));return `<article class="project"><div class="project-head"><div><strong>${esc(p.name)}</strong><br><code>${esc(p.id)}</code></div>${badge(p.status,/ACTIVE|IN_PROGRESS/.test(p.status)?'active':'pending')}</div><div class="track-wrap"><div class="track">${Object.values(stages).map(ns=>`<div class="stage">${ns.map(nodeButton).join('')}</div>`).join('')}</div></div></article>`}
function showNode(id){const n=nodeIndex[id],agent=data.agents.find(a=>n.owner?.includes(a.name));if(!n)return;document.querySelector('#drawerTitle').textContent=n.name;document.querySelector('#drawerBody').innerHTML=`<div class="detail-grid"><section class="detail"><h3>节点 / 执行模型</h3><p><b>${esc(n.node_id)}</b><br>${esc(n.model_summary||n.kind)}</p></section><section class="detail"><h3>执行 Agent</h3><p class="agent-line"><b>${esc(n.owner||'未分配')}</b>${agent?badge(agent.status,agent.status==='working'?'running':'idle'):''}</p>${agent?`<p class="muted">${esc(agent.title)}<br>${esc(agent.mapping_status)} · 观测 ${fmt(agent.observed_at)}</p>`:''}</section><section class="detail wide"><h3>里程碑 / 状态</h3><p>${badge(n.execution_status,n.tone)} · ${esc(n.milestone||n.name)}</p></section><section class="detail wide"><h3>前置依赖</h3><p>${esc(n.dependencies?.length?n.dependencies.join(' → '):'无')}</p></section><section class="detail wide"><h3>细化任务</h3><ul class="checks">${n.subtasks.length?n.subtasks.map(t=>`<li><span class="task-state">${/PASS|COMPLETE|ACCEPTED|CLOSED/.test(t.status)?'✓':'○'}</span><b>${esc(t.id)}</b> ${esc(t.title)}<br><span class="muted">${esc(t.status)}${t.owner?' · '+esc(t.owner):''}</span></li>`).join(''):'<li class="muted">尚未注册细化任务</li>'}</ul></section><section class="detail wide"><h3>Gate</h3><p>${n.gates?.length?n.gates.map(g=>badge(`${g.label}: ${g.status}`,g.tone)).join(' '):'无独立 Gate 记录'}</p></section><section class="detail wide"><h3>阻塞与下一步</h3><p>${esc(n.blocker||'无当前阻塞')}</p><p>${esc(n.next_action||'按登记状态推进')}</p></section><section class="detail wide"><h3>执行条件 / 证据</h3><p>${esc(n.execution_window||'未记录')}</p><p class="muted">${esc(n.source_ref||'TASK_BOARD.md / MASTER_PLAN.md')}</p></section></div>`;document.querySelector('#drawer').showModal()}
function render(d){data=d;nodeIndex={};const projects=normalize(d);document.querySelector('#projectCount').textContent=projects.length;document.querySelector('#milestoneCount').textContent=projects.reduce((n,p)=>n+p.nodes.length,0);document.querySelector('#runningCount').textContent=projects.reduce((n,p)=>n+p.nodes.filter(x=>/ACTIVE|IN_PROGRESS|RUNNING/.test(x.execution_status)).length,0);document.querySelector('#blockedCount').textContent=projects.reduce((n,p)=>n+p.nodes.filter(x=>/WAITING|BLOCK|PENDING_REREVIEW|CHANGES_REQUESTED/.test(x.execution_status)).length,0);document.querySelector('#projects').innerHTML=projects.map(renderProject).join('');document.querySelectorAll('[data-node]').forEach(b=>b.onclick=()=>showNode(b.dataset.node));const stale=d.source_health.filter(s=>s.status!=='OK');const alert=document.querySelector('#sourceAlert');alert.hidden=!stale.length;alert.textContent=stale.length?`来源提醒：${stale.map(s=>`${s.source_id} ${s.status}`).join('；')}`:'';document.querySelector('#diagnostics').innerHTML=`<p>数据生成 ${fmt(d.generated_at)} · Review ${esc(d.review.status)}</p><ul>${d.source_health.map(s=>`<li>${esc(s.source_id)} · ${esc(s.status)} · ${fmt(s.updated_at)}</li>`).join('')}</ul>`;document.querySelector('#stamp').textContent=`更新 ${new Date(d.generated_at*1000).toLocaleTimeString()}`}
async function load(){try{const r=await fetch('/api/status',{cache:'no-store'});if(!r.ok)throw new Error(`${r.status} ${r.statusText}`);const payload=await r.json();render(payload);renderPM(payload.pm_operational_plan,payload.agent_operational_plans)}catch(e){document.querySelector('#stamp').innerHTML=`<span class="error">刷新失败: ${esc(e.message)}</span>`}}function schedule(){clearInterval(timer);if(!paused)timer=setInterval(load,5000)}document.querySelector('#refresh').onclick=load;document.querySelector('#pause').onclick=e=>{paused=!paused;e.currentTarget.innerHTML=paused?'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m8 5 11 7-11 7Z"/></svg>':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg>';e.currentTarget.title=paused?'继续自动刷新':'暂停自动刷新';e.currentTarget.setAttribute('aria-label',e.currentTarget.title);e.currentTarget.setAttribute('aria-pressed',String(paused));schedule()};document.querySelector('#closeDrawer').onclick=()=>document.querySelector('#drawer').close();document.querySelector('#drawer').onclick=e=>{if(e.target===e.currentTarget)e.currentTarget.close()};load();schedule();
</script></body></html>'''



def run_json(*args: str) -> dict:
  completed = subprocess.run(args, cwd=ROOT.parent, text=True, capture_output=True, timeout=4, check=True)
  return json.loads(completed.stdout)


def read_text(name: str) -> str:
  try:
    return (CONTROL / name).read_text(encoding="utf-8")
  except FileNotFoundError:
    return ""


def source_health(name: str) -> dict:
  path = CONTROL / name
  try:
    updated_at = path.stat().st_mtime
    age_seconds = max(0, time.time() - updated_at)
    return {"source_id": name, "status": "STALE" if age_seconds > 86_400 else "OK", "updated_at": updated_at, "age_seconds": age_seconds}
  except OSError as error:
    return {"source_id": name, "status": "UNAVAILABLE", "updated_at": None, "age_seconds": None, "error": str(error)}


def parse_gate() -> dict[str, str]:
  result = {}
  for line in read_text("PM_GATE").splitlines():
    key, separator, value = line.partition(":")
    if separator:
      result[key.strip()] = value.strip()
  return result


def parse_plan() -> dict:
  text = read_text("MASTER_PLAN.md")
  headers = {}
  for line in text.splitlines():
    if line.startswith("## "):
      break
    key, separator, value = line.partition(":")
    if separator and key.isupper():
      headers[key] = value.strip()
  milestones = []
  section = ""
  for line in text.splitlines():
    if line.startswith("## "):
      section = line[3:]
      continue
    if section != "Milestones" or not line.startswith("| M"):
      continue
    columns = [part.strip() for part in line.strip("|").split("|")]
    if len(columns) >= 4:
      milestones.append({"id": columns[0], "name": columns[1], "status": columns[3]})
  return {"current_milestone": headers.get("CURRENT_MILESTONE", ""), "current_deliverable": headers.get("CURRENT_DELIVERABLE", ""), "progress": headers.get("PROGRAM_PROGRESS", ""), "milestones": milestones}


def parse_tasks() -> list[dict[str, str]]:
  tasks = []
  headers = []
  in_task_table = False
  for line in read_text("TASK_BOARD.md").splitlines():
    if not line.startswith("|"):
      if in_task_table and line.strip():
        break
      continue
    columns = [part.strip() for part in line.strip().strip("|").split("|")]
    if "TASK_ID" in columns:
      headers = [column.upper() for column in columns]
      in_task_table = True
      continue
    if not in_task_table or all(not column.strip("-: ") for column in columns):
      continue
    row = dict(zip(headers, columns))
    if row.get("TASK_ID"):
      tasks.append({"plan_id": row.get("PLAN_ID", ""), "deliverable_id": row.get("DELIVERABLE_ID", ""), "id": row["TASK_ID"], "owner": row.get("OWNER", ""), "status": row.get("STATUS", "")})
  return tasks


def load_evidence(name: str) -> dict:
  try:
    return json.loads((CONTROL / "EVIDENCE" / name).read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError):
    return {}

def evidence_tasks(name: str) -> list[dict]:
  return [
    {"id": item.get("TODO_ID", ""), "title": item.get("Goal", ""), "status": "COMPLETE", "owner": ""}
    for item in load_evidence(name).get("requirement_btw_checks", [])
  ]


def recent_output(name: str) -> str:
  completed = subprocess.run(("herdr", "agent", "read", name, "--source", "recent-unwrapped", "--lines", "14"), cwd=ROOT.parent, text=True, capture_output=True, timeout=4)
  return (completed.stdout or completed.stderr).strip()[-4_000:]


def gate(label: str, status: str, tone: str) -> dict:
  return {"label": label, "status": status, "tone": tone}


def execution_projection(agents: list[dict], table_tasks: list[dict]) -> dict:
  table_ids = {task["id"] for task in table_tasks}
  by_name = {agent["name"]: agent for agent in agents}
  node1_tasks = evidence_tasks("QR-PC-01-D01.json")
  node3_tasks = evidence_tasks("QR-FINAL-01-D01.json")
  android_output = by_name.get("lfa-android", {}).get("output", "")
  progress_match = re.search(r"Android QR implementation\s*[·:]\s*(\d+/\d+)", android_output)
  android_progress = progress_match.group(1) if progress_match else "进度未结构化"
  review_text = read_text("REVIEW_QUEUE.md")
  evidence = load_evidence("QR-FINAL-01-D01.json")
  node3_changes = "QR-FINAL-01 actual CHANGES_REQUESTED" in review_text
  repaired_revision_ready = evidence.get("status") == "IMPLEMENTED_PENDING_REVIEW" and len(evidence.get("implementation_files", [])) >= 11
  node3_review_accepted = "QR-FINAL-01 repaired revision independent Review accepted" in review_text and "c99cfa6d411f3181fe0453f0b34c786bf4ce44287e6c795e66b964369ee3a538" in review_text
  node3_pm_accepted = node3_review_accepted and "Actual existing lfa-pm PM_ACCEPTED" in review_text and "15214bytes" in review_text
  node1 = {
    "node_id": "QR-PC-01-D01", "name": "产品声明契约", "task_id": "RUN-20260918-QR-PC", "owner": "lfa-api", "dependencies": [], "execution_status": "ACCEPTED", "tone": "accepted", "milestone": "冻结产品声明、Schema、Registry 语义", "model_summary": "严格声明解析 + trusted Registry + JCS/SHA 身份绑定", "next_action": "冻结契约，供 Node2/Node3 使用", "execution_window": "已完成", "source_ref": "MASTER_PLAN.md:359-381; TASK_BOARD.md:448-459; EVIDENCE/QR-PC-01-D01.json", "blocker": "", "linkage_conflict": "RUN-20260918-QR-PC" not in table_ids, "subtasks": node1_tasks,
    "gates": [gate("Review", "ACCEPTED", "accepted"), gate("PM", "ACCEPTED", "accepted")],
  }
  node2 = {
    "node_id": "QR-ANDROID-01-D01", "name": "Android QR 最小实现", "task_id": "RUN-20260918-QR-ANDROID", "owner": "lfa-android", "dependencies": ["QR-PC-01-D01"], "execution_status": "ACTIVE", "tone": "active", "milestone": "预览识别、快门单次验证、Bundle 声明持久化", "model_summary": "Android preview QR 状态机 + shutter verification attempt + Capture Bundle 1.5 持久化", "next_action": f"完成快门绑定、声明持久化与生命周期检查；当前观测 {android_progress}", "execution_window": "与最终 JPEG 复核并行；无时长基线", "source_ref": "MASTER_PLAN.md:369-381; TASK_BOARD.md:448-459; lfa-android recent output", "blocker": "", "linkage_conflict": "RUN-20260918-QR-ANDROID" not in table_ids,
    "subtasks": [{"id": "QR-ANDROID-01-01", "title": "预览 QR 状态机", "status": "COMPLETE", "owner": "lfa-android"}, {"id": "QR-ANDROID-01-02", "title": "快门绑定一次验证尝试", "status": "PENDING", "owner": "lfa-android"}, {"id": "QR-ANDROID-01-03", "title": "产品声明写入 Capture Bundle", "status": "PENDING", "owner": "lfa-android"}, {"id": "QR-ANDROID-01-04", "title": "生命周期与延迟回调检查", "status": "PENDING", "owner": "lfa-android"}],
    "gates": [gate("作者验证", "IN_PROGRESS", "active"), gate("Review", "PENDING", "pending"), gate("PM", "PENDING", "pending"), gate("真机证据", "PENDING", "pending")],
  }
  node2_receipt = re.search(r"^### Node2 independent Review return and original-owner repair dispatch\n(.*?)(?=^### |^## |\Z)", read_text("TASK_BOARD.md"), re.MULTILINE | re.DOTALL)
  if node2_receipt and "CODE_REVIEW=CHANGES_REQUESTED, PM_GATE=NOT_ACCEPTED" in node2_receipt[1]:
    node2.update(execution_status="CHANGES_REQUESTED", tone="repair", next_action="修复中：原 lfa-android 修复四项 HIGH；新精确 revision 交同一 Reviewer 复审，再进入 PM Gate。", blocker="QR-ANDROID-R1..R4 四项 HIGH 未关闭；同 revision 双 Gate 未通过", source_ref="TASK_BOARD.md: Node2 independent Review return and original-owner repair dispatch")
    node2["subtasks"] = [{"id": finding, "title": detail, "status": "CHANGES_REQUESTED", "owner": "lfa-android"} for finding, detail in re.findall(r"^- (QR-ANDROID-R\d+): (.+)$", node2_receipt[1], re.MULTILINE)]
    node2["gates"] = [gate("作者修复", "IN_PROGRESS", "active"), gate("Review", "CHANGES_REQUESTED", "changes_requested"), gate("PM", "NOT_ACCEPTED", "pending"), gate("真机证据", "PENDING", "pending")]
  node3 = {
    "node_id": "QR-FINAL-01-D01", "name": "最终 JPEG QR 复核", "task_id": "RUN-20260918-QR-FINAL", "owner": "lfa-api", "dependencies": ["QR-PC-01-D01"], "execution_status": "PM_ACCEPTED" if node3_pm_accepted else ("WAITING_PM" if node3_review_accepted else ("WAITING_REVIEW" if repaired_revision_ready else ("REPAIRING" if node3_changes else "WAITING_REVIEW"))), "tone": "accepted" if node3_pm_accepted else ("warning" if repaired_revision_ready else ("repair" if node3_changes else "warning")), "milestone": "持久化完整 JPEG 上独立 QR 复核后进入同一 DheaRuntime", "model_summary": "cv2.QRCodeDetector + UTF-8 payload SHA-256 + trusted Registry + unchanged DheaRuntime.analyze", "next_action": "保持冻结，等待 Node2 后进入集成依赖检查" if node3_pm_accepted else ("由 lfa-pm 对精确 Evidence revision 执行独立 Gate" if node3_review_accepted else ("提交已修复冻结 revision，由 lfa-review 复审" if repaired_revision_ready else "修复 R1-R4，冻结新 revision 后重新提交非作者 Review")), "execution_window": "已完成双 Gate" if node3_pm_accepted else "与 Android 节点并行；Review 通过后进入 PM Gate", "source_ref": "MASTER_PLAN.md:383; TASK_BOARD.md:461-465; REVIEW_QUEUE.md:592-604; EVIDENCE/QR-FINAL-01-D01.json", "blocker": "" if node3_pm_accepted else ("等待同一 Evidence revision 的 PM Gate" if node3_review_accepted else "等待该 Evidence digest 被非作者 Review 和 PM Gate 精确绑定"), "linkage_conflict": "RUN-20260918-QR-FINAL" not in table_ids, "subtasks": node3_tasks,
    "gates": [gate("作者验证", "COMPLETE" if repaired_revision_ready else "IN_PROGRESS", "accepted" if repaired_revision_ready else "active"), gate("Review", "ACCEPTED" if node3_review_accepted else ("PENDING_REREVIEW" if repaired_revision_ready else ("CHANGES_REQUESTED" if node3_changes else "PENDING")), "accepted" if node3_review_accepted else ("warning" if repaired_revision_ready else ("changes_requested" if node3_changes else "pending"))), gate("PM", "ACCEPTED" if node3_pm_accepted else ("PENDING" if node3_review_accepted else "NOT_READY"), "accepted" if node3_pm_accepted else "pending"), gate("真机证据", "PENDING", "pending")],
  }
  integration = {
    "node_id": "QR-INTEGRATION", "name": "完整 JPEG 上传与结果闭环", "task_id": "待注册", "owner": "lfa-pm / START", "dependencies": ["QR-ANDROID-01-D01", "QR-FINAL-01-D01"], "execution_status": "WAITING_DEPENDENCY", "tone": "pending", "milestone": "Android → API → Core → App/Web 自动闭环", "model_summary": "标准 multipart API + immutable JPEG + UnifiedAnalysisRequest + DheaRuntime", "next_action": "等待 Android 与最终 JPEG 节点同 revision 双 Gate 完成后注册并调度", "execution_window": "双依赖完成后", "source_ref": "MASTER_PLAN.md:373-375", "blocker": "等待 QR-ANDROID-01-D01 与 QR-FINAL-01-D01", "linkage_conflict": False, "subtasks": [{"id": "QR-E2E-AUTO", "title": "完整 JPEG 上传、存储、Core、结果、诊断、App 自动闭环", "status": "WAITING_DEPENDENCY", "owner": "lfa-pm / START"}],
    "gates": [gate("依赖", "NOT_READY", "pending"), gate("集成", "NOT_AUTHORIZED", "pending")],
  }
  device = {
    "node_id": "QR-DEVICE-EVIDENCE", "name": "指定 Android 真机证据", "task_id": "外部证据", "owner": "PROJECT_LEAD / designated operator", "dependencies": ["QR-INTEGRATION"], "execution_status": "WAITING_DEPENDENCY", "tone": "pending", "milestone": "真实拍摄与端到端证据链", "model_summary": "指定设备受控拍摄；原始 JPEG、SHA、API、Core、App/Web 逐段绑定", "next_action": "集成通过后执行真实拍摄、原图 SHA、上传、Core、App/Web 证据链", "execution_window": "集成完成且指定设备可用后", "source_ref": "MASTER_PLAN.md:375", "blocker": "等待 QR-INTEGRATION", "linkage_conflict": False, "subtasks": [{"id": "DEVICE-CAPTURE", "title": "真实 Android 拍摄与完整原始 JPEG", "status": "PENDING", "owner": "designated operator"}, {"id": "DEVICE-TRACE", "title": "original_sha256、上传、Core、App/Web 全链路", "status": "PENDING", "owner": "PROJECT_LEAD"}],
    "gates": [gate("真机证据", "PENDING", "pending")],
  }
  nodes = [node1, node2, node3, integration, device]
  tasks = []
  blocker = "" if node3_pm_accepted else ("原 revision 的 Review R1-R4 已返工；等待新 revision 非作者复审。R1-R4：证据归因、replay/409 观察范围、OpenAPI/生成物同步、原 JPEG 失败状态" if repaired_revision_ready else ("Review R1-R4：证据归因、replay/409 观察范围、OpenAPI/生成物同步、原 JPEG 失败状态" if node3_changes else ""))
  for wave, node in [(1, node1), (2, node2), (2, node3), (3, integration), (4, device)]:
    tasks.append({**node, "title": node["name"], "breadcrumb": f"QIUQIU DHEA QR 产品识别 → QR 产品识别 → {node['node_id']}", "wave": wave, "queue_position": "当前并行" if wave == 2 else ("已完成" if wave == 1 else f"等待波次 {wave - 1}"), "blocker": blocker if node is node3 else (f"等待：{', '.join(node['dependencies'])}" if node["dependencies"] and wave > 2 else node["blocker"]), "source_ref": node["source_ref"] + ("; REVIEW_QUEUE.md:592-604; EVIDENCE/QR-FINAL-01-D01.json" if node is node3 else "")})
  return {"goal": {"goal_id": "QIUQIU_DHEA_QR_PRODUCT_IDENTIFICATION_END_TO_END", "name": "QIUQIU DHEA QR 产品识别端到端", "status": "ACTIVE"}, "workstream": {"workstream_id": "QR_PRODUCT_IDENTIFICATION", "name": "QR 产品识别（独立于几何研究）", "status": "ACTIVE", "integration_status": "NOT_AUTHORIZED", "current_wave": 2, "next_wave_label": "波次 3 · 集成", "nodes": nodes, "waves": [{"number": 1, "label": "契约冻结", "node_ids": [node1["node_id"]]}, {"number": 2, "label": "并行实现", "node_ids": [node2["node_id"], node3["node_id"]]}, {"number": 3, "label": "集成闭环", "node_ids": [integration["node_id"]]}, {"number": 4, "label": "真机证据", "node_ids": [device["node_id"]]}]}, "tasks": tasks}


def review_payload() -> dict:
  text = read_text("REVIEW_QUEUE.md")
  evidence = load_evidence("QR-FINAL-01-D01.json")
  accepted = "QR-FINAL-01 repaired revision independent Review accepted" in text and "c99cfa6d411f3181fe0453f0b34c786bf4ce44287e6c795e66b964369ee3a538" in text
  pm_accepted = accepted and "Actual existing lfa-pm PM_ACCEPTED" in text and "15214bytes" in text
  status = "PM_ACCEPTED" if pm_accepted else ("CODE_REVIEW_ACCEPTED_PM_PENDING" if accepted else ("REPAIRED_REVISION_PENDING_REREVIEW" if evidence.get("status") == "IMPLEMENTED_PENDING_REVIEW" and len(evidence.get("implementation_files", [])) >= 11 else ("CURRENT_CHANGES_REQUESTED" if "QR-FINAL-01 actual CHANGES_REQUESTED" in text else "RECORDED")))
  return {"status": status, "submissions": re.findall(r'^## .*submission.*$', text, re.MULTILINE)}


def parse_pm_operational_plan(text: str | None = None) -> dict:
  text = read_text("TASK_BOARD.md") if text is None else text
  history, errors = [], []
  sections = re.findall(r"^## PM_OPERATIONAL_PLAN_REVISIONS\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
  for section in sections:
    for raw in re.findall(r"^```json pm-operational-plan\s*\n(.*?)^```\s*$", section, re.MULTILINE | re.DOTALL):
      try:
        snapshot = json.loads(raw)
        if not isinstance(snapshot, dict) or any(not isinstance(snapshot.get(k), str) or not snapshot[k].strip() for k in ("revision", "recorded_at", "reason")) or not isinstance(snapshot.get("base_plan_version"), (str, dict)) or not snapshot["base_plan_version"]:
          raise ValueError("missing snapshot metadata")
        items = snapshot.get("items")
        if not isinstance(items, list) or any(not isinstance(i, dict) or any(not isinstance(i.get(k), str) or not i[k].strip() for k in ("id", "title", "status")) or "related_task_or_deliverable" not in i or (i["related_task_or_deliverable"] is not None and not isinstance(i["related_task_or_deliverable"], str)) for i in items):
          raise ValueError("invalid complete items")
        if len({i["id"] for i in items}) != len(items):
          raise ValueError("duplicate stable item id")
        previous = next((r for r in history if r["revision"] == snapshot["revision"]), None)
        if previous is not None:
          if previous != snapshot:
            raise ValueError("conflicting revision " + snapshot["revision"])
          continue
        history.append(snapshot)
      except (ValueError, TypeError) as error:
        errors.append("PM operational snapshot: " + str(error))
    for raw in re.findall(r"^```json pm-operational-plan-correction\s*\n(.*?)^```\s*$", section, re.MULTILINE | re.DOTALL):
      try:
        correction = json.loads(raw)
        target = next(r for r in history if r["revision"] == correction["correction_of"])
        fields = correction["corrections"]
        replacements = []
        for path, value in fields.items():
          if path != "publication_policy" and not path.startswith("blocked_reason."):
            raise ValueError("not a supplementary text field")
          parent = target
          parts = path.split(".")
          for key in parts[:-1]:
            parent = parent[key]
          old = parent[parts[-1]]
          if not isinstance(value, str) or not isinstance(old, str) or value.replace(" ", "") != old.replace(" ", ""):
            raise ValueError("transcription supplement changes more than spaces")
          replacements.append((parent, parts[-1], value))
        for parent, key, value in replacements:
          parent[key] = value
      except (ValueError, TypeError, KeyError, StopIteration) as error:
        errors.append("PM transcription supplement: " + str(error))
  current = history[-1] if history else None
  markers = re.findall(r"^CURRENT_PM_OPERATIONAL_REVISION: (\S+)\s*$", "\n".join(sections), re.MULTILINE)
  if current and (not markers or markers[-1] != current["revision"]):
    errors.append("PM current revision marker missing or inconsistent")
  return {"current_revision": current["revision"] if current else None, "current": current, "history": history, "errors": errors}


def parse_agent_operational_plans(pm: dict, text: str | None = None) -> dict:
  text = read_text("TASK_BOARD.md") if text is None else text
  history, current, errors, seen = [], {}, [], {}
  parents = {p["revision"]: p for p in pm["history"]}
  for section in re.findall(r"^## AGENT_OPERATIONAL_PLAN_REVISIONS\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL):
    for raw in re.findall(r"^```json agent-operational-plan\s*\n(.*?)^```\s*$", section, re.MULTILINE | re.DOTALL):
      try:
        s = json.loads(raw)
        if not isinstance(s, dict) or any(not isinstance(s.get(k), str) or not s[k].strip() for k in ("agent", "agent_revision", "recorded_at", "reason", "parent_pm_revision")):
          raise ValueError("missing agent metadata")
        if datetime.fromisoformat(s["recorded_at"].replace("Z", "+00:00")).utcoffset() != timedelta(0):
          raise ValueError("recorded_at must be UTC")
        parent = parents.get(s["parent_pm_revision"])
        refs = s.get("parent_pm_todo_ids")
        if not parent or not isinstance(refs, list) or not refs or any(not isinstance(r, str) for r in refs) or len(set(refs)) != len(refs):
          raise ValueError("invalid parent PM revision or references")
        parent_items = {i["id"]: i for i in parent["items"]}
        if any(r not in parent_items or s["agent"] not in parent_items[r].get("participants", []) for r in refs):
          raise ValueError("unregistered PM participant reference")
        items = s.get("items")
        if not isinstance(items, list) or any(not isinstance(i, dict) or any(not isinstance(i.get(k), str) or not i[k].strip() for k in ("id", "title", "status")) or i["status"] not in ("pending", "in_progress", "completed", "blocked", "abandoned") or "related_task_or_deliverable" not in i or not isinstance(i["related_task_or_deliverable"], (str, dict, type(None))) for i in items):
          raise ValueError("invalid complete agent items")
        if len({i["id"] for i in items}) != len(items):
          raise ValueError("duplicate agent item id")
        key = (s["agent"], s["agent_revision"])
        if key in seen:
          if seen[key] != s:
            raise ValueError("conflicting agent revision " + s["agent_revision"])
          continue
        seen[key] = s
        history.append(s)
        current[s["agent"]] = s
      except (ValueError, TypeError, KeyError) as error:
        errors.append("Agent operational snapshot: " + str(error))
  expected = sorted({a for i in (pm.get("current") or {}).get("items", []) for a in i.get("participants", [])})
  return {"current": current, "history": history, "missing": [a for a in expected if a not in current], "errors": errors}


def status_payload() -> dict:
  errors = []
  try:
    rows = run_json("herdr", "agent", "list").get("result", {}).get("agents", [])
  except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
    rows = []
    errors.append(f"agent list: {error}")
  named = {row.get("name"): row for row in rows if row.get("name") in TEAM}
  task_links = {"lfa-android": "RUN-20260918-QR-ANDROID", "lfa-api": "RUN-20260918-QR-FINAL", "lfa-start": "RUN-20260918-QR-FINAL", "lfa-review": "RUN-20260918-QR-FINAL", "lfa-pm": "QIUQIU_DHEA_QR_PRODUCT_IDENTIFICATION_END_TO_END"}
  tasks = parse_tasks()
  table_ids = {task["id"] for task in tasks}
  agents = []
  for name in TEAM:
    row = named.get(name, {})
    output = ""
    if row:
      try:
        output = recent_output(name)
      except (OSError, subprocess.SubprocessError) as error:
        errors.append(f"{name}: {error}")
    linked_task_id = task_links.get(name)
    mapping_status = "REGISTERED_MATCH" if linked_task_id in table_ids else ("INFERRED_MATCH" if linked_task_id else "UNMAPPED")
    agents.append({"name": name, "status": row.get("agent_status", "not_running"), "pane": row.get("pane_id", ""), "title": row.get("terminal_title_stripped", ""), "output": output, "linked_task_id": linked_task_id, "mapping_status": mapping_status, "observed_at": time.time()})
  pm = parse_pm_operational_plan()
  return {"generated_at": time.time(), "gate": parse_gate(), "plan": parse_plan(), "pm_operational_plan": pm, "agent_operational_plans": parse_agent_operational_plans(pm), "tasks": tasks, "execution": execution_projection(agents, tasks), "review": review_payload(), "blockers": read_text("BLOCKERS.md"), "agents": agents, "source_health": [source_health(name) for name in ("MASTER_PLAN.md", "TASK_BOARD.md", "REVIEW_QUEUE.md", "BLOCKERS.md")], "errors": errors}


class Handler(BaseHTTPRequestHandler):
  def do_GET(self) -> None:
    if self.path == "/":
      self.respond(PAGE.encode(), "text/html; charset=utf-8")
    elif self.path == "/api/status":
      self.respond(json.dumps(status_payload(), ensure_ascii=False).encode(), "application/json; charset=utf-8")
    else:
      self.send_error(404)

  def respond(self, body: bytes, content_type: str) -> None:
    try:
      self.send_response(200)
      self.send_header("Content-Type", content_type)
      self.send_header("Content-Length", str(len(body)))
      self.send_header("Cache-Control", "no-store")
      self.end_headers()
      self.wfile.write(body)
    except (BrokenPipeError, ConnectionResetError):
      pass

  def log_message(self, format: str, *args: object) -> None:
    pass


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--host", default="127.0.0.1")
  parser.add_argument("--port", type=int, default=8765)
  parser.add_argument("--check", action="store_true", help="Validate and print one status snapshot")
  args = parser.parse_args()
  if args.check:
    sample = {"revision": "check-1", "recorded_at": "2026-01-01T00:00:00Z", "reason": "parser check", "base_plan_version": "check", "items": [{"id": "stable", "title": "Full title", "status": "pending", "related_task_or_deliverable": None}]}
    newer = {**sample, "revision": "check-2", "items": [{**sample["items"][0], "status": "completed"}]}
    history_text = "## PM_OPERATIONAL_PLAN_REVISIONS\n" + "".join("```json pm-operational-plan\n" + json.dumps(s) + "\n```\nCURRENT_PM_OPERATIONAL_REVISION: " + s["revision"] + "\n" for s in (sample, newer))
    parsed = parse_pm_operational_plan(history_text)
    assert parsed["current"] == newer and parsed["history"] == [sample, newer] and not parsed["errors"]
    damaged = parse_pm_operational_plan(history_text + "```json pm-operational-plan\n{broken}\n```\n")
    assert damaged["current"] == newer and damaged["errors"]
    assert parse_pm_operational_plan("")["current"] is None
    sample["items"][0]["participants"] = ["test-agent"]
    pm_check = {"current": sample, "history": [sample]}
    agent_sample = {"agent": "test-agent", "agent_revision": "a1", "recorded_at": "2026-01-01T00:00:00Z", "reason": "check", "parent_pm_revision": "check-1", "parent_pm_todo_ids": ["stable"], "items": sample["items"]}
    def agent_blocks(*snapshots):
      return "## AGENT_OPERATIONAL_PLAN_REVISIONS\n" + "".join("```json agent-operational-plan\n" + json.dumps(s) + "\n```\n" for s in snapshots)
    checked = parse_agent_operational_plans(pm_check, agent_blocks(agent_sample, agent_sample))
    assert checked["current"]["test-agent"] == agent_sample and len(checked["history"]) == 1 and not checked["errors"]
    assert parse_agent_operational_plans(pm_check, "")["missing"] == ["test-agent"]
    for changes in ({"reason": "conflicting same revision"}, {"parent_pm_revision": "unknown"}, {"parent_pm_todo_ids": ["unknown"]}, {"agent": "outsider"}, {"items": [sample["items"][0]] * 2}, {"items": [{}]}):
      assert parse_agent_operational_plans(pm_check, agent_blocks(agent_sample, {**agent_sample, **changes}))["errors"]
    updated_agent = {**agent_sample, "agent_revision": "a2", "items": [{**sample["items"][0], "status": "completed"}]}
    assert parse_agent_operational_plans(pm_check, agent_blocks(agent_sample, updated_agent))["current"]["test-agent"] == updated_agent
    payload = status_payload()
    assert not payload["pm_operational_plan"]["errors"], payload["pm_operational_plan"]["errors"]
    assert not payload["agent_operational_plans"]["errors"], payload["agent_operational_plans"]["errors"]
    nodes = payload["execution"]["workstream"]["nodes"]
    assert len(nodes) == 5
    assert nodes[1]["dependencies"] == ["QR-PC-01-D01"]
    assert nodes[2]["dependencies"] == ["QR-PC-01-D01"]
    assert nodes[3]["dependencies"] == ["QR-ANDROID-01-D01", "QR-FINAL-01-D01"]
    assert nodes[4]["dependencies"] == ["QR-INTEGRATION"]
    assert len(nodes[1]["subtasks"]) == 4
    assert nodes[1]["execution_status"] == "CHANGES_REQUESTED"
    assert nodes[1]["gates"][1] == gate("Review", "CHANGES_REQUESTED", "changes_requested")
    assert {s["id"] for s in nodes[1]["subtasks"]} == {f"QR-ANDROID-R{i}" for i in range(1, 5)}
    assert all(s["status"] == "CHANGES_REQUESTED" for s in nodes[1]["subtasks"])
    assert payload["execution"]["tasks"][1]["blocker"] == nodes[1]["blocker"] != ""
    assert len(nodes[2]["subtasks"]) == 12
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return
  server = ThreadingHTTPServer((args.host, args.port), Handler)
  print(f"LFA PM Dashboard: http://{args.host}:{args.port}", flush=True)
  server.serve_forever()


if __name__ == "__main__":
  main()
