
# FAIRPASS: YEARS 6–8
## Complete narrative and implementation specification
### Version 1 | Authoritative continuation of Years 1–5

Implement in the existing FairPass simulation. Preserve the established role system, company dashboard, decision engine, financial ledger, individual preference recording, facilitator controls, and Year 5 checkpoint.

Years 6 and 8 are optional. Year 7 is mandatory.

All events, organizations, financial figures, and people are fictional.

The simulation must preserve different company trajectories. Companies that invested in VFI, companies that suspended verification, and companies that retained conventional ticketing must face different opportunities and constraints.

No universal ethical score. No automatic moral ranking of technological choices.

---

# PART A. ENGINE RULES FOR YEARS 6–8

## A1. Annual progression

For each active year:

1. Apply scheduled start-of-year transitions.
2. Apply the fixed external event at its specified point.
3. Display the shared decision scenario.
4. Deliver private intelligence to each role.
5. Collect individual preferred options.
6. Resolve executive powers and the company decision.
7. Apply decision costs and state changes once.
8. Resolve conditional consequences.
9. Resolve one prioritized internal event.
10. Display the actual outcome.
11. Deliver role-specific consequences.
12. Update company state and individual histories.
13. Advance when all active students have submitted.

External events are identical across companies in the same year.

Internal events depend on each company's actual state.

Years 6 and 8 use their defaults when skipped or expired.

Year 7 uses its default when expired, but must still be experienced by every company.

## A2. Timing

The facilitator releases Year 6 simultaneously after the Year 5 industry checkpoint.

Companies then progress independently.

Suggested timing:

- Year 6: 5 minutes
- Year 7: 7 minutes
- Year 8: 5 minutes

The facilitator may skip Years 6 and 8.

No written reflections occur in Years 6–8.

Individual preferred options remain mandatory in active years.

## A3. Financial continuity

Continue the existing simplified financial model.

Cash is liquid reserves.

Baseline revenue is reported separately from cash.

Routine baseline receipts and operating expenditure offset each other.

Contract revenue is reported as revenue and is not automatically treated as cash profit.

Explicit decision costs, contract implementation costs, recurring VFI operating costs, and event costs change cash.

No unlisted costs may be inferred.

Annual VFI operating cost:

- Build: €0.45M
- License: €0.90M
- Hybrid: €0.65M
- Wait: €0

Charge once at the beginning of each year in which VFI is operational.

Suspending mandatory verification does not terminate the underlying VFI system or its operating contract.

For Years 6–8, continue reporting annual baseline revenue at €24M unless a fixed external event explicitly changes it.

Continue recognizing active Northstar contract revenue at its established annual amount.

Do not recognize revenue from unactivated opportunities.

All cash changes use unique, idempotent ledger entries.

## A4. Financial fallback

An option is affordable when available cash is at least its immediate cost.

Unaffordable options remain visible but disabled.

If a decision expires:

- Apply the specified default if affordable.
- Otherwise apply the lowest-cost feasible option.
- If costs are tied, select the option with the alphabetically earliest letter.

Record the actual option and `decision_source = expired_default` or `financial_fallback`.

Do not attribute defaults to students.

No negative cash.

## A5. Mandatory verification state

Use an explicit variable:

`mandatory_vfi_active`

At the start of Year 6:

- If VFI is operational and Year 5 option A was not selected, set true.
- If VFI is operational and Year 5 option A was selected, set false.
- If VFI is not operational, set false.

This variable describes whether identity verification is mandatory for the company's own VFI-enabled services.

It does not mean that every event managed by the company uses VFI.

`vfi_operational` and `mandatory_vfi_active` are separate variables.

A company may operate VFI with optional verification.

No subsequent year automatically reverses a suspension.

## A6. Existing obligations

Carry forward all unresolved obligations from Years 1–5, including:

- Verification remediation
- Support training
- Integration governance
- Restructuring proposal
- Pilot review
- Review remediation
- Customer compensation review
- Staff escalation review
- Reservation terms review
- Active contract obligations

Year 6 and later decisions may resolve these only when an explicit rule says so.

## A7. New variables

Initialize at zero:

- `entry_efficiency`
- `entry_assistance`
- `biometric_capability`
- `biometric_exposure`
- `entry_contract_value_m`
- `security_cooperation`
- `privacy_safeguards`
- `data_disclosure_exposure`
- `stakeholder_conflict`
- `commercial_dependency`
- `artist_autonomy`
- `community_access`
- `security_assurance`
- `regulatory_scrutiny`

Initialize false:

- `facial_entry_selected`
- `facial_entry_authorized`
- `facial_entry_operational`
- `smart_entry_selected`
- `staffed_entry_selected`
- `entry_contract_active`
- `entry_contract_pending`
- `entry_compliance_review`
- `entry_remediation_required`
- `law_enforcement_request_received`
- `law_enforcement_request_resolved`
- `law_enforcement_disclosure_made`
- `law_enforcement_data_preserved`
- `law_enforcement_legal_review`
- `law_enforcement_request_contested`
- `law_enforcement_deadline_pending`
- `data_minimization_completed`
- `artist_partnership_active`
- `commercial_partnership_active`
- `partnership_conditions_disputed`
- `community_program_active`
- `year9_contract_review_required`

Use existing indicators where possible. Do not duplicate customer trust, workforce conditions, technical reliability, partnership standing, sustainability, or cash.

All 0–100 indicators remain clamped.

---

# PART B. YEAR 6 · 2032
## Beyond the Ticket

Optional year. Five-minute decision.

## B1. Start-of-year transitions

1. Charge the annual VFI operating cost if operational.
2. Recognize active Northstar contract revenue in reported revenue.
3. Carry forward unresolved obligations.
4. Do not automatically activate new technologies or commercial opportunities.

## B2. External event E6

Display before the decision.

### The Next Frontier: Getting Inside

European venues are investing in faster entry systems.

Several operators are testing facial recognition, while others are expanding mobile ticket scanning and staffed assistance.

At the same time, European regulators announce coordinated scrutiny of automated entry systems, including their necessity, lawful basis, accuracy, accessibility, and use of biometric data.

Venues are looking for suppliers who can balance speed, security, and customer experience.

Effects:

- `market_entry_technology_interest = high`
- `regulatory_scrutiny += 1`
- No automatic fines or legal violations.
- No automatic customer trust change.

The regulatory announcement applies to every company.

## B3. Shared screen: Pre-decision

# Beyond the Ticket

A major European venue operator offers your company a five-year contract to manage entry at several large venues.

The operator wants shorter queues, fewer fraudulent entries, and better information about attendance.

Its preferred solution is facial recognition, but alternative approaches are welcome.

The contract could create new revenue and employment opportunities. It also introduces responsibilities extending beyond ticket sales.

**What will you propose?**

| Option | Proposal | Initial cost |
|---|---|---:|
| A | Optional facial recognition entry | €700K |
| B | Smart ticket scanning and queue management | €400K |
| C | Staffed entry and human assistance | €450K |
| D | Decline the contract | €0 |

Facial recognition is optional for attendees, with a conventional entry route required.

For companies without VFI, facial recognition requires an additional €300K integration investment.

The additional investment does not automatically establish lawful biometric processing.

## B4. Private intelligence

**CEO**

The venue operator expects to expand the contract if the first year succeeds. Winning could diversify company revenue, but a public failure would affect multiple major venues.

**CFO**

Facial recognition requires the largest initial investment. Staffed entry has lower technical costs but higher ongoing labour requirements. The contract's profitability remains uncertain.

**CTO**

Facial recognition could reduce entry times, but false matches and missed matches remain possible. Existing VFI infrastructure may help integration without resolving biometric accuracy or legal questions.

**Marketing & PR**

Some fans welcome faster entry. Others are uncomfortable with facial recognition, even when participation is optional. Clear alternatives may influence public acceptance.

**Head of Legal**

Biometric identification creates substantial legal obligations. The venue's commercial preference is insufficient to establish a lawful basis. An impact assessment and appropriate safeguards are necessary.

**Employee Representative**

Automated entry could reduce routine scanning work. Staffed entry could create employment, but workers need authority to resolve disputes and protection from confrontations.

**Head of Sustainability**

New hardware and computing infrastructure increase environmental demands. Staffed entry may be more accessible, while improved queue management could reduce congestion.

**Head of Artist & Venue Relations**

The venue operator prefers speed. Several artists want assurances that fans can enter without biometric identification and receive help when technology fails.

## B5. Decision costs and state effects

### A. Optional facial recognition

Cost:

- €0.70M if VFI operational.
- €1.00M if VFI not operational.

Effects:

- `facial_entry_selected = true`
- `entry_contract_pending = true`
- `entry_efficiency += 3`
- `biometric_exposure += 2`
- `entry_compliance_review = true`
- `commercial_opportunity += 2`

The efficiency score represents expected potential until authorization and activation.

Set:

- `facial_entry_authorized = false`
- `facial_entry_operational = false`

No facial identification may be deployed in Year 6.

The company must complete an explicit compliance review in Year 7 before activation can be considered.

### B. Smart scanning

Cost: €0.40M.

Effects:

- `smart_entry_selected = true`
- `entry_efficiency += 2`
- `entry_assistance += 1`
- `partnership_standing += 1`
- `entry_contract_active = true`

No biometric capability is created.

### C. Staffed entry

Cost: €0.45M.

Effects:

- `staffed_entry_selected = true`
- `entry_efficiency += 1`
- `entry_assistance += 3`
- `workforce_demand += 2`
- `partnership_standing += 1`
- `entry_contract_active = true`

Staffing needs increase. Do not automatically add employees without an explicit hiring transaction.

### D. Decline

Cost: €0.

Effects:

- No entry contract.
- No new entry capability.
- Preserve existing operations.

## B6. Contract economics

The five-year venue agreement has the following annual reported revenue potential:

- Facial recognition: €1.40M, only after lawful authorization and activation.
- Smart scanning: €0.85M.
- Staffed entry: €0.95M.
- Decline: €0.

Active contracts begin contributing to reported revenue in Year 7.

Facial recognition remains pending in Year 6 and generates no contract revenue until activation.

No entry contract adds cash automatically.

The five-year term begins upon activation.

## B7. Shared screen: Post-decision

**A. Facial recognition**

Your company proposes optional facial recognition. The venue welcomes the potential for faster entry, while artists and customer representatives request evidence of safeguards and accessible alternatives.

Deployment remains subject to technical and legal review.

**B. Smart scanning**

Your company selects improved ticket scanning and queue management. Venues expect shorter queues without introducing biometric identification.

**C. Staffed entry**

Your company prioritizes trained entry staff and human assistance. Customers gain more opportunities to resolve problems directly, while the company accepts higher staffing requirements.

**D. Decline**

Your company declines the entry-management contract. Existing operations continue, and the venue operator seeks another supplier.

## B8. Private post-decision consequences

| Role | A. Facial | B. Smart | C. Staffed | D. Decline |
|---|---|---|---|---|
| CEO | Expansion depends on successful authorization and public acceptance. | The company enters a growing market with familiar technology. | A service-intensive strategy creates new commercial possibilities. | Financial exposure is avoided, along with the growth opportunity. |
| CFO | Investment is high and revenue remains conditional. | Implementation costs are moderate. | Labour commitments may affect future margins. | Cash reserves remain unchanged. |
| CTO | Your team must demonstrate accuracy, security, and fallback procedures. | Existing technical capabilities support deployment. | Technical complexity is lower, but coordination remains important. | No new technical commitments arise. |
| Marketing | Faster entry may appeal to fans, while biometric concerns remain. | Convenience improves without facial identification. | Human assistance becomes a service advantage. | The company retains its current customer proposition. |
| Legal | Biometric processing requires an explicit compliance determination. | Existing data obligations continue. | Employment and accessibility procedures become central. | No new venue-related obligations arise. |
| Employee Rep | Some scanning tasks may eventually change or disappear. | Staff require training in new systems. | Additional staffing and training are needed. | Existing employment arrangements continue. |
| Sustainability | Hardware, computing, and accessibility impacts require assessment. | Queue efficiency may improve resource use. | Human access improves, with ongoing operational costs. | No new infrastructure is required. |
| Artist Relations | Artists request meaningful alternatives to facial recognition. | Venues welcome faster entry with fewer new controversies. | Artists welcome practical assistance for fans. | The venue operator looks elsewhere. |

## B9. Conditional consequences

### Facial recognition and unresolved governance

If `integration_governance_outstanding = true`:

- Record an additional compliance finding.
- `entry_compliance_review = true`
- Do not activate facial recognition.

### Facial recognition and strong assurance evidence

If `assurance_evidence >= 3`:

- `security_assurance += 1`
- The compliance review receives stronger technical documentation.
- Authorization remains pending.

### Smart scanning with strong technical reliability

If technical reliability is at least 70:

- `partnership_standing += 1`

### Staffed entry with unresolved support training

If `support_training_outstanding = true`:

- Clear the training obligation.
- `workforce_pressure = max(0, workforce_pressure - 1)`

### Staffed entry with unresolved customer assistance obligations

If `verification_remediation_required = true`:

- Clear that obligation.
- `customer_trust += 1`

## B10. Internal event I6

Evaluate in priority order.

**1. Facial recognition with weak assurance**

Trigger:

- Facial selected.
- Assurance evidence below 3.

"The venue operator requests additional testing after a demonstration produces incorrect matches. The contract remains pending while engineers and legal advisers review the system."

Effects:

- `entry_remediation_required = true`
- No contract activation.
- No automatic trust penalty.

**2. Facial recognition with strong assurance**

Trigger:

- Facial selected.
- Assurance evidence at least 3.

"A technical demonstration produces promising results. The venue operator requests a formal compliance assessment before deployment."

Effects:

- `security_assurance += 1`
- Contract remains pending.

**3. Smart scanning with strong reliability**

Trigger:

- Smart scanning selected.
- Technical reliability at least 70.

"A major venue reports shorter entry queues during a sold-out concert. Staff successfully assist customers whose tickets fail to scan."

Effects:

- Partnership standing +1.
- Customer trust +1.

**4. Staffed entry with low reserves**

Trigger:

- Staffed entry selected.
- Cash below €2M.

"Management warns that the staffing commitment may place pressure on future budgets. Workers ask for reassurance that employment conditions will be protected."

Effects:

- Financial pressure +1.
- Workforce concerns +1.

**5. No entry contract and strong trust**

Trigger:

- No entry contract.
- Customer trust at least 72.

"An independent festival asks your company to advise on accessible entry arrangements without biometric identification."

Effects:

- `independent_festival_opportunity = true`
- No automatic revenue.

**6. Otherwise**

"The company completes its entry-management review without a major incident."

No additional effects.

## B11. Default

**B. Smart scanning (€0.40M).**

If unaffordable, use D. Decline (€0).

Skipped-year announcement:

"Management selects improved ticket scanning and queue management for the new venue partnership. The company expands into entry services without introducing facial recognition."

Apply the selected outcome and events normally.

---

# PART C. YEAR 7 · 2033
## The Safety Dilemma

Mandatory core year. Seven-minute decision.

This year explores public safety, legal authority, privacy, and the limits of corporate responsibility.

## C1. Start-of-year transitions

1. Charge annual VFI operating costs if applicable.
2. Recognize active Northstar and venue contract revenue.
3. Preserve unresolved obligations.
4. Do not automatically activate facial recognition.
5. Determine what customer data the company actually holds.

## C2. Data inventory

Every company has ordinary ticket transaction records.

Possible additional data depends on history:

**Conventional companies**

- Ticket purchases.
- Account and contact details.
- Transaction history.
- No VFI identity records.

**VFI companies**

- Ticket purchases.
- Verification status.
- Identity-linked account records.
- Any retained verification information permitted by their existing architecture.

**Companies with data linkage capability**

- Additional links between accounts, purchases, or transfers.

**Companies with facial entry selected**

- No live facial identification records unless the technology has been explicitly authorized and activated.
- A pending facial-entry contract does not create biometric records.

Do not invent location tracking, biometric databases, or identity documents that the company never collected.

Create a read-only `available_data_categories` inventory for each company.

## C3. External event E7

Display before the decision.

# Security Alert at a Major Concert

Police investigating a credible threat against a major European concert have contacted ticketing providers.

Investigators believe someone involved may have purchased tickets using multiple accounts.

They ask providers to preserve relevant records and identify potentially connected purchases.

The threat has not yet been resolved.

Authorities say the investigation is urgent, but some requested information may involve people with no connection to the threat.

### Legal status

The initial request contains:

- A formally issued preservation order covering relevant records.
- A request for additional customer information.
- No valid disclosure order for the additional information at the time of receipt.

The preservation order is binding.

The broader disclosure request requires further legal authorization.

This legal status is identical for every company.

No student company is suspected of wrongdoing.

## C4. Shared screen: Pre-decision

# The Safety Dilemma

Police investigating a credible threat have asked your company to preserve relevant ticket records and provide additional customer information.

The preservation order is legally binding. The broader request has not yet been authorized.

Your company may hold information that helps investigators. It may also hold sensitive information about customers who have done nothing wrong.

A delayed response could affect the investigation. An excessive disclosure could expose innocent people.

**How will you respond?**

| Option | Response | Cost |
|---|---|---:|
| A | Cooperate proactively and seek urgent authorization | €200K |
| B | Preserve records and require a valid disclosure order | €150K |
| C | Preserve records, offer limited technical assistance, and seek independent legal review | €250K |
| D | Preserve records and formally contest the broader request | €100K |

All options comply with the binding preservation order.

No option authorizes disclosure without a valid legal basis.

## C5. Private intelligence

**CEO**

The board fears both a security failure and a public privacy controversy. Several major clients expect immediate cooperation with legitimate authorities.

**CFO**

A prolonged legal dispute could be expensive. A privacy incident or contractual dispute could create larger future liabilities.

**CTO**

Your company's records may help identify linked purchases. The usefulness and sensitivity of those records depend on your earlier technology choices.

**Marketing & PR**

Some customers expect ticketing providers to help prevent violence. Others worry that concert attendance records could expose personal relationships, identities, or political activities.

**Head of Legal**

The preservation order is binding. The broader request requires proper authorization. You can preserve records, seek clarification, and challenge disproportionate requests.

**Employee Representative**

Support and technical staff may be asked to process sensitive records under considerable pressure. Employees want clear procedures and protection from personal blame.

**Head of Sustainability**

The investigation raises questions about who bears the risks of security measures. People attending sensitive cultural or political events may be particularly concerned about data disclosure.

**Head of Artist & Venue Relations**

Promoters want reassurance that the concert can proceed safely. Some artists worry about surveillance of audiences and the possible misuse of attendance information.

## C6. Decision effects

### A. Proactive cooperation

Cost: €0.20M.

Actions:

- Preserve all records covered by the binding order.
- Offer to identify potentially relevant data categories.
- Request urgent judicial or other competent authorization for disclosure.
- Do not disclose additional customer records before authorization.

Effects:

- `security_cooperation += 2`
- `law_enforcement_data_preserved = true`
- `law_enforcement_legal_review = true`
- `law_enforcement_deadline_pending = true`

### B. Require authorization

Cost: €0.15M.

Actions:

- Preserve all records covered by the binding order.
- Require a valid disclosure order before releasing customer records.
- Prepare a documented response procedure.

Effects:

- `privacy_safeguards += 2`
- `security_cooperation += 1`
- `law_enforcement_data_preserved = true`
- `law_enforcement_legal_review = true`

### C. Limited assistance and independent review

Cost: €0.25M.

Actions:

- Preserve all records covered by the binding order.
- Provide general technical information about record categories and system capabilities without identifying customers.
- Commission independent legal review.
- Require valid authorization before disclosure.

Effects:

- `privacy_safeguards += 2`
- `security_cooperation += 1`
- `assurance_evidence += 2`
- `law_enforcement_data_preserved = true`
- `law_enforcement_legal_review = true`

### D. Contest the request

Cost: €0.10M.

Actions:

- Preserve all records covered by the binding order.
- Formally challenge the scope of the broader request.
- Seek clarification or judicial review.
- Continue complying with any binding obligations.

Effects:

- `privacy_safeguards += 2`
- `law_enforcement_request_contested = true`
- `law_enforcement_data_preserved = true`
- `law_enforcement_legal_review = true`

## C7. Shared screen: Immediate outcome

**A. Proactive cooperation**

Your company contacts investigators and seeks urgent authorization to disclose relevant records. Police welcome the rapid response, while legal staff work to limit unnecessary exposure of customer information.

**B. Require authorization**

Your company preserves the relevant records and requests a valid disclosure order. Investigators must clarify the scope of their request before customer information can be released.

**C. Limited assistance**

Your company preserves records, explains what its systems can and cannot establish, and commissions an independent legal review. Investigators receive technical assistance while customer records remain protected pending authorization.

**D. Contest**

Your company preserves the required records and challenges the broader disclosure request. The legal dispute may delay access to additional information, while the company seeks to prevent disproportionate disclosure.

## C8. Fixed external resolution

After the company decision, reveal the following to every company.

# Investigators Obtain a Narrower Order

A competent court authorizes disclosure of records connected to a defined set of ticket transactions and accounts.

The order excludes unrelated customer records.

Investigators report that the immediate threat has been contained. The investigation continues.

The authorities do not disclose which information, if any, was decisive.

### Engine rules

Every company must now comply with the valid, narrowed order.

The disclosure is limited to:

- Records within the authorized transaction and account scope.
- Categories the company actually possesses.

Set:

- `law_enforcement_request_resolved = true`
- `law_enforcement_disclosure_made = true`
- `law_enforcement_deadline_pending = false`

Do not infer that a company's choice prevented or caused the threat to be contained.

Do not claim that a company identified the suspect.

Do not claim that a company disclosed biometric information without possessing it.

## C9. Conditional disclosure consequences

Evaluate after the narrowed order.

### 1. VFI and linked-account records

Trigger:

- VFI operational.
- Identity-linked records available.

"Your company can identify relationships between verified accounts and relevant transactions. Investigators receive information within the authorized scope."

Effects:

- `security_cooperation += 1`
- `data_disclosure_exposure += 1`

### 2. Conventional ticketing

Trigger:

- No VFI identity records.

"Your company supplies relevant transaction records. Investigators receive less identity-linked information, limiting what can be established from your records alone."

Effects:

- `data_disclosure_exposure += 0`

### 3. Additional data linkage

Trigger:

- `data_linkage_capability > 0`

"Your records reveal additional connections between purchases and accounts. Legal staff restrict disclosure to the connections covered by the order."

Effects:

- `security_assurance += 1`
- `data_disclosure_exposure += 1`

### 4. Strong legal safeguards

Trigger:

- `privacy_safeguards >= 2`

"Your company documents the disclosure and excludes unrelated records. An internal review confirms that the response remained within the authorized scope."

Effects:

- Customer trust +1.

### 5. Weak documentation

Trigger:

- `assurance_evidence < 2`
- `privacy_safeguards < 2`

"Employees report uncertainty about record handling and disclosure procedures. Management orders a review of internal controls."

Effects:

- `legal_exposure += 1`
- Create `data_handling_review_required`.

These consequences are additive where applicable.

## C10. Private post-decision consequences

| Role | A. Cooperate | B. Require order | C. Review | D. Contest |
|---|---|---|---|---|
| CEO | Rapid cooperation may reassure clients while increasing scrutiny. | A legally structured response protects organizational accountability. | Independent scrutiny creates evidence of responsible decision-making. | The company accepts commercial and legal uncertainty. |
| CFO | Urgent work creates immediate costs. | Legal procedures create predictable costs. | Independent review costs more today. | A challenge may produce future legal costs. |
| CTO | Engineers must identify relevant data quickly and accurately. | Data extraction follows a defined legal scope. | Technical limitations become part of the official record. | Technical teams preserve records while the scope is challenged. |
| Marketing | Public confidence depends on the limits of cooperation. | Customers may appreciate formal safeguards. | Independent oversight may strengthen credibility. | Privacy advocates may welcome the challenge; others may question delays. |
| Legal | Urgent authorization becomes your responsibility. | Disclosure occurs under a documented legal process. | Independent review supports proportionality. | You must justify the challenge while complying with binding orders. |
| Employee Rep | Staff face time pressure handling sensitive information. | Clear procedures help protect employees. | External review may reduce individual uncertainty. | Employees may face prolonged legal and technical work. |
| Sustainability | Security benefits must be weighed against risks to affected communities. | Data minimization limits exposure. | The review considers impacts on people whose records are held. | The challenge emphasizes proportionality and privacy protections. |
| Artist Relations | Promoters may value rapid cooperation. | Partners receive reassurance about lawful handling. | Artists may welcome independent scrutiny. | Some artists support the challenge, while promoters worry about delays. |

## C11. Internal event I7

Evaluate in priority order.

**1. Extensive data linkage and weak safeguards**

Trigger:

- `data_linkage_capability > 0`
- `privacy_safeguards < 2`

"A customer organization asks why your company retains detailed links between purchases and identities. Management must explain its retention and access policies."

Effects:

- Customer trust −1.
- `data_handling_review_required = true`

**2. Strong privacy safeguards**

Trigger:

- `privacy_safeguards >= 2`

"An independent customer organization praises the company's clear explanation of what information it holds and how lawful requests are handled."

Effects:

- Customer trust +1.
- Partnership standing +1.

**3. High workforce pressure**

Trigger:

- Workforce pressure at least 2.

"Employees who handled the investigation report stress and unclear responsibilities. Their representatives request additional training and protections."

Effects:

- Labour dispute risk +1.
- `staff_escalation_review = true`

**4. Strong artist partnerships**

Trigger:

- Partnership standing at least 73.

"Several artists invite the company to participate in a discussion about audience privacy and public safety."

Effects:

- `artist_privacy_dialogue = true`
- Partnership standing +1.

**5. Otherwise**

"The investigation closes for your company without further operational consequences."

No additional effects.

## C12. Facial recognition compliance resolution

For companies with a pending Year 6 facial-entry contract, evaluate at the end of Year 7.

Authorization is possible only if all conditions are met:

1. `facial_entry_selected = true`
2. `entry_compliance_review = true`
3. `assurance_evidence >= 3`
4. `entry_remediation_required = false`
5. `entry_assistance >= 1` OR `human_assistance_capacity >= 2`
6. No unresolved integration governance obligation

If all conditions are met:

- Set `facial_entry_authorized = true`
- Set `facial_entry_operational = true`
- Set `entry_contract_active = true`
- Set `entry_contract_pending = false`
- Begin contract revenue in Year 8.
- Record that authorization applies only to the fictional, narrowly defined optional entry use case, with a nonbiometric alternative.

If any condition fails:

- Set `facial_entry_authorized = false`
- Set `facial_entry_operational = false`
- Set `entry_contract_pending = false`
- Set `entry_contract_active = false`
- Record `facial_contract_not_activated = true`
- No facial-entry contract revenue.

No automatic penalty or fine.

This is a simulation-specific compliance determination. It does not imply that these numerical thresholds establish legal compliance in real life.

## C13. Default

**B. Preserve records and require valid authorization (€0.15M).**

If unaffordable, use D (€0.10M).

If D is also unaffordable, apply a zero-cost mandatory compliance fallback:

- Preserve the records covered by the binding order.
- Disclose only the information required by the subsequent valid narrowed order.
- No optional legal services are purchased.
- Record `mandatory_compliance_fallback = true`.

Student-facing expired-decision announcement:

"Management preserves the relevant records and requests valid authorization before disclosing customer information. The company complies with the subsequent narrowed legal order."

Year 7 remains mandatory for all companies.

---

# PART D. YEAR 8 · 2034
## The Price of Partnership

Optional year. Five-minute decision.

This year introduces a commercial opportunity that could help companies with weak finances while creating new responsibilities toward artists, audiences, and employees.

## D1. Start-of-year transitions

1. Charge annual VFI operating costs if operational.
2. Recognize active Northstar contract revenue.
3. Recognize active venue-entry contract revenue.
4. Carry forward all unresolved obligations.
5. Do not activate expired facial-entry contracts.
6. Do not automatically convert commercial opportunities into revenue.

## D2. External event E8

### A New Entertainment Giant

A European entertainment group, Meridian Live, announces plans to consolidate ticketing, venue services, and artist promotion across several markets.

Meridian wants a small number of technology partners.

The company offers substantial multi-year contracts but expects preferred partners to prioritize its venues, commercial promotions, and customer programmes.

Independent artists and smaller venues worry that consolidation will reduce their bargaining power.

Meridian argues that integration will lower costs, improve coordination, and create more stable employment.

This announcement is identical for every company.

Effects:

- `market_consolidation_pressure = high`
- No automatic financial effects.

## D3. Shared screen: Pre-decision

# The Price of Partnership

Meridian Live offers your company a major commercial opportunity.

Its proposal could bring new revenue, access to venues, and long-term stability.

However, the contract includes preferred-supplier arrangements, shared promotional programmes, and restrictions that could disadvantage independent artists and venues.

Your existing partners are asking how the deal would affect them.

**What will you do?**

| Option | Strategy | Cost |
|---|---|---:|
| A | Accept Meridian's preferred partnership | €300K |
| B | Negotiate a non-exclusive partnership | €250K |
| C | Build an independent artist and venue programme | €350K |
| D | Decline expansion and strengthen existing services | €100K |

## D4. Private intelligence

**CEO**

Meridian's offer could change the company's market position. The board wants growth, but directors are concerned about becoming dependent on one powerful client.

**CFO**

The preferred partnership offers the highest potential revenue. A non-exclusive agreement offers less certainty. The independent programme requires more effort to attract customers.

**CTO**

Meridian expects integration between ticketing, promotions, and venue systems. Some data-sharing requirements may conflict with your existing architecture or privacy commitments.

**Marketing & PR**

Meridian offers access to a large audience and marketing resources. Independent artists argue that preferential placement could make smaller events harder to discover.

**Head of Legal**

The proposed exclusivity and data-sharing clauses require competition, consumer, and data protection review. Your company must understand its contractual obligations before signing.

**Employee Representative**

The contract could stabilize employment. Meridian also expects efficiency targets, potentially increasing workload or encouraging outsourcing.

**Head of Sustainability**

Large integrated events may improve logistics but concentrate commercial power. Independent venues often serve local communities with fewer resources.

**Head of Artist & Venue Relations**

Several independent artists warn that preferred placement and exclusive agreements could reduce their negotiating power. Meridian promises more predictable access to major venues.

## D5. Decision effects

### A. Preferred partnership

Cost: €0.30M.

Effects:

- `commercial_partnership_active = true`
- `commercial_dependency += 3`
- `commercial_opportunity += 3`
- `artist_autonomy -= 2`
- `partnership_standing += 1`
- `year9_contract_review_required = true`

Reported annual contract revenue beginning Year 9:

€2.00M.

The agreement includes exclusivity and integration obligations.

### B. Non-exclusive partnership

Cost: €0.25M.

Effects:

- `commercial_partnership_active = true`
- `commercial_dependency += 1`
- `commercial_opportunity += 2`
- `artist_autonomy += 1`
- `partnership_standing += 1`

Reported annual contract revenue beginning Year 9:

€1.10M.

The agreement permits continued work with independent partners.

### C. Independent programme

Cost: €0.35M.

Effects:

- `artist_partnership_active = true`
- `artist_autonomy += 3`
- `community_access += 2`
- `commercial_opportunity += 1`
- `partnership_standing += 2`

Reported annual revenue beginning Year 9:

€0.65M, conditional on programme activation.

Programme activates immediately if partnership standing is at least 72 after the decision effects.

If below 72, create `independent_programme_pending = true`, with no revenue until activated by a later explicit decision.

### D. Strengthen existing services

Cost: €0.10M.

Effects:

- `customer_support_readiness += 1`
- `technical_reliability += 1`
- `commercial_dependency` unchanged.

No new contract revenue.

## D6. Shared screen: Post-decision

**A. Preferred partnership**

Your company signs Meridian's preferred partnership agreement. The deal offers substantial growth and more predictable commercial demand, but restricts some relationships with independent venues and artists.

**B. Non-exclusive partnership**

Your company negotiates a smaller, non-exclusive agreement. Meridian gains access to your services while the company retains the ability to work with other promoters and artists.

**C. Independent programme**

Your company invests in a programme for independent artists and venues. The initiative prioritizes flexible contracts and access for smaller organizers, with more uncertain commercial returns.

If activation is pending, append:

"The programme has attracted initial interest but has not yet secured enough participating partners to begin generating revenue."

**D. Strengthen services**

Your company declines the expansion offers and invests in existing services. Customers and current partners benefit from improvements, while the company passes up immediate growth opportunities.

## D7. Private post-decision consequences

| Role | A. Preferred | B. Non-exclusive | C. Independent | D. Services |
|---|---|---|---|---|
| CEO | Growth increases alongside dependence on Meridian. | The company balances expansion and strategic flexibility. | Growth is slower and depends on independent partners. | The company protects its existing position. |
| CFO | Revenue potential is high, with concentrated contract exposure. | Revenue is lower but dependence is limited. | Returns are less certain and depend on programme activation. | Cash expenditure is modest. |
| CTO | Integration requirements may constrain future architecture. | Integration is narrower and more manageable. | Multiple smaller partners create coordination demands. | Existing infrastructure receives attention. |
| Marketing | Meridian provides access to a large audience. | Promotional reach expands without full exclusivity. | Independent artists gain visibility. | Existing customer relationships remain central. |
| Legal | Exclusivity and data-sharing obligations require careful oversight. | Contract terms preserve more flexibility. | Numerous smaller agreements require consistent protections. | No major new commercial obligations arise. |
| Employee Rep | Stable contracts may support jobs, but efficiency pressure increases. | Growth may support employment without full dependence. | Local partnerships may create diverse work opportunities. | Existing working arrangements continue. |
| Sustainability | Consolidation may improve coordination while reducing local autonomy. | The company retains flexibility across different partners. | Smaller venues gain additional support. | Existing sustainability commitments continue. |
| Artist Relations | Major promoters gain influence over commercial priorities. | Independent partnerships remain possible. | Artists and smaller venues gain bargaining opportunities. | Existing partners retain current arrangements. |

## D8. Conditional consequences

### Preferred partnership and high commercial dependency

If `commercial_dependency >= 3`:

"Several independent partners express concern that Meridian may receive preferential treatment. They request assurances about access and contract terms."

Effects:

- `stakeholder_conflict += 1`
- `partnership_conditions_disputed = true`

### Preferred partnership and strong financial pressure

If `financial_pressure >= 1`:

"Management argues that Meridian's predictable revenue could protect employment and stabilize operations."

Effects:

- Workforce concerns −1, minimum zero.
- No automatic cash increase.

### Non-exclusive partnership with strong artist relationships

If partnership standing is at least 73:

"Several existing artists welcome the decision to retain non-exclusive relationships."

Effects:

- Partnership standing +1.
- Customer trust +1.

### Independent programme with prior regional opportunities

If any of the following is true:

- `independent_festival_opportunity`
- `artist_collective_opportunity`
- `boycott_alternative_supplier_opportunity`

Then:

"Artists and venues that previously approached your company become founding partners in the new programme."

Effects:

- Activate the independent programme.
- `independent_programme_pending = false`
- Partnership standing +1.

The €0.65M annual reported revenue begins in Year 9.

### Service improvements with outstanding customer obligations

If choice D and any of the following are active:

- `customer_compensation_review`
- `review_remediation_required`
- `data_handling_review_required`

Then:

"Management uses the service improvement programme to complete an outstanding customer or data-handling review."

Resolve one obligation in this priority order:

1. Customer compensation review.
2. Review remediation.
3. Data-handling review.

Customer trust +1.

No other obligations are automatically resolved.

## D9. Internal event I8

Evaluate in priority order.

**1. Preferred partnership with high dependency**

Trigger:

- Choice A.
- Commercial dependency at least 3.

"Meridian requests preferential access to your company's product development resources. An independent client complains that its requests are being delayed."

Effects:

- `partnership_conditions_disputed = true`
- Partnership standing −1.
- `year9_contract_review_required = true`

**2. Independent programme active**

Trigger:

- `artist_partnership_active = true`
- `independent_programme_pending = false`

"Several independent venues report that the programme has made it easier to reach audiences without signing exclusive contracts."

Effects:

- Partnership standing +1.
- Customer trust +1.

**3. Non-exclusive partnership with strong reliability**

Trigger:

- Choice B.
- Technical reliability at least 70.

"Meridian reports successful integration with your platform while existing clients continue receiving service."

Effects:

- Partnership standing +1.
- Commercial opportunity +1.

**4. High workforce pressure**

Trigger:

- Workforce pressure at least 2.

"Employees warn that commercial expansion has increased workload without corresponding staffing changes."

Effects:

- Workforce conditions −1.
- Labour dispute risk +1.

**5. Otherwise**

"The company completes the commercial review without a major incident."

No additional effects.

## D10. Default

**D. Decline expansion and strengthen existing services (€0.10M).**

If unaffordable, apply a zero-cost maintenance fallback:

- No new investment.
- No new contract.
- No additional state changes.

Skipped-year announcement:

"Management postpones major commercial expansion and concentrates on existing customer and partner services. The company retains its current contracts and strategic flexibility."

---

# PART E. YEAR 9 HANDOFF

At the beginning of Year 9:

1. Charge annual VFI operating costs if operational.
2. Recognize active Northstar contract revenue.
3. Recognize active venue-entry contract revenue.
4. Recognize active Meridian contract revenue.
5. Recognize active independent programme revenue.
6. Preserve unresolved legal, technical, customer, workforce, and contract obligations.
7. Preserve all company decisions and individual preferences.
8. Preserve the Year 5 checkpoint snapshot.

## E1. Year 9 contract review

If `year9_contract_review_required = true`, the company must address the consequences of commercial dependence or contested partnership conditions during Year 9.

No automatic contract termination.

## E2. Unresolved biometric obligations

If facial recognition was not authorized in Year 7:

- It remains non-operational.
- No biometric contract revenue.
- No biometric data collection.
- A future decision must explicitly reopen the authorization process.

## E3. Unresolved law enforcement obligations

The Year 7 request is resolved after the narrowed order.

No open disclosure request remains.

Any separate data-handling or employee obligations carry forward.

## E4. Independent programme

If the programme is active, recognize its annual revenue.

If pending, it generates no revenue until a later explicit activation.

## E5. Commercial dependence

Preserve commercial dependency and artist autonomy scores.

These must influence Year 9 strategic choices.

---

# PART F. VALIDATION AND ACCEPTANCE TESTS

Test all combinations of Years 6–8 decisions against representative reachable company states from Years 1–5.

There are 64 ordinary decision combinations across Years 6–8.

Also test skipped years, expired decisions, financial fallbacks, and executive-power interactions.

Verify:

1. Year 6 and Year 8 can be skipped.
2. Year 7 remains mandatory.
3. All active students submit individual preferences.
4. No additional written reflections are required.
5. Every company receives the same fixed external events.
6. Internal events depend on actual company state.
7. No company can spend more cash than available.
8. Every cash effect is applied once.
9. VFI recurring costs are charged once per operational year.
10. Contract revenue is recognized only after activation.
11. Facial recognition is never operational merely because option A was selected.
12. Facial recognition never creates biometric records before authorization.
13. Companies without VFI can use conventional entry technologies.
14. Mandatory VFI suspension persists until explicitly reversed.
15. Year 7 police requests use only data categories the company possesses.
16. All Year 7 choices comply with the binding preservation order.
17. No additional customer data is disclosed before valid authorization.
18. The narrowed order is applied consistently.
19. No company is credited with preventing the threat without evidence.
20. No company is automatically blamed for the security threat.
21. Data minimization and legal safeguards produce conditional consequences.
22. Year 7 facial compliance evaluation produces exactly one activation or non-activation result.
23. No facial contract revenue is recognized before activation.
24. Meridian partnership revenue begins no earlier than Year 9.
25. Independent programme revenue requires activation.
26. Non-exclusive partnerships do not create exclusivity obligations.
27. Commercial dependency affects later company options.
28. Unresolved obligations carry into Year 9.
29. No event invents layoffs, fines, lawsuits, or security incidents without a defined trigger.
30. All student-facing narratives reflect actual company decisions and resolved outcomes.
31. Replaying a year never duplicates effects.
32. The Year 5 checkpoint snapshot remains unchanged.
33. Company and individual histories retain all decisions and consequences.
34. No universal ethics score is introduced.
35. Companies with different technology strategies retain genuinely different capabilities, constraints, and commercial opportunities.

## Final implementation instruction

Years 6–8 must be implemented as a continuation of the existing simulation.

Use the established application architecture and role system.

All external events, conditional effects, private messages, financial transitions, and defaults in this document are authoritative.

Preserve the human consequences and the uncertainty of ethical decision-making.

Do not introduce random events or unexplained state changes.

END OF YEARS 6–8 SPECIFICATION.
