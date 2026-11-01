import "./styles.css";
import D from "./data.json";
import { NetScene, REL } from "./scene";

type Src = { title: string; pub: string; date: string; tier: string; url: string };
const SRC = D.sources as Record<string, Src>;
const JUR = D.jur as { code: string; name: string; group: string; inst: string; est: string }[];
const NAME: Record<string, string> = Object.fromEntries(JUR.map(j => [j.code, j.name]));
const app = document.getElementById("app")!;
let scene: NetScene | null = null;
const esc = (s: string) => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));
const tierCls = (t: string) => t === "A" ? "A" : t === "B" ? "B" : t === "C-news" ? "Cn" : "Ca";
const srcLink = (id: string) => { const s = SRC[id]; return s ? `<a class="src" href="${s.url}" target="_blank" rel="noopener"><span class="tier ${tierCls(s.tier)}">${s.tier}</span>${esc(s.pub)}, ${s.date}</a>` : ""; };

const state = { tab: "network", jur: "IN", thr: 5, nmax: 2 };
function readHash() {
  const [t, j] = location.hash.replace("#", "").split("/");
  if (["network", "compare", "india", "sources"].includes(t)) state.tab = t;
  if (j && NAME[j.toUpperCase()]) state.jur = j.toUpperCase();
}
function setHash() { history.replaceState(null, "", "#" + state.tab + (state.tab === "network" ? "/" + state.jur.toLowerCase() : "")); }

function classify(codes: Record<string, string>) {
  const comp = D.comp as string[]; const y = comp.filter(c => codes[c] === "Y").length; const n = comp.filter(c => codes[c] === "N").length;
  return { y, n, u: comp.length - y - n, cls: y >= state.thr && n <= state.nmax ? "Baseline" : y >= 1 ? "Uplift" : "Gap" };
}

function render() {
  document.querySelectorAll<HTMLAnchorElement>("#tabs a").forEach(a => a.classList.toggle("on", a.dataset.tab === state.tab));
  if (scene && state.tab !== "network") { scene.dispose(); scene = null; }
  ({ network, compare, india, sources } as Record<string, () => void>)[state.tab]();
  setHash();
}

function network() {
  const groups = ["Subject", "Frontier power", "Middle power", "Bloc regulator"];
  const chips = groups.map(g => JUR.filter(j => j.group === g).map(j => `<button class="chip ${j.code === state.jur ? "on" : ""}" data-j="${j.code}">${esc(j.name)}<small>${g === "Subject" ? "subject" : ""}</small></button>`).join("")).join("");
  const j = JUR.find(x => x.code === state.jur)!;
  const facts = (D.facts as any[]).filter(f => f.j === state.jur);
  const g = (D.graph as any)[state.jur];
  const usedRel = Array.from(new Set(g.edges.map((e: any) => e.rel))) as string[];
  if (!app.querySelector(".net")) {
    app.innerHTML = `<h2>Who houses, funds, steers and empowers each institute</h2>
    <p class="lead">Pick a jurisdiction. The institute sits at the centre. Bodies above it hold money, legal basis or accountability; bodies below deliver work or partner. Drag to rotate. Each line is sourced in the panel.</p>
    <div class="chips" id="chips"></div>
    <div class="net"><div class="stage" id="stage"><div class="hint">drag to rotate · scroll to zoom</div><div class="legend" id="legend"></div></div><aside class="side" id="side"></aside></div>`;
    scene = new NetScene(document.getElementById("stage")!);
  }
  document.getElementById("chips")!.innerHTML = chips;
  document.querySelectorAll<HTMLButtonElement>("#chips .chip").forEach(b => b.onclick = () => { state.jur = b.dataset.j!; network(); setHash(); });
  document.getElementById("legend")!.innerHTML = usedRel.map(r => `<span><i style="background:${REL[r].color}"></i>${REL[r].label}</span>`).join("");
  const edgeList = g.edges.map((e: any) => { const na = g.nodes.find((n: any) => n.id === e.a).label, nb = g.nodes.find((n: any) => n.id === e.b).label; return `<div class="fact"><p><span style="color:${REL[e.rel].color};font-weight:700">${REL[e.rel].label}</span>: ${esc(na)} → ${esc(nb === g.nodes.find((n: any) => n.id === "i").label ? j.inst.split(" (")[0] : nb)}</p>${srcLink(e.src)}</div>`; }).join("");
  document.getElementById("side")!.innerHTML = `<h2>${esc(j.name)}</h2><div class="meta">${esc(j.inst)} · ${esc(j.est)} · ${esc(j.group)}</div>
   ${facts.map(f => `<div class="fact"><b>${esc(f.dim)}</b><p>${esc(f.text)}</p>${f.src.map(srcLink).join("")}</div>`).join("")}
   <h3>Links drawn in the network</h3>${edgeList}`;
  scene!.show(g.nodes, g.edges, j.inst.split(" (")[0]);
}

function compare() {
  const feats = D.features as any[]; const cols = [...(D.comp as string[]), "IN"];
  const rows = feats.map(f => { const c = classify(f.codes); return `<tr><td><b>${esc(f.label)}</b><br><span style="color:var(--mute);font-size:13px">${esc(f.defn)}</span></td><td><span class="cls ${c.cls}">${c.cls === "Gap" ? "No peer" : c.cls}</span><br><span style="font-size:12px;color:var(--mute)">${c.y} yes · ${c.n} no · ${c.u} not stated</span></td>${cols.map(k => `<td class="c ${f.codes[k]} ${k === "IN" ? "india" : ""}" data-f="${f.code}" data-k="${k}">${f.codes[k] === "U" ? "·" : f.codes[k]}</td>`).join("")}</tr>`; }).join("");
  app.innerHTML = `<h2>Seventeen features across ten peers and India</h2>
  <p class="lead">Y means present in the sources read, N absent or explicitly denied, · not stated. A feature is <b>baseline</b> when enough peers show it; the rest are <b>uplift</b> candidates that only a few peers have.</p>
  <div class="ctrl"><label>Baseline when at least <b id="tv">${state.thr}</b> of 10 peers have it <input id="thr" type="range" min="3" max="9" value="${state.thr}"></label>
  <label>and at most <b id="nv">${state.nmax}</b> clearly lack it <input id="nmax" type="range" min="0" max="5" value="${state.nmax}"></label></div>
  <div class="grid"><table class="m"><thead><tr><th>Feature</th><th>Class</th>${cols.map(k => `<th>${k === "IN" ? "India" : NAME[k]}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div>
  <div class="note">Click a cell for the evidence. Codes are judgments from the sourced facts; edit them in the workbook to test the conclusions.</div>`;
  const thr = document.getElementById("thr") as HTMLInputElement, nm = document.getElementById("nmax") as HTMLInputElement;
  thr.oninput = () => { state.thr = +thr.value; compare(); }; nm.oninput = () => { state.nmax = +nm.value; compare(); };
  app.querySelectorAll<HTMLTableCellElement>("td.c").forEach(td => td.onclick = (ev) => {
    const f = feats.find(x => x.code === td.dataset.f); const k = td.dataset.k!;
    pop(ev as MouseEvent, `<b>${esc(f.label)}: ${esc(k === "IN" ? "India" : NAME[k])} = ${f.codes[k] === "U" ? "not stated" : f.codes[k]}</b><p>${esc(f.evid)}</p><p style="color:var(--mute)">See ${esc(k === "IN" ? "India" : NAME[k])} in the Network tab for its sourced facts.</p>`);
  });
}

function pop(ev: MouseEvent, html: string) {
  document.querySelector(".pop")?.remove();
  const d = document.createElement("div"); d.className = "pop"; d.innerHTML = `<button class="x" aria-label="Close">×</button>` + html;
  document.body.appendChild(d);
  const x = Math.min(ev.clientX + 12, window.innerWidth - d.offsetWidth - 12), y = Math.min(ev.clientY + 12, window.innerHeight - d.offsetHeight - 12);
  d.style.left = Math.max(8, x) + "px"; d.style.top = Math.max(8, y) + "px";
  d.querySelector(".x")!.addEventListener("click", () => d.remove());
}

const UPLIFT_MODEL: Record<string, string> = {
  F3: "Korea's Framework Act names the institute and its functions; the EU AI Office rests on a Commission Decision and the AI Act.",
  F4: "EU AI Act Article 92 lets the AI Office request API or source-code access, with fines for refusal.",
  F5: "The UK signs pre-deployment access MoUs; the US uses voluntary agreements. Write a minimum window into them.",
  F7: "UK, US, Canada, Australia and Singapore publish budgets; India publishes only the pillar total.",
  F10: "The UK can mobilise £15M in grants; Canada runs a CIFAR stream. India already funds Safe & Trusted projects.",
  F12: "EU Scientific Panel experts must be independent of providers and publish declarations of interest.",
  F13: "The UK published its Claude Mythos Preview cyber evaluation with methods and limits.",
  F14: "Korea ties the institute to operators' duties above a training-compute threshold (Art. 32); the EU ties evaluation to GPAI duties.",
  F15: "The UK institute has priority access to over £1.5bn of national compute.",
  F16: "Japan's draft revised plan gives its institute an incident and vulnerability sharing role.",
};
function india() {
  const feats = D.features as any[];
  const base = feats.filter(f => classify(f.codes).cls === "Baseline");
  const up = feats.filter(f => classify(f.codes).cls !== "Baseline");
  const b = D.budget as any[]; const max = Math.max(...b.map(x => x.usd));
  app.innerHTML = `<h2>India: what to copy, what to add</h2>
  <p class="lead">India announced its institute in January 2025. It has no published budget, an unfilled director post, and no stated role in the April 2026 apex bodies. A consultation on AI regulation is due in November 2026, and pre-release testing of the most capable models is being weighed with no tester named.</p>
  <div class="cols">
   <div class="card"><h3>Baseline: replicate now</h3>${base.map(f => `<div class="item"><span class="k">${esc(f.label)}</span> ${f.codes.IN === "Y" ? '<span class="pill Enabler">India has it</span>' : '<span class="pill Gap">India lacks it</span>'}<div class="s">${classify(f.codes).y} of 10 peers</div></div>`).join("")}</div>
   <div class="card"><h3>Safety uplift: best of the few</h3>${up.map(f => `<div class="item"><span class="k">${esc(f.label)}</span> ${f.codes.IN === "Y" ? '<span class="pill Enabler">India has it</span>' : ""}<div class="s">${esc(UPLIFT_MODEL[f.code] ?? f.evid)}</div></div>`).join("")}</div>
   <div class="card"><h3>Feasibility today</h3>${(D.feas as any[]).map(x => `<div class="item"><span class="k">${esc(x.factor)}</span><span class="pill ${x.reading}">${x.reading}</span><div class="s">${esc(x.text)}</div>${x.src.map(srcLink).join("")}</div>`).join("")}</div>
  </div>
  <h3>Annual money, in US dollars</h3>
  <div class="bars">${b.map(x => `<div class="bar ${x.j === "IN" ? "in" : ""}"><span>${esc(NAME[x.j])}: ${esc(x.label)}</span><div class="t" style="width:${Math.max(0.6, (x.usd / max) * 100)}%"></div><span class="v">$${(x.usd / 1e6).toFixed(2)}M</span></div>`).join("")}</div>
  <div class="note">Exchange rates are approximate (GBP 1.30, CAD 0.72, AUD 0.65, INR 0.0114 USD). India's bar is the whole Safe &amp; Trusted AI pillar (₹20.46 crore over five years), not a dedicated institute budget. An Australia-level institute would cost about ₹42 crore a year.</div>`;
}

function sources() {
  const all = Object.entries(SRC);
  app.innerHTML = `<h2>${all.length} sources</h2><p class="lead">A: statute or binding act. B: official government or institute publication. C-news and C-analysis: news outlets and expert commentary.</p>
  <div class="ctrl"><input type="search" id="q" placeholder="Filter by title or publisher"><span id="tiers"></span></div>
  <div class="grid"><table class="m"><thead><tr><th>Tier</th><th>Source</th><th>Publisher</th><th>Date</th></tr></thead><tbody id="rows"></tbody></table></div>`;
  let tier = ""; const tiers = ["", "A", "B", "C-news", "C-analysis"];
  const draw = () => {
    const q = (document.getElementById("q") as HTMLInputElement).value.toLowerCase();
    document.getElementById("tiers")!.innerHTML = tiers.map(t => `<button class="chip ${t === tier ? "on" : ""}" data-t="${t}">${t || "All"}</button>`).join(" ");
    document.querySelectorAll<HTMLButtonElement>("#tiers .chip").forEach(b => b.onclick = () => { tier = b.dataset.t!; draw(); });
    document.getElementById("rows")!.innerHTML = all.filter(([, s]) => (!tier || s.tier === tier) && (s.title + s.pub).toLowerCase().includes(q))
      .map(([, s]) => `<tr><td><span class="tier ${tierCls(s.tier)}">${s.tier}</span></td><td><a href="${s.url}" target="_blank" rel="noopener">${esc(s.title)}</a></td><td>${esc(s.pub)}</td><td>${s.date}</td></tr>`).join("");
  };
  draw(); (document.getElementById("q") as HTMLInputElement).oninput = draw;
}

document.querySelectorAll<HTMLAnchorElement>("#tabs a").forEach(a => a.onclick = (e) => { e.preventDefault(); state.tab = a.dataset.tab!; app.innerHTML = ""; render(); });
readHash(); render();
window.addEventListener("hashchange", () => { const t = state.tab, j = state.jur; readHash(); if (t !== state.tab || j !== state.jur) { if (t !== state.tab) app.innerHTML = ""; render(); } });
