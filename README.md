# VFI simulation

Open **Open Teacher.cmd** on the teaching laptop. The default local address is `http://127.0.0.1:8766/?screen=teacher` while the simulation server is running. Use an available port if another project occupies 8766; do not stop that project.

1. Start a named session for each class. Choose company count, six to eight roles, decision years and one estimated discussion duration for all decisions, plus the first-checkpoint and finish targets. Years 1, 3, 5, 7, 9 and 10 are core decisions.
2. Show the joining QR and password. Each company joins on one shared laptop, chooses an invented name and an EU headquarters, then uses its company QR to connect private student phones.
3. Each active student reads their confidential intelligence and submits one private recommendation before the company decides. Recommendations cannot be edited. A student may then activate their executive power once across the decade. Written reflections occur only in Years 1, 5 and 10; Year 10 has two written answers.
4. Use the Year 5 controls to bring companies together, reveal the industry checkpoint after submissions are complete, then begin Year 6. **Begin final checkpoint** gives mandatory decisions a final submission window and resolves remaining years chronologically. **Release final industry results** becomes available once every active student has submitted the closing reflection. Use **Show debrief** for the supplied discussion prompts.
5. Download each session's PDF and JSON logs. Students can download their own PDF, HTML or text report. Voluntary anonymous feedback is separate and never required for report access. Final release locks company decisions and outcomes.

The discussion estimate does not expire decisions: teams may finish faster or slower. Only facilitator-closed submission windows apply the specified defaults and affordability fallbacks. Missing recommendations remain marked not submitted; no retrospective choice is invented. Disconnected participants can be marked inactive so their missing responses do not block checkpoints. No overall ethics score is produced. Mission conditions without defined measurable thresholds are marked unevaluable.

Use the same Wi-Fi for laptop and phones when running the existing network-enabled classroom launcher. This implementation work used a separate fictional-data loopback preview and did not change network access or publish to Keeper.

## Local development

Run `npm install`, `npm run build`, then `python server.py --port 8766`. The server defaults to loopback. Python dependencies are in `requirements.txt`; data persists in `fairpass.sqlite3`. Keep the private teacher key out of published files. The existing classroom launch shortcut manages its own host setting.

React and Material UI 7 retain the established interface theme. New versioned sessions use `engine_v4.py`, the year-rule modules, `powers_v4.py`, `service_v4.py`, `closure_v4.py`, `v4_scenarios.json` and `v4-ui.jsx`. Exact supplied specifications and approved clarifications are in `specifications/`. Existing legacy sessions retain `content.json`, `outcomes.py` and their established story catalogue.

Run `python -m unittest test_v4 test_vfi_midpoint test_vfi_6_8 test_vfi_closure` for the new engine and `python -m unittest test_server test_outcomes test_narrative` for legacy compatibility. Reports are printable but currently untagged PDFs; HTML and text alternatives are available. Scoped browser checks do not establish full accessibility conformance. All agent preview and media checks must remain silent.

## Legacy session interface and media

The following describes the retained interface for previously saved legacy sessions.

### Company introduction and decision flow

The lecturer's association promo establishes the industry issues and commitments. Students join a company, open its separate introduction, then start the current year. The Company screen explains the festival origin, current business and public commitments; it remains available throughout play. The decision timer starts through the existing start action after the introduction.

Each annual briefing shows the situation and readable Offer, Team and Details information. Cash-after-option comparisons appear only alongside actual decision options. There is no full-company-brief button. On-screen Back controls, browser Back and the brand link return to earlier information. Moving between views preserves the unsubmitted option selection; saved decisions and outcomes remain in Record. Phones use the same information with native card paging and normal text size. AI-generated images are not used.


### Branching case media

The ten-year case is presented through authored fictional correspondence, support records, test logs, agreement extracts, event reports and closing accounts. story.json is the editable catalogue of documents and audio transcripts. narrative.py chooses documents from the saved choices and existing replayed state; outcomes.py and decision-model.json remain the mechanics. Media stays inside the existing company and phone reading views. Audio is optional, never autoplays, and always has a written transcript. No generated images or external media services are used.

The public/media/story MP3 files use the installed Microsoft David and Zira desktop voices as synthetic narration. To regenerate changed bodies locally, run render_story_audio.ps1 through the 32-bit Windows PowerShell host with ffmpeg available. The optional -Only parameter accepts comma-separated document IDs. A body edit needs its matching audio regenerated; callbacks, follow-ups and current figures are displayed separately from the recorded message. Audio files belong to public/media/story and are copied into dist during the normal build. Private role facts are generated only for the authenticated role and are not placed in public audio files.


## Student welcome

The first student page presents the existing introduction in three Material UI cards: Your company, The opportunity and Your challenge. It uses three columns on desktop and one column below 64rem; the original wording and company setup action are preserved. On compact desktops the reading areas remain independently scrollable; on narrow screens the page scrolls normally. Verified at 1280 × 720 and 390px width, with no horizontal overflow and a working setup handoff. The local build passed. This revision has not been published to GitHub or deployed by the agent.
