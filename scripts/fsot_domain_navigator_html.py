"""Generate self-contained FSOT domain navigator browser UI."""

from __future__ import annotations

import json
from typing import Any


def render_html(doc: dict[str, Any]) -> str:
    payload = json.dumps(doc, ensure_ascii=False)
    payload = payload.replace("</", "<\\/")  # guard script breakout
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>FSOT Domain Navigator</title>
  <style>
    :root {{
      --bg: #0b0f14;
      --surface: #141b24;
      --surface2: #1a2430;
      --border: #2a3848;
      --text: #e8eef4;
      --muted: #8fa3b8;
      --accent: #3dd6c3;
      --accent-dim: #2a9d8f;
      --amber: #f4b942;
      --tier-a: #4ade80;
      --tier-b: #60a5fa;
      --tier-c: #fb923c;
      --tier-d: #f87171;
      --radius: 10px;
      --font: "Segoe UI", system-ui, -apple-system, sans-serif;
      --mono: "Cascadia Code", "Consolas", monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      line-height: 1.5;
    }}
    header {{
      border-bottom: 1px solid var(--border);
      background: linear-gradient(180deg, var(--surface) 0%, var(--bg) 100%);
      padding: 1.25rem 1.5rem 1rem;
    }}
    header h1 {{
      font-size: 1.35rem;
      font-weight: 600;
      letter-spacing: -0.02em;
    }}
    header h1 span {{ color: var(--accent); }}
    .subtitle {{ color: var(--muted); font-size: 0.875rem; margin-top: 0.25rem; }}
    .stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 0.85rem;
    }}
    .stat {{
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 0.4rem 0.75rem;
      font-size: 0.8rem;
    }}
    .stat strong {{ color: var(--accent); }}
    .layout {{
      display: grid;
      grid-template-columns: 260px 1fr 320px;
      gap: 0;
      min-height: calc(100vh - 140px);
    }}
    @media (max-width: 1100px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar, .detail {{ display: none; }}
      .sidebar.open, .detail.open {{ display: block; }}
    }}
    .sidebar {{
      border-right: 1px solid var(--border);
      padding: 1rem;
      overflow-y: auto;
      background: var(--surface);
    }}
    .sidebar h2 {{
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 0.6rem;
    }}
    .intent-chip {{
      display: block;
      width: 100%;
      text-align: left;
      background: var(--surface2);
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 8px;
      padding: 0.5rem 0.65rem;
      margin-bottom: 0.4rem;
      font-size: 0.8rem;
      cursor: pointer;
      transition: border-color 0.15s, background 0.15s;
    }}
    .intent-chip:hover, .intent-chip.active {{
      border-color: var(--accent-dim);
      background: #1e2d3a;
    }}
    .intent-chip small {{
      display: block;
      color: var(--muted);
      font-size: 0.72rem;
      margin-top: 0.15rem;
    }}
    .main {{
      padding: 1rem 1.25rem;
      overflow-y: auto;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1rem;
      align-items: center;
    }}
    .search-wrap {{
      flex: 1;
      min-width: 200px;
      position: relative;
    }}
    .search-wrap input {{
      width: 100%;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      color: var(--text);
      padding: 0.65rem 0.85rem 0.65rem 2.2rem;
      font-size: 0.95rem;
      outline: none;
    }}
    .search-wrap input:focus {{ border-color: var(--accent-dim); }}
    .search-wrap::before {{
      content: "⌕";
      position: absolute;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--muted);
      font-size: 1rem;
    }}
    .filter-btn {{
      background: var(--surface2);
      border: 1px solid var(--border);
      color: var(--muted);
      border-radius: 8px;
      padding: 0.45rem 0.7rem;
      font-size: 0.78rem;
      cursor: pointer;
    }}
    .filter-btn.active {{
      border-color: var(--accent);
      color: var(--accent);
      background: #1a2f2c;
    }}
    .results-meta {{
      color: var(--muted);
      font-size: 0.8rem;
      margin-bottom: 0.75rem;
    }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 0.85rem 1rem;
      margin-bottom: 0.5rem;
      cursor: pointer;
      transition: border-color 0.12s;
    }}
    .card:hover, .card.selected {{
      border-color: var(--accent-dim);
    }}
    .card-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 0.5rem;
    }}
    .card-title {{
      font-weight: 600;
      font-size: 0.92rem;
      word-break: break-word;
    }}
    .kind-badge {{
      font-size: 0.65rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      background: var(--surface2);
      color: var(--muted);
      white-space: nowrap;
    }}
    .card-sub {{
      color: var(--muted);
      font-size: 0.8rem;
      margin-top: 0.35rem;
    }}
    .tier {{
      display: inline-block;
      font-size: 0.68rem;
      font-weight: 600;
      padding: 0.12rem 0.4rem;
      border-radius: 4px;
      margin-left: 0.35rem;
    }}
    .tier-A_strong {{ background: #14532d; color: var(--tier-a); }}
    .tier-B_verified {{ background: #1e3a5f; color: var(--tier-b); }}
    .tier-C_thin {{ background: #431407; color: var(--tier-c); }}
    .tier-D_needs_work {{ background: #450a0a; color: var(--tier-d); }}
    .detail {{
      border-left: 1px solid var(--border);
      padding: 1rem;
      overflow-y: auto;
      background: var(--surface);
    }}
    .detail h2 {{
      font-size: 1rem;
      margin-bottom: 0.5rem;
      word-break: break-word;
    }}
    .detail .empty {{
      color: var(--muted);
      font-size: 0.85rem;
      margin-top: 2rem;
      text-align: center;
    }}
    .detail-section {{
      margin-top: 1rem;
    }}
    .detail-section h3 {{
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--muted);
      margin-bottom: 0.4rem;
    }}
    .path-row {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
      margin-bottom: 0.35rem;
      font-size: 0.78rem;
    }}
    .path-row label {{
      color: var(--muted);
      min-width: 4.5rem;
      flex-shrink: 0;
    }}
    .path-row code {{
      font-family: var(--mono);
      background: var(--surface2);
      padding: 0.2rem 0.45rem;
      border-radius: 4px;
      word-break: break-all;
      flex: 1;
      font-size: 0.72rem;
    }}
    .copy-btn {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--muted);
      border-radius: 4px;
      padding: 0.15rem 0.4rem;
      font-size: 0.68rem;
      cursor: pointer;
      flex-shrink: 0;
    }}
    .copy-btn:hover {{ color: var(--accent); border-color: var(--accent-dim); }}
    .tag-list {{ display: flex; flex-wrap: wrap; gap: 0.3rem; }}
    .tag {{
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 0.15rem 0.4rem;
      font-size: 0.72rem;
      color: var(--muted);
    }}
    footer {{
      border-top: 1px solid var(--border);
      padding: 0.6rem 1.5rem;
      font-size: 0.72rem;
      color: var(--muted);
    }}
    footer a {{ color: var(--accent-dim); }}
  </style>
</head>
<body>
  <header>
    <h1>FSOT <span>Domain Navigator</span></h1>
    <p class="subtitle">Find verification panels, benchmarks, and Lean modules by scientific domain or problem intent.</p>
    <div class="stats" id="stats"></div>
  </header>
  <div class="layout">
    <aside class="sidebar">
      <h2>Problem intents</h2>
      <div id="intents"></div>
    </aside>
    <main class="main">
      <div class="toolbar">
        <div class="search-wrap">
          <input type="search" id="q" placeholder="Search: entanglement, superconductivity, psychometrics…" autocomplete="off" />
        </div>
        <button class="filter-btn active" data-filter="all">All</button>
        <button class="filter-btn" data-filter="core">Core 35</button>
        <button class="filter-btn" data-filter="panel">Panels</button>
        <button class="filter-btn" data-filter="intent">Intents</button>
        <button class="filter-btn" data-filter="desktop">Desktop</button>
      </div>
      <div class="results-meta" id="meta"></div>
      <div id="results"></div>
    </main>
    <aside class="detail" id="detail">
      <p class="empty">Select a result to see download paths and reproduction bundle.</p>
    </aside>
  </div>
  <footer>
    Generated <span id="gen-at"></span> · Rebuild: <code>python scripts/build_fsot_domain_navigator_db.py</code> ·
    <a href="https://github.com/dappalumbo91/FSOT-2.1-Lean">FSOT-2.1-Lean</a>
  </footer>
  <script type="application/json" id="nav-data">{payload}</script>
  <script>
    const DATA = JSON.parse(document.getElementById("nav-data").textContent);
    const panelByName = Object.fromEntries((DATA.extension_panels || []).map(p => [p.panel, p]));
    const coreByName = Object.fromEntries((DATA.core_domains || []).map(c => [c.name, c]));

    let items = [];
    let filter = "all";
    let selectedId = null;
    let activeIntent = null;

    function tierBadge(tier) {{
      if (!tier) return "";
      const cls = "tier tier-" + tier;
      const label = tier.replace("_", " ");
      return `<span class="${{cls}}">${{label}}</span>`;
    }}

    function buildIndex() {{
      items = [];
      for (const c of DATA.core_domains || []) {{
        items.push({{
          id: "core:" + c.name,
          kind: "core",
          title: c.name,
          core: c.name,
          sub: `${{c.empirical_records?.toLocaleString() ?? "?"}} records · median ${{c.median_error_pct ?? "?"}}% · breadth ${{c.breadth_pct ?? "?"}}%`,
          tier: c.coverage_tier,
          haystack: [c.name, c.lean_domain, c.breadth_note, ...(c.labs || [])].join(" ").toLowerCase(),
          raw: c,
        }});
      }}
      for (const p of DATA.extension_panels || []) {{
        items.push({{
          id: "panel:" + p.panel,
          kind: "panel",
          title: p.panel,
          core: p.routes_to_core,
          sub: `→ ${{p.routes_to_core}} · ${{p.record_count ?? "?"}} records · tier ${{p.tier ?? "?"}}`,
          tier: p.coverage_tier,
          haystack: [p.panel, p.routes_to_core, p.lean_module, ...(p.maps_to_lean || []), ...(p.tags || [])].join(" ").toLowerCase(),
          raw: p,
        }});
      }}
      for (const r of DATA.problem_routes || []) {{
        items.push({{
          id: "intent:" + r.intent,
          kind: "intent",
          title: r.intent.replace(/_/g, " "),
          core: r.core_domain,
          sub: `${{r.core_domain}} · ${{(r.panels || []).length}} panels · ${{(r.keywords || []).slice(0, 4).join(", ")}}`,
          tier: null,
          haystack: [r.intent, r.core_domain, ...(r.keywords || []), ...(r.panels || [])].join(" ").toLowerCase(),
          raw: r,
        }});
      }}
      for (const d of DATA.desktop_projects || []) {{
        items.push({{
          id: "desktop:" + d.folder,
          kind: "desktop",
          title: d.folder,
          core: d.theme_label || d.theme,
          sub: `${{d.lean_lab}} · ${{d.wire_status}}`,
          tier: null,
          haystack: [d.folder, d.theme, d.theme_label, d.lean_lab].join(" ").toLowerCase(),
          raw: d,
        }});
      }}
    }}

    function tokens(q) {{
      return q.toLowerCase().split(/\\s+/).filter(Boolean);
    }}

    function matches(item, q) {{
      if (filter !== "all" && item.kind !== filter) return false;
      if (activeIntent) {{
        const route = DATA.problem_routes.find(r => r.intent === activeIntent);
        if (!route) return false;
        const hay = route.keywords.join(" ") + " " + route.core_domain + " " + route.panels.join(" ");
        const t = tokens(q).length ? tokens(q) : tokens(hay);
        if (!t.every(tok => item.haystack.includes(tok))) return false;
        if (item.kind === "panel") return (route.panels || []).includes(item.title) || item.raw.routes_to_core === route.core_domain;
        if (item.kind === "core") return item.title === route.core_domain;
        if (item.kind === "intent") return item.raw.intent === activeIntent;
        return t.every(tok => item.haystack.includes(tok));
      }}
      if (!q.trim()) return true;
      return tokens(q).every(tok => item.haystack.includes(tok));
    }}

    function renderStats() {{
      const s = DATA.summary || {{}};
      document.getElementById("stats").innerHTML = [
        ["Core domains", s.core_domains],
        ["Extension panels", s.extension_panels],
        ["Problem routes", s.problem_routes],
        ["Empirical records", s.total_empirical_records?.toLocaleString()],
        ["C_thin", s.c_thin_panels],
      ].map(([k, v]) => `<div class="stat"><strong>${{v ?? "—"}}</strong> ${{k}}</div>`).join("");
      document.getElementById("gen-at").textContent = DATA.generated_at || "";
    }}

    function renderIntents() {{
      const el = document.getElementById("intents");
      el.innerHTML = (DATA.problem_routes || []).map(r => `
        <button class="intent-chip" data-intent="${{r.intent}}">
          ${{r.intent.replace(/_/g, " ")}}
          <small>${{r.core_domain}} · ${{(r.keywords || []).slice(0, 3).join(", ")}}</small>
        </button>
      `).join("");
      el.querySelectorAll(".intent-chip").forEach(btn => {{
        btn.addEventListener("click", () => {{
          const intent = btn.dataset.intent;
          if (activeIntent === intent) {{
            activeIntent = null;
            btn.classList.remove("active");
          }} else {{
            activeIntent = intent;
            el.querySelectorAll(".intent-chip").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
          }}
          renderResults();
        }});
      }});
    }}

    function renderResults() {{
      const q = document.getElementById("q").value;
      const hits = items.filter(it => matches(it, q));
      document.getElementById("meta").textContent =
        `${{hits.length}} result${{hits.length === 1 ? "" : "s"}}` +
        (activeIntent ? ` · intent: ${{activeIntent.replace(/_/g, " ")}}` : "") +
        (q.trim() ? ` · “${{q.trim()}}”` : "");
      const box = document.getElementById("results");
      if (!hits.length) {{
        box.innerHTML = '<p class="card-sub">No matches. Try a problem intent chip or broader keywords.</p>';
        return;
      }}
      box.innerHTML = hits.slice(0, 120).map(it => `
        <div class="card${{selectedId === it.id ? " selected" : ""}}" data-id="${{it.id}}">
          <div class="card-head">
            <div class="card-title">${{it.title}}${{tierBadge(it.tier)}}</div>
            <span class="kind-badge">${{it.kind}}</span>
          </div>
          <div class="card-sub">${{it.sub}}</div>
        </div>
      `).join("") + (hits.length > 120 ? `<p class="card-sub">+ ${{hits.length - 120}} more — refine search</p>` : "");
      box.querySelectorAll(".card").forEach(card => {{
        card.addEventListener("click", () => {{
          selectedId = card.dataset.id;
          renderResults();
          renderDetail(items.find(x => x.id === selectedId));
        }});
      }});
    }}

    function pathRow(label, value) {{
      if (!value) return "";
      const esc = value.replace(/"/g, "&quot;");
      return `<div class="path-row"><label>${{label}}</label><code>${{esc}}</code>
        <button class="copy-btn" data-copy="${{esc}}">Copy</button></div>`;
    }}

    function renderDetail(item) {{
      const el = document.getElementById("detail");
      if (!item) {{
        el.innerHTML = '<p class="empty">Select a result to see download paths and reproduction bundle.</p>';
        return;
      }}
      let html = `<h2>${{item.title}}${{tierBadge(item.tier)}}</h2><p class="card-sub">${{item.sub}}</p>`;

      if (item.kind === "panel") {{
        const b = item.raw.download_bundle || {{}};
        html += `<div class="detail-section"><h3>Download / reproduce</h3>
          ${{pathRow("Benchmark", b.benchmark_data)}}
          ${{pathRow("Ingest", b.ingest_script)}}
          ${{pathRow("Build", b.build_script)}}
          ${{pathRow("Manifest", b.manifest)}}
          ${{pathRow("Lean", b.lean_module)}}
        </div>`;
        if (item.raw.maps_to_lean?.length) {{
          html += `<div class="detail-section"><h3>Maps to Lean</h3><div class="tag-list">` +
            item.raw.maps_to_lean.map(t => `<span class="tag">${{t}}</span>`).join("") + `</div></div>`;
        }}
        const siblings = (DATA.by_core_domain || {{}})[item.raw.routes_to_core] || [];
        if (siblings.length > 1) {{
          html += `<div class="detail-section"><h3>Related panels (${{item.raw.routes_to_core}})</h3><div class="tag-list">` +
            siblings.filter(n => n !== item.title).slice(0, 12).map(n => `<span class="tag">${{n}}</span>`).join("") +
            `</div></div>`;
        }}
      }} else if (item.kind === "core") {{
        html += `<div class="detail-section"><h3>Subfield breadth</h3>
          <p class="card-sub">${{item.raw.subfields_touched}} / ${{item.raw.subfields_studied}} subfields (${{item.raw.breadth_pct}}%)</p>
          <p class="card-sub">${{item.raw.breadth_note || ""}}</p></div>`;
        const panels = (DATA.by_core_domain || {{}})[item.title] || [];
        if (panels.length) {{
          html += `<div class="detail-section"><h3>Extension panels (${{panels.length}})</h3><div class="tag-list">` +
            panels.slice(0, 15).map(n => `<span class="tag">${{n}}</span>`).join("") +
            (panels.length > 15 ? `<span class="tag">+${{panels.length - 15}} more</span>` : "") +
            `</div></div>`;
        }}
      }} else if (item.kind === "intent") {{
        const r = item.raw;
        html += `<div class="detail-section"><h3>Keywords</h3><div class="tag-list">` +
          (r.keywords || []).map(k => `<span class="tag">${{k}}</span>`).join("") + `</div></div>`;
        html += `<div class="detail-section"><h3>Panels</h3>`;
        for (const pname of r.panels || []) {{
          const p = panelByName[pname];
          if (p) {{
            const b = p.download_bundle || {{}};
            html += `<p class="card-sub" style="margin-top:0.5rem"><strong>${{pname}}</strong></p>`;
            html += pathRow("Benchmark", b.benchmark_data);
            html += pathRow("Lean", b.lean_module);
          }} else {{
            html += `<span class="tag">${{pname}}</span> `;
          }}
        }}
        html += `</div>`;
      }} else if (item.kind === "desktop") {{
        html += `<div class="detail-section"><h3>Desktop lab</h3>
          ${{pathRow("Theme", item.raw.theme)}}
          ${{pathRow("Lean lab", item.raw.lean_lab)}}
          ${{pathRow("Status", item.raw.wire_status)}}
        </div>`;
      }}

      el.innerHTML = html;
      el.querySelectorAll(".copy-btn").forEach(btn => {{
        btn.addEventListener("click", e => {{
          e.stopPropagation();
          navigator.clipboard.writeText(btn.dataset.copy);
          btn.textContent = "OK";
          setTimeout(() => btn.textContent = "Copy", 1200);
        }});
      }});
    }}

    document.getElementById("q").addEventListener("input", renderResults);
    document.querySelectorAll(".filter-btn").forEach(btn => {{
      btn.addEventListener("click", () => {{
        document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        filter = btn.dataset.filter;
        renderResults();
      }});
    }});

    buildIndex();
    renderStats();
    renderIntents();
    renderResults();

    const params = new URLSearchParams(location.search);
    const q0 = params.get("q");
    if (q0) document.getElementById("q").value = q0;
    const intent0 = params.get("intent");
    if (intent0) {{
      activeIntent = intent0;
      document.querySelector(`[data-intent="${{intent0}}"]`)?.classList.add("active");
    }}
    if (q0 || intent0) renderResults();
  </script>
</body>
</html>"""