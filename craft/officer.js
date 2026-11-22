// Officer phone view. Polls the team blob for live sync.

(function () {
  "use strict";

  const C = window.content;
  const S = window.brewerystorage;
  const LOCAL_KEY = "brewery-2032-officer";

  const FLOW = ["welcome", "round1", "outcome1", "event", "round2", "final", "stakes", "reflection", "summary"];
  function indexOf(s) { return FLOW.indexOf(s); }

  // Officer-side step order. Each step maps to the team screen at which it unlocks.
  const STEPS = [
    { id: "mission",  unlockAt: 0 },                 // always unlocked
    { id: "round1",   unlockAt: indexOf("round1") },
    { id: "outcome1", unlockAt: indexOf("outcome1") },
    { id: "event",    unlockAt: indexOf("event") },
    { id: "round2",   unlockAt: indexOf("round2") },
    { id: "end",      unlockAt: indexOf("final") }
  ];

  let local = loadLocal() || freshLocal();
  let teamId = null;
  let team = null;
  let pollHandle = null;

  function freshLocal() { return { sessionId: "", brewery: "", roleId: "", stepIdx: 0, missionCollapsed: false }; }
  function loadLocal() { try { const r = localStorage.getItem(LOCAL_KEY); return r ? JSON.parse(r) : null; } catch (e) { return null; } }
  function saveLocal() { try { localStorage.setItem(LOCAL_KEY, JSON.stringify(local)); } catch (e) {} }

  // -- URL params ----------------------------------------------------

  function paramsFromUrl() {
    const p = new URLSearchParams(window.location.search);
    return { session: p.get("session"), brewery: p.get("brewery"), role: p.get("role") };
  }

  // -- Routing -------------------------------------------------------

  function show(screen) {
    document.querySelectorAll(".screen").forEach(el => el.classList.toggle("active", el.dataset.screen === screen));
    window.scrollTo(0, 0);
    if (screen === "join") renderJoin();
    if (screen === "picker") renderPicker();
    if (screen === "mission") renderMission();
  }

  // -- Join ----------------------------------------------------------

  function renderJoin() {
    const t = C.officers;
    document.getElementById("join-heading").textContent = t.sessionPromptHeading;
    document.getElementById("join-hint").textContent = t.pickerHint;
    document.getElementById("join-code-label").textContent = t.sessionCodeLabel;
    document.getElementById("join-brewery-label").textContent = t.breweryNameLabel;
    document.querySelector('[data-action="join"]').textContent = t.joinLabel;
    document.getElementById("join-code").value = local.sessionId || "";
    document.getElementById("join-brewery").value = local.brewery || "";
  }

  async function doJoin(sessionId, brewery) {
    const errEl = document.getElementById("join-error");
    errEl.hidden = true;
    if (!sessionId || !brewery) { errEl.hidden = false; errEl.textContent = "Session code and brewery name required."; return; }
    try {
      const tid = await S.findTeamId(sessionId, brewery);
      if (!tid) { errEl.hidden = false; errEl.textContent = "That brewery has not joined this session yet. Wait for the group laptop to start."; return; }
      teamId = tid;
      local.sessionId = sessionId; local.brewery = brewery;
      saveLocal();
      team = await S.readTeam(teamId);
      if (local.roleId) show("mission"); else show("picker");
      startPolling();
    } catch (e) {
      errEl.hidden = false; errEl.textContent = e.message || "Could not join.";
    }
  }

  // -- Role picker ---------------------------------------------------

  function renderPicker() {
    const t = C.officers;
    document.getElementById("picker-heading").textContent = t.pickerHeading;
    document.getElementById("picker-hint").textContent = t.pickerHint;
    document.getElementById("picker-brewery").textContent = local.brewery;
    const grid = document.getElementById("role-grid");
    grid.innerHTML = "";
    t.roles.forEach(role => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "role-btn";
      const title = document.createElement("strong"); title.textContent = role.title; btn.appendChild(title);
      if (role.tagline) {
        const sub = document.createElement("span"); sub.className = "role-tagline"; sub.textContent = role.tagline; btn.appendChild(sub);
      }
      btn.addEventListener("click", () => {
        local.roleId = role.id;
        local.stepIdx = 0;
        local.missionCollapsed = false;
        saveLocal();
        show("mission");
      });
      grid.appendChild(btn);
    });
  }

  // -- Mission + steps -----------------------------------------------

  function currentRole() { return C.officers.roles.find(r => r.id === local.roleId); }

  function teamScreenIdx() {
    if (!team || !team.screen) return -1;
    return FLOW.indexOf(team.screen);
  }

  function stepIdxForTeamScreen() {
    const idx = teamScreenIdx();
    // Map team's current screen to the matching officer step.
    // welcome → mission, round1 → round1 prompts, outcome1 → outcome1 prompts,
    // event → event prompts, round2 → round2 prompts, anything past → end.
    if (idx <= 0) return 0;
    if (idx === 1) return 1; // round1
    if (idx === 2) return 2; // outcome1
    if (idx === 3) return 3; // event
    if (idx === 4) return 4; // round2
    return 5;                // final/stakes/reflection/summary → end
  }

  function renderMission() {
    const role = currentRole();
    if (!role) return show("picker");
    const t = C.officers;

    // Auto-track team's current screen so officer prompts always match what's on the laptop.
    local.stepIdx = stepIdxForTeamScreen();

    document.getElementById("mission-role-tag").textContent = role.title;
    document.getElementById("mission-brewery").textContent = local.brewery;

    const card = document.getElementById("mission-card");
    card.innerHTML = "";
    const priv = document.createElement("p");
    priv.className = "privacy-top";
    priv.textContent = t.privacyReminder;
    card.appendChild(priv);

    // Collapsible header
    const header = document.createElement("button");
    header.type = "button";
    header.className = "mission-toggle";
    header.setAttribute("aria-expanded", local.missionCollapsed ? "false" : "true");
    const headerLabel = document.createElement("span");
    headerLabel.textContent = "Your mission as " + role.title;
    const chevron = document.createElement("span");
    chevron.className = "chevron";
    chevron.textContent = local.missionCollapsed ? "+" : "–";
    header.appendChild(headerLabel);
    header.appendChild(chevron);
    header.addEventListener("click", () => {
      local.missionCollapsed = !local.missionCollapsed;
      saveLocal();
      renderMission();
    });
    card.appendChild(header);

    if (!local.missionCollapsed) {
      const inner = document.createElement("div");
      inner.className = "mission-body";
      const p = document.createElement("p"); p.textContent = role.mission; inner.appendChild(p);
      const remH = document.createElement("h3"); remH.textContent = "Reminders"; inner.appendChild(remH);
      const ul = document.createElement("ul");
      role.reminders.forEach(r => { const li = document.createElement("li"); li.textContent = r; ul.appendChild(li); });
      inner.appendChild(ul);
      card.appendChild(inner);
    }

    const block = document.getElementById("step-block");
    block.innerHTML = "";
    const step = STEPS[local.stepIdx];

    if (step.id === "mission") {
      const note = document.createElement("p");
      note.className = "step-intro";
      note.textContent = "Read your mission and reminders. Tap next when your group is ready to start round 1.";
      block.appendChild(note);
    } else if (step.id === "end") {
      const screen = team && team.screen;
      const note = document.createElement("p");
      note.className = "step-intro";
      let msg;
      if (screen === "final") {
        msg = "The team is reading the final results. Look at the cards. Did your stake land where you hoped?";
      } else if (screen === "stakes") {
        msg = "The team is checking which stakes were protected. Your row will be marked yes or no on the laptop.";
      } else if (screen === "reflection") {
        msg = "The team is writing reflections. Share what you noticed during the rounds.";
      } else if (screen === "summary") {
        msg = "The exercise is complete. Stay in your role for the debrief.";
      } else {
        msg = "The team has reached the final results.";
      }
      note.textContent = msg;
      block.appendChild(note);
    } else {
      const stepData = role.rounds[step.id];
      if (stepData) {
        const h3 = document.createElement("h3"); h3.textContent = stepData.heading; block.appendChild(h3);
        const ul2 = document.createElement("ul");
        stepData.prompts.forEach(p => { const li = document.createElement("li"); li.textContent = p; ul2.appendChild(li); });
        block.appendChild(ul2);
      }
    }

    // Live sync hints from team state
    const liveBlock = document.createElement("div");
    liveBlock.className = "live-context";
    if (team) {
      if (step.id === "round1" && team.round1) liveBlock.textContent = "Group has chosen: " + optionLabel("round1", team.round1);
      else if (step.id === "outcome1" && team.round1) liveBlock.textContent = "Round 1 chosen: " + optionLabel("round1", team.round1);
      else if (step.id === "event" && team.event) liveBlock.textContent = "Event drawn: " + (C.events[team.event] ? C.events[team.event].title : team.event);
      else if (step.id === "round2" && team.round2) liveBlock.textContent = "Group has chosen: " + optionLabel("round2", team.round2);
      else if (step.id === "end" && team.submitted) liveBlock.textContent = "Stakes submitted by the group.";
    }
    if (liveBlock.textContent) block.appendChild(liveBlock);

    // Sync indicator
    const syncEl = document.getElementById("sync-tag");
    const tIdx = teamScreenIdx();
    if (tIdx < 0) syncEl.textContent = C.officers.syncStatusWaiting;
    else syncEl.textContent = C.officers.syncStatusOnRound + " " + (team.screen || "—");

    const status = document.getElementById("step-status");
    if (teamScreenIdx() < 0) {
      status.hidden = false;
      status.textContent = "Waiting for the group laptop to start round 1.";
    } else {
      status.hidden = true;
    }
  }

  function optionLabel(round, optId) {
    if (round === "round1") {
      const opt = C.round1.options.find(o => o.id === optId);
      return opt ? opt.label : optId;
    }
    if (round === "round2" && team) {
      const key = team.round1 + "_" + team.event;
      const set = C.round2[key];
      if (!set) return optId;
      const opt = set.options.find(o => o.id === optId);
      return opt ? opt.label : optId;
    }
    return optId;
  }

  // -- Polling -------------------------------------------------------

  function startPolling() {
    stopPolling();
    const ms = (C.storage && C.storage.pollSeconds ? C.storage.pollSeconds : 6) * 1000;
    pollHandle = setInterval(async () => {
      if (!teamId) return;
      try {
        team = await S.readTeam(teamId);
        if (document.querySelector('[data-screen="mission"].active')) renderMission();
      } catch (e) { /* ignore */ }
    }, ms);
  }
  function stopPolling() { if (pollHandle) { clearInterval(pollHandle); pollHandle = null; } }

  // -- Wiring --------------------------------------------------------

  document.addEventListener("click", async function (ev) {
    const t = ev.target.closest("[data-action]");
    if (!t) return;
    const a = t.dataset.action;

    if (a === "join") {
      const code = document.getElementById("join-code").value.trim();
      const brewery = document.getElementById("join-brewery").value.trim();
      await doJoin(code, brewery);
    }

    if (a === "next-step") {
      const maxIdx = maxUnlockedStepIdx();
      if (local.stepIdx < maxIdx) { local.stepIdx++; saveLocal(); renderMission(); }
    }
    if (a === "prev-step") {
      if (local.stepIdx > 0) { local.stepIdx--; saveLocal(); renderMission(); }
    }
    if (a === "change-role") {
      local.roleId = "";
      saveLocal();
      show("picker");
    }
  });

  // -- Boot ----------------------------------------------------------

  (async function boot() {
    const p = paramsFromUrl();

    // If URL points to a different session or brewery than local state, treat it as a new game
    // and reset role + step progress. Prevents stale stepIdx from earlier testing carrying over.
    if ((p.session && p.session !== local.sessionId) || (p.brewery && p.brewery !== local.brewery)) {
      local = freshLocal();
    }

    if (p.session) local.sessionId = p.session;
    if (p.brewery) local.brewery = p.brewery;  // URLSearchParams.get already decodes
    if (p.role && C.officers.roles.find(r => r.id === p.role)) local.roleId = p.role;
    saveLocal();

    // Always render the join screen first so something is visible even if remote calls fail.
    show("join");
    if (local.sessionId && local.brewery) {
      await doJoin(local.sessionId, local.brewery);
    }
  })();

})();
