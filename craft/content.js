// All editable copy lives in this file.
// Edit text here, not in app.js, between cohorts.
//
// Schema:
//   welcome          , opening screen
//   round1           , opening decision
//   outcomes1        , three round-1 outcome blocks, keyed by option id
//   events           , three industry events, keyed E1, E2, E3
//   round2           , nine option sets, keyed `${round1}_${event}`
//   finalOutcomes    , twenty-seven outcomes, keyed `${round1}_${event}_${round2}`
//   stakeCheck       , four yes/no stake questions
//   reflection       , three closing prompts

window.content = {

  welcome: {
    title: "A brewery faces a 2032 deadline",
    body: [
      "Your group runs a mid-sized craft brewery in the Nordic Craft Brewers Association. Six breweries are tracked publicly against a joint pledge: by 2032, cut water use 40 percent per liter brewed and reach 90 percent recyclable or reusable packaging.",
      "Each of you has a role card with a stake to protect. Keep your card private. The CEO leads the discussion. The group makes one decision per round on this screen.",
      "You will play three rounds covering nine years. Industry events between rounds change what is on the table. At the end, you will check which stakes were protected."
    ],
    startLabel: "Begin",
    resetLabel: "Start over"
  },

  round1: {
    heading: "Round 1, Year 1 to 4",
    situation: "The pledge is public. The board wants a credible path. The first four years set the trajectory for the rest of the decade. Old equipment is mid-life. Cash reserves cover one major capital cycle.",
    question: "Which opening move does your brewery make?",
    options: [
      {
        id: "X",
        label: "Replace the systems",
        description: "Replace the bottling and water systems with closed-loop infrastructure. Hits the targets fast. Three years of heavy spending and a workforce restructuring.",
        cost: "Heavy spending. Major disruption to operations. Strong environmental signal."
      },
      {
        id: "Y",
        label: "Run efficiency programs",
        description: "Train staff, optimize existing equipment, reduce waste at the margins across the brewery. Low risk. No disruption. The math gets you about halfway.",
        cost: "Low spending. Stable workforce. Limited progress on the targets."
      },
      {
        id: "Z",
        label: "Pilot one product line",
        description: "Pilot a closed-loop system on one product line while running efficiency programs across the rest. Moderate cost and moderate progress. Two operating models to manage at once.",
        cost: "Moderate spending. Moderate disruption. Two operating models running side by side."
      }
    ],
    discussionPrompt: "Briefly note what your group discussed before deciding.",
    reasoningPrompt: "Why did you choose this option?"
  },

  outcomes1: {
    X: {
      label: "Year 4: results from replacing the systems",
      environmental: { water_pct: 30, packaging_pct: 50, note: "Strong early gains. The new systems are running and the trajectory is well ahead of where the slow path would be." },
      financial: { state: "strained", note: "Capital reserves drawn down. Debt service is rising. The next round will be tight." },
      workforce: { state: "restructured", note: "Layoffs in the legacy bottling line. New roles created in closed-loop operations, but not everyone made the move." }
    },
    Y: {
      label: "Year 4: results from efficiency programs",
      environmental: { water_pct: 12, packaging_pct: 20, note: "Some progress on both fronts, but well short of the 2032 trajectory. The math does not get the brewery to the targets." },
      financial: { state: "healthy", note: "No major outlays. Margins are intact. The cash position is strong going into round two." },
      workforce: { state: "stable", note: "Roles unchanged. Training delivered across teams. Morale is good." }
    },
    Z: {
      label: "Year 4: results from the pilot",
      environmental: { water_pct: 20, packaging_pct: 35, note: "Moderate gains. The pilot is working but only on one product line. Scaling is the open question." },
      financial: { state: "strained", note: "Running two operating models at once is expensive. Margins are tight." },
      workforce: { state: "mostly stable", note: "Retraining on the pilot line. No layoffs. Two ways of working in the same brewery." }
    },
    reflectionPrompt: "Looking at these outcomes, what do you wish you had weighted differently?"
  },

  // Targets used for progress bars
  targets: {
    water_pct: 40,
    packaging_pct: 90
  },

  events: {
    E1: {
      title: "Regulatory acceleration",
      description: "The EU tightens the water deadline from 2032 to 2030. Two fewer years to hit the target. The packaging deadline is unchanged."
    },
    E2: {
      title: "Industry-wide pilot failure",
      description: "Closed-loop water systems prove unreliable across the industry. Insurance costs spike. Stable replacement technology is two to three years away."
    },
    E3: {
      title: "First public ranking",
      description: "The association publishes its first annual progress report. Top performers and laggards are named. Press picks up the story. Customers and investors are watching."
    },
    reflectionPrompt: "Briefly note how the team's plan needs to change after this event."
  },

  round2: {

    // X (transformational start) ---------------------------------------

    "X_E1": {
      heading: "Round 2, Year 8 to 9",
      situation: "Your closed-loop systems are running. The earlier deadline puts pressure on phase two of the rollout. Cash is tight after Round 1.",
      options: [
        { id: "X2", label: "Double down on the rollout", description: "Take on debt to fund phase two of the closed-loop rollout. The 2030 target is reachable. Financial exposure rises sharply.", cost: "High debt. Reliable target hit. High financial risk." },
        { id: "Y2", label: "Pause and consolidate", description: "Stop new spending and prove what you already have. Miss the new earlier target. Financial state recovers as outflows ease.", cost: "Spending freeze. Target missed. Margins recover." },
        { id: "Z2", label: "Selective acceleration", description: "Continue the rollout in the highest-impact areas only. Hit the target on time at moderate cost. Some teams continue under restructuring strain.", cost: "Moderate spending. Target on time. Workforce strain continues." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    },

    "X_E2": {
      heading: "Round 2, Year 8 to 9",
      situation: "Your closed-loop water system is now classified as high-risk. Insurance has tripled. Replacement components will not be ready for two years.",
      options: [
        { id: "X2", label: "Push through with redundancy", description: "Invest in backup systems and absorb insurance. The water target stays in reach. Financial reserves are exhausted.", cost: "Severe financial strain. Target reachable. Continued workforce churn." },
        { id: "Y2", label: "Mothball the new system", description: "Pause the closed-loop and fall back on efficiency. Margins recover. The water target slips out of reach.", cost: "System idle. Water target missed. Financial recovery." },
        { id: "Z2", label: "Adapt the pieces that work", description: "Keep the reliable subsystems running, swap the unreliable ones, accelerate packaging where the technology is mature. Mixed gains.", cost: "Moderate spend. Partial water progress. Strong packaging progress." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    },

    "X_E3": {
      heading: "Round 2, Year 8 to 9",
      situation: "Your early environmental numbers put you near the top of the first public ranking. Press and investors are calling. Workforce morale is uneven after the restructuring.",
      options: [
        { id: "X2", label: "Press the lead", description: "Publicize the rollout, court press and investors, accelerate the next phase on the strength of attention. The lead grows. Workforce gets little new attention.", cost: "Marketing and spending. Strong ranking. Continued workforce strain." },
        { id: "Y2", label: "Quiet operations", description: "Keep the head down, stabilize finances, let the numbers speak for themselves. Visibility fades. Margins improve.", cost: "Low spend. Lower ranking. Financial recovery." },
        { id: "Z2", label: "Reinvest in the workforce", description: "Use the lead to fund retraining, profit-sharing, and stable contracts in the new operations. Visible reinvestment narrative. Costs absorb the surplus.", cost: "Workforce spend. Strong ranking. Stabilized teams." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    },

    // Y (incremental start) --------------------------------------------

    "Y_E1": {
      heading: "Round 2, Year 8 to 9",
      situation: "Efficiency programs got you about halfway. The earlier water deadline is two years out. The brewery has cash but no infrastructure to hit the target.",
      options: [
        { id: "X2", label: "Emergency transformation", description: "Crash program to install closed-loop infrastructure. Compresses three years of work into two. Cost and execution risk are high.", cost: "Heavy spending. Possible target hit. High failure risk." },
        { id: "Y2", label: "Stay the course", description: "Continue efficiency programs. Accept missing the water target. Public reputation takes the hit. Operations stay calm.", cost: "Low spend. Target missed. Stable workforce." },
        { id: "Z2", label: "Pivot to packaging", description: "Concentrate spend on packaging where mature technology exists. Hit the packaging target. Accept missing the water target.", cost: "Moderate spending. Packaging hit. Water missed." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    },

    "Y_E2": {
      heading: "Round 2, Year 8 to 9",
      situation: "Closed-loop water technology is unreliable industry-wide. You did not adopt it. Efficiency progress continues but the targets remain out of reach.",
      options: [
        { id: "X2", label: "Wait for the technology, then move", description: "Hold position now and adopt closed-loop once components stabilize. Late investment. Targets likely missed by 2032.", cost: "Modest spend. Targets likely missed. Late workforce disruption." },
        { id: "Y2", label: "Stay the course", description: "Continue efficiency programs. Accept missing the targets. Avoid the volatility hitting the rest of the industry.", cost: "Low spend. Targets missed. Stable workforce." },
        { id: "Z2", label: "Accelerate packaging only", description: "Move fast on packaging where the technology is mature. Use the moment to lead on one of the two targets. Water target slips.", cost: "Targeted spending. Packaging hit. Water missed." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    },

    "Y_E3": {
      heading: "Round 2, Year 8 to 9",
      situation: "The first public ranking placed your brewery in the bottom half. Customers are paying attention. Cash reserves are intact.",
      options: [
        { id: "X2", label: "Bet the company", description: "Launch a full transformation visible to the industry. High capital outlay against the late timeline. Strong signal to the market.", cost: "Heavy spending. Targets reachable. Workforce restructured." },
        { id: "Y2", label: "Stay the course", description: "Continue efficiency programs. Accept the low ranking. Protect margins and workforce stability.", cost: "Low spend. Targets missed. Reputation absorbed." },
        { id: "Z2", label: "Launch a visible pilot", description: "Build one closed-loop project as proof of seriousness. Modest investment with public progress to show. Targets stay tight.", cost: "Moderate spending. Partial progress. Public narrative shifts." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    },

    // Z (middle path start) --------------------------------------------

    "Z_E1": {
      heading: "Round 2, Year 8 to 9",
      situation: "The pilot worked and efficiency programs delivered. The earlier water deadline puts pressure on the rest of the brewery. Margins are tight from running both tracks.",
      options: [
        { id: "X2", label: "Scale the pilot", description: "Roll closed-loop infrastructure across the remaining lines. The water target is reachable on the new timeline. Financial exposure deepens.", cost: "Heavy spending. Target hit. Workforce disruption." },
        { id: "Y2", label: "Drop the pilot", description: "Cut the pilot, focus on efficiency, recover margins. The water target moves out of reach. Operations simplify.", cost: "Spending stops. Water missed. Financial recovery." },
        { id: "Z2", label: "Run both tracks faster", description: "Keep the dual model and push speed on both. Moderate progress on both targets. Sustained operational strain.", cost: "Continued moderate spending. Partial target hit. Continued strain." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    },

    "Z_E2": {
      heading: "Round 2, Year 8 to 9",
      situation: "Your pilot used the closed-loop technology now classified as high-risk. Insurance is up. The pilot is on the edge of being uneconomic.",
      options: [
        { id: "X2", label: "Replace the pilot", description: "Tear out the existing pilot and rebuild once new components are available. Years of work resets. Targets slip.", cost: "Heavy spend on rebuild. Targets missed. Workforce shifts again." },
        { id: "Y2", label: "Pull the pilot, double efficiency", description: "Shut down the pilot, redirect resources to efficiency programs across all lines. Margins recover. Targets stay out of reach.", cost: "Pilot shut. Targets missed. Financial recovery." },
        { id: "Z2", label: "Iterate the pilot", description: "Troubleshoot the existing pilot, swap unreliable components, hold the dual-track approach. Progress is slow but the model survives.", cost: "Moderate spend. Partial progress. Workforce stable." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    },

    "Z_E3": {
      heading: "Round 2, Year 8 to 9",
      situation: "The first public ranking placed your brewery in the middle. The pilot is a story the press finds interesting. Cash is tight from running two tracks.",
      options: [
        { id: "X2", label: "Showcase and scale", description: "Use the press attention to scale the pilot across the brewery. The capital cost is high. Workforce changes accelerate.", cost: "Heavy spending. Target hit. Workforce disruption." },
        { id: "Y2", label: "Wind the pilot down", description: "Close the pilot, return to efficiency programs, recover margins. The story fades. Targets miss.", cost: "Pilot closed. Targets missed. Financial recovery." },
        { id: "Z2", label: "Document and continue", description: "Publish progress reports openly, continue the dual track at current speed. Modest narrative gain. Operational strain continues.", cost: "Continued moderate spend. Partial progress. Public credibility." }
      ],
      discussionPrompt: "Briefly note what your group discussed before deciding.",
      reasoningPrompt: "Why did you choose this option?"
    }

  },

  // Twenty-seven final outcome cells.
  // Stake check rules:
  //   CFO           , financial !== 'crisis'
  //   Worker        , workforce !== 'restructured'
  //   Sustainability, environmental === 'hit'
  //   Brand         , ranking === 'top half'
  //   CEO           , three or more of the above
  finalOutcomes: {

    // X (transformational start) - regulatory acceleration
    "X_E1_X2": { environmental: { state: "hit", note: "Both targets met under the 2030 deadline." }, financial: { state: "crisis", note: "Debt service exceeds operating margin." }, workforce: { state: "restructured", note: "Second wave of layoffs in legacy roles." }, ranking: "top half" },
    "X_E1_Y2": { environmental: { state: "missed", note: "Water progress stalled at the Round 1 level." }, financial: { state: "healthy", note: "Outflows dropped, margins rebuilt." }, workforce: { state: "disrupted", note: "Restructured teams settled, new hires paused." }, ranking: "bottom half" },
    "X_E1_Z2": { environmental: { state: "hit", note: "Water and packaging targets met on the new timeline." }, financial: { state: "strained", note: "Spending kept moderate, debt manageable." }, workforce: { state: "disrupted", note: "Restructured teams stabilized through retraining." }, ranking: "top half" },

    // X (transformational start) - pilot failure
    "X_E2_X2": { environmental: { state: "partial", note: "Backup systems delivered most of the water target." }, financial: { state: "crisis", note: "Insurance and redundancy drained reserves." }, workforce: { state: "restructured", note: "Continued churn under operational stress." }, ranking: "top half" },
    "X_E2_Y2": { environmental: { state: "partial", note: "Mothballed system held packaging gains, water rolled back." }, financial: { state: "strained", note: "Idle assets weigh on the balance sheet." }, workforce: { state: "disrupted", note: "Roles in closed-loop operations sidelined." }, ranking: "bottom half" },
    "X_E2_Z2": { environmental: { state: "partial", note: "Packaging target hit, water short of the goal." }, financial: { state: "strained", note: "Selective spend kept reserves intact." }, workforce: { state: "disrupted", note: "Teams reorganized around what works." }, ranking: "top half" },

    // X (transformational start) - public ranking
    "X_E3_X2": { environmental: { state: "hit", note: "Both targets met ahead of 2032." }, financial: { state: "strained", note: "Marketing and phase-two spending absorbed surplus." }, workforce: { state: "restructured", note: "Workforce reshape continued without new investment." }, ranking: "top half" },
    "X_E3_Y2": { environmental: { state: "partial", note: "Round 1 gains held, no further progress." }, financial: { state: "healthy", note: "Outflows minimized, margins recovered." }, workforce: { state: "stable", note: "No further changes to roles." }, ranking: "bottom half" },
    "X_E3_Z2": { environmental: { state: "hit", note: "Both targets met on schedule." }, financial: { state: "strained", note: "Surplus reinvested in workforce stabilization." }, workforce: { state: "stable", note: "Retraining and profit-sharing settled the new operations." }, ranking: "top half" },

    // Y (incremental start) - regulatory acceleration
    "Y_E1_X2": { environmental: { state: "partial", note: "Crash program delivered packaging, water short." }, financial: { state: "crisis", note: "Compressed timeline drove cost overruns." }, workforce: { state: "restructured", note: "Layoffs in legacy bottling under time pressure." }, ranking: "bottom half" },
    "Y_E1_Y2": { environmental: { state: "missed", note: "Both targets missed on the original and new timelines." }, financial: { state: "healthy", note: "Margins protected throughout." }, workforce: { state: "stable", note: "No changes to roles." }, ranking: "bottom half" },
    "Y_E1_Z2": { environmental: { state: "partial", note: "Packaging target hit, water target missed." }, financial: { state: "healthy", note: "Targeted spend stayed within reserves." }, workforce: { state: "stable", note: "Roles unchanged across the brewery." }, ranking: "bottom half" },

    // Y (incremental start) - pilot failure
    "Y_E2_X2": { environmental: { state: "partial", note: "Late closed-loop investment recovered some water progress." }, financial: { state: "strained", note: "Late spending with limited time to amortize." }, workforce: { state: "disrupted", note: "Late restructuring across legacy bottling." }, ranking: "bottom half" },
    "Y_E2_Y2": { environmental: { state: "missed", note: "Both targets missed at the 2032 mark." }, financial: { state: "healthy", note: "Avoided industry-wide volatility." }, workforce: { state: "stable", note: "No changes to roles." }, ranking: "bottom half" },
    "Y_E2_Z2": { environmental: { state: "partial", note: "Packaging target hit, water target missed." }, financial: { state: "healthy", note: "Targeted spend on mature technology." }, workforce: { state: "stable", note: "Roles unchanged." }, ranking: "top half" },

    // Y (incremental start) - public ranking
    "Y_E3_X2": { environmental: { state: "hit", note: "Late transformation delivered both targets." }, financial: { state: "crisis", note: "Heavy late spending overruns." }, workforce: { state: "restructured", note: "Compressed restructuring across the brewery." }, ranking: "top half" },
    "Y_E3_Y2": { environmental: { state: "missed", note: "Both targets missed at the 2032 mark." }, financial: { state: "healthy", note: "Margins protected throughout." }, workforce: { state: "stable", note: "Roles unchanged." }, ranking: "bottom half" },
    "Y_E3_Z2": { environmental: { state: "partial", note: "Pilot hit packaging, water target missed." }, financial: { state: "strained", note: "Pilot spending absorbed reserves." }, workforce: { state: "stable", note: "Retraining around the pilot, no layoffs." }, ranking: "top half" },

    // Z (middle path start) - regulatory acceleration
    "Z_E1_X2": { environmental: { state: "hit", note: "Scaled rollout met both targets on the new timeline." }, financial: { state: "strained", note: "Scaling absorbed reserves, debt manageable." }, workforce: { state: "disrupted", note: "Restructuring across legacy lines, retraining for the rest." }, ranking: "top half" },
    "Z_E1_Y2": { environmental: { state: "missed", note: "Water target slipped out of reach after the pilot was cut." }, financial: { state: "healthy", note: "Costs dropped sharply." }, workforce: { state: "stable", note: "Pilot teams reabsorbed into existing operations." }, ranking: "bottom half" },
    "Z_E1_Z2": { environmental: { state: "partial", note: "Packaging target hit, water target close but short." }, financial: { state: "strained", note: "Sustained dual-track spend." }, workforce: { state: "disrupted", note: "Continued retraining across both tracks." }, ranking: "top half" },

    // Z (middle path start) - pilot failure
    "Z_E2_X2": { environmental: { state: "partial", note: "Rebuild delayed water progress past 2032." }, financial: { state: "crisis", note: "Two rounds of heavy spending on the same system." }, workforce: { state: "disrupted", note: "Pilot teams reassigned twice." }, ranking: "bottom half" },
    "Z_E2_Y2": { environmental: { state: "partial", note: "Packaging gains held, water target missed." }, financial: { state: "healthy", note: "Resources redirected to efficiency." }, workforce: { state: "stable", note: "Pilot teams absorbed back into operations." }, ranking: "bottom half" },
    "Z_E2_Z2": { environmental: { state: "partial", note: "Iteration held packaging target, water target close but short." }, financial: { state: "strained", note: "Component swaps and continued spend." }, workforce: { state: "stable", note: "Pilot teams continued with new components." }, ranking: "top half" },

    // Z (middle path start) - public ranking
    "Z_E3_X2": { environmental: { state: "hit", note: "Scaled pilot met both targets." }, financial: { state: "strained", note: "Scaling absorbed reserves." }, workforce: { state: "disrupted", note: "Restructuring across legacy lines." }, ranking: "top half" },
    "Z_E3_Y2": { environmental: { state: "missed", note: "Pilot closure left targets out of reach." }, financial: { state: "healthy", note: "Costs dropped sharply." }, workforce: { state: "stable", note: "Pilot teams reabsorbed." }, ranking: "bottom half" },
    "Z_E3_Z2": { environmental: { state: "partial", note: "Packaging hit, water close but short." }, financial: { state: "strained", note: "Sustained dual-track spend." }, workforce: { state: "stable", note: "No layoffs, retraining continues." }, ranking: "top half" }

  },

  finalSnapshot: {
    heading: "Final outcome, Year 9, 2032",
    reflectionPrompt: "Was your overall approach more incremental, more transformational, or a sequence of both? Briefly explain."
  },

  stakeCheck: {
    heading: "Stake check",
    intro: "Here is which stakes the brewery ended up protecting, based on the final outcome.",
    questions: [
      { id: "cfo",            text: "CFO: avoid financial crisis",                                      role: "CFO" },
      { id: "worker",         text: "Worker representative: no involuntary layoffs",                    role: "Worker representative" },
      { id: "sustainability", text: "Head of sustainability: both 2032 targets hit",                    role: "Head of sustainability" },
      { id: "brand",          text: "Head of operations: top half of the industry ranking",             role: "Head of operations" }
    ],
    ceoLabel: "CEO overall, at least three of four stakes met",
    reflectionPrompt: "Which stake landed where you did not expect, and why? Briefly explain."
  },

  reflection: {
    heading: "Reflection",
    prompts: [
      { id: "hardest",   text: "Which stake at your table was hardest to protect, and why?" },
      { id: "replay",    text: "If you could replay Round 1 knowing what you know now, what would you choose? What does that tell you about the difference between incremental and transformational change?" },
      { id: "sequencing", text: "Where in your final path did you sequence approaches, incremental then transformational or the reverse? If you did not, what kept you on one path?" }
    ]
  },

  summary: {
    heading: "Group summary for the debrief",
    pathLabel: "Path through the tree",
    stakesLabel: "Stakes met",
    reflectionsLabel: "Group reflections",
    printLabel: "Print this page",
    submitLabel: "Submit run to the classroom session",
    submittedLabel: "Submitted",
    compareLabel: "See all teams"
  },

  // Storage configuration. Points at the keeper-blob-server container (see ./keeper-blob-server/).
  // For local development, run the Python server: `python keeper-blob-server/blob.py` and use http://localhost:8088/api/blob.
  storage: {
    base: "/api/blob",
    pollSeconds: 6
  },

  session: {
    setupHeading: "Set up your team",
    setupIntro: "One person types a brewery name. The team plays as that brewery. The classroom session lets the instructor compare all teams at the end.",
    breweryLabel: "Brewery name (invent one)",
    breweryHint: "Used only to label your team. No personal names.",
    codeLabel: "Classroom session code",
    codeHint: "Your instructor will share this on the board. If you are the instructor, create one below.",
    newSessionLabel: "Create a new classroom session",
    newSessionHint: "Instructor only. Generates a session code to share with the class.",
    joinLabel: "Continue",
    sessionCreatedLabel: "Classroom session code",
    sessionCreatedHint: "Write this on the board. All teams use the same code.",
    joiningLabel: "Joining session",
    qrHeading: "Officers, scan this on your phones",
    qrIntro: "Each officer scans, picks the role from their printed card, and follows along. Keep this QR visible until everyone has scanned.",
    qrFallbackLabel: "Or open this URL on your phone",
    qrSessionLabel: "Session",
    qrBreweryLabel: "Brewery",
    qrContinueLabel: "Continue to the scenario",
    errorJoinFailed: "Could not connect to the classroom session. Check the code and try again.",
    errorNetwork: "Network error. Check the connection and try again."
  },

  // Per-officer content. Lives on the officer phone, not the group laptop.
  officers: {

    pickerHeading: "Pick your role",
    pickerHint: "This page is private. Read it on your own device.",
    sessionPromptHeading: "Join the classroom session",
    sessionCodeLabel: "Session code (from the board)",
    breweryNameLabel: "Brewery name (from your team)",
    joinLabel: "Join",
    syncStatusWaiting: "Waiting for the team to start",
    syncStatusOnRound: "Team is on",
    syncStatusOffline: "No connection. Reload to retry.",
    privacyReminder: "Keep this card to yourself. Do not show your screen to anyone. Make your case by arguing the values you care about, not by reading the prompts out loud.",

    roles: [

      {
        id: "ceo",
        title: "CEO",
        tagline: "Leads the discussion. Makes the final call each round.",
        mission: "You lead the conversation and you make the final call each round. You do not have a preferred path. Your job is to land the company somewhere that protects as many of the team's commitments as possible at the end of round three. You win if at least three of the four stakes are met. Listen carefully, every other role at the table is fighting for one specific outcome.",
        reminders: [
          "Hear each colleague out before you decide. You are the only one who can weigh all four sides.",
          "The boldest move is not always the right one. The cautious move is not always safe either.",
          "Three of four stakes is your win. Do not lose a colleague trying to chase a perfect score."
        ],
        rounds: {
          round1: { heading: "Opening move", prompts: [
            "Ask each colleague what they would pick and why.",
            "Notice who stays quiet at the table. A quiet stake is one you might forget."
          ]},
          outcome1: { heading: "After year 4", prompts: [
            "Read the three result cards together. Which area of the business just took damage?",
            "Use round two to recover what is hurting, not to push the same bet harder."
          ]},
          event: { heading: "Industry event", prompts: [
            "Ask each role how the event hits their stake. Some get harder, some get easier.",
            "The event is the same for every team. What separates teams is how they respond."
          ]},
          round2: { heading: "Response", prompts: [
            "This is the moment to combine approaches. Match the move to the gap you still need to close.",
            "If the table is split, name the stake at the heart of the disagreement out loud."
          ]}
        }
      },

      {
        id: "cfo",
        title: "CFO",
        tagline: "Protects the company's finances.",
        mission: "You are responsible for keeping the company alive financially. The brewery can be under pressure and tight on cash, that is fine. The brewery cannot end the period in financial crisis. Your stake is met if the company avoids financial crisis at the end of round three. The targets matter, but only if there is still a company to run.",
        reminders: [
          "Push back on plans that spend a lot of money quickly without a way to recover the cash.",
          "\"Strained\" is survivable. \"Crisis\" is not. That is the line you defend.",
          "If the cash is gone after round one, your voice is the most important one in round two."
        ],
        rounds: {
          round1: { heading: "Opening move", prompts: [
            "Replacing the systems means heavy spending for years. Running efficiency programs holds the cash. Piloting one line splits the bill.",
            "Ask how the brewery pays the next bill if the table goes for the biggest option."
          ]},
          outcome1: { heading: "After year 4", prompts: [
            "Look at the financial card together. Is the company under strain, or in real trouble?",
            "If under strain, push for a recovery move in round two before reaching for more spending."
          ]},
          event: { heading: "Industry event", prompts: [
            "Each event hits the company's money differently. Name the cost out loud before the table picks a response.",
            "If reserves are running low, you should be the loudest voice in the room right now."
          ]},
          round2: { heading: "Response", prompts: [
            "Refuse any plan that piles on more debt if there is no way to pay it back.",
            "Pausing or taking a smaller, focused step usually protects your stake."
          ]}
        }
      },

      {
        id: "ops",
        title: "Head of operations",
        tagline: "Speaks for the brewery floor and the equipment.",
        mission: "You see the brewery from the floor up. The bottling line and water systems are getting old and they are getting expensive to keep running. You want shared accountability across the team and a plan that is realistic for the people doing the work every day. Your stake is met if the company finishes in the top half of the public industry ranking, that is how outsiders read whether you are serious about change.",
        reminders: [
          "Old equipment fails at the worst possible time. Replacing it is not optional, only a question of when.",
          "Do not let small adjustments dress themselves up as real change. Push back when the table is fooling itself.",
          "Your stake is the public ranking. The brewery has to look serious from the outside, not just inside the room."
        ],
        rounds: {
          round1: { heading: "Opening move", prompts: [
            "Replacing the systems is operational renewal. Efficiency programs leave the equipment problem for later. The pilot buys time on one line.",
            "Ask the table what the brewery looks like in 2030 if nothing structural changes now."
          ]},
          outcome1: { heading: "After year 4", prompts: [
            "Did the brewery actually change, or did the team mostly train people on the same equipment?",
            "If nothing structural moved, raise it early in round two. The window is closing."
          ]},
          event: { heading: "Industry event", prompts: [
            "Each event tests how the operation is set up. What has to change for the brewery to keep running?",
            "If the event exposes weakness, name what needs fixing before the table closes round two."
          ]},
          round2: { heading: "Response", prompts: [
            "Defend the choices that genuinely improve the brewery. Push back on cosmetic moves.",
            "If the equipment is already past its life, refuse the keep-going option."
          ]}
        }
      },

      {
        id: "sustainability",
        title: "Head of sustainability",
        tagline: "Holds the public pledge to hit the 2032 targets.",
        mission: "You are the one holding the pledge the company made publicly. Your stake is met only if the company hits both 2032 targets on the numbers, water down forty percent per liter brewed, and ninety percent recyclable or reusable packaging. Almost is not enough. If the company makes a public commitment and then misses it, that is your stake gone.",
        reminders: [
          "Only plans that hit both targets count. Almost-there does not count.",
          "If the math does not get the brewery to forty and ninety, say it out loud at the table.",
          "Argue for the option that closes the gap, even when it costs more or pushes the workforce."
        ],
        rounds: {
          round1: { heading: "Opening move", prompts: [
            "Replacing the systems hits both targets reliably. Efficiency programs do not get the brewery there. The pilot is a bet on whether you can scale it later.",
            "Ask the table to read the actual percentages on each option, not just the framing."
          ]},
          outcome1: { heading: "After year 4", prompts: [
            "Read the water and packaging percentages on the card. Is the trajectory enough to land both targets?",
            "If you are behind, raise the alarm now. Round two is where the gap has to close."
          ]},
          event: { heading: "Industry event", prompts: [
            "Each event changes what hitting the targets actually costs. Recompute the picture out loud.",
            "Some events reward speed. Some reward adaptability. Name which one this is."
          ]},
          round2: { heading: "Response", prompts: [
            "Push for the option that protects both targets, even at financial or workforce cost.",
            "If the table picks a half-measure, get it on the record which target is being given up."
          ]}
        }
      },

      {
        id: "worker",
        title: "Worker representative",
        tagline: "Speaks for the people who work at the brewery.",
        mission: "You speak for the people who work at the brewery. Your stake is met if no one loses their job because of these decisions. Retraining people for new work is fine. Gradual change is fine. Major disruption is acceptable, as long as nobody is laid off. Cuts are not.",
        reminders: [
          "Refuse plans that route through layoffs. Push for retraining and reassignment instead.",
          "A workforce that is shaken up but intact can recover. A workforce that has been cut cannot.",
          "Slow and steady or middle-path moves usually protect your stake. Big sudden changes usually cost jobs."
        ],
        rounds: {
          round1: { heading: "Opening move", prompts: [
            "Replacing the systems comes with cuts in the older parts of the brewery. Efficiency programs keep everyone in their job. The pilot retrains people without firing anyone.",
            "Ask the table whether the layoffs in the replacement option are actually necessary, or just assumed."
          ]},
          outcome1: { heading: "After year 4", prompts: [
            "If people lost their jobs in round one, push hard against any further cuts in round two.",
            "If the workforce held together, defend that ground. Do not let it be traded away now."
          ]},
          event: { heading: "Industry event", prompts: [
            "Cuts have long tails. Each event can either pile on more pressure or take it off.",
            "If the event creates pressure to lay people off, name the alternative before the table votes."
          ]},
          round2: { heading: "Response", prompts: [
            "Refuse any plan whose ending leaves the workforce restructured.",
            "Push for retraining and focused approaches that protect the people already there."
          ]}
        }
      }

    ]
  },

  comparison: {
    heading: "All teams in this session",
    waitingLabel: "No teams have submitted yet",
    columnBrewery: "Brewery",
    columnPath: "Path",
    columnEnv: "Environmental",
    columnFin: "Financial",
    columnWork: "Workforce",
    columnRank: "Ranking",
    columnStakes: "Stakes met",
    refreshLabel: "Refresh"
  }

};
