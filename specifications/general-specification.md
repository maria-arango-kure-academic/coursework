# FAIRPASS: GENERAL SIMULATION SPECIFICATION
## Implementation instructions for Codex

### 1. Project objective

FairPass is an interactive business ethics simulation for approximately 45 university students per session, divided into 6–7 competing companies of 6–8 students.

Students manage established European ticketing companies over ten simulated years, beginning in 2027.

The central technology is Verified Fan Identity (VFI), which limits ticket purchases to five tickets per verified individual, per event.

Over the decade, companies face commercial opportunities, technological developments, economic shocks, labour issues, stakeholder conflicts, and questions about responsibility.

The simulation must support different trajectories. Companies can succeed or struggle through different strategies. There is no predetermined moral outcome and no overall ethics score.

Company performance does not determine students' academic grades. The simulation generates evidence for an individual ethics reflection assignment.

**Implementation priority:** Preserve existing functional code and infrastructure. Adapt the existing implementation to this specification. Do not rebuild working components unnecessarily or invent additional scenarios.

---

### 2. Classroom setup

Each session contains approximately 45 students, organized into 6–7 companies.

Each company has:

- One shared company screen, displayed on a laptop or other device.
- Individual student phones, accessed through a QR code.
- Six mandatory executive roles and two optional roles.
- Identical starting resources and market conditions.
- A company name and an EU headquarters country selected by students.

The headquarters country is decorative. It has no effect on laws, taxes, costs, events, or simulation outcomes.

Company names and national flags appear on the company screen and the whole-class industry dashboard.

The facilitator has a separate control interface.

### 3. Classroom opening sequence

**Step 1: Advertisement**

The instructor plays a 60-second promotional video introducing Verified Fan Identity.

The video is external to the simulation interface.

**Step 2: Introductory slide**

Display this text:

> 2027. You're the executive leadership team of a European ticketing company.
>
> Your board has just watched this advertisement.
>
> Your competitors are already evaluating the technology.
>
> What will you do?

**Step 3: Students enter the simulation**

Students scan a QR code and join their company.

Display the following briefing in the simulation interface.

### 4. Student-facing introductory briefing

# Welcome to the European Live Entertainment Market

#### Your company

It is 2027. You are part of the executive leadership team of an established European ticketing company.

Your company provides ticketing services for concerts, festivals, and other live events. You have an established customer base, experienced employees, and a functioning technology platform.

Business is stable, but competition is intense. Promoters and venues expect reliable services, customers want affordable and convenient access to events, and shareholders expect continued growth.

Your company is also a member of the European Live Entertainment Association, whose members have publicly committed to fair access, responsible technology, environmental sustainability, fair working conditions, and long-term economic viability.

#### The opportunity

Ticket scalping is a growing concern. Popular events sell out within minutes, while tickets reappear on resale platforms at inflated prices.

A new technology, **Verified Fan Identity (VFI)**, promises to change this. By verifying individual customers and limiting purchases to five tickets per person, per event, VFI aims to reduce automated purchasing and give genuine fans a fairer chance.

Early trials are promising, and major promoters are considering adoption. The technology could also support new services, including ticket transfers, loyalty programmes, and more convenient venue entry.

However, implementation requires investment, technical development, and operational changes. The market is still evolving, and competitors are pursuing different strategies.

#### Your challenge

Over the next ten years, your leadership team will make decisions that shape your company's future.

You will face commercial opportunities, technological developments, unexpected events, and competing stakeholder expectations. Your decisions will have immediate and long-term consequences.

Each executive has a distinct role, responsibilities, and access to information that other team members may not have.

**Your objective is to lead your company through the next decade, balancing its commercial ambitions with its responsibilities to employees, customers, business partners, and society.**

---

### 5. Company setup

After reading the briefing, each company selects:

1. Company name: free text.
2. Headquarters: dropdown containing the 27 EU member states.

Display the corresponding national flag.

The company name and headquarters are locked after confirmation.

All companies begin with identical conditions:

- Annual revenue: €24 million.
- Cash reserves: €6 million.
- Employees: 120.
- Established conventional ticketing platform.
- No VFI implementation.
- No major unresolved legal liabilities.
- Equal starting customer trust, workforce conditions, technical reliability, sustainability, and partnership standing.

Starting indicator values may be configured centrally. All companies in a session must use the same values.

### 6. Executive role selection

Each student chooses one available role.

Every role can be occupied by only one student per company.

Six mandatory roles:

1. Chief Executive Officer (CEO)
2. Chief Financial Officer (CFO)
3. Chief Technology Officer (CTO)
4. Head of Marketing & Public Relations
5. Head of Legal
6. Employee Representative

Optional seventh and eighth roles:

7. Head of Sustainability
8. Head of Artist & Venue Relations

After selecting a role, the student receives a confidential executive briefing containing:

- Role responsibilities.
- Secret mission.
- Single-use executive power.
- Year 1 private intelligence.

The role description, mission, and power remain accessible throughout the simulation.

Private information must never appear on the shared company screen.

### 7. Executive missions

Each role has an objective evaluated at the end of the simulation.

**CEO: Board Confidence**

Achieve at least three of four board objectives covering financial viability, market position, organizational stability, and industry commitments.

**CFO: Financial Resilience**

Avoid financial distress and finish Year 10 with positive cash reserves.

**CTO: Technical Independence**

Maintain sufficient control over critical infrastructure and avoid excessive dependence on a single external provider.

**Marketing & PR: Market Recognition**

Finish among the leading companies for customer trust and maintain a competitive market position.

**Head of Legal: Legal Resilience**

Avoid major unresolved legal liabilities and serious regulatory penalties.

**Employee Representative: Protect the Workforce**

Avoid involuntary layoffs and maintain acceptable working conditions.

**Head of Sustainability: Sustainable Operations**

Meet environmental targets while supporting accessible and responsible services.

**Head of Artist & Venue Relations: Preferred Partner**

Maintain strong commercial partnerships and high satisfaction among artists, promoters, and venues.

Missions must have explicit evaluation rules tied to the simulation state. Where thresholds have not yet been finalized, keep them configurable. Do not invent student-facing mission achievements.

### 8. Executive powers

Each executive has one special power.

**Universal rules:**

- Each power can be activated only once during the entire ten-year simulation.
- Students may verbally threaten to use their power as often as they wish.
- A verbal threat has no automatic mechanical effect.
- Actual activation consumes the power permanently.
- Every activation has defined consequences or costs.
- Powers interact with company state and existing obligations.
- All activations are recorded in company and individual histories.
- Costs and consequences should follow from the intervention, without arbitrary trust penalties.

**CEO: Executive Override**

The CEO can override the team's preferred option.

Once activated, the CEO's selected decision becomes final and is locked.

The override is single-use. The CEO retains ordinary leadership responsibilities afterward.

**CFO: Spending Freeze**

Blocks a proposed expenditure.

The team must select a feasible alternative or defer the expenditure. Delays, contractual costs, and lost opportunities may follow.

**CTO: Technical Veto**

Blocks a proposed technical implementation.

The company must revise or defer implementation. Technical remediation, delays, or contractual consequences may follow.

**Marketing & PR: Public Campaign**

Launches a major communications campaign.

The campaign consumes company funds. Its effects depend on company credibility, current circumstances, and the campaign's purpose.

**Head of Legal: Formal Legal Review**

Requires a formal assessment of a proposed decision.

The review incurs legal fees and may delay implementation. Findings may reveal additional obligations or contractual risks.

**Employee Representative: Industrial Action**

Initiates a strike.

The strike disrupts operations and creates financial and potentially reputational consequences.

The company's original decision remains in force unless management voluntarily revises it.

**Head of Sustainability: Impact Assessment**

Commissions a formal assessment of environmental and social impacts.

The assessment costs money and time. Findings may identify new risks or opportunities.

The original decision remains in force unless management changes it.

**Head of Artist & Venue Relations: Contract Clause**

Invokes a material change clause in the company's largest client contract.

The clause concerns significant changes to technology, data practices, or service delivery.

Activation creates legal and relationship-management costs. The client may renegotiate or terminate its agreement if contractual conditions are met.

The clause does not automatically reverse the company's decision.

**Important distinction:** Binding powers can block or finalize a decision. Consequential powers change company circumstances while leaving the decision intact.

### 9. Shared company screen

Each company has one shared screen with three primary views.

#### A. Pre-decision view

Display:

- Current simulated year.
- Scenario title.
- Short scenario narrative, ideally 50–70 words.
- Three or four decision options.
- Costs and other essential information.
- Relevant company status.
- Decision countdown.
- Decision submission controls.

The scenario must be readable in approximately 30 seconds.

#### B. Post-decision view

Display:

- Final company decision.
- Immediate narrative consequences.
- Financial or operational changes.
- Concrete effects on affected people.
- Any new obligations or unresolved problems.
- Relevant external and internal events.

Only show consequences supported by the company's actual state.

#### C. Live company status

Accessible throughout the simulation.

Track:

- Cash reserves and financial health.
- Revenue and market position.
- Customer trust and experience.
- Workforce size and working conditions.
- Technical reliability and capabilities.
- Sustainability.
- Artist, promoter and venue relationships.
- Legal exposure.
- Active contracts.
- Outstanding obligations.
- Significant historical decisions.

Avoid presenting a single ethics score.

### 10. Individual student phone interface

Each student sees:

- Their executive role and responsibilities.
- Their secret mission.
- Their remaining executive power.
- Private information for the current year.
- Private consequences after the decision.
- Their individual decision log.
- Reflection prompts in Years 1, 5, and 10.

Private intelligence should usually be 25–40 words and directly relevant to the executive's responsibilities and mission.

It should provide meaningful evidence, including possible consequences for people, legal obligations, stakeholder interests, and organizational constraints.

Students decide whether to share this information with teammates.

### 11. Individual preferences

For every active year, each student records:

**Which option did you personally support?**

The available answers correspond to that year's decision options.

The student's preference is recorded independently of the company's final decision.

The system must preserve:

- Student's preferred option.
- Company's actual decision.
- Whether the CEO used an override.
- Executive powers activated.
- Relevant consequences.
- Role-specific intelligence received.

This allows the final report to compare individual preferences with collective outcomes.

### 12. Individual reflections

Written reflections occur only in Years 1, 5, and 10.

Students should write approximately one or two sentences. These reflections are private and appear in their final reports.

**Year 1: Initial judgment**

What considerations shaped your position? What was difficult about the negotiation, and what helped your team reach its decision?

**Year 5: Reassessment**

Whose interests did your team prioritize? What made the negotiation difficult, and how did earlier decisions shape the options available?

**Year 10: Accountability**

Which decision would you defend, and which would you reconsider? What responsibilities should your company accept for the consequences of its choices?

All active team members must submit their required reflections before the company advances or completes the simulation.

The shared screen displays submission progress, never reflection content.

The facilitator can mark an absent or disconnected participant inactive to prevent deadlocks.

### 13. Annual simulation structure

The simulation contains ten years:

| Year | Main theme |
|---|---|
| 1 | Procurement and strategic direction |
| 2 | Testing and prototyping |
| 3 | Launch and commercial deployment |
| 4 | Customer services and functionality |
| 5 | Privacy, public scrutiny and monetization pressures |
| 6 | New entry technologies and biometric capabilities |
| 7 | Safety, security and data sharing |
| 8 | Artists, audiences and stakeholder conflict |
| 9 | Final strategic direction |
| 10 | Disclosure and reporting |

Core years: 1, 3, 5, 7, 9, 10.

Optional years: 2, 4, 6, 8.

The facilitator configures which years are active and the decision time for each active year.

Skipped years are resolved automatically through their predefined defaults.

### 14. Decision resolution

Every year has:

- One annual decision.
- Three or four options.
- A predefined default.
- Immediate consequences.
- Persistent state changes.
- Possible delayed effects.
- Role-specific private information.
- Role-specific post-decision consequences.

The engine records the resolution mode:

- `student_decision`
- `deadline_expired`
- `facilitator_skipped`

Expired and skipped decisions apply the predefined default.

Skipped decisions are narrated as automatic developments and must never be attributed to individual students.

All state updates must be atomic and idempotent.

### 15. External events

External events are shared developments affecting the entire industry.

Rules:

- Occur in the same simulated year for every company.
- Have identical underlying conditions and shock parameters.
- Are independent of individual company decisions.
- May have different consequences because company states differ.
- Are resolved exactly once per company.
- Remain active even when the facilitator skips a year.

Examples include economic downturns, market recovery, public controversies, and regulatory developments.

External events must never be selected to punish or reward a company.

### 16. Internal events

Internal events emerge from a company's own state and history.

Rules:

- Evaluate after the relevant annual decision and external event, unless a scenario specifies another order.
- Use deterministic conditions and priority rules.
- Select the first eligible event from the year's event definitions.
- Apply at most one primary internal event per company per year.
- Include positive, negative, and mixed developments.
- Preserve consequences and unresolved obligations.
- Never introduce capabilities or contracts the company does not possess.

Examples include technical failures, successful launches, employee disputes, customer complaints, unexpected partnerships, and supplier problems.

### 17. Ethical narrative requirements

The simulation is an ethics assignment.

Consequences must communicate what happens to people, alongside financial and operational outcomes.

For example:

"Twenty-four employees will lose their jobs and employer-provided benefits. The restructuring reduces annual costs but increases pressure on the remaining customer support team."

Avoid relying exclusively on abstract indicators such as workforce −10 or reputation +5.

Ethical significance should emerge from concrete effects on:

- Employees and their livelihoods.
- Customers and access to entertainment.
- Artists, promoters and venues.
- People affected by data collection and verification.
- Communities and the environment.
- The company's obligations to different stakeholders.

Do not create obviously correct or incorrect choices. Decisions should involve credible competing considerations.

Do not make surveillance the inevitable outcome of the story. Surveillance-related possibilities emerge conditionally from technologies, data practices, contracts, and political developments.

Positive and negative outcomes must both be possible across different strategies.

### 18. Year 5 whole-class checkpoint

Year 5 is a mandatory synchronization point.

Sequence:

1. Every company completes its Year 5 decision.
2. The external and internal events are resolved.
3. Students receive their private consequences.
4. Students submit their individual preferences and reflections.
5. Each company waits until every active member has submitted.
6. The company enters checkpoint waiting status.
7. All companies synchronize.
8. The facilitator reveals the industry dashboard.
9. The facilitator releases Year 6.

The checkpoint shows all company names and flags.

Compare companies across separate dimensions:

- Financial performance.
- Market position.
- Customer trust.
- Workforce conditions.
- Sustainability.
- Partnerships.
- Industry commitments.

Do not calculate an overall ethics ranking.

Save the checkpoint results for comparison with Year 10.

### 19. Year 10 final checkpoint

After the final decision and reporting activity:

- Resolve final consequences.
- Evaluate secret missions.
- Collect individual preferences and reflections.
- Wait for all active team members.
- Synchronize companies.
- Reveal final industry results.
- Compare Year 5 and Year 10.
- Generate individual student reports.

The facilitator controls when the final results become visible.

### 20. Final individual report

Each student receives a personalized report containing:

- Company name and headquarters.
- Executive role.
- Secret mission and final outcome.
- Executive power use.
- Company's ten-year decision history.
- Student's preferred option for every active year.
- Company's actual decision for each year.
- Private intelligence received.
- Private consequences for the student's role.
- Individual reflections from Years 1, 5, and 10.
- Important external and internal events.
- Company performance and industry comparison.
- Significant stakeholder consequences.
- Final industry commitments review.

The report should clearly distinguish:

- What the student preferred.
- What the company decided.
- What happened afterward.
- Which developments were outside the company's control.

The report supports an individual take-home ethics reflection of approximately 500 words.

Company performance and mission achievement do not determine the student's academic grade.

### 21. Facilitator controls

The facilitator must be able to:

- Create and reset sessions.
- Configure the number of companies.
- Set active and skipped years.
- Set decision time limits.
- Start, pause, resume, and advance the simulation.
- View company progress.
- Monitor individual submissions without exposing private reflection text on classroom screens.
- Mark disconnected participants inactive.
- Trigger synchronized checkpoints.
- Release companies after checkpoints.
- View industry rankings.
- Export reports and simulation data.

Companies may progress independently between checkpoints.

A company must never receive information about another company's future decisions.

### 22. Technical implementation requirements

Use the existing application architecture wherever possible.

The engine should support:

- Structured scenario definitions.
- Company-state persistence.
- Individual student records.
- Role-specific content.
- Conditional decisions and consequences.
- Delayed effects and obligations.
- Deterministic internal events.
- Synchronized external events.
- Single-use executive powers.
- Mandatory reflection checkpoints.
- Industry rankings.
- Individual report generation.

Keep scenario text separate from the rules engine so that narrative content can be revised without rewriting application logic.

The same initial conditions and decisions must produce reproducible outcomes.

Test that every company can complete all ten years, including with every optional year skipped.

Do not invent additional storylines, ethical scores, executive powers, or mission criteria.

### 23. Timing and usability

Total workshop duration: approximately 90 minutes.

Design for five-minute decisions.

Recommended limits:

- Scenario: 50–70 words.
- Private intelligence: 25–40 words.
- Post-decision outcome: 30–50 words.
- Private consequence: one or two sentences.
- Written reflection: one or two sentences, only three times.

Interfaces must work on ordinary student phones and laptops.

Avoid excessive scrolling, complex tables on phones, and lengthy instructions during active rounds.

The simulation should prioritize discussion, negotiation, and decision-making over reading and data entry.

### 24. Implementation acceptance criteria

The implementation is ready for classroom testing when:

1. Companies can join, name themselves, and choose EU headquarters.
2. Every student can select a unique role and access confidential information.
3. Company screens show the appropriate scenarios and options.
4. Students can record individual preferences.
5. Company decisions resolve correctly, including CEO overrides.
6. Executive powers work once and produce their defined consequences.
7. External events occur consistently across companies.
8. Internal events depend on company state.
9. Skipped years apply their defaults without requiring student participation.
10. Year 1 and Year 5 reflections require all active students to submit.
11. Year 5 rankings synchronize across the entire session.
12. Company histories preserve decisions, events, and stakeholder consequences.
13. Year 10 generates individual reports.
14. No impossible states, duplicate financial charges, or unauthorized capabilities appear.
15. A full ten-year simulation can be completed within the classroom time limit.

**This specification governs the simulation's general mechanics, interfaces, and student experience. The separate annual scenario specifications provide the exact decisions, private intelligence, events, and conditional outcomes.**