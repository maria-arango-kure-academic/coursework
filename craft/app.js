// Brewery 2032 simulation — group laptop controller.
// Talks to storage.js for live sync via jsonblob (Path 2 architecture).
// Officer phones poll the same team blob via officer.js.

(function () {
  "use strict";

  const C = window.content;
  const S = window.brewerystorage;
  const LOCAL_KEY = "brewery-2032-local";
  const SCREENS = ["welcome", "round1", "outcome1", "event", "round2", "final", "stakes", "reflection", "summary"];
  const META_SCREENS = ["setup", "session-created", "qr", "compare"];

  const local = loadLocal() || freshLocal();
  let team = local.team || null;       // remote team state, mirrored from jsonblob
  let teamId = local.teamId || null;
  let sessionId = local.sessionId || null;
  let brewery = local.brewery || "";

  function freshLocal() {
    return {
      sessionId: null,
      teamId: null,
      brewery: "",
      team: null,
      reflections: { r1_discussion: "", r1_reasoning: "", o1: "", event: "", r2_discussion: "", r2_reasoning: "", final: "", stakeReflection: "", hardest: "", replay: "", sequencing: "" },
      screen: "setup"
    };
  }

  function loadLocal() {
    try { const raw = localStorage.getItem(LOCAL_KEY); return raw ? JSON.parse(raw) : null; } catch (e) { return null; }
  }

  function saveLocal() {
    local.sessionId = sessionId;
    local.teamId = teamId;
    local.brewery = brewery;
    local.team = team;
    try { localStorage.setItem(LOCAL_KEY, JSON.stringify(local)); } catch (e) {}
  }

  function reset() {
    try { localStorage.removeItem(LOCAL_KEY); } catch (e) {}
    Object.assign(local, freshLocal());
    team = null; teamId = null; sessionId = null; brewery = "";
    show("setup");
  }

  // -- URL params (for ?view=compare) ---------------------------------

  function urlParams() {
    return new URLSearchParams(window.location.search);
  }

  // -- Routing --------------------------------------------------------

  function show(screen) {
    local.screen = screen;
    saveLocal();
    document.querySelectorAll(".screen").forEach(el => {
      el.classList.toggle("active", el.dataset.screen === screen);
    });
    const isFlow = SCREENS.includes(screen);
    document.getElementById("progress").style.display = isFlow ? "" : "none";
    document.querySelectorAll(".dot").forEach(el => {
      const idx = SCREENS.indexOf(screen);
      const stepIdx = SCREENS.indexOf(el.dataset.step);
      el.classList.toggle("done", stepIdx < idx);
      el.classList.toggle("current", stepIdx === idx);
    });
    window.scrollTo(0, 0);
    render(screen);
    // Sync screen change to team blob so officer phones can react.
    if (isFlow && team && teamId) {
      team.screen = screen;
      S.writeTeam(teamId, team).catch(() => {});
    }
  }

  function render(screen) {
    if (screen === "setup") renderSetup();
    if (screen === "session-created") renderSessionCreated();
    if (screen === "qr") renderQR();
    if (screen === "welcome") renderWelcome();
    if (screen === "round1") renderRound1();
    if (screen === "outcome1") renderOutcome1();
    if (screen === "event") renderEvent();
    if (screen === "round2") renderRound2();
    if (screen === "final") renderFinal();
    if (screen === "stakes") renderStakes();
    if (screen === "reflection") renderReflection();
    if (screen === "summary") renderSummary();
    if (screen === "compare") renderCompare();
  }

  // -- Setup screen ---------------------------------------------------

  function renderSetup() {
    const t = C.session;
    document.getElementById("setup-heading").textContent = t.setupHeading;
    document.getElementById("setup-intro").textContent = t.setupIntro;
    document.getElementById("setup-brewery-label").textContent = t.breweryLabel;
    document.getElementById("setup-brewery-hint").textContent = t.breweryHint;
    document.getElementById("setup-code-label").textContent = t.codeLabel;
    document.getElementById("setup-code-hint").textContent = t.codeHint;
    document.querySelector('[data-action="join"]').textContent = t.joinLabel;
    document.querySelector('[data-action="new-session"]').textContent = t.newSessionLabel;
    document.getElementById("brewery-input").value = brewery || "";
    document.getElementById("session-input").value = sessionId || "";
  }

  function renderSessionCreated() {
    const t = C.session;
    document.getElementById("session-created-heading").textContent = t.sessionCreatedLabel;
    document.getElementById("session-created-hint").textContent = t.sessionCreatedHint;
    document.getElementById("big-session-code").textContent = sessionId || "";
  }

  function renderQR() {
    const t = C.session;
    document.getElementById("qr-heading").textContent = t.qrHeading;
    document.getElementById("qr-intro").textContent = t.qrIntro;
    document.getElementById("qr-session-label").textContent = t.qrSessionLabel + ":";
    document.getElementById("qr-session-value").textContent = sessionId;
    document.getElementById("qr-brewery-label").textContent = t.qrBreweryLabel + ":";
    document.getElementById("qr-brewery-value").textContent = brewery;
    document.getElementById("qr-fallback-label").textContent = t.qrFallbackLabel;

    const officerUrl = buildOfficerUrl();
    document.getElementById("qr-url").textContent = officerUrl;
    drawQR("qr-canvas", officerUrl);

    document.querySelector('[data-action="next-from-qr"]').textContent = t.qrContinueLabel;
  }

  function buildOfficerUrl() {
    const base = window.location.href.replace(/index\.html.*$/, "").replace(/\?.*$/, "").replace(/[^/]*$/, "");
    const root = base.endsWith("/") ? base : base + "/";
    return root + "officer.html?session=" + encodeURIComponent(sessionId) + "&brewery=" + encodeURIComponent(brewery);
  }

  function drawQR(elId, text) {
    const el = document.getElementById(elId);
    el.innerHTML = "";
    if (typeof qrcode !== "function") {
      el.textContent = text;
      return;
    }
    const qr = qrcode(0, "M");
    qr.addData(text);
    qr.make();
    el.innerHTML = qr.createSvgTag({ scalable: true, margin: 2 });
    const svg = el.querySelector("svg");
    if (svg) {
      svg.setAttribute("width", "260");
      svg.setAttribute("height", "260");
      svg.style.background = "#fff";
      svg.style.padding = "0.5rem";
      svg.style.borderRadius = "6px";
    }
  }

  // -- Welcome --------------------------------------------------------

  function renderWelcome() {
    document.getElementById("welcome-title").textContent = C.welcome.title;
    const body = document.getElementById("welcome-body");
    body.innerHTML = "";
    C.welcome.body.forEach(p => { const el = document.createElement("p"); el.textContent = p; body.appendChild(el); });
    document.querySelector('[data-action="start"]').textContent = C.welcome.startLabel;
  }

  // -- Round 1 --------------------------------------------------------

  function renderRound1() {
    document.getElementById("r1-heading").textContent = C.round1.heading;
    document.getElementById("r1-situation").textContent = C.round1.situation;
    document.getElementById("r1-question").textContent = C.round1.question;
    document.getElementById("r1-discussion-label").textContent = C.round1.discussionPrompt;
    document.getElementById("r1-reasoning-label").textContent = C.round1.reasoningPrompt;

    const fs = document.getElementById("r1-options");
    fs.innerHTML = "";
    C.round1.options.forEach(opt => fs.appendChild(optionEl("r1", opt, getRound1() === opt.id)));

    bindReflection("r1_discussion");
    bindReflection("r1_reasoning");
    updateContinue("round1", '[data-action="next-from-r1"]', () => !!getRound1());
  }

  function getRound1() { return team && team.round1; }
  function getEvent() { return team && team.event; }
  function getRound2() { return team && team.round2; }

  // -- Outcome 1 ------------------------------------------------------

  function renderOutcome1() {
    if (!getRound1()) return show("round1");
    const o = C.outcomes1[getRound1()];
    document.getElementById("o1-heading").textContent = o.label;
    const cards = document.getElementById("o1-cards");
    cards.innerHTML = "";
    cards.appendChild(envCard(o.environmental));
    cards.appendChild(stateCard("Financial", o.financial.state, o.financial.note));
    cards.appendChild(stateCard("Workforce", o.workforce.state, o.workforce.note));
    document.getElementById("o1-prompt").textContent = C.outcomes1.reflectionPrompt;
    bindReflection("o1");
  }

  // -- Event ----------------------------------------------------------

  async function renderEvent() {
    if (!getEvent()) {
      const params = urlParams();
      const override = params.get("event");
      let chosen;
      if (override && C.events[override]) chosen = override;
      else { const keys = ["E1", "E2", "E3"]; chosen = keys[Math.floor(Math.random() * keys.length)]; }
      team.event = chosen;
      await pushTeam("event");
    }
    const e = C.events[getEvent()];
    const cardEl = document.getElementById("event-card");
    cardEl.innerHTML = "";
    const h = document.createElement("h3"); h.textContent = e.title; cardEl.appendChild(h);
    const p = document.createElement("p"); p.textContent = e.description; cardEl.appendChild(p);
    document.getElementById("event-prompt").textContent = C.events.reflectionPrompt;
    bindReflection("event");
  }

  // -- Round 2 --------------------------------------------------------

  function renderRound2() {
    if (!getRound1() || !getEvent()) return show("round1");
    const key = getRound1() + "_" + getEvent();
    const r2 = C.round2[key];
    document.getElementById("r2-heading").textContent = r2.heading;
    document.getElementById("r2-situation").textContent = r2.situation;
    document.getElementById("r2-discussion-label").textContent = r2.discussionPrompt;
    document.getElementById("r2-reasoning-label").textContent = r2.reasoningPrompt;
    const fs = document.getElementById("r2-options");
    fs.innerHTML = "";
    r2.options.forEach(opt => fs.appendChild(optionEl("r2", opt, getRound2() === opt.id)));
    bindReflection("r2_discussion");
    bindReflection("r2_reasoning");
    updateContinue("round2", '[data-action="next-from-r2"]', () => !!getRound2());
  }

  // -- Final ----------------------------------------------------------

  function renderFinal() {
    document.getElementById("final-heading").textContent = C.finalSnapshot.heading;
    const f = currentFinal();
    if (!f) return;
    const cards = document.getElementById("final-cards");
    cards.innerHTML = "";
    cards.appendChild(stateCard("Environmental", envFinalState(f.environmental.state), f.environmental.note));
    cards.appendChild(stateCard("Financial", f.financial.state, f.financial.note));
    cards.appendChild(stateCard("Workforce", f.workforce.state, f.workforce.note));
    cards.appendChild(stateCard("Industry ranking", f.ranking, ""));
    document.getElementById("final-prompt").textContent = C.finalSnapshot.reflectionPrompt;
    bindReflection("final");
  }

  function envFinalState(s) {
    if (s === "hit") return "targets met";
    if (s === "partial") return "partial";
    if (s === "missed") return "missed";
    return s;
  }

  // -- Stakes ---------------------------------------------------------

  function renderStakes() {
    document.getElementById("stakes-heading").textContent = C.stakeCheck.heading;
    document.getElementById("stakes-intro").textContent = C.stakeCheck.intro;

    // Recap of the final outcome so the team does not have to remember
    const f = currentFinal();
    const recap = document.getElementById("stakes-recap");
    recap.innerHTML = "";
    if (f) {
      const items = [
        ["Environmental", envFinalState(f.environmental.state)],
        ["Financial",    f.financial.state],
        ["Workforce",    f.workforce.state],
        ["Ranking",      f.ranking]
      ];
      items.forEach(([label, val]) => {
        const chip = document.createElement("span");
        chip.className = "recap-chip";
        const k = document.createElement("strong"); k.textContent = label + ":"; chip.appendChild(k);
        const v = document.createElement("span"); v.className = "state-pill " + stateClass(val); v.textContent = val; chip.appendChild(v);
        recap.appendChild(chip);
      });
    }

    // Auto-compute stakes from the data
    const auto = computedStakes(f);
    if (team) {
      team.stakes = auto;
      team.ceoScore = Object.values(auto).filter(v => v === true).length;
      pushTeam("stakes-auto");
    }

    const list = document.getElementById("stakes-list");
    list.innerHTML = "";
    C.stakeCheck.questions.forEach(q => {
      const row = document.createElement("div");
      row.className = "stake-row summary";
      const v = auto ? auto[q.id] : null;
      const mark = v === true ? "yes" : v === false ? "no" : "—";
      row.innerHTML = '<span class="stake-text">' + escape(q.text) + '</span><span class="mark ' + (v === true ? "yes" : v === false ? "no" : "") + '">' + mark + '</span>';
      list.appendChild(row);
    });
    updateCeoScore();

    // Reflection field
    let refLabel = document.getElementById("stakes-reflection-label");
    let refTa = document.querySelector('textarea[data-field="stakeReflection"]');
    if (!refLabel) {
      const wrap = document.createElement("label");
      wrap.className = "reflection";
      const span = document.createElement("span");
      span.id = "stakes-reflection-label";
      wrap.appendChild(span);
      const ta = document.createElement("textarea");
      ta.rows = 3;
      ta.placeholder = "one or two sentences";
      ta.setAttribute("data-field", "stakeReflection");
      wrap.appendChild(ta);
      list.parentNode.insertBefore(wrap, document.getElementById("ceo-score").nextSibling);
      refLabel = span;
      refTa = ta;
    }
    refLabel.textContent = C.stakeCheck.reflectionPrompt;
    bindReflection("stakeReflection");
  }

  function ceoScoreFromAuto() {
    const f = currentFinal();
    return f ? computedStakeCount(f) : 0;
  }

  function renderReflection() {
    document.getElementById("reflection-heading").textContent = C.reflection.heading;
    const wrap = document.getElementById("reflection-prompts");
    wrap.innerHTML = "";
    C.reflection.prompts.forEach(p => {
      const lab = document.createElement("label");
      lab.className = "reflection";
      const span = document.createElement("span"); span.textContent = p.text; lab.appendChild(span);
      const ta = document.createElement("textarea");
      ta.rows = 4;
      ta.placeholder = "share your group's thinking";
      ta.value = local.reflections[p.id] || "";
      ta.addEventListener("input", () => { local.reflections[p.id] = ta.value; saveLocal(); pushTeamReflections(); });
      lab.appendChild(ta);
      wrap.appendChild(lab);
    });
  }

  function renderSummary() {
    document.getElementById("summary-heading").textContent = C.summary.heading;
    document.getElementById("summary-path-label").textContent = C.summary.pathLabel;
    document.getElementById("summary-stakes-label").textContent = C.summary.stakesLabel;
    document.getElementById("summary-reflections-label").textContent = C.summary.reflectionsLabel;
    document.querySelector('[data-action="print"]').textContent = C.summary.printLabel;
    document.querySelector('[data-action="goto-compare"]').textContent = C.summary.compareLabel;

    const path = pathLabel(getRound1()) + "  →  " + eventLabel(getEvent()) + "  →  " + pathLabel(getRound2());
    document.getElementById("summary-path").textContent = path;

    const stakesWrap = document.getElementById("summary-stakes");
    stakesWrap.innerHTML = "";
    C.stakeCheck.questions.forEach(q => {
      const row = document.createElement("div");
      row.className = "stake-row summary";
      const v = team && team.stakes ? team.stakes[q.id] : null;
      const mark = v === true ? "yes" : v === false ? "no" : "—";
      row.innerHTML = '<span class="role">' + q.role + '</span><span class="stake-text">' + q.text + '</span><span class="mark ' + (v === true ? "yes" : v === false ? "no" : "") + '">' + mark + '</span>';
      stakesWrap.appendChild(row);
    });
    const score = ceoScore();
    const ceoLine = document.createElement("div");
    ceoLine.className = "ceo-score";
    ceoLine.textContent = C.stakeCheck.ceoLabel + " — " + score + " of 4";
    stakesWrap.appendChild(ceoLine);

    const finalCards = document.getElementById("summary-final-cards");
    finalCards.innerHTML = "";
    const f = currentFinal();
    if (f) {
      finalCards.appendChild(card("Environmental", [stateLine(f.environmental)]));
      finalCards.appendChild(card("Financial", [stateLine(f.financial)]));
      finalCards.appendChild(card("Workforce", [stateLine(f.workforce)]));
      finalCards.appendChild(card("Industry ranking", [f.ranking]));
    }

    const refWrap = document.getElementById("summary-reflections");
    refWrap.innerHTML = "";
    const refs = [
      { label: "Round 1 discussion", value: local.reflections.r1_discussion },
      { label: "Round 1 reasoning", value: local.reflections.r1_reasoning },
      { label: "After outcome 1", value: local.reflections.o1 },
      { label: "After the event", value: local.reflections.event },
      { label: "Round 2 discussion", value: local.reflections.r2_discussion },
      { label: "Round 2 reasoning", value: local.reflections.r2_reasoning },
      { label: "After final outcome", value: local.reflections.final },
      { label: C.stakeCheck.reflectionPrompt, value: local.reflections.stakeReflection },
      { label: C.reflection.prompts[0].text, value: local.reflections.hardest },
      { label: C.reflection.prompts[1].text, value: local.reflections.replay },
      { label: C.reflection.prompts[2].text, value: local.reflections.sequencing }
    ];
    refs.forEach(r => {
      const block = document.createElement("div");
      block.className = "ref-block";
      const h = document.createElement("h4"); h.textContent = r.label; block.appendChild(h);
      const p = document.createElement("p"); p.textContent = r.value || "(no response)"; block.appendChild(p);
      refWrap.appendChild(block);
    });
  }

  // -- Compare --------------------------------------------------------

  async function renderCompare() {
    const t = C.comparison;
    document.getElementById("compare-heading").textContent = t.heading;
    document.getElementById("compare-session-value").textContent = sessionId || "—";
    const wrap = document.getElementById("compare-table-wrap");
    wrap.innerHTML = '<p class="status">Loading</p>';
    try {
      const teams = await S.listTeamsInSession(sessionId);
      if (!teams.length) { wrap.innerHTML = '<p class="status">' + t.waitingLabel + '</p>'; return; }
      wrap.innerHTML = "";
      const table = document.createElement("table");
      table.className = "compare-table";
      table.innerHTML = "<thead><tr>" +
        "<th>" + t.columnBrewery + "</th>" +
        "<th>" + t.columnPath + "</th>" +
        "<th>" + t.columnEnv + "</th>" +
        "<th>" + t.columnFin + "</th>" +
        "<th>" + t.columnWork + "</th>" +
        "<th>" + t.columnRank + "</th>" +
        "<th>" + t.columnStakes + "</th>" +
        "</tr></thead><tbody></tbody>";
      const tbody = table.querySelector("tbody");
      teams.forEach(tm => {
        const tr = document.createElement("tr");
        const path = (tm.round1 || "—") + " / " + (tm.event || "—") + " / " + (tm.round2 || "—");
        const f = (tm.round1 && tm.event && tm.round2) ? C.finalOutcomes[tm.round1 + "_" + tm.event + "_" + tm.round2] : null;
        const env = f ? f.environmental.state : "—";
        const fin = f ? f.financial.state : "—";
        const work = f ? f.workforce.state : "—";
        const rank = f ? f.ranking : "—";
        const stakeCount = f ? computedStakeCount(f) : 0;
        tr.innerHTML = "<td>" + escape(tm.brewery) + "</td>" +
          "<td>" + path + "</td>" +
          "<td>" + env + "</td>" +
          "<td>" + fin + "</td>" +
          "<td>" + work + "</td>" +
          "<td>" + rank + "</td>" +
          "<td>" + (f ? stakeCount + " of 4" : "—") + "</td>";
        tbody.appendChild(tr);
      });
      wrap.appendChild(table);
    } catch (e) {
      wrap.innerHTML = '<p class="error">' + escape(e.message || "Could not load") + '</p>';
    }
  }

  function escape(s) { return String(s == null ? "" : s).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c])); }

  // Stake check rules computed from final outcome data
  function computedStakes(f) {
    if (!f) return { cfo: null, worker: null, sustainability: null, brand: null };
    return {
      cfo: f.financial.state !== "crisis",
      worker: f.workforce.state !== "restructured",
      sustainability: f.environmental.state === "hit",
      brand: f.ranking === "top half"
    };
  }
  function computedStakeCount(f) {
    const s = computedStakes(f);
    return Object.values(s).filter(v => v === true).length;
  }

  // -- Helpers --------------------------------------------------------

  function optionEl(group, opt, checked) {
    const wrap = document.createElement("label");
    wrap.className = "option";
    if (checked) wrap.classList.add("selected");
    const input = document.createElement("input");
    input.type = "radio";
    input.name = group + "-option";
    input.value = opt.id;
    input.checked = !!checked;
    input.addEventListener("change", async () => {
      if (group === "r1") { team.round1 = opt.id; await pushTeam("round1-decided"); renderRound1(); }
      if (group === "r2") { team.round2 = opt.id; await pushTeam("round2-decided"); renderRound2(); }
    });
    wrap.appendChild(input);
    const body = document.createElement("div");
    body.className = "option-body";
    const t = document.createElement("strong"); t.textContent = opt.label; body.appendChild(t);
    const d = document.createElement("p"); d.textContent = opt.description; body.appendChild(d);
    const c = document.createElement("p"); c.className = "cost"; c.textContent = opt.cost; body.appendChild(c);
    wrap.appendChild(body);
    return wrap;
  }

  function card(title, lines) {
    const el = document.createElement("article");
    el.className = "card";
    const h = document.createElement("h3"); h.textContent = title; el.appendChild(h);
    lines.forEach(line => { const p = document.createElement("p"); p.textContent = line; el.appendChild(p); });
    return el;
  }

  function envCard(env) {
    const el = document.createElement("article");
    el.className = "card env-card";
    const h = document.createElement("h3"); h.textContent = "Environmental"; el.appendChild(h);
    const targets = (C.targets || { water_pct: 40, packaging_pct: 90 });
    el.appendChild(progressRow("Water reduction", env.water_pct, targets.water_pct, "of 40% target"));
    el.appendChild(progressRow("Packaging recyclable", env.packaging_pct, targets.packaging_pct, "of 90% target"));
    if (env.note) {
      const note = document.createElement("p"); note.className = "card-note"; note.textContent = env.note; el.appendChild(note);
    }
    return el;
  }

  function progressRow(label, value, target, suffix) {
    const wrap = document.createElement("div");
    wrap.className = "progress-row";
    const top = document.createElement("div");
    top.className = "progress-label";
    const lab = document.createElement("span"); lab.textContent = label; top.appendChild(lab);
    const val = document.createElement("span"); val.className = "progress-value";
    val.textContent = value + "% " + suffix;
    top.appendChild(val);
    wrap.appendChild(top);
    const bar = document.createElement("div");
    bar.className = "progress-bar";
    const fill = document.createElement("div");
    fill.className = "progress-fill";
    const pct = Math.max(0, Math.min(100, target ? (value / target) * 100 : 0));
    fill.style.width = pct + "%";
    if (pct >= 100) fill.classList.add("complete");
    else if (pct >= 60) fill.classList.add("partial");
    else fill.classList.add("low");
    bar.appendChild(fill);
    // target marker
    const marker = document.createElement("div");
    marker.className = "progress-marker";
    marker.style.left = "100%";
    bar.appendChild(marker);
    wrap.appendChild(bar);
    return wrap;
  }

  function stateCard(title, state, note) {
    const el = document.createElement("article");
    el.className = "card state-card";
    const h = document.createElement("h3"); h.textContent = title; el.appendChild(h);
    const pill = document.createElement("span");
    pill.className = "state-pill " + stateClass(state);
    pill.textContent = state;
    el.appendChild(pill);
    if (note) {
      const p = document.createElement("p"); p.className = "card-note"; p.textContent = note; el.appendChild(p);
    }
    return el;
  }

  function stateClass(state) {
    const s = String(state || "").toLowerCase();
    if (s === "healthy" || s === "stable" || s === "mostly stable" || s === "top half" || s === "targets met" || s === "hit") return "good";
    if (s === "strained" || s === "disrupted" || s === "partial") return "warn";
    if (s === "crisis" || s === "restructured" || s === "missed" || s === "bottom half") return "bad";
    return "neutral";
  }

  function stateLine(obj) {
    if (!obj) return "";
    if (typeof obj === "string") return obj;
    return obj.state + (obj.note ? ". " + obj.note : "");
  }

  function bindReflection(field) {
    const ta = document.querySelector('textarea[data-field="' + field + '"]');
    if (!ta) return;
    ta.value = local.reflections[field] || "";
    ta.oninput = () => { local.reflections[field] = ta.value; saveLocal(); };
  }

  function updateContinue(screen, selector, predicate) {
    const btn = document.querySelector('[data-screen="' + screen + '"] ' + selector);
    if (!btn) return;
    btn.disabled = !predicate();
  }

  function currentFinal() {
    if (!getRound1() || !getEvent() || !getRound2()) return null;
    const key = getRound1() + "_" + getEvent() + "_" + getRound2();
    return C.finalOutcomes[key];
  }

  function pathLabel(id) {
    if (!id) return "—";
    const r1map = { X: "Replace the systems", Y: "Run efficiency programs", Z: "Pilot one product line" };
    if (r1map[id]) return id + " (" + r1map[id] + ")";
    const key = getRound1() + "_" + getEvent();
    const set = C.round2[key];
    if (!set) return id;
    const opt = set.options.find(o => o.id === id);
    return opt ? id + " (" + opt.label + ")" : id;
  }

  function eventLabel(id) {
    if (!id) return "—";
    return id + " (" + C.events[id].title + ")";
  }

  function stakeRow(q) {
    const row = document.createElement("div");
    row.className = "stake-row";
    const role = document.createElement("span"); role.className = "role"; role.textContent = q.role; row.appendChild(role);
    const text = document.createElement("span"); text.className = "stake-text"; text.textContent = q.text; row.appendChild(text);
    const buttons = document.createElement("span");
    buttons.className = "stake-buttons";
    ["yes", "no"].forEach(val => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "toggle";
      b.textContent = val;
      const isOn = (val === "yes" && team.stakes[q.id] === true) || (val === "no" && team.stakes[q.id] === false);
      if (isOn) b.classList.add("on");
      b.addEventListener("click", async () => {
        team.stakes[q.id] = (val === "yes");
        team.ceoScore = ceoScore();
        await pushTeam("stake-toggled");
        renderStakes();
      });
      buttons.appendChild(b);
    });
    row.appendChild(buttons);
    return row;
  }

  function ceoScore() {
    return Object.values((team && team.stakes) || {}).filter(v => v === true).length;
  }

  function updateCeoScore() {
    document.getElementById("ceo-score").textContent = C.stakeCheck.ceoLabel + ", " + ceoScore() + " of 4";
  }

  // -- Remote sync ----------------------------------------------------

  async function pushTeam(reason) {
    if (!teamId || !team) return;
    team.screen = local.screen;
    team.reflections = Object.assign({}, local.reflections);
    team.finalOutcomeKey = (getRound1() && getEvent() && getRound2()) ? getRound1() + "_" + getEvent() + "_" + getRound2() : null;
    saveLocal();
    try { await S.writeTeam(teamId, team); } catch (e) { console.warn("sync failed", reason, e); }
  }

  async function pushTeamReflections() {
    if (!teamId || !team) return;
    team.reflections = Object.assign({}, local.reflections);
    try { await S.writeTeam(teamId, team); } catch (e) {}
  }

  // -- JSON export ----------------------------------------------------

  function downloadJson(filename, obj) {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function exportTeam() {
    if (!team) return;
    const out = Object.assign({}, team, { reflections: local.reflections });
    downloadJson("brewery-team-" + safe(brewery) + ".json", out);
  }

  async function exportSession() {
    if (!sessionId) return;
    try {
      const teams = await S.listTeamsInSession(sessionId);
      downloadJson("brewery-session-" + sessionId + ".json", { sessionId, exported_at: new Date().toISOString(), teams });
    } catch (e) {
      alert("Could not load session: " + e.message);
    }
  }

  function safe(s) { return String(s).replace(/[^a-z0-9_-]/gi, "-").slice(0, 40) || "team"; }

  async function openReportWindow() {
    if (!sessionId) { alert("No session loaded."); return; }
    const w = window.open("", "_blank");
    if (!w) { alert("Pop-up blocked. Allow pop-ups for this site, then try again."); return; }
    w.document.write('<!doctype html><html><head><meta charset="utf-8"><title>Loading session report...</title></head><body><p style="font-family:sans-serif;padding:2rem">Loading session report, please wait...</p></body></html>');
    w.document.close();
    let teams;
    try {
      teams = await S.listTeamsInSession(sessionId);
    } catch (e) {
      w.document.body.innerHTML = '<p style="font-family:sans-serif;padding:2rem;color:#a33">Could not load session: ' + escape(e.message || e) + '</p>';
      return;
    }
    const html = buildReportHtml(teams, sessionId);
    w.document.open();
    w.document.write(html);
    w.document.close();
    setTimeout(() => { try { w.focus(); w.print(); } catch (e) {} }, 400);
  }

  function buildReportHtml(teams, sid) {
    const rows = teams.map(tm => buildTeamReportSection(tm)).join("");
    return '<!doctype html><html><head><meta charset="utf-8"><title>Brewery 2032 — session ' + escape(sid) + '</title>' +
      '<style>' + reportCss() + '</style></head><body>' +
      '<header><h1>Brewery 2032 session report</h1><p class="meta">Session ' + escape(sid) + ' · generated ' + escape(new Date().toLocaleString()) + ' · ' + teams.length + ' team' + (teams.length === 1 ? '' : 's') + '</p></header>' +
      rows +
      '</body></html>';
  }

  function buildTeamReportSection(tm) {
    const f = (tm.round1 && tm.event && tm.round2) ? C.finalOutcomes[tm.round1 + "_" + tm.event + "_" + tm.round2] : null;
    const stakes = computedStakes(f);
    const path = pathLabelStr("round1", tm.round1) + "  →  " + (tm.event ? tm.event + " (" + (C.events[tm.event]?.title || "") + ")" : "—") + "  →  " + pathLabelStr("round2", tm.round2, tm);
    const ref = tm.reflections || {};
    const refRows = [
      ["Round 1 group discussion", ref.r1_discussion],
      ["Round 1 reasoning", ref.r1_reasoning],
      ["After outcome 1", ref.o1],
      ["After the event", ref.event],
      ["Round 2 group discussion", ref.r2_discussion],
      ["Round 2 reasoning", ref.r2_reasoning],
      ["After final outcome", ref.final],
      ["Stake reflection", ref.stakeReflection],
      ["Hardest stake to protect", ref.hardest],
      ["Replay round 1", ref.replay],
      ["Where the team sequenced approaches", ref.sequencing]
    ].filter(r => r[1] && r[1].trim());

    let outcomeHtml = "";
    if (f) {
      outcomeHtml = '<div class="grid">' +
        outcomeBox("Environmental", envFinalState(f.environmental.state), f.environmental.note) +
        outcomeBox("Financial", f.financial.state, f.financial.note) +
        outcomeBox("Workforce", f.workforce.state, f.workforce.note) +
        outcomeBox("Industry ranking", f.ranking, "") +
        '</div>';
    }
    const stakeCount = Object.values(stakes).filter(v => v === true).length;
    const stakeListItems = C.stakeCheck.questions.map(q => {
      const v = stakes[q.id];
      const yn = v === true ? "yes" : v === false ? "no" : "—";
      return '<li class="stake-' + yn + '"><span>' + escape(q.text) + '</span><strong>' + yn + '</strong></li>';
    }).join("");

    return '<section class="team">' +
      '<h2>' + escape(tm.brewery || "Untitled brewery") + '</h2>' +
      '<p class="path">' + escape(path) + '</p>' +
      outcomeHtml +
      '<h3>Stake check</h3>' +
      '<ul class="stakes">' + stakeListItems + '</ul>' +
      '<p class="ceo">CEO score: ' + stakeCount + ' of 4</p>' +
      (refRows.length ? '<h3>Reflections</h3>' + refRows.map(r => '<div class="ref"><h4>' + escape(r[0]) + '</h4><p>' + escape(r[1]) + '</p></div>').join("") : "") +
      '</section>';
  }

  function pathLabelStr(round, id, tm) {
    if (!id) return "—";
    if (round === "round1") {
      const map = { X: "Replace the systems", Y: "Run efficiency programs", Z: "Pilot one product line" };
      return id + " (" + (map[id] || "") + ")";
    }
    if (round === "round2" && tm) {
      const key = tm.round1 + "_" + tm.event;
      const set = C.round2[key];
      if (!set) return id;
      const opt = set.options.find(o => o.id === id);
      return opt ? id + " (" + opt.label + ")" : id;
    }
    return id;
  }

  function outcomeBox(title, state, note) {
    const cls = stateClass(state);
    return '<div class="box"><h4>' + escape(title) + '</h4><span class="pill ' + cls + '">' + escape(state) + '</span>' + (note ? '<p>' + escape(note) + '</p>' : '') + '</div>';
  }

  function reportCss() {
    return [
      'body { font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color: #1a1a1a; max-width: 760px; margin: 1.5rem auto; padding: 0 1rem; line-height: 1.5; }',
      'header { border-bottom: 2px solid #333; padding-bottom: 0.75rem; margin-bottom: 1.25rem; }',
      'header h1 { margin: 0 0 0.25rem; font-size: 1.6rem; }',
      'header .meta { color: #666; font-size: 0.9rem; margin: 0; }',
      'section.team { page-break-before: always; padding-top: 1rem; margin-top: 1rem; }',
      'section.team:first-of-type { page-break-before: auto; padding-top: 0; margin-top: 0; }',
      'section.team h2 { font-size: 1.3rem; margin: 0 0 0.4rem; }',
      'section.team h3 { font-size: 1rem; margin: 1.25rem 0 0.5rem; color: #444; text-transform: uppercase; letter-spacing: 0.04em; }',
      'section.team h4 { font-size: 0.85rem; margin: 0 0 0.25rem; color: #555; text-transform: lowercase; }',
      'p.path { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.92rem; background: #f4f4f4; padding: 0.5rem 0.75rem; border-radius: 4px; }',
      '.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin-bottom: 0.5rem; }',
      '.box { border: 1px solid #d0d0d0; border-radius: 4px; padding: 0.65rem 0.8rem; }',
      '.box p { margin: 0.4rem 0 0; font-size: 0.88rem; color: #333; }',
      '.pill { display: inline-block; padding: 0.18rem 0.6rem; border-radius: 999px; font-size: 0.78rem; border: 1px solid #d0d0d0; background: #f5f5f5; color: #444; }',
      '.pill.good { background: #e6f3ee; color: #2a6b58; border-color: #b2d8c8; }',
      '.pill.warn { background: #faf3e0; color: #6b5a30; border-color: #e3d2a3; }',
      '.pill.bad { background: #fce8e8; color: #8a3a3a; border-color: #e3b8b8; }',
      'ul.stakes { list-style: none; padding: 0; margin: 0; }',
      'ul.stakes li { display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid #eee; font-size: 0.92rem; }',
      'ul.stakes li strong { font-weight: 600; }',
      'ul.stakes li.stake-yes strong { color: #2a6b58; }',
      'ul.stakes li.stake-no strong { color: #8a3a3a; }',
      'p.ceo { font-weight: 600; margin: 0.75rem 0 0; padding: 0.5rem 0.75rem; background: #f4f4f4; border-radius: 4px; }',
      '.ref { margin-bottom: 0.65rem; }',
      '.ref p { margin: 0; font-size: 0.92rem; white-space: pre-wrap; }',
      '@media print { body { margin: 0; max-width: none; } .ref { page-break-inside: avoid; } .box { page-break-inside: avoid; } }'
    ].join("\n");
  }

  // -- Wiring ---------------------------------------------------------

  document.addEventListener("click", async function (ev) {
    const t = ev.target.closest("[data-action]");
    if (!t) return;
    const a = t.dataset.action;

    if (a === "new-session") {
      const errEl = document.getElementById("setup-error");
      const stEl = document.getElementById("setup-status");
      errEl.hidden = true; stEl.hidden = false; stEl.textContent = "Creating session";
      try {
        const id = await S.createSession();
        sessionId = id; saveLocal();
        stEl.hidden = true;
        show("session-created");
      } catch (e) {
        stEl.hidden = true; errEl.hidden = false; errEl.textContent = e.message || "Could not create session";
      }
    }

    if (a === "back-to-setup") show("setup");

    if (a === "copy-code") {
      try { await navigator.clipboard.writeText(sessionId); t.textContent = "Copied"; setTimeout(() => t.textContent = "Copy code", 1500); } catch (e) {}
    }

    if (a === "join") {
      const errEl = document.getElementById("setup-error");
      const stEl = document.getElementById("setup-status");
      errEl.hidden = true;
      const breweryVal = document.getElementById("brewery-input").value.trim();
      const codeVal = document.getElementById("session-input").value.trim();
      if (!breweryVal) { errEl.hidden = false; errEl.textContent = "Brewery name required"; return; }
      if (!codeVal) { errEl.hidden = false; errEl.textContent = "Session code required"; return; }
      brewery = breweryVal; sessionId = codeVal;
      stEl.hidden = false; stEl.textContent = C.session.joiningLabel;
      try {
        const tid = await S.joinTeam(sessionId, brewery);
        teamId = tid;
        team = await S.readTeam(teamId);
        saveLocal();
        stEl.hidden = true;
        show("qr");
      } catch (e) {
        stEl.hidden = true; errEl.hidden = false; errEl.textContent = e.message || C.session.errorJoinFailed;
      }
    }

    if (a === "next-from-qr") show("welcome");
    if (a === "start") show("round1");
    if (a === "next-from-r1" && getRound1()) show("outcome1");
    if (a === "next-from-o1") show("event");
    if (a === "next-from-event") show("round2");
    if (a === "next-from-r2" && getRound2()) show("final");
    if (a === "next-from-final") show("stakes");
    if (a === "next-from-stakes") {
      team.submitted = true;
      await pushTeam("submitted");
      show("reflection");
    }
    if (a === "next-from-reflection") { await pushTeamReflections(); show("summary"); }
    if (a === "open-report") openReportWindow();
    if (a === "export-json") exportTeam();
    if (a === "export-all") exportSession();
    if (a === "goto-compare") show("compare");
    if (a === "refresh-compare") renderCompare();
    if (a === "back-to-summary") show("summary");
    if (a === "reset") reset();
  });

  // -- Boot -----------------------------------------------------------

  (async function boot() {
    const params = urlParams();
    if (params.get("view") === "compare") {
      const code = params.get("session") || sessionId;
      if (code) { sessionId = code; saveLocal(); }
      show("compare");
      return;
    }

    if (sessionId && teamId && team) {
      // Resume — refresh team from remote in background
      try { team = await S.readTeam(teamId); saveLocal(); } catch (e) {}
      show(local.screen || "welcome");
      return;
    }

    show("setup");
  })();

})();
