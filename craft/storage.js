// Shared storage layer.
// Talks to a tiny JSON blob service (default: keeper-blob-server in this folder).
// The base URL is configured in content.js as content.storage.base.
// One blob per session (the index of teams) and one blob per team (the team's full state).
// Read-modify-write on the session index is best-effort. Concurrent joins by multiple teams
// in the same second can race; in classroom use this is rare. The team blob is written only
// by the group laptop, so it has a single writer.

(function () {
  "use strict";

  function getBase() {
    if (window.content && window.content.storage && window.content.storage.base) return window.content.storage.base;
    return "http://localhost:8088/api/blob";
  }

  function extractIdFromLocation(loc) {
    if (!loc) return null;
    const parts = loc.split("/");
    return parts[parts.length - 1];
  }

  async function createBlob(value) {
    const res = await fetch(getBase(), {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(value)
    });
    if (!res.ok) throw new Error("create blob failed: " + res.status);
    // Prefer body.id (our keeper service returns it), fall back to Location header (jsonblob shape)
    try {
      const body = await res.clone().json();
      if (body && body.id) return body.id;
    } catch (e) {}
    const loc = res.headers.get("Location") || res.headers.get("location") || "";
    const id = extractIdFromLocation(loc);
    if (!id) throw new Error("blob id not returned");
    return id;
  }

  async function readBlob(id) {
    const res = await fetch(getBase() + "/" + id, {
      method: "GET",
      headers: { "Accept": "application/json" },
      cache: "no-store"
    });
    if (!res.ok) throw new Error("read blob failed: " + res.status);
    return res.json();
  }

  async function writeBlob(id, value) {
    const res = await fetch(getBase() + "/" + id, {
      method: "PUT",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(value)
    });
    if (!res.ok) throw new Error("write blob failed: " + res.status);
    return res.json();
  }

  // -- Session API -----------------------------------------------------

  async function createSession() {
    const sessionId = await createBlob({ created_at: new Date().toISOString(), teams: {} });
    return sessionId;
  }

  async function joinTeam(sessionId, brewery) {
    const session = await readBlob(sessionId);
    if (session.teams && session.teams[brewery]) {
      return session.teams[brewery];
    }
    const teamState = freshTeamState(sessionId, brewery);
    const teamId = await createBlob(teamState);
    session.teams = session.teams || {};
    session.teams[brewery] = teamId;
    await writeBlob(sessionId, session);
    return teamId;
  }

  async function findTeamId(sessionId, brewery) {
    const session = await readBlob(sessionId);
    return (session.teams && session.teams[brewery]) || null;
  }

  async function listTeamsInSession(sessionId) {
    const session = await readBlob(sessionId);
    const entries = Object.entries(session.teams || {});
    const out = [];
    for (const [brewery, teamId] of entries) {
      try {
        const team = await readBlob(teamId);
        out.push(team);
      } catch (e) {
        out.push({ brewery, error: true });
      }
    }
    return out;
  }

  function freshTeamState(sessionId, brewery) {
    return {
      sessionId,
      brewery,
      screen: "round1",
      round1: null,
      event: null,
      round2: null,
      submitted: false,
      stakes: { cfo: null, worker: null, sustainability: null, brand: null },
      ceoScore: null,
      finalOutcomeKey: null,
      updated_at: new Date().toISOString()
    };
  }

  // -- Team API --------------------------------------------------------

  async function readTeam(teamId) {
    return readBlob(teamId);
  }

  async function writeTeam(teamId, state) {
    state.updated_at = new Date().toISOString();
    return writeBlob(teamId, state);
  }

  window.brewerystorage = {
    createSession,
    joinTeam,
    findTeamId,
    listTeamsInSession,
    readTeam,
    writeTeam,
    freshTeamState
  };

})();
