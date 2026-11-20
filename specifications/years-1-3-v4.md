# FAIRPASS: YEARS 1–3
## Complete implementation specification, version 4

**Status: Authoritative replacement for all previous Years 1–3 drafts.**

Implement this specification in the existing FairPass application. Preserve the exact student-facing content. Use the general simulation specification for role selection, executive powers, interface structure, and facilitator controls.

All organizations, events, and numerical assumptions are fictional.

---

# PART 1. SHARED ENGINE RULES

## 1.1 Starting conditions

All companies begin Year 1 in 2027 with identical conditions.

| Variable | Starting value |
|---|---:|
| Cash reserves | €6.00M |
| Annual baseline revenue | €24.00M |
| Employees | 120 |
| Customer trust | 70/100 |
| Workforce conditions | 70/100 |
| Technical reliability | 70/100 |
| Sustainability | 70/100 |
| Partnership standing | 70/100 |
| Technical independence | 0 |
| Supplier dependence | 0 |
| Internal technical capability | 0 |
| Reliability readiness | 0 |
| Customer readiness | 0 |
| Development progress | 0 |
| Assurance evidence | 0 |
| Workforce pressure | 0 |
| Labour dispute risk | 0 |
| Legal exposure | 0 |
| VFI operational | No |
| Procurement strategy | None |
| Northstar contract | None |

The board's €3M investment authorization is a spending limit within existing cash reserves. It is not additional cash.

## 1.2 Financial accounting

Use a single cash ledger. Monetary values are stored in millions of euros.

**Cash model for Years 1–3:**

- Starting cash: €6M.
- Baseline revenue is displayed as company scale and market context.
- Routine baseline operating receipts and expenses are assumed to offset each other.
- Baseline revenue does not automatically increase cash.
- Only explicitly defined investments, economic shocks, contract costs, and executive-power effects change cash.
- No borrowing, interest, taxes, depreciation, or unlisted financing is introduced.

### Year 1 investments

| Strategy | Cost | Cash remaining |
|---|---:|---:|
| Build | €2.80M | €3.20M |
| License | €0.60M | €5.40M |
| Hybrid | €1.60M | €4.40M |
| Wait | €0.15M | €5.85M |

Deduct the investment exactly once when Year 1 resolves.

### Year 2 costs

| Decision | Cost |
|---|---:|
| Stress testing | €0.30M |
| Customer testing | €0.25M |
| Accelerate delivery | €0.15M |
| Independent assessment | €0.35M |

Deduct once when Year 2 resolves.

### Economic shock

The Year 2 external event reduces Year 3 demand-based revenue by 10%.

- Year 3 baseline revenue: €21.60M.
- Lost baseline revenue: €2.40M.
- Assumed cash contribution lost: 10% of €2.40M.
- Year 3 cash deduction: €0.24M.

Apply the €0.24M deduction once at the beginning of Year 3.

Do not deduct €2.40M from cash.

### VFI recurring costs

| Procurement | Annual operating cost |
|---|---:|
| Build | €0.45M |
| License | €0.90M |
| Hybrid | €0.65M |
| Wait | €0 |

These are future operating commitments.

For this simplified model, no VFI recurring fees are charged in Years 1–3, including for systems becoming operational during Year 3.

From Year 4 onward, charge the applicable annual operating cost once per operational year.

### Contract accounting

Year 3 Northstar awards create the following immediate costs:

| Result | Cash deduction | Annual contract revenue from Year 4 |
|---|---:|---:|
| Full awarded | €0.60M | €2.40M |
| Pilot awarded | €0.25M | €0.80M |
| Conventional awarded | €0.15M | €1.00M |
| Conditional award | €0.05M | €0 until activated |
| Unsuccessful bid | €0.05M | €0 |
| Declined | €0 | €0 |

Contract revenue is recorded separately from cash.

It does not automatically increase cash in Year 3.

From Year 4, active contracts contribute to reported annual revenue. The future financial model must distinguish contract revenue from net cash contribution.

### Financial feasibility

A company can select an option only if it can afford the required immediate expenditure.

`cash >= decision_cost`

If the option is unaffordable, display it as unavailable.

Do not allow negative cash.

If a default is unaffordable, use the lowest-cost feasible option and record `financial_fallback`.

For Years 1–3, all ordinary default paths are affordable.

### Transaction safety

Every financial effect must have a unique identifier:

`session_id + company_id + year + effect_id`

Do not apply the same effect twice, including after page refresh, retries, skipped years, or facilitator actions.

## 1.3 Annual decision sequence

For every active year:

1. Display the shared scenario and decision options.
2. Deliver private intelligence to student phones.
3. Collect each student's preferred option.
4. Resolve the company decision, including any executive powers.
5. Apply immediate decision effects.
6. Resolve the scheduled external event.
7. Evaluate and resolve one internal event.
8. Display the actual outcome and event announcements.
9. Deliver private role-specific consequences.
10. Update company status.
11. Collect written reflections if required.
12. Advance.

Individual preferences are mandatory in every active year.

Written reflections occur only in Years 1, 5, and 10.

For facilitator-skipped years, apply the default and events automatically without individual submissions.

## 1.4 Event rules

**External events:**

- Fixed by simulated year.
- Identical for every company.
- Independent of company decisions.
- May have different financial consequences because company states differ.
- Applied exactly once.

**Internal events:**

- Determined by company state.
- Evaluated in stated priority order.
- Only the first eligible primary event occurs.
- May create benefits, costs, obligations, or opportunities.
- Applied exactly once.

---

# PART 2. YEAR 1 · 2027
## The Five-Ticket Promise

**Core year. Five-minute decision.**

## 2.1 Shared screen: Pre-decision

Verified Fan Identity (VFI) promises to reduce automated ticket buying by limiting purchases to five tickets per verified person, per event.

Major promoters are interested. Fans hope for fairer access, although some are concerned about identity requirements.

Your company can enter this market, but the technology is still developing.

**How will you approach VFI?**

| Option | Initial investment | Estimated launch |
|---|---:|---|
| A. Build internally | €2.8M | 18–24 months |
| B. License a provider | €600K | 6–9 months |
| C. Hybrid development | €1.6M | 9–15 months |
| D. Wait and observe | €150K | Undetermined |

Shared status: €6M cash, €24M annual revenue, 120 employees.

## 2.2 Private intelligence

**CEO**

The board wants growth within three years. Directors also worry that losing major clients could eventually threaten the company's 120 jobs.

**CFO**

Licensing costs €900K annually after launch, compared with €450K for building and €650K for hybrid. Financial pressure could eventually force staffing reductions or higher service fees.

**CTO**

Internal development requires recruiting specialists. External systems are faster, but your engineers cannot yet verify how reliably they prevent duplicate identities.

**Marketing & PR**

Fans strongly support anti-scalping measures, but some worry about submitting identity documents. A complicated process could exclude customers who already struggle with digital services.

**Head of Legal**

Identity verification is possible under EU law, but each design requires a lawful basis and appropriate safeguards. Supplier contracts currently leave some responsibilities unclear.

**Employee Representative**

Building could create skilled jobs. Licensing may shift technical work to suppliers, while verification disputes could increase pressure on customer support staff.

**Head of Sustainability**

Verification requires additional computing resources. Some customers lack conventional identity documents, potentially limiting access to events even when tickets are available.

**Head of Artist & Venue Relations**

Northstar Live, representing 18% of company revenue, wants VFI within twelve months. Several smaller venues worry about the cost of helping customers who cannot verify themselves.

## 2.3 Decision effects

| Variable | Build | License | Hybrid | Wait |
|---|---:|---:|---:|---:|
| Cash | −2.80 | −0.60 | −1.60 | −0.15 |
| Technical independence | +3 | −2 | +1 | 0 |
| Supplier dependence | 0 | +3 | +2 | 0 |
| Internal capability | +2 | 0 | +1 | 0 |
| Initial development progress | 0 | 2 | 1 | 0 |
| Annual VFI cost commitment | 0.45 | 0.90 | 0.65 | 0 |

Set the procurement strategy.

VFI remains non-operational throughout Year 1.

## 2.4 Shared screen: Post-decision

**A. Build**

Your company invests €2.8M in its own system. Recruitment begins, creating skilled employment opportunities. Fans will wait longer for verified ticketing, and financial reserves fall to €3.2M.

**B. License**

Your company signs a supplier agreement. Fans may benefit from verified ticketing sooner. Some technical work moves outside the company, while customer support prepares for new verification disputes. Cash remaining: €5.4M.

**C. Hybrid**

Your company combines external verification with internal development. Existing employees will receive new responsibilities and training. The approach creates employment opportunities and integration demands. Cash remaining: €4.4M.

**D. Wait**

Your company continues conventional ticketing. Customers avoid new identity requirements, but automated purchasing remains a problem. Employees retain existing responsibilities, while some promoters consider alternative suppliers. Cash remaining: €5.85M.

## 2.5 Private consequences

| Role | Build | License | Hybrid | Wait |
|---|---|---|---|---|
| CEO | The investment may support long-term growth, but financial reserves are tighter. | Faster delivery may protect major contracts, with recurring obligations. | The board expects progress from both internal and external teams. | Preserved cash protects flexibility, but future contracts remain uncertain. |
| CFO | Only €3.2M remains available for unexpected costs and employment obligations. | Recurring fees may eventually compete with staffing and service budgets. | Development and supplier costs will both require monitoring. | Reserves remain strong, although future revenue is uncertain. |
| CTO | Your team controls the design and bears responsibility for its reliability. | Customers will depend on a system your engineers cannot fully modify. | Your engineers can shape the experience but depend on external verification. | Existing systems remain reliable, while the scalping problem continues. |
| Marketing | Fans must wait for the promised benefits. | Earlier availability could improve access if verification works well. | Customer experience can be adapted, although delivery remains uncertain. | Customers avoid verification barriers but remain exposed to scalpers. |
| Legal | Your company directly controls data practices and implementation decisions. | Responsibility for identity disputes must be clarified with the supplier. | Shared responsibilities require clear contractual and technical boundaries. | Current data practices continue, with fewer new obligations. |
| Employee Rep | Recruitment opportunities increase, alongside delivery pressure. | Technical work shifts externally; support employees face new demands. | Training opportunities increase, but so does workload. | Existing jobs remain stable for now, with fewer new opportunities. |
| Sustainability | Infrastructure choices remain under company control. | Supplier practices will influence energy use and accessibility. | Both supplier and internal practices will affect sustainability. | No major infrastructure expansion occurs; ticket access remains unchanged. |
| Artist Relations | Northstar may not wait for your development timetable. | Northstar's preferred timetable appears achievable. | Northstar's timetable remains uncertain. | Northstar may seek another provider, affecting future employment and revenue. |

## 2.6 External event E1

### Promoters announce trials

Three major European promoters announce VFI trials. Artists welcome the possibility of reducing ticket scalping, while fan organizations request assurances that verification will remain accessible.

The industry association invites ticketing companies to participate in developing common standards.

Effects:

- `market_vfi_interest = growing`
- `market_standardization = unsettled`
- No cash or trust changes.

## 2.7 Internal event I1

Select based on procurement.

**Build**

Specialist recruitment begins. Existing engineers take on additional responsibilities while vacancies are filled.

Effects:

- Workforce pressure +1.
- `recruitment_pressure = true`.

**License**

Customer support representatives request training before verification begins.

Effect: `support_training_needed = true`.

**Hybrid**

Internal and supplier teams disagree over responsibility for failed verifications.

Effect: `integration_responsibility_unresolved = true`.

**Wait**

A small promoter praises conventional ticketing, while Northstar requests a timetable for future VFI availability.

Effects:

- `northstar_vfi_interest = true`.
- `conventional_market_opportunity = true`.

## 2.8 Reflection

Each active student selects their preferred option.

**Written prompt:**

What considerations shaped your position? What was difficult about the negotiation, and what helped your team reach its decision?

One or two sentences.

Every active student must submit before progression.

## 2.9 Default

**C. Hybrid.**

Apply the same €1.6M investment and associated effects.

Skipped-year announcement:

"Management approves a hybrid VFI development programme, combining licensed verification technology with internally developed customer services. Initial investment: €1.6 million. Remaining cash: €4.4 million."

---

# PART 3. YEAR 2 · 2028
## The Pilot Problem

**Optional year. Five-minute decision.**

## 3.1 Shared screen: Pre-decision

Early VFI trials show promising results against automated purchasing. They also reveal problems: customers struggling with verification, failed transactions, and support teams overwhelmed during major ticket releases.

Your company has limited resources to prepare its technology and services.

**Where should you concentrate your efforts?**

| Option | Priority | Cost |
|---|---|---:|
| A. Stress testing | Reliability and recovery | €300K |
| B. Customer testing | Accessibility, usability and support | €250K |
| C. Accelerate delivery | Earliest launch timetable | €150K |
| D. Independent assessment | External technical and operational review | €350K |

For non-adopters, the work concerns their conventional platform and potential VFI adoption.

## 3.2 Private intelligence

**CEO**

The board wants progress, but a failed launch could damage relationships with clients who depend on reliable ticket sales for their livelihoods.

**CFO**

Delays increase costs. However, a major ticketing failure could require refunds and compensation that reduce funds available for wages and operations.

**CTO**

Stress tests have revealed possible bottlenecks during simultaneous purchases. You cannot guarantee these will occur in normal operations.

**Marketing & PR**

Early trials show some fans abandoning purchases when asked to upload identity documents. Others appreciate the reduction in automated buying.

**Legal**

Customers must have meaningful ways to exercise their rights and challenge verification errors. The company's procedures remain incomplete.

**Employee Representative**

Support staff report increasing overtime during trial periods. Several employees have requested additional training and clearer escalation procedures.

**Sustainability**

Verification failures may disproportionately affect customers with limited digital access or documentation. Infrastructure testing could also identify unnecessary energy consumption.

**Artist & Venue Relations**

Promoters fear cancellations and entry delays. Several artists are concerned that genuine fans may be excluded by verification failures.

## 3.3 Decision effects

| Variable | A | B | C | D |
|---|---:|---:|---:|---:|
| Cash | −0.30 | −0.25 | −0.15 | −0.35 |
| Reliability readiness | +2 | 0 | −1 | +1 |
| Customer readiness | 0 | +2 | −1 | +1 |
| Development progress | 0 | 0 | +2 | −1 |
| Assurance evidence | +1 | +1 | 0 | +2 |
| Workforce pressure | +1 | 0 | +2 | 0 |

Additional rules:

- Build + A: clear recruitment pressure.
- Build + C: workforce pressure +1.
- License + A or D: `supplier_assessed = true`.
- Hybrid + A or D: clear integration responsibility obligation.
- Wait + B: `customer_demand_evidence = true`.
- Wait + D: `supplier_evaluation_ready = true`.

For Wait, development progress remains zero regardless of Year 2 choice.

## 3.4 Shared screen: Post-decision

**A. Stress testing**

Your engineers identify and resolve several capacity problems. Major sales are better protected against technical failure, but customers experiencing verification difficulties still have limited support.

**B. Customer testing**

Your team improves registration and support procedures. More customers can complete transactions successfully, although peak-demand reliability remains less thoroughly tested.

**C. Accelerate delivery**

The project moves closer to launch. Promoters welcome the progress, but employees report increased overtime and several customer-facing problems remain unresolved.

**D. Independent assessment**

External specialists identify technical, accessibility and operational weaknesses. The findings provide useful evidence, but addressing them will require additional work.

For non-adopters, refer to their existing platform instead of VFI development.

## 3.5 Private consequences

| Role | A | B | C | D |
|---|---|---|---|---|
| CEO | Reliability improves, supporting client confidence. | More customers can use the service successfully. | Delivery advances, but operational pressure grows. | Independent findings may require changes to the timetable. |
| CFO | Testing costs €300K and may prevent expensive failures. | Support improvements cost €250K. | Spending is lower today, with unresolved future costs. | Review costs €350K, with remediation potentially required. |
| CTO | Technical reliability improves. | Customer-facing weaknesses receive attention. | Less time remains to resolve known technical problems. | Independent findings provide a prioritized technical assessment. |
| Marketing | Customer experience remains a potential weakness. | Registration becomes easier for more customers. | Early launch could attract attention, including complaints. | Findings may strengthen the credibility of future claims. |
| Legal | Technical testing creates useful evidence of precautions. | Customer rights and dispute procedures improve. | Known customer-facing weaknesses remain unresolved. | The review documents obligations requiring follow-up. |
| Employee Rep | Engineers face intensive testing demands. | Support staff receive greater attention and training. | Overtime and workload pressure increase. | Employees may face additional remediation work. |
| Sustainability | Infrastructure efficiency becomes better understood. | Accessibility barriers are reduced. | Accessibility and efficiency remain less thoroughly examined. | The review identifies social and environmental impacts. |
| Artist Relations | Promoters gain evidence of reliability. | Artists gain reassurance about customer access. | Early availability may help secure contracts. | Clients may appreciate the review or worry about delays. |

## 3.6 External event E2

### European entertainment spending falls

Rising household costs have reduced spending on concerts and festivals.

Promoters report weaker ticket sales and pressure to lower service fees. Some smaller venues are reducing events, while artists and technical crews face cancelled work.

Industry analysts expect ticketing demand to fall by 10% over the coming year.

Effects:

- Set Year 3 demand multiplier to 0.90.
- Schedule one €0.24M cash reduction for the beginning of Year 3.
- Do not deduct the cash during Year 2.

## 3.7 Internal event I2

Evaluate in order.

**1. Low reserves**

Trigger: Cash below €2.5M.

"Finance recommends eliminating 12 positions to protect liquidity. Management has not yet approved the proposal. Affected employees would lose their jobs and associated employment benefits."

Effects:

- `restructuring_proposed_12 = true`.
- Workforce concerns +1.
- No immediate layoffs.

**2. High workforce pressure**

Trigger: Workforce pressure at least 2.

"Employees report sustained overtime and missed rest periods. Their representatives request immediate changes to staffing and escalation procedures."

Effects:

- Workforce conditions −1.
- Labour dispute risk +1.

**3. Strong customer readiness**

Trigger: Customer readiness at least 2.

"Fans who previously struggled with online ticketing report that improved registration and assistance have helped them purchase tickets successfully."

Effect: Customer trust +1.

**4. Strong reliability**

Trigger: Reliability readiness at least 2.

"A high-demand ticket release completes without major disruption. Promoters report fewer technical complaints."

Effect: Partnership standing +1.

**5. Otherwise**

"Management reviews staffing, development costs and client commitments in response to the downturn."

Effect: None.

## 3.8 Default

**A. Stress testing.**

For non-adopters, conduct a technical feasibility review.

Charge €0.30M once.

Skipped-year announcement:

"Your company completes a routine technical testing and feasibility programme. The findings help prepare for future commercial decisions, although some questions remain unresolved."

No written reflection.

---

# PART 4. YEAR 3 · 2029
## Opening Night

**Core year. Five-minute decision.**

## 4.1 Start-of-year economic adjustment

Before presenting the scenario:

- Apply the scheduled €0.24M cash reduction once.
- Set annual baseline revenue to €21.60M.
- Record the shock as applied.

## 4.2 Readiness calculation

Use the following Year 1 starting progress:

| Procurement | Initial progress |
|---|---:|
| Build | 0 |
| License | 2 |
| Hybrid | 1 |
| Wait | 0 |

Year 2 decisions modify progress:

- Stress: 0.
- Customer testing: 0.
- Accelerate: +2.
- Independent assessment: −1.

At the beginning of Year 3, add one routine progress point to Build, License and Hybrid.

Wait receives zero.

Calculate:

`development_progress = max(0, initial_progress + year2_change + routine_progress)`

`reliability_readiness = max(0, year2_reliability_change)`

`customer_readiness = max(0, year2_customer_change)`

Apply outstanding obligations as calculated penalties:

- Recruitment pressure: development progress −1.
- Unresolved integration responsibility: reliability readiness −1.
- Unresolved support training: customer readiness −1.

All calculated values have a minimum of zero.

Do not permanently subtract these penalties from stored scores.

### Operational VFI

VFI becomes operational in Year 3 if:

1. Procurement was Build, License or Hybrid.
2. Effective development progress is at least 2.
3. Effective reliability readiness is at least 1.

Otherwise VFI remains in development or integration.

Wait never becomes operational in Year 3.

## 4.3 Shared screen: Pre-decision

Northstar Live is preparing a major European tour and inviting ticketing providers to bid.

The contract could help your company recover from the economic slowdown and support employment. Northstar expects reliable sales, fair access and effective customer support.

An ambitious proposal could bring significant revenue, but failures would affect thousands of fans and people whose livelihoods depend on the tour.

**What will you offer?**

| Option | Proposal |
|---|---|
| A. Full VFI rollout | Verified ticketing across the tour |
| B. Limited VFI pilot | Selected events, with possible expansion |
| C. Conventional ticketing | Existing platform with additional fraud controls |
| D. Decline | Focus on current clients and operations |

## 4.4 Private intelligence

**CEO**

Northstar's contract could protect jobs during the downturn. A failed delivery could damage the company's ability to retain other clients.

**CFO**

The full contract offers substantial revenue, but service failures could trigger compensation payments. Existing reserves may be insufficient for an expensive recovery.

**CTO**

Your team's readiness depends on earlier testing. Promising demonstrations do not guarantee reliable performance during a major public launch.

**Marketing & PR**

Northstar's audience includes customers with limited experience of digital verification. Failed registrations could mean losing access to tickets they expected to purchase.

**Legal**

Northstar's proposed contract includes service-level obligations. Customer refunds, disputes and accessibility complaints may create additional responsibilities.

**Employee Representative**

A full rollout requires extended customer support coverage. Staff are concerned about overtime, and some fear that failures will lead to disciplinary action.

**Sustainability**

Northstar expects accessible ticket purchasing and entry. Customers unable to complete verification may need alternative arrangements.

**Artist & Venue Relations**

Northstar has other suppliers available. Artists want to reduce scalping but are concerned about fans being excluded or stranded at venue entrances.

## 4.5 Northstar contract resolution

Evaluate using effective readiness and available cash.

### A. Full rollout

**Awarded** if:

- VFI operational.
- Development progress at least 3.
- Reliability readiness at least 1.
- Cash at least €0.60M.

**Conditional** if:

- Procurement is Build, License or Hybrid.
- Development progress at least 1.
- Cash at least €0.05M.
- Full award conditions are unmet.

**Unsuccessful** otherwise.

### B. Limited pilot

**Awarded** if:

- VFI operational.
- Development progress at least 2.
- Cash at least €0.25M.

**Conditional** if:

- Procurement is Build, License or Hybrid.
- Development progress at least 1.
- Cash at least €0.05M.
- Pilot award conditions are unmet.

**Unsuccessful** otherwise.

### C. Conventional ticketing

**Awarded** if:

- Technical reliability at least 65/100.
- Cash at least €0.15M.

**Unsuccessful** otherwise.

### D. Decline

Always declined.

### Contract status

Store exactly one:

- `full_awarded`
- `pilot_awarded`
- `conventional_awarded`
- `full_conditional`
- `pilot_conditional`
- `unsuccessful`
- `declined`

## 4.6 Contract financial effects

| Status | Immediate cash deduction | Annual revenue from Year 4 |
|---|---:|---:|
| Full awarded | €0.60M | €2.40M |
| Pilot awarded | €0.25M | €0.80M |
| Conventional awarded | €0.15M | €1.00M |
| Conditional | €0.05M | €0 until activation |
| Unsuccessful | €0.05M | €0 |
| Declined | €0 | €0 |

No contract revenue is recognized in Year 3.

No bid or implementation cost may be charged more than once.

## 4.7 Shared screen: Post-decision

Display the selected proposal and exactly one resolved outcome.

### Proposal A: Full rollout

Your company proposes verified ticketing across the tour. Thousands of fans could benefit from reduced scalping, but successful delivery requires reliable verification and effective customer support.

### Proposal B: Limited pilot

Your company proposes a smaller implementation. Selected audiences would test the system before wider deployment, limiting the initial number of people affected by potential problems.

### Proposal C: Conventional

Your company offers established ticketing with enhanced fraud controls. Customers avoid new verification requirements, although automated resale remains harder to prevent.

### Proposal D: Decline

Your company withdraws from the bid. Existing staff avoid the demands of a major new contract, but the company loses a potential revenue opportunity during the downturn.

### Resolved outcome messages

**Full awarded**

Northstar awards your company the full tour contract. Your verified ticketing system meets the required readiness threshold, and implementation begins.

**Pilot awarded**

Northstar awards your company a limited pilot. Your verification system is ready for selected events, with expansion dependent on performance.

**Conventional awarded**

Northstar selects your conventional ticketing service. The company will deliver established ticketing with enhanced fraud monitoring.

**Full conditional**

Northstar offers a conditional full contract. Your company must complete additional development and demonstrate operational readiness before the agreement becomes active.

**Pilot conditional**

Northstar offers a conditional pilot. Your company must complete outstanding preparation before ticket sales begin.

**Unsuccessful**

Northstar selects another provider. Your company incurs the bid preparation cost but assumes no new delivery obligations.

**Declined**

Your company does not submit a bid. Existing operations continue.

## 4.8 Private consequences

For awarded contracts, display the relevant role-and-option message.

For conditional awards, display the message as a potential future implication, preceded by:

"Your company has received a conditional offer. The following implications depend on successful activation."

For unsuccessful bids, replace the normal consequence with:

"Northstar selected another provider. Your company has no new delivery obligations, but the potential revenue and associated opportunities will not materialize."

For declined bids, display the Decline message.

| Role | Full | Pilot | Conventional | Decline |
|---|---|---|---|---|
| CEO | Growth potential rises, alongside responsibility for major delivery failures. | A smaller commitment may provide evidence for expansion. | The company relies on proven services during uncertainty. | Future growth and employment security remain concerns. |
| CFO | Revenue potential rises, but so does compensation exposure. | Financial exposure is more limited. | Implementation costs remain manageable. | Cash is preserved, with no new contract revenue. |
| CTO | Thousands of customers may depend on your system's readiness. | Problems can be identified in a smaller deployment. | Existing infrastructure remains central. | No additional technical commitments arise. |
| Marketing | Successful delivery could improve access for many fans. | Customer experience can be evaluated before expansion. | Fans avoid verification barriers but remain exposed to scalping. | The company has less influence over the tour's ticketing experience. |
| Legal | Contractual and customer obligations increase substantially. | Obligations are limited to the pilot scope. | Existing service obligations remain. | No new Northstar liabilities arise. |
| Employee Rep | Staffing demands increase, potentially protecting jobs while intensifying workload. | Additional work is concentrated around selected events. | Existing teams continue familiar operations. | No additional workload, but fewer opportunities for employment growth. |
| Sustainability | Accessibility arrangements become critical at scale. | Impacts can be assessed with fewer attendees. | Existing access arrangements continue. | No new deployment impacts arise. |
| Artist Relations | A successful tour could strengthen your largest client relationship. | Northstar may expand the partnership after the pilot. | Northstar may prefer another provider for VFI events. | Northstar will seek another supplier for this tour. |

## 4.9 External event E3

### Verified ticketing expands

Several European tours report fewer suspicious bulk purchases after introducing VFI.

However, fan organizations report inconsistent experiences. Some customers gained access to events they previously struggled to attend, while others experienced verification failures and difficult refund processes.

The industry association announces a review of technical and accessibility standards.

Effects:

- `market_vfi_interest = mainstream`
- `market_accessibility_scrutiny = elevated`
- No automatic trust or financial changes.

## 4.10 Internal event I3

Evaluate in priority order.

**1. Full awarded + low customer readiness**

Trigger: Full contract awarded and effective customer readiness below 2.

"Hundreds of customers cannot complete verification before ticket sales close. Some lose the opportunity to attend the concert, while support employees face a surge in complaints."

Effects:

- Customer trust −1.
- Workforce pressure +1.
- `verification_remediation_required = true`.

**2. Full awarded + adequate customer readiness**

Trigger: Full contract awarded and effective customer readiness at least 2.

"Ticket sales proceed smoothly. Fans report fewer suspicious bulk purchases, and Northstar praises your company's delivery."

Effects:

- Customer trust +1.
- Partnership standing +1.

**3. Pilot awarded**

"Most customers complete their purchases successfully, but a smaller group requires additional assistance. Northstar requests improvements before expanding the programme."

Effects:

- `pilot_review_pending = true`
- `pilot_expansion_opportunity = true`

**4. Conventional awarded**

"Ticket sales proceed without major technical incidents. Some fans complain that resale prices remain high, while Northstar praises reliable delivery."

Effects:

- Partnership standing +1.
- `scalping_concerns = true`

**5. No active contract + cash at least €3M**

"A smaller promoter approaches your company about serving regional events overlooked by larger providers."

Effect:

- `regional_opportunity = true`

**6. Otherwise**

"Management reassesses its commercial pipeline following the procurement season."

Effect: None.

## 4.11 Default

**C. Conventional ticketing.**

Evaluate the bid using the same contract rules.

Skipped-year announcement:

"Your company submits a conventional ticketing proposal with enhanced fraud monitoring. Northstar evaluates the offer alongside competing providers."

Append the actual contract outcome.

No written reflection.

---

# PART 5. YEAR 4 HANDOFF RULES

These transitions must be implemented even before Year 4's scenario content is added.

## 5.1 Conditional Northstar contracts

At the start of Year 4, add one routine development progress point to companies with Build, License or Hybrid procurement strategies.

Then recalculate effective readiness.

For a conditional full contract, activate if:

- VFI operational.
- Development progress at least 3.
- Reliability readiness at least 1.
- Cash at least €0.55M.

For a conditional pilot, activate if:

- VFI operational.
- Development progress at least 2.
- Cash at least €0.20M.

If activated:

- Charge the remaining implementation cost once.
- Full conditional: €0.55M.
- Pilot conditional: €0.20M.
- Set the contract to the corresponding awarded status.
- Begin contract revenue recognition in Year 4.

If requirements are unmet:

- Set contract status to `expired`.
- Charge no additional implementation costs.
- Recognize no contract revenue.

No conditional award remains pending after this transition.

## 5.2 Recruitment pressure

Created by Year 1 Build.

Resolved by Year 2 Stress testing.

If unresolved at Year 3, reduce effective development progress by one.

At the beginning of Year 4, clear the temporary recruitment-pressure flag after recording its effect on development history.

## 5.3 Support training

Created by Year 1 License.

Resolved by Year 2 Customer testing.

If unresolved, reduce effective customer readiness by one.

At the start of Year 4, retain the obligation as `support_training_outstanding`.

It may be resolved by later customer support or accessibility improvements.

## 5.4 Integration responsibility

Created by Year 1 Hybrid.

Resolved by Year 2 Stress testing or Independent assessment.

If unresolved, reduce effective reliability readiness by one.

At the start of Year 4, retain the obligation as `integration_governance_outstanding`.

It may be resolved through later technical or contractual work.

## 5.5 Restructuring proposal

Created only by the Year 2 low-cash internal event.

No layoffs occur automatically.

At the start of Year 4:

- If cash is at least €2.5M, withdraw the proposal.
- If cash remains below €2.5M, retain it as an unresolved management obligation.

Future decisions may address it through financing, staffing changes or operational restructuring.

Skipping Year 4 does not authorize layoffs.

## 5.6 Verification remediation

Created by the Year 3 verification-failure internal event.

Carry forward as an active obligation.

It may be resolved by later investments in support, accessibility, testing or verification procedures.

Do not clear it automatically.

## 5.7 Pilot review

Created by a Year 3 pilot award.

Carry forward as a pending review and possible expansion opportunity.

Expansion requires a later decision or explicitly defined event.

## 5.8 Regional opportunity

Created by an applicable Year 3 internal event.

Remains available through Year 5.

Does not automatically generate revenue.

Expires after Year 5 unless activated.

---

# PART 6. FINAL VALIDATION

Run all 64 combinations of the four decisions across Years 1–3.

Also test skipped-year defaults, expired decisions, and relevant executive-power effects.

Verify:

1. All companies begin with €6M cash.
2. Year 1 closing cash is correct for all four strategies.
3. No initial investment is charged twice.
4. Year 2 testing costs are applied once.
5. The economic shock deducts €0.24M once at the start of Year 3.
6. Year 3 reported baseline revenue is €21.6M.
7. VFI recurring fees are not charged during Years 1–3.
8. Wait cannot become VFI operational.
9. Readiness calculations are deterministic and nonnegative.
10. Outstanding obligations affect readiness only once per evaluation.
11. Every Northstar bid resolves to exactly one outcome.
12. Contract costs match the actual outcome.
13. Contract revenue is not added to Year 3 cash.
14. Unsuccessful bids generate no contract revenue.
15. Conditional contracts are resolved at the start of Year 4.
16. Every outcome message matches the actual contract status.
17. Internal events never refer to contracts that were not awarded.
18. No restructuring proposal automatically removes employees.
19. External events occur identically across companies.
20. Internal events depend on company state.
21. Skipped years apply defaults and events without individual submissions.
22. Every active year records individual preferred options.
23. Only Year 1 requires a written reflection within Years 1–3.
24. All active students submit the Year 1 reflection before progression.
25. All decisions, events, financial effects and private consequences are preserved in individual reports.
26. No company can spend more cash than it has.
27. No capability appears without a corresponding development or activation transition.
28. No contract generates revenue before its activation year.
29. All delayed obligations have defined carry-forward or expiry rules.
30. Replaying a decision or event does not duplicate its effects.

**This is the complete, authoritative Years 1–3 specification. Replace every earlier version with this document.**