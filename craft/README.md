# Brewery 2032 — in-class simulation

Static web app for a 30 to 40 minute classroom exercise on incremental versus transformational change. Students work in groups of five running a craft brewery against a 2032 industry sustainability pledge. Each group has a shared laptop and five officer phones.

## Architecture

- Static HTML, CSS, and vanilla JavaScript. No build step. No framework.
- Hosted on GitHub Pages.
- Live sync between the group laptop and the five officer phones uses [jsonblob.com](https://jsonblob.com), a free anonymous public JSON store. No account, no API key, no software install.
- Anonymous data only: brewery name (invented by the group), session code, role title, decisions, reflections. Nothing identifying a person.
- After class, the group laptop and instructor can download the team and session data as JSON for archival in the repo.

This is the intermediate setup. The plan is to migrate live sync to Keeper once that infrastructure is ready. See "Future migration" below.

## How to run locally

```
cd teaching/courses/change-management/brewery-simulation
python -m http.server 8000
```

Open `http://localhost:8000`. The same URL works on phones connected to the same wifi if you replace `localhost` with the laptop's IP.

You can also open `index.html` directly in a browser, but jsonblob calls require an active network connection regardless.

## How to deploy to GitHub Pages

1. In the repo settings, enable Pages on the branch where this folder lives.
2. The site is served at `https://<user>.github.io/<repo>/academic/teaching/change-management/brewery-simulation/`.
3. Officer URL is the same path with `officer.html`.
4. Comparison view is `index.html?view=compare&session=<code>`.

## Files

- `index.html` — group laptop. Setup, QR, decisions, outcomes, stake check, reflection, summary, comparison view.
- `officer.html` — officer phone. Role picker, mission card, per-step prompts, sync indicator.
- `app.js` — group laptop logic.
- `officer.js` — officer phone logic.
- `storage.js` — jsonblob client used by both pages.
- `content.js` — all editable copy. Edit this between cohorts, not the other files.
- `styles.css` — visual styles.

## Editing content

All scenario text, option descriptions, outcome states, event descriptions, role missions, and reflection prompts live in `content.js`. The structure is documented at the top of the file.

Things you will change between cohorts:
- Brewery scenario in `welcome.body`
- Round 1 options in `round1.options` and corresponding outcomes in `outcomes1`
- Industry events in `events`
- Round 2 option sets in `round2` (nine sets keyed `round1_event`)
- Final outcomes in `finalOutcomes` (twenty seven cells keyed `round1_event_round2`)
- Stake check questions in `stakeCheck.questions`
- Officer mission cards and per-step prompts in `officers.roles[i]`

Things to leave alone unless you change the structure:
- Storage configuration in `storage.base`
- Screen IDs in HTML

## Adding or modifying events

To add a fourth event:
1. Add `E4` to `events` in `content.js`.
2. Add three Round 2 sets keyed `X_E4`, `Y_E4`, `Z_E4` to `round2`.
3. Add nine final outcomes keyed `X_E4_X2` through `Z_E4_Z2` to `finalOutcomes`.
4. Update the random draw key list in `app.js` (`renderEvent`) to include `E4`.

## How a class session runs

1. Instructor opens `index.html` on a laptop, clicks "create new session," writes the resulting session code on the board.
2. Each group laptop opens `index.html`, types a brewery name and the session code, clicks continue.
3. The group laptop displays a QR code. Each officer scans it with their phone, picks the role from their printed card, and follows the per-step prompts.
4. The group plays through Round 1, the industry event, Round 2, the final outcome, and the stake check on the laptop. Officer phones advance step-by-step alongside.
5. At the end, each laptop hits "submit" (automatic on the stake check screen). The instructor opens the comparison view to see all teams.
6. Optional: instructor downloads the session JSON and commits it under `data/sessions/<date>/` for archival.

## Anonymity

The data sent to jsonblob is limited to: brewery name (invented), session code, decisions (X/Y/Z), event drawn (E1/E2/E3), stake yes/no answers, and reflection text. No names, no emails, no IP addresses, no device identifiers.

Officer cards remain physical and are not sent anywhere. Roles on phones are local to each phone.

## Future migration

When Keeper is ready to host this, the only file that needs to change is `storage.js`. The interface (createSession, joinTeam, readTeam, writeTeam, listTeamsInSession) stays the same; only the URL base and request format need updating.

## Constraints currently accepted

- Data transits jsonblob during the live class. Anyone with the session code could read or overwrite the team blobs. Acceptable because the data is anonymous and the blobs only need to live for 30 to 40 minutes.
- jsonblob has no SLA. If it is down, fall back to the printed role cards, run the exercise on the laptop alone, and skip cross-team comparison.
- No optimistic locking on the session index. If two teams join in the same second, one may overwrite the other. With teams trickling in over a minute or two, this is rare in practice. Workaround: instructor confirms all teams appear in the comparison view; if one is missing, that team rejoins.
