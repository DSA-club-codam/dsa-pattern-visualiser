/* =====================================================================
   viz.js — shared engine for every visualisation page.
   - Components: ArrayRow, vars, countMap, kvMap, stack, queue, legend
   - Page shell: VIZ.mount(PAGE) builds the whole page from data
   - Canvas plug-ins: VIZ.canvas.register(id, { build, render })
   A page never re-implements anything in this file. If a page needs
   something new, add it here (after the user approves it) and show it
   in gallery.html.
   ===================================================================== */
(function () {
  "use strict";
  const VIZ = (window.VIZ = window.VIZ || {});
  VIZ.schemaVersion = 1;

  // ---------- small helpers ----------
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const el = (tag, cls, html) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  };
  const cssNum = (name, fallback) => {
    const v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue(name));
    return Number.isFinite(v) ? v : fallback;
  };
  VIZ.esc = esc;
  VIZ.el = el;

  // =====================================================================
  // ArrayRow — one row of array cells with indices, pointers, bands,
  // a swap arc and an optional "best" bar underneath.
  // Cells are keyed by identity (ids) so a swap slides the cells.
  // =====================================================================
  const ROLE_ROW = { back: 0, front: 1, mid: 2 };

  class ArrayRow {
    /**
     * @param host     element to draw into (its width decides the cell size)
     * @param values   initial values (length n, 0..20)
     * @param opts     { roles: ["back","front"], bar: true|false, minWidth }
     */
    constructor(host, values, opts = {}) {
      this.host = host;
      this.values = values.slice();
      this.roles = opts.roles || ["back", "front"];
      this.hasBar = !!opts.bar;
      this.build();
    }

    build() {
      const n = Math.max(1, this.values.length);
      const pmin = cssNum("--cell-pitch-min", 30), pmax = cssNum("--cell-pitch-max", 60);
      const avail = Math.max(120, this.host.clientWidth - 34);
      const pitch = Math.max(pmin, Math.min(pmax, Math.floor(avail / n)));
      const size = pitch - 6;
      this.pitch = pitch;
      this.size = size;
      // top to bottom: band labels · swap arc · indices · cells · pointers · best bar
      const idxTop = 20;
      const cellTop = 40;
      const ptrTop = cellTop + size + 6;
      const rows = this.roles.length;
      const barTop = ptrTop + rows * 26 + 8;
      this.geo = { cellTop, idxTop, ptrTop, barTop };

      const track = el("div", "ar-track");
      track.style.width = n * pitch + "px";
      track.style.height = (this.hasBar ? barTop + 28 : ptrTop + rows * 26) + "px";
      track.style.fontSize = Math.max(13, Math.min(18, size * 0.38)) + "px";
      track.classList.toggle("small", pitch < 44);
      this.track = track;

      this.bandEls = {};
      for (const kind of ["best", "gap", "window"]) {
        const b = el("div", "ar-band " + kind);
        b.style.top = cellTop - 5 + "px";
        b.style.height = size + 10 + "px";
        b.style.opacity = 0;
        const l = el("div", "ar-blabel " + kind);
        l.style.opacity = 0;
        track.append(b, l);
        this.bandEls[kind] = { band: b, label: l };
      }
      this.arc = el("div", "ar-arc", "<span></span>");
      this.arc.style.top = "4px";
      this.arc.style.opacity = 0;
      track.append(this.arc);

      for (let i = 0; i < this.values.length; i++) {
        const ix = el("div", "ar-idx", String(i));
        ix.style.left = i * pitch + "px";
        ix.style.width = pitch + "px";
        ix.style.top = idxTop + "px";
        track.append(ix);
      }
      this.cells = this.values.map((v, id) => {
        const c = el("div", "ar-cell", esc(v));
        c.style.width = size + "px";
        c.style.height = size + "px";
        c.style.top = cellTop + "px";
        c.style.transform = `translateX(${id * pitch + 3}px)`;
        track.append(c);
        return c;
      });
      this.ptrEls = {};
      this.roles.forEach((role, row) => {
        const p = el("div", "ar-ptr " + role);
        p.style.width = pitch + "px";
        p.style.top = ptrTop + row * 26 + "px";
        p.style.opacity = 0;
        track.append(p);
        this.ptrEls[role] = p;
      });
      if (this.hasBar) {
        this.bar = el("div", "ar-bar");
        this.bar.style.top = barTop + "px";
        this.bar.style.opacity = 0;
        this.barLbl = el("div", "ar-barlbl");
        this.barLbl.style.top = barTop + 8 + "px";
        this.barLbl.style.opacity = 0;
        track.append(this.bar, this.barLbl);
      }
      this.host.innerHTML = "";
      this.host.append(track);
    }

    /**
     * @param s {
     *   arr:      current values by position
     *   ids:      identity at each position (optional; default = position)
     *   cls:      { pos: "current conflict ..." } extra classes per position
     *   tags:     { pos: ">k" } small red badge per position
     *   bands:    [{ kind: "window"|"best"|"gap", from, to, label }]  (to is inclusive)
     *   arc:      { from, to, label } | null
     *   pointers: [{ role: "back"|"front"|"mid", label, at, dim }]
     *   bar:      { from, to, label } | null
     * }
     */
    update(s) {
      const p = this.pitch;
      const arr = s.arr;
      const ids = s.ids || arr.map((_, i) => i);
      const cls = s.cls || {};
      const tags = s.tags || {};
      ids.forEach((id, pos) => {
        const c = this.cells[id];
        if (!c) return;
        c.style.transform = `translateX(${pos * p + 3}px)`;
        c.className = "ar-cell" + (cls[pos] ? " " + cls[pos] : "");
        c.innerHTML = esc(arr[pos]) + (tags[pos] ? `<span class="tag">${esc(tags[pos])}</span>` : "");
      });
      // bands
      const used = new Set();
      for (const b of s.bands || []) {
        const e = this.bandEls[b.kind];
        if (!e || b.to < b.from) continue;
        used.add(b.kind);
        e.band.style.left = b.from * p + "px";
        e.band.style.width = (b.to - b.from + 1) * p + "px";
        e.band.style.opacity = 1;
        e.label.textContent = b.label || "";
        e.label.style.left = ((b.from + b.to + 1) * p) / 2 + "px";
        e.label.style.opacity = b.label ? 1 : 0;
      }
      for (const k of Object.keys(this.bandEls)) {
        if (!used.has(k)) {
          this.bandEls[k].band.style.opacity = 0;
          this.bandEls[k].label.style.opacity = 0;
        }
      }
      // arc
      if (s.arc && s.arc.to > s.arc.from) {
        this.arc.style.left = (s.arc.from + 0.5) * p + "px";
        this.arc.style.width = (s.arc.to - s.arc.from) * p + "px";
        this.arc.querySelector("span").textContent = s.arc.label || "";
        this.arc.style.opacity = 1;
      } else this.arc.style.opacity = 0;
      // pointers
      const seen = new Set();
      for (const ptr of s.pointers || []) {
        const e = this.ptrEls[ptr.role];
        if (!e) continue;
        seen.add(ptr.role);
        const at = Math.max(0, Math.min(arr.length - 1, ptr.at == null ? 0 : ptr.at));
        e.innerHTML = "▲<br>" + esc(ptr.label);
        e.style.left = at * p + "px";
        e.style.opacity = ptr.at == null ? 0 : ptr.dim ? 0.35 : 1;
      }
      for (const r of Object.keys(this.ptrEls)) if (!seen.has(r)) this.ptrEls[r].style.opacity = 0;
      // bar
      if (this.hasBar) {
        if (s.bar) {
          this.bar.style.left = s.bar.from * p + 5 + "px";
          this.bar.style.width = (s.bar.to - s.bar.from + 1) * p - 10 + "px";
          this.bar.style.opacity = 1;
          this.barLbl.style.left = s.bar.from * p + 5 + "px";
          this.barLbl.textContent = s.bar.label || "";
          this.barLbl.style.opacity = 1;
        } else {
          this.bar.style.opacity = 0;
          this.barLbl.style.opacity = 0;
        }
      }
    }
  }
  VIZ.ArrayRow = ArrayRow;

  // =====================================================================
  // Aux components
  // =====================================================================

  /** vars: [{ label, value, role?: "back"|"front"|"mid", flash?: bool }] */
  VIZ.vars = function (host, vars, flash) {
    host.innerHTML = "";
    const dl = el("dl", "vars");
    for (const v of vars) {
      const dt = el("dt", v.role || "", esc(v.label));
      const span = el("span", "", esc(v.value == null ? "—" : v.value));
      if (flash && v.flash) span.classList.add("flash");
      const dd = el("dd");
      dd.append(span);
      dl.append(dt, dd);
    }
    host.append(dl);
  };

  /** countMap: rows [{ key, count }], limit = max allowed count */
  VIZ.countMap = function (host, rows, limit, title) {
    host.innerHTML = title ? `<h3>${title}</h3>` : "";
    for (const r of rows) {
      let slots = "";
      const cap = Math.max(limit + 1, r.count);
      for (let i = 1; i <= cap; i++)
        slots += `<span class="cm-slot${i > limit ? " extra" : ""}${i <= r.count ? " on" : ""}"></span>`;
      const over = r.count > limit;
      host.insertAdjacentHTML(
        "beforeend",
        `<div class="cm-row${over ? " over" : ""}"><span class="cm-key mono">${esc(r.key)}</span>` +
          `<span class="cm-slots">${slots}</span><span class="cm-num mono">${r.count}${over ? " &gt; " + limit : ""}</span></div>`
      );
    }
  };

  /** kvMap: rows [{ key, value, mark?: "hit"|"new" }] */
  VIZ.kvMap = function (host, rows, title) {
    host.innerHTML = (title ? `<h3>${title}</h3>` : "") +
      `<table class="kv">${rows.map((r) => `<tr class="${r.mark || ""}"><td class="mono">${esc(r.key)}</td><td class="mono">${esc(r.value)}</td></tr>`).join("")}</table>`;
  };

  /** stack: items bottom→top [{ value, mark?: "new"|"gone" }] */
  VIZ.stack = function (host, items, title) {
    host.innerHTML = (title ? `<h3>${title}</h3>` : "") + `<div class="sq-lbl">top</div>`;
    const s = el("div", "stk");
    items.forEach((it, i) => s.append(el("div", (i === items.length - 1 ? "top " : "") + (it.mark || ""), esc(it.value))));
    host.append(s);
    host.insertAdjacentHTML("beforeend", `<div class="sq-lbl">bottom</div>`);
  };

  /** queue: items front→back [{ value, mark?: "new"|"gone" }] */
  VIZ.queue = function (host, items, title) {
    host.innerHTML = (title ? `<h3>${title}</h3>` : "") + `<div class="sq-lbl">front → back</div>`;
    const q = el("div", "que");
    items.forEach((it) => q.append(el("div", it.mark || "", esc(it.value))));
    host.append(q);
  };

  /** legend: [{ swatch, text, label? }] — swatch names are listed in design-system.md */
  VIZ.legend = function (host, items) {
    host.innerHTML = "";
    for (const it of items) {
      const d = el("div");
      let sw;
      if (it.swatch.startsWith("ptr-")) sw = el("span", "sw ptr " + it.swatch.slice(4), "▲");
      else sw = el("span", "sw " + it.swatch, it.label ? esc(it.label) : "");
      d.append(sw, document.createTextNode(it.text));
      host.append(d);
    }
  };

  /** code block: lines [{ src, comment }] */
  VIZ.codeBlock = function (lines) {
    const pre = el("pre", "code");
    pre.innerHTML = lines
      .map((l, i) => `<span class="ln" data-line="${i + 1}"><b>${i + 1}</b>${esc(l.src)}${l.comment ? (l.src.trim() ? "  " : "") + '<span class="c">' + esc(l.comment) + "</span>" : ""}</span>`)
      .join("");
    return pre;
  };

  // =====================================================================
  // Canvas plug-in registry
  // =====================================================================
  const canvases = {};
  VIZ.canvas = {
    register(id, impl) { canvases[id] = impl; },
    get(id) { return canvases[id]; },
  };

  // =====================================================================
  // Page shell
  // =====================================================================
  const LANG_LABEL = { python: "Python3", cpp: "C++17", c: "C" };
  const LANG_ORDER = ["python", "cpp", "c"];

  // Rule-of-thumb table: n → what complexity still fits in ~1 second.
  const CHEATSHEET = [
    { max: 10, fits: "O(n!)", ex: "all permutations" },
    { max: 20, fits: "O(2ⁿ)", ex: "all subsets, backtracking" },
    { max: 500, fits: "O(n³)", ex: "three nested loops" },
    { max: 5000, fits: "O(n²)", ex: "two nested loops, brute force on pairs" },
    { max: 1e6, fits: "O(n log n) or O(n)", ex: "sorting, two pointers, sliding window, hash map" },
    { max: Infinity, fits: "O(log n) or O(1)", ex: "binary search, maths" },
  ];

  function fmtN(n) {
    if (n === Infinity) return "more";
    if (n >= 1000 && Math.log10(n) % 1 === 0) return "10" + String(Math.log10(n)).split("").map((d) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[d]).join("");
    return n.toLocaleString("en-GB");
  }

  VIZ.mount = function (PAGE, root) {
    root = root || document.getElementById("app");
    const P = PAGE.problem, S = PAGE.site || {};
    const st = { a: 0, e: 0, cur: 0, timer: null, lang: "python" };

    // ---------- layout (ADR 017) ----------
    // left column = animation, code under it; right column = variables, controls, caption.
    // Controls sit above the caption so the Next button never moves when a caption is longer.
    const SRC = P.source || {};
    const srcShort = SRC.short || { LeetCode: "LC", NeetCode: "NC" }[SRC.site] || "";
    const label = SRC.id ? `${srcShort} ${SRC.id} · ` : "";

    // ---------- static skeleton ----------
    const parts = {
      canvas: `<div class="panel vz-canvas" id="vz-canvas"></div>`,
      aux: `<div class="vz-aux" id="vz-aux"><div class="panel" id="vz-vars"></div></div>`,
      caption: `<div class="panel vz-caption" aria-live="polite">
        <div><span class="phase" id="vz-phase"></span><span class="vz-cap" id="vz-cap"></span></div>
        <div class="vz-inv" id="vz-inv"></div></div>`,
      controls: `<div class="vz-controls">
        <button id="vz-reset">⏮ Reset</button><button id="vz-prev">◀ Prev</button>
        <button id="vz-play">▶ Play</button><button id="vz-next">Next ▶</button>
        <label>Speed <input id="vz-speed" type="range" min="1" max="10" value="5"></label>
        <span class="vz-counter" id="vz-counter"></span></div>
        <div class="hint">Keyboard: ← / → to step, Space to play or pause, Home to reset.</div>`,
      code: `<details class="panel" id="vz-code"><summary>Show code</summary><div class="vz-tabs" id="vz-tabs" role="tablist" aria-label="Language"></div><div id="vz-code-body"></div></details>`,
    };
    const body = `<div class="vz-stage"><div class="vz-col">${parts.canvas}${parts.code}</div>
           <div class="vz-col">${parts.aux}${parts.controls}${parts.caption}</div></div>`;
    root.innerHTML = `
      <header class="vz-header"><h1>${esc(label)}${esc(P.title)}</h1>
        <span class="pill ${esc(P.difficulty.toLowerCase())}">${esc(P.difficulty)}</span>
        ${SRC.url ? `<a class="ext" href="${esc(SRC.url)}" target="_blank" rel="noopener">Open on ${esc(SRC.site || "the source site")} ↗</a>` : ""}</header>
      <div class="vz-meta" id="vz-meta"></div>
      <div class="vz-approaches" id="vz-approaches" role="tablist" aria-label="Approaches"></div>
      <details class="panel" id="vz-compare" hidden><summary>Compare approaches</summary><div class="vz-table-wrap" id="vz-compare-body"></div></details>
      <details class="panel" id="vz-constraints"><summary>Constraints — what they tell you</summary><div id="vz-constraints-body"></div></details>
      <details class="panel" id="vz-card"><summary>Why this pattern?</summary><div id="vz-card-body"></div></details>
      <div class="vz-examples" id="vz-examples" role="group" aria-label="Example input"></div>
      ${body}
      <details class="panel" id="vz-legend-wrap"><summary>Legend</summary><div class="vz-legend" id="vz-legend" aria-label="Legend"></div></details>
      <footer class="vz-footer" id="vz-footer"></footer>`;
    const $ = (id) => document.getElementById(id);

    // ---------- constraints (problem level) ----------
    (function constraints() {
      const rows = (P.constraints || [])
        .map((c) => `<tr><td class="mono">${esc(c.text)}</td><td>${esc(c.meaning)}</td><td>${esc(c.impact)}</td></tr>`)
        .join("");
      let hit = -1;
      if (P.nMax) hit = CHEATSHEET.findIndex((r) => P.nMax <= r.max);
      const sheet = CHEATSHEET.map((r, i) => {
        const prev = i === 0 ? null : CHEATSHEET[i - 1].max;
        const range = prev === null ? `n ≤ ${fmtN(r.max)}` : r.max === Infinity ? `n > ${fmtN(prev)}` : `n ≤ ${fmtN(r.max)}`;
        return `<tr class="${i === hit ? "hit" : ""}"><td class="mono">${range}</td><td class="mono">${r.fits}</td><td>${r.ex}</td></tr>`;
      }).join("");
      $("vz-constraints-body").innerHTML =
        `<div class="vz-table-wrap"><table class="vz-table"><thead><tr><th>Constraint</th><th>What it means</th><th>What it changes</th></tr></thead><tbody>${rows}</tbody></table></div>` +
        `<p class="vz-sub"><b>Rule of thumb:</b> about 10⁸ simple operations run in one second. Find the row for n to see which complexity is fast enough.` +
        (hit >= 0 ? ` Here n can be up to ${fmtN(P.nMax)}.` : "") + `</p>` +
        `<div class="vz-table-wrap"><table class="vz-table"><thead><tr><th>n</th><th>Fast enough</th><th>Typical approach</th></tr></thead><tbody>${sheet}</tbody></table></div>`;
    })();

    // ---------- footer ----------
    (function footer() {
      const links = [`<a href="index.html">All visualisations</a>`];
      if (S.notionPatterns) links.push(`<a href="${esc(S.notionPatterns)}" target="_blank" rel="noopener">Pattern guides (Notion) ↗</a>`);
      if (S.bigO) links.push(`<a href="${esc(S.bigO)}" target="_blank" rel="noopener">Big-O reference ↗</a>`);
      if (S.leetcodeProfile) links.push(`<a href="${esc(S.leetcodeProfile)}" target="_blank" rel="noopener">Accepted solutions on LeetCode ↗</a>`);
      $("vz-footer").innerHTML = links.join("");
    })();

    // ---------- approach tabs ----------
    const approaches = PAGE.approaches;
    if (approaches.length > 1) {
      $("vz-approaches").innerHTML = approaches
        .map((a, i) => `<button role="tab" data-a="${i}" aria-selected="false">${esc(a.name)}</button>`)
        .join("");
      $("vz-compare").hidden = false;
      $("vz-compare-body").innerHTML =
        `<table class="vz-table"><thead><tr><th>Approach</th><th>Time</th><th>Space</th><th>When to choose it</th></tr></thead><tbody>` +
        approaches.map((a) => `<tr><td><a href="#${esc(a.id)}">${esc(a.name)}</a></td><td class="mono">${esc(a.time)}</td><td class="mono">${esc(a.space)}</td><td>${esc(a.whenToUse || "")}</td></tr>`).join("") +
        `</tbody></table>`;
      $("vz-approaches").addEventListener("click", (e) => {
        const b = e.target.closest("[data-a]");
        if (b) selectApproach(+b.dataset.a, true);
      });
    } else $("vz-approaches").remove();

    // ---------- per-approach parts ----------
    let canvasImpl = null, ctx = null;

    function selectApproach(i, push) {
      stop();
      st.a = i;
      const A = approaches[i];
      if (push !== false && approaches.length > 1) history.replaceState(null, "", "#" + A.id);
      document.querySelectorAll("#vz-approaches [data-a]").forEach((b) => b.setAttribute("aria-selected", +b.dataset.a === i));
      const bigO = S.bigO ? ` <a class="ext" href="${esc(S.bigO)}" target="_blank" rel="noopener">Big-O ↗</a>` : "";
      $("vz-meta").innerHTML =
        `<span class="badge">${esc(A.pattern)}</span>` +
        (A.ds || []).map((d) => `<span class="badge ds">${esc(d)}</span>`).join("") +
        `<span class="cx">${esc(A.time)} time · ${esc(A.space)} space</span>${bigO}`;
      const C = A.card || {};
      const bf = P.bruteForce || {};
      $("vz-card-body").innerHTML =
        `<ul>` +
        (C.signals ? `<li><b>Signals:</b> ${esc(C.signals)}</li>` : "") +
        (bf.summary ? `<li><b>Brute force:</b> ${esc(bf.summary)}</li>` : "") +
        (C.pattern ? `<li><b>Pattern:</b> ${esc(C.pattern)}</li>` : "") +
        (C.coreIdea ? `<li><b>Core idea:</b> ${esc(C.coreIdea)}</li>` : "") +
        `<li id="vz-ops"></li></ul>` +
        (bf.code ? `<details><summary>Brute force code (Python3)</summary><div id="vz-bf-code"></div></details>` : "");
      if (bf.code) $("vz-bf-code").append(VIZ.codeBlock(bf.code));
      VIZ.legend($("vz-legend"), A.legend || []);
      buildCode(A);
      // examples
      const ex = A.examples;
      const mains = ex.map((x, j) => [x, j]).filter(([x]) => x.kind !== "edge");
      const edges = ex.map((x, j) => [x, j]).filter(([x]) => x.kind === "edge");
      const btn = ([x, j]) => `<button data-ex="${j}" aria-pressed="false" title="${esc(x.inputText)}">${esc(x.label)}</button>`;
      $("vz-examples").innerHTML =
        `<span class="lbl">Examples:</span>${mains.map(btn).join("")}` +
        (edges.length ? `<span class="sep"></span><span class="lbl">Edge cases:</span>${edges.map(btn).join("")}` : "");
      canvasImpl = VIZ.canvas.get(A.canvas);
      if (!canvasImpl) throw new Error("Canvas not registered: " + A.canvas);
      selectExample(0);
    }

    function buildCode(A) {
      const langs = LANG_ORDER.filter((l) => A.code[l]);
      if (!langs.includes(st.lang)) st.lang = langs[0];
      const acc = new Set(A.accepted || []);
      $("vz-tabs").innerHTML = langs
        .map((l) => `<button role="tab" data-lang="${l}" aria-selected="${l === st.lang}">${LANG_LABEL[l]}${acc.has(l) ? '<span class="acc" title="Accepted">✓</span>' : ""}</button>`)
        .join("");
      const body = $("vz-code-body");
      body.innerHTML = "";
      for (const l of langs) {
        const pre = VIZ.codeBlock(A.code[l].lines);
        pre.dataset.lang = l;
        pre.hidden = l !== st.lang;
        body.append(pre);
      }
      const notes = [];
      if (acc.size) notes.push("✓ = accepted on " + (SRC.site || "the judge") + " in that language.");
      if (!A.code.c && A.noC) notes.push("No C version: " + A.noC);
      if (notes.length) body.insertAdjacentHTML("beforeend", `<p class="note">${notes.map(esc).join(" ")}</p>`);
    }

    $("vz-tabs").addEventListener("click", (e) => {
      const b = e.target.closest("[data-lang]");
      if (!b) return;
      st.lang = b.dataset.lang;
      document.querySelectorAll("#vz-tabs [data-lang]").forEach((x) => x.setAttribute("aria-selected", x.dataset.lang === st.lang));
      document.querySelectorAll("#vz-code-body pre").forEach((p) => (p.hidden = p.dataset.lang !== st.lang));
      highlightCode();
    });

    function selectExample(j) {
      stop();
      st.e = j;
      st.cur = 0;
      document.querySelectorAll("#vz-examples [data-ex]").forEach((b) => b.setAttribute("aria-pressed", +b.dataset.ex === j));
      buildCanvas();
      render(false);
    }

    function buildCanvas() {
      const A = approaches[st.a], X = A.examples[st.e];
      const aux = $("vz-aux");
      aux.querySelectorAll(".extra").forEach((n) => n.remove());
      ctx = { canvas: $("vz-canvas"), aux, approach: A, example: X, problem: P, extraPanel() {
        const p = el("div", "panel extra");
        aux.append(p);
        return p;
      } };
      canvasImpl.build(ctx);
      const ops = X.ops || {};
      const unit = P.bruteForce && P.bruteForce.opsUnit ? P.bruteForce.opsUnit : "operations";
      $("vz-ops").innerHTML = ops.brute != null
        ? `<b>On this input:</b> brute force needs ${ops.brute} ${esc(unit)}, this approach needs ${ops.approach}.`
        : "";
    }

    function highlightCode() {
      const A = approaches[st.a], s = A.examples[st.e].steps[st.cur];
      for (const pre of document.querySelectorAll("#vz-code-body pre")) {
        const line = (A.code[pre.dataset.lang].anchors || {})[s.anchor];
        let on = null;
        pre.querySelectorAll(".ln").forEach((l) => {
          const hit = +l.dataset.line === line;
          l.classList.toggle("on", hit);
          if (hit) on = l;
        });
        if (on && !pre.hidden && pre.scrollHeight > pre.clientHeight) {
          const top = on.offsetTop - pre.offsetTop, h = pre.clientHeight;
          if (top < pre.scrollTop || top > pre.scrollTop + h - 40) pre.scrollTop = Math.max(0, top - h / 3);
        }
      }
    }

    function render(flash) {
      const A = approaches[st.a], X = A.examples[st.e], steps = X.steps, s = steps[st.cur];
      canvasImpl.render(s, ctx, flash);
      VIZ.vars($("vz-vars"), s.vars || [], flash);
      $("vz-phase").textContent = (A.phases && A.phases[s.phase]) || s.phase;
      $("vz-cap").textContent = s.caption;
      const inv = s.invariant || A.invariant;
      $("vz-inv").textContent = inv ? "Invariant: " + inv : "";
      $("vz-counter").textContent = `Step ${st.cur + 1} / ${steps.length}`;
      $("vz-prev").disabled = st.cur === 0;
      $("vz-next").disabled = st.cur === steps.length - 1;
      highlightCode();
    }

    const nSteps = () => approaches[st.a].examples[st.e].steps.length;
    function go(i, flash) { st.cur = Math.max(0, Math.min(nSteps() - 1, i)); render(flash); }
    function delay() { return 2200 - $("vz-speed").value * 200; }
    function stop() { clearTimeout(st.timer); st.timer = null; $("vz-play").textContent = "▶ Play"; }
    function tick() {
      if (st.cur >= nSteps() - 1) return stop();
      go(st.cur + 1, true);
      st.timer = setTimeout(tick, delay());
    }
    function toggle() {
      if (st.timer) return stop();
      if (st.cur >= nSteps() - 1) go(0);
      $("vz-play").textContent = "⏸ Pause";
      st.timer = setTimeout(tick, Math.min(400, delay()));
    }

    $("vz-reset").onclick = () => { stop(); go(0); };
    $("vz-prev").onclick = () => { stop(); go(st.cur - 1); };
    $("vz-next").onclick = () => { stop(); go(st.cur + 1, true); };
    $("vz-play").onclick = toggle;
    $("vz-examples").addEventListener("click", (e) => {
      const b = e.target.closest("[data-ex]");
      if (b) selectExample(+b.dataset.ex);
    });
    root.addEventListener("click", (e) => { if (e.target.closest("button")) e.target.closest("button").blur(); });
    document.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
      if (e.key === "ArrowRight") { stop(); go(st.cur + 1, true); }
      else if (e.key === "ArrowLeft") { stop(); go(st.cur - 1); }
      else if (e.key === " ") { e.preventDefault(); toggle(); }
      else if (e.key === "Home") { stop(); go(0); }
    });
    let rt;
    window.addEventListener("resize", () => {
      clearTimeout(rt);
      rt = setTimeout(() => { buildCanvas(); render(false); }, 120);
    });
    window.addEventListener("hashchange", () => {
      const i = approaches.findIndex((a) => "#" + a.id === location.hash);
      if (i >= 0 && i !== st.a) selectApproach(i, false);
    });

    const start = Math.max(0, approaches.findIndex((a) => "#" + a.id === location.hash));
    selectApproach(start, false);

    // test hook for the smoke test in build.py
    VIZ._page = { st, go, selectApproach, selectExample, nSteps };
  };
})();
