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

TEAM = ("lfa-start", "lfa-pm", "lfa-android", "lfa-api", "lfa-ios", "lfa-review", "lfa-grok-review", "lfa-claude-review")
ROOT = Path(__file__).resolve().parent
CONTROL = ROOT / ".agent-control"
SHADOW_PROJECTION = CONTROL / "MACHINE" / "HARNESS-VERIFICATION-SHADOW" / "qr-android-projection.json"

PAGE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LFA 项目观察台</title>
<style>
:root{color-scheme:dark;--bg:#0b0e11;--panel:#12171c;--panel2:#181e24;--line:#35414c;--text:#f1f5f8;--muted:#aab5bf;--blue:#78aaff;--green:#54d69b;--amber:#ffd166;--red:#ff8585;--focus:#fff}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:0}button{font:inherit}.shell{max-width:1500px;margin:auto;padding:16px}.skip{position:absolute;top:-60px;left:12px;background:var(--blue);color:#07111d;padding:10px 12px;z-index:20}.skip:focus{top:10px}.top,.controls,.summary,.project-head,.node-top,.drawer-head,.agent-line{display:flex;align-items:center}.top{justify-content:space-between;gap:16px;margin-bottom:12px}.brand h1{font-size:22px;margin:0}.brand p,.muted{color:var(--muted);margin:2px 0 0}.controls{gap:8px}.stamp{color:var(--muted);font-variant-numeric:tabular-nums}.icon{width:44px;height:44px;border:1px solid var(--line);border-radius:5px;background:var(--panel);color:var(--text);cursor:pointer}.icon svg{display:block;width:18px;height:18px;margin:auto;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.icon:hover,.icon[aria-pressed=true]{border-color:var(--blue);background:#172338}button:focus-visible,summary:focus-visible{outline:3px solid var(--focus);outline-offset:2px}.summary{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:0 0 12px}.metric,.board,.project{border:1px solid var(--line);background:var(--panel);border-radius:6px}.metric{padding:8px 12px;min-width:0}.metric b{display:block;font-size:17px;overflow-wrap:anywhere}.metric span{color:var(--muted);font-size:12px}.board{overflow:hidden}.board-title{padding:11px 13px;border-bottom:1px solid var(--line)}.board-title h2{font-size:16px;margin:0}.project{margin:10px;background:var(--panel2);overflow:hidden}.project-head{justify-content:space-between;gap:12px;padding:9px 11px;border-bottom:1px solid var(--line)}.project-head strong{font-size:15px}.project-head code{color:var(--muted);overflow-wrap:anywhere}.track-wrap{padding:14px}.track{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(210px,100%),1fr));align-items:stretch;gap:16px}.stage{position:relative;display:grid;gap:8px;align-content:center}.stage::after,.stage::before{display:none}.node{position:relative;width:100%;min-height:108px;text-align:left;border:1px solid var(--line);border-left:4px solid var(--muted);border-radius:5px;background:#0f1419;color:var(--text);padding:10px;cursor:pointer}.node:hover{border-color:var(--blue);transform:translateY(-1px)}.node.accepted{border-left-color:var(--green);opacity:.78}.node.active,.node.running{border-left-color:var(--blue);background:#111c29}.node.warning,.node.repair{border-left-color:var(--amber);background:#211d12}.node.blocked,.node.error{border-left-color:var(--red);background:#211415}.node-top{justify-content:space-between;gap:8px}.node-id{font:11px ui-monospace,monospace;color:var(--muted);overflow-wrap:anywhere}.node-name{display:block;font-weight:700;margin:5px 0}.node-meta{color:var(--muted);font-size:12px}.badge{display:inline-flex;align-items:center;min-height:23px;padding:2px 7px;border:1px solid var(--line);border-radius:999px;font-size:11px;line-height:1.3;overflow-wrap:anywhere}.accepted{color:var(--green);border-color:#287b5c}.active,.running{color:#b8d2ff;border-color:#416ea9}.warning,.repair{color:var(--amber);border-color:#806826}.blocked,.error{color:var(--red);border-color:#914545}.pending,.idle{color:var(--muted)}.drawer{width:min(620px,calc(100vw - 24px));height:100dvh;max-height:none;margin:0 0 0 auto;border:0;border-left:1px solid var(--line);background:var(--panel);color:var(--text);padding:0}.drawer::backdrop{background:#0009}.drawer-head{position:sticky;top:0;z-index:2;justify-content:space-between;gap:12px;padding:14px 16px;border-bottom:1px solid var(--line);background:var(--panel)}.drawer-head h2{font-size:18px;margin:0}.drawer-body{padding:16px}.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.detail{padding:10px;border:1px solid var(--line);border-radius:5px;background:var(--panel2);min-width:0;overflow-wrap:anywhere}.detail.wide{grid-column:1/-1}.detail h3{font-size:12px;color:var(--muted);margin:0 0 5px}.detail p{margin:0}.checks{list-style:none;padding:0;margin:0}.checks li{padding:7px 0;border-bottom:1px solid var(--line)}.checks li:last-child{border:0}.task-state{display:inline-block;width:16px;color:var(--green)}.agent-line{gap:8px;flex-wrap:wrap}.source-alert{margin:0 0 12px;padding:9px 12px;border:1px solid #806826;background:#2a2515;color:#ffe7a1;border-radius:5px}.diagnostics-body{padding:10px;color:var(--muted)}@media(max-width:650px){body{font-size:14px}.shell{padding:10px}.top{align-items:flex-start;flex-direction:column}.controls{width:100%}.stamp{margin-right:auto;font-size:12px}.summary{grid-template-columns:repeat(3,minmax(0,1fr))}.project{margin:8px}.project-head{align-items:flex-start;flex-direction:column}.track-wrap{overflow:visible;padding:12px 14px}.track{display:grid;grid-auto-flow:row;grid-template-columns:1fr;gap:12px;min-width:0;border-left:2px solid var(--line);padding-left:14px}.stage{display:grid}.node{min-height:0}.detail-grid{grid-template-columns:1fr}.detail.wide{grid-column:auto}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}.node:hover{transform:none}}
</style></head>
<body><a class="skip" href="#portfolio">跳到当前交付路径</a><main class="shell">
<header class="top"><div class="brand"><h1>LFA 项目观察台</h1><p id="workstreamName">当前交付状态与下一动作</p></div><div class="controls"><span id="stamp" class="stamp">加载中</span><button id="pause" class="icon" title="暂停自动刷新" aria-label="暂停自动刷新" aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg></button><button id="refresh" class="icon" title="立即刷新" aria-label="立即刷新"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11a8.1 8.1 0 0 0-15.5-2M4 4v5h5M4 13a8.1 8.1 0 0 0 15.5 2M20 20v-5h-5"/></svg></button></div></header>
<p class="readonly"><b>只读项目观察台</b><span>状态由 herdr-team 权威记录提供；本页面不派单、不审批、不修改状态，也不操作 Agent。</span></p>
<div id="sourceAlert" class="source-alert" role="status" hidden></div>
<nav class="view-tabs" role="tablist" aria-label="观察台视图"><button id="tab-current" role="tab" aria-selected="true" aria-controls="view-current" data-view="current">当前执行</button><button id="tab-plan" role="tab" aria-selected="false" aria-controls="view-plan" data-view="plan" tabindex="-1">计划与历史</button><button id="tab-diagnostics" role="tab" aria-selected="false" aria-controls="view-diagnostics" data-view="diagnostics" tabindex="-1">诊断</button></nav>
<div id="view-current" class="view-panel" role="tabpanel" aria-labelledby="tab-current" data-panel="current">
<section class="program-board board" aria-labelledby="programTitle"><div class="board-title"><span class="eyebrow">当前主线</span><h2 id="programTitle">项目现在处于哪里</h2><p id="programSummary" class="muted">来自 MASTER_PLAN</p></div><div id="programStrip" class="program-strip"></div></section>
<section class="overview" aria-labelledby="overviewTitle"><div class="overview-head"><div><span class="eyebrow">实时执行</span><h2 id="overviewTitle">当前 LFA Agent</h2></div><button id="focusAction" class="focus-action" type="button">查看执行详情</button></div><div class="overview-grid"><article><span>当前主线</span><strong id="currentFocus">加载中</strong></article><article><span>实时执行</span><strong id="currentOwner">加载中</strong></article><article class="blocker-card"><span>任务归属</span><strong id="currentBlocker">加载中</strong></article><article><span>当前交付状态</span><strong id="nextOwner">加载中</strong></article><article class="next-step"><span>下一 Gate</span><strong id="nextAction">加载中</strong></article></div><p id="stateConflict" class="state-conflict" hidden></p></section>
<section class="summary" aria-label="实时执行摘要"><div class="metric"><b id="actionCount">-</b><span>活跃 Agent</span></div><div class="metric"><b id="runningCount">-</b><span>已映射任务</span></div><div class="metric"><b id="blockedCount">-</b><span>UNMAPPED</span></div></section>
<section id="portfolio" class="board primary-board"><div class="board-title"><span class="eyebrow">实时会话</span><h2>当前 Agent 会话</h2><p class="muted">显示 Herdr 当前在线的命名 LFA Agent、实时会话标题及状态；任务归属必须来自 TASK_BOARD。</p></div><div class="browser-tools" role="search"><label for="nodeSearch">查找 Agent</label><input id="nodeSearch" type="search" placeholder="Agent、任务或归属" autocomplete="off"><label for="nodeStatus">状态</label><select id="nodeStatus"><option value="">全部状态</option><option value="active">执行中</option><option value="waiting">空闲或等待</option></select><span id="filterResult" role="status" aria-live="polite"></span></div><div id="currentProject"></div></section>
</div>
<div id="view-plan" class="view-panel" role="tabpanel" aria-labelledby="tab-plan" data-panel="plan" hidden><section class="board"><div class="board-title"><span class="eyebrow">母计划</span><h2>总体路线详情</h2><p class="muted">完整 M0-M7 节点。</p></div><div id="programProject"></div></section><section class="board"><div class="board-title"><span class="eyebrow">登记记录</span><h2>其他已登记工作</h2><p class="muted">账本投影与历史任务，非实时执行。</p></div><div id="otherProjects"></div></section></div>
<div id="view-diagnostics" class="view-panel" role="tabpanel" aria-labelledby="tab-diagnostics" data-panel="diagnostics" hidden><section class="global" aria-labelledby="globalTitle"><div class="board-title"><span class="eyebrow">来源状态</span><h2 id="globalTitle">项目全局态势</h2><p class="muted">以下数字来自不同权威记录，保留各自口径。</p></div><div class="global-grid"><div class="metric"><b id="globalActionCount">-</b><span>未完成 PM 项</span></div><div class="metric"><b id="globalBlockedCount">-</b><span>阻塞 PM 项</span></div><div class="metric"><b id="globalWorkingCount">-</b><span>执行中 Agent</span></div><div class="metric"><b id="globalSourceCount">-</b><span>异常来源</span></div></div><div id="managementIssues" class="issues" aria-live="polite"></div></section><section class="board"><div class="board-title"><span class="eyebrow">执行记录</span><h2 id="pmPlanTitle">执行清单与 revision 历史</h2></div><div id="pmPlan" class="diagnostics-body">加载中</div><div class="diagnostics-body"><div id="diagnostics"></div><section id="pmHistory"></section></div></section><section class="board shadow-board" aria-labelledby="shadowTitle"><div class="board-title"><span class="eyebrow">证据诊断</span><h2 id="shadowTitle">验证投影</h2><p class="muted">只读诊断，不改变正式 Gate。</p></div><div id="shadowProjection" class="shadow-content" aria-live="polite" aria-busy="true">加载中</div></section></div>
<style>.program-board{margin-bottom:12px}.program-strip{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:1px;background:var(--line)}.program-step{min-width:0;padding:10px;background:var(--panel)}.program-step.current{background:#111c29;border-top:3px solid var(--blue)}.program-step.done{border-top:3px solid var(--green)}.program-step.parked{opacity:.62}.program-step code{display:block;color:var(--muted);font-size:11px}.program-step strong{display:block;margin:3px 0;overflow-wrap:anywhere}.program-step small{color:var(--muted)}.overview-grid{grid-template-columns:1fr 1fr 1.25fr 1fr!important}.overview-grid .next-step{grid-column:1/-1}.view-tabs{display:flex;gap:4px;margin:0 0 12px;padding:4px;border:1px solid var(--line);border-radius:6px;background:var(--panel);overflow-x:auto}.view-tabs button{min-width:max-content;min-height:44px;padding:0 16px;border:0;border-radius:4px;background:transparent;color:var(--muted);font-weight:700;cursor:pointer}.view-tabs button[aria-selected="true"]{background:#20324e;color:var(--text)}.view-tabs button:focus-visible{outline:3px solid var(--focus);outline-offset:1px}.view-panel[hidden]{display:none}.view-panel>.board,.view-panel>.global{margin-bottom:12px}@media(max-width:1100px){.program-strip{grid-template-columns:repeat(4,minmax(0,1fr))}}@media(max-width:650px){.program-strip{grid-template-columns:1fr}.view-tabs{scrollbar-width:thin}}</style>
<style>@media(max-width:900px){.overview-grid{grid-template-columns:1fr 1fr!important}}@media(max-width:650px){.overview-grid{grid-template-columns:1fr!important}}</style>
<style>html,body{max-width:100%;overflow-x:hidden}.readonly{display:flex;gap:10px;align-items:baseline;margin:0 0 12px;padding:9px 12px;border:1px solid #416ea9;border-radius:5px;background:#111c29}.readonly span{color:var(--muted)}.global{margin-bottom:12px;border:1px solid var(--line);border-radius:6px;background:var(--panel);overflow:hidden}.global-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--line)}.global-grid .metric{border:0;border-radius:0}.issues{padding:0 13px}.issues ul{margin:8px 0 10px;padding-left:20px}.issues li{margin:4px 0;overflow-wrap:anywhere}.browser-tools{display:grid;grid-template-columns:auto minmax(180px,1fr) auto minmax(130px,220px) auto;align-items:center;gap:8px;padding:10px 13px;border-bottom:1px solid var(--line)}.browser-tools label{color:var(--muted);font-size:12px}.browser-tools input,.browser-tools select{min-width:0;min-height:44px;border:1px solid var(--line);border-radius:5px;background:#0f1419;color:var(--text);padding:0 10px;font:inherit}.browser-tools input:focus-visible,.browser-tools select:focus-visible{outline:3px solid var(--focus);outline-offset:2px}.browser-tools #filterResult{color:var(--muted);font-size:12px}.node[hidden]{display:none}.eyebrow{display:block;color:var(--blue);font-size:11px;font-weight:700;text-transform:uppercase}.overview{margin-bottom:12px;border:1px solid #416ea9;border-radius:6px;background:var(--panel)}.overview-head{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 14px;border-bottom:1px solid var(--line)}.overview-head h2{margin:2px 0 0;font-size:18px}.focus-action{min-height:44px;padding:0 14px;border:1px solid #416ea9;border-radius:5px;background:#172338;color:var(--text);font-weight:700;cursor:pointer}.focus-action:hover{background:#20324e}.overview-grid{display:grid;grid-template-columns:1.4fr 1fr .65fr 1.4fr;gap:1px;background:var(--line)}.overview-grid article{min-width:0;padding:12px 13px;background:var(--panel)}.overview-grid .blocker-card{background:#211d12;border-top:3px solid var(--amber)}.overview-grid span{display:block;margin-bottom:4px;color:var(--muted);font-size:12px}.overview-grid strong{display:block;font-size:14px;line-height:1.45;overflow-wrap:anywhere}.state-conflict{margin:0;padding:9px 13px;color:#ffe7a1;background:#2a2515;border-top:1px solid #806826}.primary-board{margin-bottom:12px}.auxiliary{margin:12px 0}.auxiliary>summary{cursor:pointer;padding:12px 13px;list-style-position:inside}.auxiliary>summary span{display:inline-flex;align-items:baseline;gap:10px}.auxiliary>summary small{color:var(--muted);font-weight:400}.shadow-content{padding:10px 13px;min-width:0;overflow-wrap:anywhere}.shadow-state{margin:0}.shadow-statuses{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:10px}.shadow-status{min-width:0;padding:8px 10px;background:var(--panel2)}.shadow-status span{display:block;color:var(--muted);font-size:12px}.shadow-status strong,.shadow-value{font-family:ui-monospace,monospace;overflow-wrap:anywhere;word-break:break-word}.shadow-status strong{display:block;margin-top:2px}.shadow-section{padding:9px 0;border-top:1px solid var(--line)}.shadow-section:first-of-type{border-top:0}.shadow-section h3{font-size:13px;margin:0 0 6px}.shadow-fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 14px;margin:0}.shadow-fields div{min-width:0}.shadow-fields dt{color:var(--muted);font-size:12px}.shadow-fields dd{margin:0}.shadow-list{margin:0;padding-left:20px}.shadow-list li{padding:2px 0;overflow-wrap:anywhere}.shadow-error{color:var(--red)}.recorded-projects{margin:10px}.recorded-projects>summary,.pm-complete>summary{cursor:pointer;padding:10px 12px}.recorded-projects .project{opacity:.82}.shadow-node-rows{display:none}.pm-focus{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.pm-actions{margin:8px 0}.pm-complete{margin-top:10px;border-top:1px solid var(--line)}#pmPlan li{margin:8px 0;overflow-wrap:anywhere}#pmPlan p,#pmHistory p{overflow-wrap:anywhere}@media(max-width:900px){.overview-grid{grid-template-columns:1fr 1fr}.global-grid{grid-template-columns:1fr 1fr}.shadow-statuses,.shadow-fields{grid-template-columns:1fr}}@media(max-width:650px){.readonly{align-items:flex-start;flex-direction:column;gap:2px}.overview-grid{grid-template-columns:1fr}.overview-head{align-items:stretch;flex-direction:column}.focus-action{width:100%}.browser-tools{grid-template-columns:1fr}.browser-tools label{margin-bottom:-5px}.auxiliary>summary span{align-items:flex-start;flex-direction:column;gap:2px}}@media(max-width:500px){.shadow-statuses,.shadow-fields{grid-template-columns:1fr}}</style>
<style>.empty-state{margin:0;padding:24px 14px;text-align:center;color:var(--muted)}.empty-state b{color:var(--text);font-size:16px}.focus-action:disabled{cursor:not-allowed;opacity:.5}</style>
<style>.agent-label{display:inline-flex;align-items:center;gap:6px}.agent-label svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}</style>
</main><dialog id="drawer" class="drawer" aria-labelledby="drawerTitle"><div class="drawer-head"><h2 id="drawerTitle">节点详情</h2><button id="closeDrawer" class="icon" aria-label="关闭详情"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div><div id="drawerBody" class="drawer-body"></div></dialog>
<script>
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const fmt=t=>t?new Date(t*1000).toLocaleString():'未记录';const statusText=t=>({ACCEPTED:'已通过',PM_ACCEPTED:'PM 已通过',SUPERSEDED:'已被修正',PARTIAL:'部分完成',HOLD:'暂停',HOLD_FOR_CONTRACT_CORRECTION:'等待契约修正',UNFROZEN:'未冻结',CHANGES_REQUESTED:'需要修改',WAITING_DEPENDENCY:'等待依赖',WAITING_REVIEW:'等待复审',WAITING_PM:'等待 PM',PENDING_REREVIEW:'等待复审',REPAIRING:'修复中',NOT_READY:'未就绪',NOT_AUTHORIZED:'未授权',IN_PROGRESS:'执行中',ACTIVE:'执行中',RUNNING:'执行中',IDLE:'空闲',DONE:'已完成',BLOCKED:'等待输入',UNKNOWN:'状态未知',NOT_STARTED:'未开始',PARKED:'已停放',RECORDED:'已记录',completed:'已完成',pending:'待处理',blocked:'阻塞',working:'执行中',idle:'空闲',done:'已完成',unknown:'状态未知'}[t]||t);const badge=(t,k='pending')=>`<span class="badge ${esc(k)}" title="${esc(t)}">${esc(statusText(t))}</span>`;let paused=false,loading=false,timer,data,nodeIndex={},shadowProjection=null,openNodeId=null,lastSuccess=null,currentView='current',focusNodeId=null;
function renderPM(p,agents){
  const root=document.querySelector('#pmPlan'),opened=new Set([...root.querySelectorAll('details[open]')].map(e=>e.dataset.key)),current=p.current;
  const describe=x=>esc(typeof x==='object'&&x!==null?JSON.stringify(x):x??'未映射');
  const revision=r=>`<p><b>${esc(r.revision||r.agent_revision)}</b> · ${esc(r.recorded_at)} · ${r.items.length} 项<br>${esc(r.reason)}<br>previous_revision: ${esc(r.previous_revision??'未提供')} · 发送原文摘要: ${esc(r.previous_submission_sha256??'未提供')}</p>`;
  const agentView=(name,id)=>{const a=agents.current[name],key=id+':'+name;return `<details data-key="${esc(key)}" ${opened.has(key)?'open':''}><summary>${esc(name)} · ${a?esc(a.agent_revision)+' · '+a.items.length+' 项':'PENDING · 缺失真实快照'}</summary>${a?revision(a)+`<p>上游 ${esc(a.parent_pm_revision)} · ${esc(a.parent_pm_todo_ids.join(', '))}</p><p class="muted">以下为该角色完整执行清单，不推断每项与当前 PM-TODO 一对一对应。</p><ol>${a.items.map(t=>`<li><code>${esc(t.id)}</code> ${badge(t.status)} ${esc(t.title)}<br>关联 ${describe(t.related_task_or_deliverable)}</li>`).join('')}</ol>`:''}</details>`};
  const h=current?.hierarchy||{};
  const counts=current?.items.reduce((out,i)=>(out[i.status]=(out[i.status]||0)+1,out),{})||{},actionable=current?.items.filter(i=>!['completed','abandoned'].includes(i.status))||[];
  const item=i=>`<li><details data-key="${esc(i.id)}" ${opened.has(i.id)?'open':''}><summary><code>${esc(i.id)}</code> ${badge(i.status)} ${esc(i.title)}</summary><p>parent: ${describe(i.parent_task_or_deliverable)} · 关联 ${describe(i.related_task_or_deliverable)}</p>${current.blocked_reason?.[i.id]?`<p>${esc(current.blocked_reason[i.id])}</p>`:''}<p>participants: ${esc((i.participants||[]).join(', ')||'未登记')}</p>${(i.participants||[]).map(a=>agentView(a,i.id)).join('')}</details></li>`;
  root.innerHTML=current?`<div class="pm-focus"><b>${esc(h.current_plan_section??'当前计划未登记')}</b>${Object.entries(counts).map(([status,count])=>badge(`${status}: ${count}`,status)).join('')}</div><p>当前任务：${esc((h.registered_tasks||[]).join(' / ')||'未登记')}</p><ol class="pm-actions">${actionable.length?actionable.map(i=>`<li><code>${esc(i.id)}</code> ${badge(i.status)} ${esc(i.title)}</li>`).join(''):'<li class="muted">无未完成行动项</li>'}</ol><details class="pm-complete" data-key="pm-complete" ${opened.has('pm-complete')?'open':''}><summary>完整 PM 执行清单 · ${current.items.length} 项</summary><p>整体大计划：${esc(h.overall_goal??'未登记')}</p><p>当前计划：${describe(h.current_plan_reference??current.base_plan_version)}<br>${esc((h.registered_plans||[]).join(' → '))}</p>${revision(current)}<ol class="pm-items">${current.items.map(item).join('')}</ol></details>`:'尚无 PM 完整快照';
  let history=document.querySelector('#pmHistory');if(!history){history=document.createElement('section');history.id='pmHistory';document.querySelector('#view-diagnostics').append(history)}
  history.innerHTML=`<h3>PM 执行清单 revision 历史</h3>${p.history.map(revision).join('')}<h3>Agent 完整快照历史</h3>${agents.history.map(revision).join('')}<p>缺失快照：${esc(agents.missing.join(', ')||'无')}</p><p class="error">${esc([...p.errors,...agents.errors].join('; '))}</p><p class="muted">发送原文摘要不是账本hash，不代表防篡改。TODO完成不等于业务Gate通过。</p>`;
}
function renderShadow(state){
  const root=document.querySelector('#shadowProjection'),value=v=>esc(v===null?'null':Array.isArray(v)?JSON.stringify(v):typeof v==='object'?JSON.stringify(v):v),field=(k,v)=>`<div><dt>${esc(k)}</dt><dd class="shadow-value">${value(v)}</dd></div>`;
  root.setAttribute('aria-busy','false');
  if(!state||state.status!=='AVAILABLE'){root.innerHTML=`<p class="shadow-state shadow-error" role="status"><b>验证投影 ${esc(state?.status||'不可用')}</b><br>${esc(state?.error||'投影数据不可用')}</p>`;return}
  const p=state.projection,legacy=Object.values(nodeIndex).find(n=>n.task_id===p.task_id),status=(k,v)=>`<div class="shadow-status"><span>${esc(k)}</span><strong>${value(v)}</strong></div>`;
  root.innerHTML=`<div class="shadow-statuses" aria-label="验证投影状态">${status('任务',p.task_id)}${status('目标 revision',p.subject_revision)}${status('接收状态',p.ingestion_status)}${status('证据状态',p.evidence_status)}${status('验收状态',p.acceptance_status)}${status('正式阶段',legacy?.execution_status??'未匹配')}</div><p><b>作用：</b>不改变正式阶段、不调度、不代表通过。</p>${p.criteria.map((c,i)=>`<article class="shadow-section" aria-labelledby="criterion-${i}"><h3 id="criterion-${i}">判据 ${esc(c.criterion_id)}</h3><dl class="shadow-fields">${field('criterion_id',c.criterion_id)}${field('required',c.required)}${field('status',c.status)}${field('generation',c.generation)}${field('selected_event_id',c.selected_event_id)}${field('superseded_event_ids',c.superseded_event_ids)}${field('evidence_refs',c.evidence_refs)}${field('reason_codes',c.reason_codes)}</dl></article>`).join('')}<section class="shadow-section"><h3>诊断</h3><ul class="shadow-list">${p.diagnostics.length?p.diagnostics.map(d=>`<li class="shadow-value">${value(d)}</li>`).join(''):'<li class="shadow-value">[]</li>'}</ul></section><section class="shadow-section"><h3>投影来源</h3><dl class="shadow-fields">${field('generated_from_event_digest',p.generated_from_event_digest)}${field('reducer_version',p.reducer_version)}</dl></section>`;
}

function normalize(d){const live=d.execution.workstream.nodes.map(n=>({...n,kind:'实时 Agent 会话',stage:n.stage??0,subtasks:[]}));const program=d.plan.milestones.map((m,i)=>({node_id:m.id,name:m.name,execution_status:m.status,tone:m.status==='ACCEPTED'?'accepted':m.status==='IN_PROGRESS'?'active':'pending',owner:'PROJECT_LEAD',dependencies:i?[d.plan.milestones[i-1].id]:[],stage:i,kind:'总体里程碑',subtasks:d.tasks.filter(t=>t.plan_id===m.id).map(t=>({id:t.id,title:`${t.deliverable_id} → ${t.id}`,status:t.status,owner:t.owner}))}));const registeredProjection={id:d.registered_execution.workstream.workstream_id,name:d.registered_execution.workstream.name,status:'RECORDED',nodes:d.registered_execution.workstream.nodes.map(n=>({...n,kind:'账本投影，非实时执行',subtasks:n.subtasks||[]}))};const grouped={};d.tasks.forEach(t=>(grouped[t.plan_id]??=[]).push(t));const registered=Object.entries(grouped).filter(([id])=>!id.startsWith('M')).map(([id,ts])=>({id,name:id,status:'RECORDED',nodes:ts.map((t,i)=>({node_id:`${id}-${i}-${t.id}`,name:t.deliverable_id||t.id,task_id:t.id,execution_status:t.status,tone:/ACCEPTED|DONE|COMPLETE/.test(t.status)?'accepted':'pending',owner:t.owner,dependencies:[],stage:i,kind:'已登记任务，非实时执行',subtasks:[]}))}));return [{id:d.execution.workstream.workstream_id,name:d.execution.workstream.name,status:d.execution.workstream.status,nodes:live},{id:'MASTER_PLAN',name:'总体路线',status:d.plan.progress,nodes:program},registeredProjection,...registered]}
function agentIcon(name){const paths=name==='lfa-start'?'<path d="m5 9 4-4 4 4M9 5v14M13 15h6M16 12l3 3-3 3"/>':name==='lfa-pm'?'<path d="M9 5h10M9 12h10M9 19h10M5 5h.01M5 12h.01M5 19h.01"/>':/android|ios/.test(name)?'<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>':name==='lfa-api'?'<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01"/>':'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>';return `<svg viewBox="0 0 24 24" aria-hidden="true">${paths}</svg>`}
function shadowRows(n){const p=shadowProjection;if(!p||n.task_id!==p.task_id)return '';const legacyEvidence=n.gates?.find(g=>g.label==='作者验证')?.status??'未记录',legacyAcceptance=n.gates?.find(g=>g.label==='PM')?.status??'未记录';return `<span class="shadow-node-rows"><b></b><b>Evidence</b><b>Acceptance</b><b>Legacy</b><span>${esc(legacyEvidence)}</span><span>${esc(legacyAcceptance)}</span><b>Shadow</b><span>${esc(p.evidence_status)}</span><span>${esc(p.acceptance_status)}</span></span>`}
function nodeButton(n){nodeIndex[n.node_id]=n;if(n.kind==='实时 Agent 会话')return `<button class="node ${esc(n.tone)}" data-node="${esc(n.node_id)}"><span class="node-top"><span class="node-id agent-label">${agentIcon(n.owner)}Agent ${esc(n.owner||'未命名')}</span>${badge(n.execution_status,n.tone)}</span><span class="node-name">${esc(n.name)}</span></button>`;const taskText=n.subtasks.length?`${n.subtasks.length} 项主任务`:'未登记主任务';return `<button class="node ${esc(n.tone)}" data-node="${esc(n.node_id)}"><span class="node-top"><span class="node-id">${esc(n.node_id)}</span>${badge(n.execution_status,n.tone)}</span><span class="node-name">${esc(n.name)}</span><span class="node-meta">${esc(n.owner||'未分配')} · ${taskText}</span>${shadowRows(n)}</button>`}
function renderProject(p){const stages={};p.nodes.forEach(n=>(stages[n.stage]??=[]).push(n));return `<article class="project"><div class="project-head"><div><strong>${esc(p.name)}</strong><br><code>${esc(p.id)}</code></div>${badge(p.status,/ACTIVE|IN_PROGRESS/.test(p.status)?'active':'pending')}</div><div class="track-wrap"><div class="track">${Object.values(stages).map(ns=>`<div class="stage">${ns.map(nodeButton).join('')}</div>`).join('')}</div></div></article>`}
function setNodeUrl(id,replace=false){const url=new URL(location.href);id?url.searchParams.set('node',id):url.searchParams.delete('node');history[replace?'replaceState':'pushState']({},'',url)}
function sourceRefs(n){const refs=(n.source_ref||'TASK_BOARD.md / MASTER_PLAN.md').split(';').map(x=>x.trim()).filter(Boolean);return `<ul class="source-refs">${refs.map(r=>`<li><code>${esc(r)}</code></li>`).join('')}</ul>`}
function showNode(id,{updateUrl=true}={}){const n=nodeIndex[id];if(!n)return false;openNodeId=id;const agent=data.agents.find(a=>n.owner?.includes(a.name)),shadow=shadowRows(n),unregistered=agent?.snapshot_status==='CURRENT_SNAPSHOT_UNREGISTERED',taskHeading=n.kind==='实时 Agent 会话'?'当前会话任务':'主任务清单';document.querySelector('#drawerTitle').textContent=n.name;document.querySelector('#drawerBody').innerHTML=`<div class="detail-grid"><section class="detail wide"><h3>阻塞与下一步</h3><p>${esc(n.blocker||'无当前阻塞')}</p><p>${esc(n.next_action||'按登记状态推进')}</p></section><section class="detail"><h3>负责人</h3><p class="agent-line"><b>${esc(n.current_actor||n.owner||'未分配')}</b>${agent?badge(agent.status,agent.status==='working'?'running':'idle'):''}</p>${n.next_actor?`<p class="muted">下一接棒：${esc(n.next_actor)}</p>`:''}${agent?`<p class="muted">${esc(agent.title)}<br>${esc(agent.mapping_status)} · ${esc(agent.snapshot_status)} · 观测 ${fmt(agent.observed_at)}</p>`:''}</section><section class="detail"><h3>状态</h3><p>${badge(n.execution_status,n.tone)} · ${esc(n.milestone||n.name)}</p>${shadow}</section><section class="detail wide"><h3>${taskHeading}</h3><p class="muted">${n.kind==='实时 Agent 会话'?'当前执行任务以 Herdr 实时会话标题为准。登记快照仅在“计划与历史”和“诊断”中作为参考，不代表当前执行项。':'以下是登记的主任务，不代表当前 Agent 正在执行。'}</p><ul class="checks">${n.subtasks.length?n.subtasks.map(t=>`<li><span class="task-state">${/PASS|COMPLETE|ACCEPTED|CLOSED/i.test(t.status)?'✓':'○'}</span><b>${esc(t.id)}</b> ${esc(t.title)}<br><span class="muted">${esc(statusText(t.status))}${t.owner?' · '+esc(t.owner):''}</span></li>`).join(''):`<li class="muted">${unregistered?'当前 TODO 快照未登记':n.kind==='实时 Agent 会话'?'当前会话标题即当前执行任务':'未登记主任务'}${unregistered?'<br><span class="muted">终端 TODO 仅为观察，不作为权威细化任务。</span>':''}</li>`}</ul></section>${n.gates?.length?`<section class="detail wide"><h3>Gate</h3><p>${n.gates.map(g=>badge(`${g.label}: ${g.status}`,g.tone)).join(' ')}</p></section>`:''}<section class="detail"><h3>节点 / 执行模型</h3><p><b>${esc(n.node_id)}</b><br>${esc(n.model_summary||n.kind)}</p></section><section class="detail"><h3>并行前置条件</h3><ul class="checks">${n.dependencies?.length?n.dependencies.map(x=>`<li><code>${esc(x)}</code></li>`).join(''):'<li>无</li>'}</ul></section>${n.release_condition?`<section class="detail wide"><h3>解除条件</h3><p>${esc(n.release_condition)}</p>`:''}<section class="detail wide"><h3>执行条件</h3><p>${esc(n.execution_window||'未记录')}</p></section><section class="detail wide"><h3>证据定位</h3>${sourceRefs(n)}</section></div>`;const drawer=document.querySelector('#drawer');if(!drawer.open)drawer.showModal();if(updateUrl)setNodeUrl(id);return true}
function closeNode({updateUrl=true}={}){openNodeId=null;const drawer=document.querySelector('#drawer');if(drawer.open)drawer.close();if(updateUrl)setNodeUrl(null)}
function filterGroup(n){return /ACCEPTED|PM_ACCEPTED/.test(n.execution_status)?'accepted':/ACTIVE|IN_PROGRESS|RUNNING|REPAIRING|WORKING/.test(n.execution_status)?'active':/WAITING|BLOCK|IDLE|DONE|UNKNOWN|PENDING|NOT_READY|NOT_AUTHORIZED|HOLD|UNFROZEN/.test(n.execution_status)?'waiting':'action'}
function applyFilters(){const query=document.querySelector('#nodeSearch').value.trim().toLowerCase(),status=document.querySelector('#nodeStatus').value,buttons=[...document.querySelectorAll('#currentProject [data-node]')];let shown=0;buttons.forEach(button=>{const n=nodeIndex[button.dataset.node],match=(!query||[n.node_id,n.name,n.owner,n.task_id].some(v=>String(v||'').toLowerCase().includes(query)))&&(!status||filterGroup(n)===status);button.hidden=!match;if(match)shown++});document.querySelector('#filterResult').textContent=`显示 ${shown}/${buttons.length}`}
function collectConflicts(d){const out=[];d.execution.workstream.nodes.filter(n=>n.linkage_conflict).forEach(n=>out.push(`${n.node_id}：任务映射未登记`));const byRelated=new Map((d.pm_operational_plan.current?.items||[]).map(i=>[i.related_task_or_deliverable,i]));d.execution.workstream.nodes.filter(n=>n.execution_status!=='SUPERSEDED').forEach(n=>{const p=byRelated.get(n.node_id);if(p?.status==='completed'&&!/ACCEPTED|PM_ACCEPTED/.test(n.execution_status))out.push(`${n.node_id}：PM 清单已完成，但节点 ${statusText(n.execution_status)}`)});d.errors.forEach(e=>out.push(`数据读取：${e}`));return [...new Set(out)]}
function renderGlobal(d){const items=d.pm_operational_plan.current?.items||[],conflicts=collectConflicts(d);document.querySelector('#globalActionCount').textContent=items.filter(i=>!['completed','abandoned'].includes(i.status)).length;document.querySelector('#globalBlockedCount').textContent=items.filter(i=>i.status==='blocked').length;document.querySelector('#globalWorkingCount').textContent=d.agents.filter(a=>a.status==='working').length;document.querySelector('#globalSourceCount').textContent=d.source_health.filter(s=>s.status!=='OK').length;document.querySelector('#managementIssues').innerHTML=conflicts.length?`<ul>${conflicts.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:'<p class="muted">未发现跨来源状态冲突。</p>'}
function renderManagerView(d){document.querySelector('#programStrip').innerHTML=d.plan.milestones.map(m=>`<div class="program-step ${m.id===d.plan.current_milestone?'current':m.status==='ACCEPTED'?'done':m.status==='PARKED'?'parked':''}"><code>${esc(m.id)}</code><strong>${esc(m.name)}</strong><small>${esc(statusText(m.status))}</small></div>`).join('')}
function renderOverview(d){const nodes=d.execution.workstream.nodes,current=nodes[0],record=d.plan.current_deliverable_record,warning=document.querySelector('#stateConflict');focusNodeId=current?.node_id??null;document.querySelector('#workstreamName').textContent=`主线 ${d.plan.current_milestone} → ${d.plan.current_deliverable}`;document.querySelector('#currentFocus').textContent=`${d.plan.current_milestone} → ${d.plan.current_deliverable}`;document.querySelector('#currentOwner').textContent=current?`${current.current_actor} · ${current.name}`:'当前无 LFA Agent 执行';document.querySelector('#currentBlocker').textContent=current?.milestone||'无活跃任务归属';document.querySelector('#nextOwner').textContent=record?`${record.name} · ${statusText(record.status)}`:'未找到当前交付记录';document.querySelector('#nextAction').textContent=d.plan.next_gate||'未登记';document.querySelector('#focusAction').disabled=!focusNodeId;const unmapped=nodes.filter(n=>n.linkage_conflict);warning.hidden=!unmapped.length;warning.textContent=unmapped.length?`${unmapped.map(n=>n.owner).join('、')} 正在执行，但任务归属为 UNMAPPED；不得推断其所属主线。`:''}
function render(d){data=d;nodeIndex={};shadowProjection=d.shadow_projection?.status==='AVAILABLE'?d.shadow_projection.projection:null;const [current,program,...others]=normalize(d),nodes=current.nodes;document.querySelector('#currentProject').innerHTML=nodes.length?renderProject(current):'<p class="empty-state" role="status"><b>当前无 LFA Agent 执行</b><br>MASTER_PLAN 与 TASK_BOARD 仍可在下方查看，但不代表 Agent 正在运行。</p>';document.querySelector('#programProject').innerHTML=renderProject(program);document.querySelector('#otherProjects').innerHTML=others.length?others.map(renderProject).join(''):'<p class="diagnostics-body">无其他登记工作</p>';document.querySelector('#programSummary').textContent=`${d.plan.current_milestone} → ${d.plan.current_deliverable} · ${esc(d.plan.current_deliverable_record?.name||'未找到交付记录')} · 总进度 ${d.plan.progress}`;document.querySelector('#actionCount').textContent=nodes.length;document.querySelector('#runningCount').textContent=nodes.filter(n=>!n.linkage_conflict).length;document.querySelector('#blockedCount').textContent=nodes.filter(n=>n.linkage_conflict).length;document.querySelectorAll('[data-node]').forEach(b=>b.onclick=()=>showNode(b.dataset.node));renderManagerView(d);applyFilters();renderGlobal(d);const stale=d.source_health.filter(s=>s.status!=='OK');const alert=document.querySelector('#sourceAlert');alert.hidden=!stale.length;alert.innerHTML=stale.length?`<b>数据可能过期</b> · ${stale.map(s=>`${esc(s.source_id)}：${esc(statusText(s.status))}`).join('；')}`:'';document.querySelector('#diagnostics').innerHTML=`<p>数据生成 ${fmt(d.generated_at)} · Review ${esc(d.review.status)}</p><ul>${d.source_health.map(s=>`<li>${esc(s.source_id)} · ${esc(s.status)} · ${fmt(s.updated_at)}</li>`).join('')}</ul>`;const requested=openNodeId||new URLSearchParams(location.search).get('node');if(requested&&!showNode(requested,{updateUrl:false}))setNodeUrl(null,true)}
function selectView(name,{focus=false,updateUrl=true}={}){const tabs=[...document.querySelectorAll('[role="tab"][data-view]')],target=tabs.find(tab=>tab.dataset.view===name)||tabs[0];tabs.forEach(tab=>{const selected=tab===target;tab.setAttribute('aria-selected',String(selected));tab.tabIndex=selected?0:-1;document.querySelector(`[data-panel="${tab.dataset.view}"]`).hidden=!selected});if(updateUrl){const url=new URL(location.href);url.hash=target.dataset.view;history.replaceState(null,'',url)}if(focus)target.focus()}
async function load(){if(loading)return;loading=true;document.querySelector('#refresh').setAttribute('aria-busy','true');document.querySelector('#stamp').textContent='正在刷新';try{const r=await fetch('/api/status',{cache:'no-store'});if(!r.ok)throw new Error(`${r.status} ${r.statusText}`);const payload=await r.json();render(payload);renderOverview(payload);renderShadow(payload.shadow_projection);renderPM(payload.pm_operational_plan,payload.agent_operational_plans);lastSuccess=payload.generated_at;document.querySelector('#stamp').textContent=`更新 ${new Date(lastSuccess*1000).toLocaleTimeString()}`}catch(e){document.querySelector('#stamp').innerHTML=`<span class="error">刷新失败${lastSuccess?'，保留 '+new Date(lastSuccess*1000).toLocaleTimeString()+' 数据':''}: ${esc(e.message)}</span>`}finally{loading=false;document.querySelector('#refresh').removeAttribute('aria-busy')}}function schedule(){clearInterval(timer);if(!paused)timer=setInterval(load,5000)}document.querySelector('#focusAction').onclick=()=>focusNodeId&&showNode(focusNodeId);document.querySelector('#refresh').onclick=load;document.querySelector('#nodeSearch').oninput=applyFilters;document.querySelector('#nodeStatus').onchange=applyFilters;document.querySelector('#pause').onclick=e=>{paused=!paused;e.currentTarget.innerHTML=paused?'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m8 5 11 7-11 7Z"/></svg>':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg>';e.currentTarget.title=paused?'继续自动刷新':'暂停自动刷新';e.currentTarget.setAttribute('aria-label',e.currentTarget.title);e.currentTarget.setAttribute('aria-pressed',String(paused));schedule()};document.querySelector('#closeDrawer').onclick=()=>closeNode();document.querySelector('#drawer').onclick=e=>{if(e.target===e.currentTarget)closeNode()};document.querySelector('#drawer').addEventListener('cancel',e=>{e.preventDefault();closeNode()});addEventListener('popstate',()=>{selectView(location.hash.slice(1),{updateUrl:false});const id=new URLSearchParams(location.search).get('node');id?showNode(id,{updateUrl:false}):closeNode({updateUrl:false})});load();schedule();
document.querySelectorAll('[role="tab"][data-view]').forEach((tab,index,tabs)=>{tab.onclick=()=>selectView(tab.dataset.view);tab.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?tabs.length-1:(index+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;selectView(tabs[next].dataset.view,{focus:true})}});selectView(location.hash.slice(1));
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
  deliverables = []
  section = ""
  for line in text.splitlines():
    if line.startswith("## "):
      section = line[3:]
      continue
    if not line.startswith("| M"):
      continue
    columns = [part.strip() for part in line.strip("|").split("|")]
    if section == "Milestones" and len(columns) >= 4:
      milestones.append({"id": columns[0], "name": columns[1], "status": columns[3]})
    elif section == "Deliverables" and len(columns) >= 4:
      deliverables.append({"id": columns[0], "name": columns[1], "status": columns[3]})
  current_deliverable = headers.get("CURRENT_DELIVERABLE", "")
  return {
    "current_milestone": headers.get("CURRENT_MILESTONE", ""),
    "current_deliverable": current_deliverable,
    "current_deliverable_record": next((item for item in deliverables if item["id"] == current_deliverable), None),
    "next_gate": headers.get("NEXT_GATE", ""),
    "progress": headers.get("PROGRAM_PROGRESS", ""),
    "milestones": milestones,
  }


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


def registered_projection() -> dict:
  plan = read_text("MASTER_PLAN.md")
  accepted = "PM_ACCEPTED" if "Integration engineering Gate: QR-E2E-01" in plan else "IN_PROGRESS"
  nodes = [
    {
      "node_id": "QR-PC-01-D01", "name": "产品声明契约", "task_id": "RUN-20260918-QR-PC", "owner": "lfa-api", "dependencies": [], "stage": 0,
      "execution_status": "PM_ACCEPTED", "tone": "accepted", "milestone": "产品声明、Schema 与 Registry", "model_summary": "产品族声明与服务端可信 Registry", "next_action": "历史基线；当前命名空间已由 QLI cutover 取代", "execution_window": "已完成", "source_ref": "MASTER_PLAN.md:367-379", "blocker": "", "linkage_conflict": False, "subtasks": evidence_tasks("QR-PC-01-D01.json"), "gates": [gate("Review", "ACCEPTED", "accepted"), gate("PM", "ACCEPTED", "accepted")],
    },
    {
      "node_id": "QR-ANDROID-01-D01", "name": "Android QR 最小实现", "task_id": "RUN-20260918-QR-ANDROID", "owner": "lfa-android", "dependencies": ["QR-PC-01-D01"], "stage": 1,
      "execution_status": "PM_ACCEPTED", "tone": "accepted", "milestone": "预览识别、快门绑定与声明持久化", "model_summary": "Android QR 状态机与 Capture Bundle 绑定", "next_action": "工程 Gate 已通过；后续由 QLI 与拍前确认契约修订承接", "execution_window": "已完成", "source_ref": "MASTER_PLAN.md:369; MASTER_PLAN.md:385", "blocker": "", "linkage_conflict": False, "subtasks": [], "gates": [gate("Review", "ACCEPTED", "accepted"), gate("PM", "ACCEPTED", "accepted"), gate("真机证据", "PARTIAL", "warning")],
    },
    {
      "node_id": "QR-FINAL-01-D01", "name": "最终 JPEG QR 复核（已被修正）", "task_id": "RUN-20260918-QR-FINAL", "owner": "lfa-api", "dependencies": ["QR-PC-01-D01"], "stage": 1,
      "execution_status": "SUPERSEDED", "tone": "warning", "milestone": "历史最终 JPEG 二次身份 Gate", "model_summary": "历史实现曾在持久化 JPEG 上复核 QR", "next_action": "保留历史证据；不得继续强化或部署最终 JPEG QR 内容 Gate", "execution_window": "历史 Gate 已完成，当前产品意图已修正", "source_ref": "MASTER_PLAN.md:371-383; MASTER_PLAN.md:757-761", "blocker": "HOLD_FOR_CONTRACT_CORRECTION", "linkage_conflict": False, "subtasks": evidence_tasks("QR-FINAL-01-D01.json"), "gates": [gate("历史 Review", "ACCEPTED", "accepted"), gate("当前适用性", "SUPERSEDED", "warning")],
    },
    {
      "node_id": "QR-E2E-01-D01", "name": "Android 来源端到端集成", "task_id": "RUN-20260920-QR-E2E", "owner": "lfa-android / lfa-api", "dependencies": ["QR-ANDROID-01-D01", "QR-FINAL-01-D01"], "stage": 2,
      "execution_status": accepted, "tone": "accepted" if accepted == "PM_ACCEPTED" else "active", "milestone": "完整 JPEG 上传、API、Core、App/Web 闭环", "model_summary": "隔离 HTTPS Gateway + Android 来源请求 + DheaRuntime", "next_action": "工程闭环已接受；真实设备证据仍单独判定", "execution_window": "工程 Gate 已完成", "source_ref": "MASTER_PLAN.md:387-393", "blocker": "", "linkage_conflict": False, "subtasks": [], "gates": [gate("Review", "ACCEPTED", "accepted"), gate("PM", "ACCEPTED", "accepted"), gate("真机", "PENDING", "pending")],
    },
    {
      "node_id": "QLI-CUTOVER", "name": "QLI 全文与运行时切换", "task_id": "RUN-20260920-QLI-CUTOVER", "owner": "lfa-api / lfa-start / lfa-android", "dependencies": ["QR-E2E-01-D01"], "stage": 3,
      "execution_status": "PM_ACCEPTED", "tone": "accepted", "milestone": "精确 payload 1:QLI:DHEA:1234567890", "model_summary": "API/Core、文档、Android 兼容性三切片与 synthetic HTTP", "next_action": "切换已完成；旧 QIUQIU 仅可作为拒绝测试或历史事实", "execution_window": "已完成", "source_ref": "MASTER_PLAN.md:658-676; MASTER_PLAN.md:690-724", "blocker": "", "linkage_conflict": False, "subtasks": [], "gates": [gate("API/Core", "ACCEPTED", "accepted"), gate("Docs", "ACCEPTED", "accepted"), gate("Android", "ACCEPTED", "accepted"), gate("运行时", "COMPLETE", "accepted")],
    },
    {
      "node_id": "QLI-DEVICE-RECEIPT", "name": "真实设备上传回执", "task_id": "PM-TODO-010", "owner": "PROJECT_LEAD / designated operator", "dependencies": ["QLI-CUTOVER"], "stage": 4,
      "execution_status": "PARTIAL", "tone": "warning", "milestone": "设备 JPEG、SHA、HTTP 与服务端结果绑定", "model_summary": "Redmi 捕获与服务端原图字节一致；结果 QR_NOT_READABLE", "next_action": "保留 5/6 场景证据；完成剩余设备场景与 APK/source binding", "execution_window": "部分证据已登记", "source_ref": "MASTER_PLAN.md:724-728; MASTER_PLAN.md:740-755", "blocker": "场景 1-4、APK/source binding 与独立设备接受未完成", "linkage_conflict": False, "subtasks": [], "gates": [gate("传输字节", "PARTIAL", "warning"), gate("产品识别", "NOT_READY", "pending"), gate("设备接受", "UNVERIFIED", "pending")],
    },
    {
      "node_id": "ANDROID-UI-010-R01", "name": "上下双观察窗与真机显示", "task_id": "ANDROID-UI-010-R01", "owner": "lfa-android", "dependencies": ["QLI-CUTOVER"], "stage": 4,
      "execution_status": "PARTIAL", "tone": "warning", "milestone": "上方试剂窗、下方二维码窗", "model_summary": "非权威取景指导与完整 JPEG 保持不变", "next_action": "完成实物同时放置、QR 启用/移除/异码拒绝和真实上传", "execution_window": "工程 Gate 已通过，设备证据部分完成", "source_ref": "MASTER_PLAN.md:411-427", "blocker": "实际物理放置与拍摄上传未完成", "linkage_conflict": False, "subtasks": [], "gates": [gate("Review", "ACCEPTED", "accepted"), gate("PM", "ACCEPTED", "accepted"), gate("设备", "PARTIAL", "warning")],
    },
    {
      "node_id": "EXIF-ORDER-R01", "name": "EXIF 解码顺序修复", "task_id": "RUN-20260920-EXIF-ORDER-REPAIR", "owner": "lfa-api", "dependencies": ["QLI-DEVICE-RECEIPT"], "stage": 5,
      "execution_status": "HOLD_FOR_CONTRACT_CORRECTION", "tone": "warning", "milestone": "Core EXIF 证据先于 QR 拒绝", "model_summary": "EXIF 正常化仍需要；最终 JPEG QR Gate 已被产品意图修正", "next_action": "保留已做工作；不得按旧最终 JPEG 身份 Gate 接受或部署", "execution_window": "HOLD", "source_ref": "MASTER_PLAN.md:730-738; MASTER_PLAN.md:757-761", "blocker": "等待拍前产品确认契约冻结", "linkage_conflict": False, "subtasks": [], "gates": [gate("契约", "HOLD", "warning")],
    },
    {
      "node_id": "PRECAPTURE-CONTRACT-TABLE-R01", "name": "拍前产品确认 API 契约", "task_id": "RUN-20260920-PRECAPTURE-CONTRACT-R01", "owner": "lfa-start / lfa-api / lfa-android / lfa-review", "next_actor": "lfa-android", "waiting_parties": ["lfa-android", "lfa-review", "lfa-pm"], "release_condition": "API 字段/状态/错误/幂等表完成，同 revision 经 Android 确认与 Review 后，由 PM 决定实施 Gate", "plan_milestone": "M1", "dependencies": ["QLI-CUTOVER"], "stage": 5,
      "execution_status": "RECORDED", "tone": "pending", "milestone": "Android 读 QR → 服务端确认 → 允许快门", "model_summary": "服务端确认身份、session/attempt 绑定、有效期、提交与恢复语义", "next_action": "账本保留；须由当前任务板和真实 Agent 会话重新授权后执行", "execution_window": "历史登记，非实时执行", "source_ref": "MASTER_PLAN.md:757-779", "blocker": "CONTRACT_REVISION=UNFROZEN；IMPLEMENTATION_AUTHORIZED=NO", "linkage_conflict": False, "subtasks": [], "gates": [gate("契约", "UNFROZEN", "warning"), gate("实施", "NOT_AUTHORIZED", "pending"), gate("Review", "PENDING", "pending"), gate("PM", "PENDING", "pending")],
    },
    {
      "node_id": "QR-DEVICE-CLOSURE", "name": "指定设备最终闭环", "task_id": "PM-TODO-010 / PM-TODO-015", "owner": "PROJECT_LEAD / designated operator", "current_actor": "PROJECT_LEAD / designated operator", "next_actor": "lfa-pm", "waiting_parties": ["PROJECT_LEAD", "lfa-pm"], "release_condition": "三个并行前置条件全部完成：拍前契约实施、Android 真机显示、EXIF 顺序修复", "plan_milestone": "M1", "dependencies": ["PRECAPTURE-CONTRACT-TABLE-R01", "ANDROID-UI-010-R01", "EXIF-ORDER-R01"], "stage": 6,
      "execution_status": "WAITING_DEPENDENCY", "tone": "pending", "milestone": "真实拍摄、服务器确认、完整 JPEG、Core、App/Web 证据链", "model_summary": "所有缺失事实保持 null；不把 QR_NOT_READABLE 当产品 PASS", "next_action": "契约实施双 Gate 后执行剩余真实设备场景并完成最终十五项关闭评估", "execution_window": "等待当前契约链", "source_ref": "MASTER_PLAN.md:405-427; MASTER_PLAN.md:763-785", "blocker": "拍前确认契约未冻结；设备场景与最终关闭证据未完成", "linkage_conflict": False, "subtasks": [], "gates": [gate("设备证据", "PENDING", "pending"), gate("最终关闭", "BLOCKED", "blocked")],
    },
  ]
  tasks = [{**node, "title": node["name"], "breadcrumb": f"QIUQIU DHEA QR 产品识别 → {node['node_id']}", "wave": node["stage"], "queue_position": "已登记"} for node in nodes]
  critical_path = [
    {"label": "API 契约表", "actor": "lfa-api", "status": "RECORDED", "node_id": "PRECAPTURE-CONTRACT-TABLE-R01"},
    {"label": "同 revision 确认", "actor": "lfa-android", "status": "WAITING_DEPENDENCY", "node_id": "PRECAPTURE-CONTRACT-TABLE-R01"},
    {"label": "独立 Review", "actor": "lfa-review", "status": "WAITING_DEPENDENCY", "node_id": "PRECAPTURE-CONTRACT-TABLE-R01"},
    {"label": "实施 Gate", "actor": "lfa-pm", "status": "NOT_AUTHORIZED", "node_id": "PRECAPTURE-CONTRACT-TABLE-R01"},
    {"label": "指定设备闭环", "actor": "PROJECT_LEAD", "status": "WAITING_DEPENDENCY", "node_id": "QR-DEVICE-CLOSURE"},
  ]
  return {"goal": {"goal_id": "QIUQIU_DHEA_QR_PRODUCT_IDENTIFICATION_END_TO_END", "name": "QIUQIU DHEA QR 产品识别端到端", "status": "RECORDED"}, "workstream": {"workstream_id": "QR_PRODUCT_IDENTIFICATION", "name": "QR 产品识别登记投影（非实时）", "status": "RECORDED", "integration_status": "CONTRACT_REVISION_UNFROZEN", "plan_milestone": "M1", "current_node_id": None, "current_wave": None, "next_wave_label": "须重新授权后执行", "critical_path": critical_path, "nodes": nodes, "waves": []}, "tasks": tasks}

def live_execution(agents: list[dict]) -> dict:
  nodes = [
    {
      "node_id": f"LIVE-{agent['name']}",
      "name": agent["title"] or agent["linked_task_id"] or agent["name"],
      "task_id": agent["linked_task_id"],
      "owner": agent["name"],
      "current_actor": agent["name"],
      "execution_status": "RUNNING" if agent["status"] == "working" else agent["status"].upper(),
      "tone": "running" if agent["status"] == "working" else "pending",
      "stage": index,
      "kind": "实时 Agent 会话",
      "milestone": agent["ownership_chain"],
      "model_summary": agent["mapping_status"],
      "next_action": "以 Agent 会话和任务板记录为准",
      "execution_window": f"Herdr 当前观测为 {agent['status']}",
      "source_ref": "Herdr agent get; TASK_BOARD.md; Agent operational snapshot",
      "blocker": "" if agent["mapping_status"] == "REGISTERED_MATCH" else "UNMAPPED：未找到可信任务归属",
      "linkage_conflict": agent["mapping_status"] != "REGISTERED_MATCH",
      "dependencies": [],
      "subtasks": agent.get("subtasks", []),
      "gates": [],
    }
    for index, agent in enumerate(agent for agent in agents if agent["status"] != "not_running")
  ]
  return {"workstream": {"workstream_id": "LIVE_AGENT_EXECUTION", "name": "实时 LFA Agent 执行", "status": "ACTIVE" if nodes else "IDLE", "current_node_id": nodes[0]["node_id"] if nodes else None, "nodes": nodes}}


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
  sections = [text]
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
  markers = re.findall(r"^CURRENT_PM_OPERATIONAL_REVISION: (\S+)\s*$", text, re.MULTILINE)
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


def load_shadow_projection(path: Path = SHADOW_PROJECTION, raw: str | bytes | None = None) -> dict:
  try:
    projection = json.loads(path.read_text(encoding="utf-8") if raw is None else raw)
  except OSError as error:
    return {"status": "UNAVAILABLE", "projection": None, "error": str(error)}
  except (json.JSONDecodeError, UnicodeError) as error:
    return {"status": "INVALID", "projection": None, "error": f"invalid JSON: {error}"}

  top_keys = {"schema_version", "task_id", "subject_revision", "ingestion_status", "evidence_status", "acceptance_status", "criteria", "diagnostics", "generated_from_event_digest", "reducer_version"}
  criterion_keys = {"criterion_id", "required", "status", "generation", "selected_event_id", "superseded_event_ids", "evidence_refs", "reason_codes"}
  ingestion_statuses = {"VALID", "CONFLICTED", "INVALID_PAYLOAD"}
  evidence_statuses = {"DISPATCHABLE", "NOT_READY", "NOT_SUBMISSION", "MALFORMED", "UNKNOWN_STATUS", "CONFLICTED", "UNAVAILABLE"}
  acceptance_statuses = {"PASS", "FAIL", "UNVERIFIED", "PENDING", "INVALID", "STALE", "CONFLICTED", "UNAVAILABLE"}
  criterion_statuses = {"PASS", "FAIL", "UNVERIFIED", "PENDING", "INVALID", "STALE", "CONFLICTED"}
  sha256_revision = re.compile(r"sha256:[0-9a-f]{64}\Z")
  sha256_digest = re.compile(r"[0-9a-f]{64}\Z")

  def strings(values: object) -> bool:
    return isinstance(values, list) and all(isinstance(value, str) for value in values) and len(values) == len(set(values))

  valid = (
    isinstance(projection, dict)
    and set(projection) == top_keys
    and projection["schema_version"] == "herdr-dashboard-projection/1.3"
    and isinstance(projection["task_id"], str) and bool(projection["task_id"])
    and isinstance(projection["subject_revision"], str) and bool(sha256_revision.fullmatch(projection["subject_revision"]))
    and isinstance(projection["ingestion_status"], str) and projection["ingestion_status"] in ingestion_statuses
    and isinstance(projection["evidence_status"], str) and projection["evidence_status"] in evidence_statuses
    and isinstance(projection["acceptance_status"], str) and projection["acceptance_status"] in acceptance_statuses
    and isinstance(projection["criteria"], list) and bool(projection["criteria"])
    and isinstance(projection["diagnostics"], list)
    and isinstance(projection["generated_from_event_digest"], str) and bool(sha256_digest.fullmatch(projection["generated_from_event_digest"]))
    and isinstance(projection["reducer_version"], str) and bool(projection["reducer_version"])
  )
  if valid:
    for criterion in projection["criteria"]:
      generation = criterion.get("generation") if isinstance(criterion, dict) else None
      valid = (
        isinstance(criterion, dict) and set(criterion) == criterion_keys
        and isinstance(criterion["criterion_id"], str) and bool(criterion["criterion_id"])
        and type(criterion["required"]) is bool
        and isinstance(criterion["status"], str) and criterion["status"] in criterion_statuses
        and (generation is None or type(generation) is int and generation >= 1)
        and (criterion["selected_event_id"] is None or isinstance(criterion["selected_event_id"], str))
        and strings(criterion["superseded_event_ids"])
        and strings(criterion["evidence_refs"])
        and strings(criterion["reason_codes"])
      )
      if not valid:
        break
  if valid:
    valid = all(
      isinstance(diagnostic, dict)
      and set(diagnostic) == {"source_ref", "code"}
      and isinstance(diagnostic["source_ref"], str) and bool(diagnostic["source_ref"])
      and isinstance(diagnostic["code"], str) and bool(diagnostic["code"])
      for diagnostic in projection["diagnostics"]
    )
  if not valid:
    return {"status": "INVALID", "projection": None, "error": "projection does not match herdr-dashboard-projection/1.3"}
  return {"status": "AVAILABLE", "projection": projection, "error": None}


def status_payload() -> dict:
  errors = []
  named = {}
  for name in TEAM:
    try:
      row = run_json("herdr", "agent", "get", name).get("result", {}).get("agent", {})
      if row:
        named[name] = row
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
      pass
  tasks = parse_tasks()
  task_by_id = {task["id"]: task for task in tasks}
  pm = parse_pm_operational_plan()
  agent_plans = parse_agent_operational_plans(pm)
  agents = []
  for name in TEAM:
    row = named.get(name, {})
    output = ""
    if row:
      try:
        output = recent_output(name)
      except (OSError, subprocess.SubprocessError) as error:
        errors.append(f"{name}: {error}")
    snapshot = agent_plans["current"].get(name, {})
    snapshot_registered = name in agent_plans["current"]
    active_items = [item for item in snapshot.get("items", []) if item.get("status") == "in_progress"]
    linked_task_id = next((item.get("related_task_or_deliverable") for item in active_items if isinstance(item.get("related_task_or_deliverable"), str) and item["related_task_or_deliverable"] in task_by_id), None)
    task = task_by_id.get(linked_task_id)
    mapping_status = "REGISTERED_MATCH" if task else "UNMAPPED"
    ownership_chain = f"{task['plan_id']} → {task['deliverable_id']} → {task['id']}" if task else "UNMAPPED"
    agents.append({"name": name, "status": row.get("agent_status", "not_running"), "pane": row.get("pane_id", ""), "title": row.get("terminal_title_stripped", ""), "output": output, "linked_task_id": linked_task_id, "mapping_status": mapping_status, "snapshot_status": "CURRENT_SNAPSHOT_REGISTERED" if snapshot_registered else "CURRENT_SNAPSHOT_UNREGISTERED", "ownership_chain": ownership_chain, "subtasks": snapshot.get("items", []) if snapshot_registered else [], "observed_at": time.time()})
  registered = registered_projection()
  return {"generated_at": time.time(), "gate": parse_gate(), "plan": parse_plan(), "pm_operational_plan": pm, "agent_operational_plans": agent_plans, "tasks": tasks, "execution": live_execution(agents), "registered_execution": registered, "review": review_payload(), "shadow_projection": load_shadow_projection(), "blockers": read_text("BLOCKERS.md"), "agents": agents, "source_health": [source_health(name) for name in ("MASTER_PLAN.md", "TASK_BOARD.md", "REVIEW_QUEUE.md", "BLOCKERS.md")], "errors": errors}


class Handler(BaseHTTPRequestHandler):
  def do_GET(self) -> None:
    path = self.path.partition("?")[0]
    if path == "/":
      self.respond(PAGE.encode(), "text/html; charset=utf-8")
    elif path == "/api/status":
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
    shadow = payload["shadow_projection"]
    assert shadow["status"] == "AVAILABLE", shadow
    projection = shadow["projection"]
    assert projection["evidence_status"] == "NOT_READY"
    assert projection["acceptance_status"] == "UNVERIFIED"
    assert projection["criteria"][0]["status"] == "UNVERIFIED"
    assert "DEVICE_EVIDENCE_PENDING" in projection["criteria"][0]["reason_codes"]
    assert 'id="pmPlan"' in PAGE and 'id="pmPlanTitle"' in PAGE
    assert 'id="shadowTitle">验证投影</h2>' in PAGE
    assert '不改变正式阶段、不调度、不代表通过' in PAGE
    assert 'class="pm-complete"' in PAGE and 'id="otherProjects"' in PAGE
    assert "n.task_id!==p.task_id" in PAGE and "正式阶段" in PAGE
    assert "数据可能过期" in PAGE and "grid-template-columns:repeat(auto-fit" in PAGE
    assert all(f'id="{field}"' in PAGE for field in ("currentFocus", "currentBlocker", "currentOwner", "nextOwner", "nextAction", "focusAction", "programStrip"))
    assert 'function renderOverview' in PAGE and 'role="tablist"' in PAGE and '当前无 LFA Agent 执行' in PAGE
    assert all(f"field('{key}'" in PAGE for key in ("criterion_id", "required", "status", "generation", "selected_event_id", "superseded_event_ids", "evidence_refs", "reason_codes", "generated_from_event_digest", "reducer_version"))
    assert all(f'id="{field}"' in PAGE for field in ("globalActionCount", "globalBlockedCount", "globalWorkingCount", "globalSourceCount", "managementIssues", "nodeSearch", "nodeStatus", "filterResult"))
    assert all(marker in PAGE for marker in ("function collectConflicts", "function applyFilters", "function setNodeUrl", "function sourceRefs", "openNodeId", "lastSuccess"))
    invalid_pass = {**projection, "acceptance_status": "PASS", "criteria": [{**projection["criteria"][0], "status": "PASS", "unexpected": True}]}
    assert load_shadow_projection(raw=json.dumps(invalid_pass))["status"] == "INVALID"
    duplicate_refs = {**projection, "criteria": [{**projection["criteria"][0], "evidence_refs": ["same", "same"]}]}
    assert load_shadow_projection(raw=json.dumps(duplicate_refs))["status"] == "INVALID"
    assert load_shadow_projection(raw=b"\xff")["status"] == "INVALID"
    assert load_shadow_projection(raw="{broken")["status"] == "INVALID"
    assert load_shadow_projection(Path("/definitely/missing/qr-android-projection.json"))["status"] == "UNAVAILABLE"
    assert not payload["pm_operational_plan"]["errors"], payload["pm_operational_plan"]["errors"]
    assert not payload["agent_operational_plans"]["errors"], payload["agent_operational_plans"]["errors"]
    assert payload["plan"]["current_milestone"] == "M1"
    assert payload["plan"]["current_deliverable"] == "M1-D05"
    assert payload["plan"]["current_deliverable_record"]["id"] == "M1-D05"
    assert payload["plan"]["next_gate"] == "M1_EXIT_BASELINE_AND_REPAIR_BOUNDARIES_ACCEPTED"
    assert live_execution([])["workstream"]["nodes"] == []
    online_names = {agent["name"] for agent in payload["agents"] if agent["status"] != "not_running"}
    assert {node["owner"] for node in payload["execution"]["workstream"]["nodes"]} == online_names
    registered_nodes = payload["registered_execution"]["workstream"]["nodes"]
    by_id = {node["node_id"]: node for node in registered_nodes}
    assert len(registered_nodes) == 10 and "QLI-CUTOVER" in by_id
    assert by_id["PRECAPTURE-CONTRACT-TABLE-R01"]["execution_status"] == "RECORDED"
    assert "current_actor" not in by_id["PRECAPTURE-CONTRACT-TABLE-R01"]
    assert payload["registered_execution"]["workstream"]["current_node_id"] is None
    mapped = live_execution([{"name": "lfa-api", "status": "working", "title": "API task", "linked_task_id": "TASK-1", "mapping_status": "REGISTERED_MATCH", "ownership_chain": "M1 → M1-D05 → TASK-1", "subtasks": [{"id": "TODO-1", "title": "Visible task", "status": "in_progress"}]}])
    assert mapped["workstream"]["nodes"][0]["milestone"] == "M1 → M1-D05 → TASK-1"
    assert mapped["workstream"]["nodes"][0]["subtasks"] == [{"id": "TODO-1", "title": "Visible task", "status": "in_progress"}]
    idle = live_execution([{"name": "lfa-api", "status": "idle", "title": "API paused", "linked_task_id": None, "mapping_status": "UNMAPPED", "ownership_chain": "UNMAPPED"}])
    assert idle["workstream"]["nodes"][0]["execution_status"] == "IDLE"
    unmapped = live_execution([{"name": "lfa-api", "status": "working", "title": "Unknown task", "linked_task_id": None, "mapping_status": "UNMAPPED", "ownership_chain": "UNMAPPED"}])
    assert unmapped["workstream"]["nodes"][0]["linkage_conflict"] is True
    assert "UNMAPPED" in unmapped["workstream"]["nodes"][0]["blocker"]
    assert "账本投影与历史任务，非实时执行" in PAGE
    assert all(f'data-view="{view}"' in PAGE and f'data-panel="{view}"' in PAGE for view in ("current", "plan", "diagnostics"))
    assert "ArrowLeft" in PAGE and "aria-selected" in PAGE
    assert "n.gates?.length?" in PAGE and "无独立 Gate 记录" not in PAGE
    assert all(agent["snapshot_status"] == "CURRENT_SNAPSHOT_REGISTERED" or not agent["subtasks"] for agent in payload["agents"])
    assert all(agent["snapshot_status"] != "CURRENT_SNAPSHOT_REGISTERED" or agent["name"] in payload["agent_operational_plans"]["current"] for agent in payload["agents"])
    assert "CURRENT_SNAPSHOT_UNREGISTERED" in PAGE
    assert "当前 TODO 快照未登记" in PAGE
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return
  server = ThreadingHTTPServer((args.host, args.port), Handler)
  print(f"LFA PM Dashboard: http://{args.host}:{args.port}", flush=True)
  server.serve_forever()


if __name__ == "__main__":
  main()
