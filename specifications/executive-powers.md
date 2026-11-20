
# FAIRPASS: EXECUTIVE POWERS
## Complete cross-year implementation specification
### Authoritative supplement for Years 1–10

This specification defines how all eight executive powers work, including activation, conflicts, costs, immediate consequences, delayed effects, private messages, and final reporting.

Apply these rules consistently across all ten years.

Do not replace the existing year-specific decisions, narratives, or financial rules.

---

# 1. CORE PRINCIPLES

Every executive has one special power.

Each student may activate their power only once during the entire ten-year simulation.

Powers are optional.

A power can be used in any active decision year, including Years 1, 5, 7, 9, and 10.

Powers are unavailable during facilitator-skipped years.

A power already used cannot be activated again.

Powers must produce real consequences.

Using a power must never be treated as automatically ethical or unethical.

The consequences depend on:
- The power activated.
- The company's actual circumstances.
- The decision under discussion.
- Other powers activated.
- Available financial resources.
- Existing contractual and legal obligations.

A power cannot create technology, money, contracts, or legal authority the company does not possess.

---

# 2. POWER ACTIVATION INTERFACE

Each student's private app displays:

## Your Executive Power

[Role-specific power name]

[Short description of the power]

Status:
- Available
- Activated
- Used

Button:

"Activate my executive power"

Before activation, display a confirmation:

"You may use this power only once during the ten-year simulation. Activating it may affect your company's decision, finances, employees, or commercial relationships."

Buttons:

- Confirm activation
- Cancel

After confirmation, the power is committed to the current decision round.

It cannot be withdrawn.

The company screen receives an announcement.

The student's private screen displays the immediate effect.

The power's final outcome is displayed after the company decision resolves.

---

# 3. ACTIVATION WINDOW

A power may be activated after the student receives private intelligence and before the company decision is locked.

The activation window closes when:

- The company decision is finalized.
- The CEO successfully overrides and locks the decision.
- The decision timer expires.
- The facilitator advances the company.

Students must submit their personal recommendation before activating their power.

The power may support or oppose that recommendation.

Record both independently.

A student cannot activate a power after learning the final company outcome.

---

# 4. ROLE POWERS

## 4.1 CEO
### Executive Override

**Power:** Select and immediately lock the company's decision.

The CEO may choose any legally and financially feasible option.

The CEO's choice replaces the team's proposed decision.

Other executives' recommendations remain recorded.

The decision resolves using the normal scenario rules.

### Immediate effects

- Set `decision_source = ceo_override`.
- Set `ceo_override_used = true`.
- Lock the company decision.
- Close the power activation window.
- Record any disagreement between individual recommendations and the final decision.

### Consequences

If at least half of the other active executives recommended a different option:

- Workforce conditions −1.
- Record `executive_governance_conflict = true`.

Otherwise:

- No additional indicator change.

### Company announcement

"The CEO exercises executive authority and makes the final decision on behalf of the company."

Display the selected option.

### CEO private consequence

"You exercised your executive authority. The decision is final, and you are accountable for its consequences."

If governance conflict occurred, append:

"Several executives disagreed with your choice. The decision has created tension within the leadership team."

---

## 4.2 CFO
### Spending Freeze

**Power:** Block one proposed expenditure.

The CFO may freeze the expenditure associated with a specific decision option.

The freeze applies to the current year only.

It cannot cancel legally binding payments, previously committed expenses, or mandatory operating obligations.

### Activation

The CFO selects one option to block.

The option must have a positive discretionary cost.

### Immediate effects

- Mark the selected option `blocked_by_cfo`.
- The company cannot select it.
- Record `cfo_spending_freeze_used = true`.

### Consequences

- Financial pressure −1, minimum zero.
- Partnership standing −1 if the blocked option concerned a pending external contract.
- No cash is deducted for the blocked option.

### Company announcement

"The CFO freezes expenditure on [option]. The company must select another feasible course of action."

### CFO private consequence

"You prevented the proposed expenditure. The company retains those funds, but the blocked opportunity may have commercial or operational consequences."

---

## 4.3 CTO
### Technical Veto

**Power:** Block one technically dependent proposal.

The CTO may veto a decision option involving:

- New technical deployment.
- Major system integration.
- Automated decision-making.
- Biometric processing.
- Significant changes to existing technology.

The veto must concern an actual technical component.

It cannot block an unrelated financial, employment, or reporting decision.

### Immediate effects

- Mark the selected option `blocked_by_cto`.
- Record `cto_technical_veto_used = true`.
- The company must choose another feasible option.

### Consequences

- Technical reliability +1.
- Delivery progress −1, minimum zero, if the veto delays an active development project.
- Partnership standing −1 if a committed client timetable is affected.

### Company announcement

"The CTO invokes a technical veto, citing unresolved implementation or reliability concerns."

Display the blocked option.

### CTO private consequence

"You prevented a technical commitment that you considered insufficiently prepared. The company must find an alternative, and delivery may be delayed."

---

## 4.4 Marketing & PR
### Emergency Public Campaign

**Power:** Launch a company-wide public communications campaign.

The campaign costs €150K.

It may support the company's decision, explain safeguards, or respond to public criticism.

It cannot erase documented harms, complaints, or legal obligations.

### Activation

Available only if the company can afford €0.15M.

### Immediate effects

- Cash −0.15M.
- Record `marketing_campaign_used = true`.
- Record the current year and company decision.

### Conditional consequences

If customer trust is below 70:

- Customer trust +1.

If customer trust is at least 70:

- Partnership standing +1.

If the company has unresolved customer complaints:

- The campaign also generates public requests for evidence of remediation.
- Record `communications_scrutiny = true`.

### Company announcement

"Marketing launches an emergency public campaign explaining the company's position and commitments."

### Marketing private consequence

"You have shaped the company's public response. Stakeholders will judge its credibility against the company's actual conduct."

---

## 4.5 Head of Legal
### Formal Legal Review

**Power:** Require a formal review before the company decision takes effect.

Cost: €100K.

The review may identify contractual, data protection, employment, or regulatory obligations.

It does not automatically authorize a legally restricted activity.

### Immediate effects

- Cash −0.10M.
- Assurance evidence +1.
- Record `legal_review_used = true`.
- Record `legal_review_current_year = true`.

### Conditional consequences

If an unresolved legal or governance obligation exists:

- Identify the highest-priority relevant obligation.
- Record it as formally reviewed.
- Do not automatically resolve it.

If the proposed option requires a legal authorization the company does not possess:

- The option remains conditional or unavailable according to the scenario's existing rules.

### Company announcement

"The Head of Legal requires a formal review before implementation. The company receives a documented assessment of its obligations."

### Legal private consequence

"You required the company to examine its legal responsibilities. The review creates evidence of due diligence and may identify additional work."

---

## 4.6 Employee Representative
### Collective Work Stoppage

**Power:** Call a temporary work stoppage.

The action represents an organized collective response by employees.

It does not automatically reverse the company decision.

### Immediate effects

- Cash −0.20M, limited by available cash.
- Workforce pressure +1.
- Labour dispute risk +1.
- Record `employee_work_stoppage_used = true`.
- Record `work_stoppage_current_year = true`.

If the company cannot cover the €0.20M disruption cost:

- Deduct available cash.
- Record the unpaid disruption cost as an outstanding operational liability.
- Set financial distress true.

### Conditional consequences

If workforce conditions are below 70:

- Partnership standing −1.
- Create `workforce_negotiation_required = true`.

If workforce conditions are at least 70:

- Create `workforce_consultation_required = true`.

### Company announcement

"Employees begin a temporary work stoppage following the Employee Representative's intervention. Operations are disrupted, and management faces demands for consultation."

### Employee Representative private consequence

"You have used collective action to bring employee concerns into the decision. The company faces operational costs, and negotiations remain necessary."

---

## 4.7 Head of Sustainability
### Mandatory Impact Assessment

**Power:** Require a formal environmental and social impact assessment.

Cost: €100K.

The assessment examines relevant effects on:

- Accessibility.
- Environmental resource use.
- Workers.
- Customers.
- Local communities.
- Existing sustainability commitments.

### Immediate effects

- Cash −0.10M.
- Assurance evidence +1.
- Record `sustainability_assessment_used = true`.

### Conditional consequences

If the proposed decision introduces a new technology or infrastructure:

- Record `sustainability_followup_required = true`.

If the proposed decision affects customer access or working conditions:

- Record the relevant stakeholder impact in the assessment.

The assessment does not automatically change the company's decision.

### Company announcement

"The Head of Sustainability commissions a formal impact assessment. Management must consider the findings during implementation."

### Sustainability private consequence

"You required the company to document environmental and social consequences. The assessment may reveal obligations that require future action."

---

## 4.8 Head of Artist & Venue Relations
### Material Change Clause

**Power:** Invoke a material change clause in the company's largest active client contract.

The clause allows the company to request renegotiation when major changes affect contractual obligations.

It does not automatically cancel the contract or reverse a company decision.

### Activation requirements

- At least one active major client contract.
- A documented material change affecting delivery, access, technology, or contractual responsibilities.

If no qualifying contract exists, the power remains available.

### Immediate effects

- Cash −0.10M in legal and negotiation expenditure.
- Partnership standing −1.
- Record `material_change_clause_used = true`.
- Create `major_contract_renegotiation_pending = true`.

### Conditional consequences

If the company has strong partnership standing, at least 73:

- The client agrees to discuss revised terms.
- Record `contract_renegotiation_open = true`.

Otherwise:

- The client formally disputes the invocation.
- Record `contract_dispute_pending = true`.

No contract is automatically terminated.

### Company announcement

"The Head of Artist & Venue Relations invokes a material change clause. The company's largest client is asked to renegotiate contractual obligations."

### Artist Relations private consequence

"You have forced a contractual discussion about the company's obligations. The outcome depends on the client relationship and the strength of the company's position."

---

# 5. CONFLICTS BETWEEN POWERS

Multiple students may activate powers during the same decision round.

Resolve powers in the following order:

1. CFO spending freeze.
2. CTO technical veto.
3. Head of Legal review.
4. Sustainability impact assessment.
5. Artist & Venue Relations material change clause.
6. Employee Representative work stoppage.
7. Marketing public campaign.
8. CEO executive override.

This order is authoritative.

## 5.1 CEO override

The CEO may override the team's preferred option.

The CEO cannot select an option blocked by a valid CFO freeze or CTO veto.

The CEO cannot override legal impossibility or financial infeasibility.

Once activated, the CEO's choice locks the company decision.

## 5.2 Multiple blocking powers

The CFO and CTO may block different options.

Both blocks remain effective for the current decision.

If every affordable option is blocked:

- Apply the scenario's zero-cost continuity fallback.
- If no such fallback exists, record `decision_deferred_due_to_executive_conflict`.
- Do not create an unauthorized expenditure or capability.
- Continue the scenario using the no-new-commitment outcome.

## 5.3 Advisory and disruptive powers

Legal, Sustainability, Marketing, Employee Representative, and Artist Relations powers do not automatically change the selected company option.

Their costs, reviews, disputes, and other consequences apply independently.

## 5.4 Conflicting commitments

A power cannot cancel:

- A binding legal obligation.
- An already incurred expense.
- A previously awarded contract.
- A completed historical event.
- A required customer disclosure.
- A facilitator checkpoint.

---

# 6. FINANCIAL RULES

All power-related costs use the existing financial ledger.

Each power has a unique effect ID.

Do not charge the same power twice.

## 6.1 Spending powers

Marketing, Legal, Sustainability, and Artist Relations powers require sufficient cash before activation.

If unaffordable, disable activation and explain why.

Do not consume the power.

## 6.2 Work stoppage

The Employee Representative's work stoppage can create an outstanding operational liability if cash is insufficient.

Record the unpaid amount.

Do not allow negative cash.

## 6.3 Decision affordability

After resolving power costs, recalculate which decision options remain affordable.

A previously affordable option may become unavailable.

If the company's proposed choice becomes unaffordable, the team must choose another feasible option before the deadline.

If the deadline expires, apply the year-specific financial fallback.

---

# 7. COMPANY INTERFACE

When a power is activated, display a short announcement in the shared company interface.

Examples:

- "The CFO has frozen expenditure on Option A."
- "The CTO has vetoed Option B."
- "The Head of Legal has required a formal review."
- "The Employee Representative has called a work stoppage."
- "The CEO has exercised executive authority."

Display active interventions beside the decision options.

Blocked options must be clearly identified and unavailable for selection.

Do not reveal private role intelligence.

After the decision resolves, show:

- Powers activated.
- Immediate organizational consequences.
- Actual final decision.
- Relevant financial costs.
- New obligations.
- Any changes to company indicators.

---

# 8. INDIVIDUAL APP

Every student's private app must show:

- Their role.
- Their confidential mission.
- Their power.
- Whether the power remains available.
- Their current-year private intelligence.
- Their personal recommendation.
- Any power they activated.
- The result of that power.
- The actual company decision.
- Their private post-decision consequence.

A student who has used their power sees:

"Executive power used in Year [year]."

The activation control remains disabled for the rest of the simulation.

---

# 9. DECISION RECORDS

For every activated power, record:

- Session ID.
- Company ID.
- Student ID.
- Role.
- Year.
- Power type.
- Activation timestamp.
- Target option, if applicable.
- Company state at activation.
- Immediate effect.
- Financial cost.
- Decision outcome.
- Conditional consequences.
- Outstanding obligations created.
- Whether the power affected the final company choice.

Also preserve all individual recommendations.

---

# 10. YEAR-SPECIFIC INTERACTIONS

## Year 1

Powers can affect initial procurement.

A CFO freeze or CTO veto may block a technology strategy.

The CEO can override the team's choice within the remaining feasible options.

Do not create VFI capability before the established development timeline.

## Year 2

Powers can affect testing priorities.

Technical vetoes may block acceleration.

Legal or Sustainability reviews add evidence but do not automatically complete the selected testing programme.

## Year 3

Powers can affect the Northstar bid.

A material change clause cannot be invoked against a contract that has not yet been awarded.

CEO override cannot force Northstar to award a contract.

Contract outcomes continue to use actual readiness.

## Year 4

Powers can affect customer-service investment.

A spending freeze may block an expensive feature.

No power automatically activates VFI.

## Year 5

Powers can affect the boycott response.

A public campaign may influence trust but cannot erase customer exclusions.

A work stoppage may increase pressure for better employee procedures.

Legal review may document weaknesses.

The Year 5 checkpoint remains mandatory.

## Year 6

Powers can affect the venue-entry proposal.

A CTO veto may block facial recognition.

Legal review does not authorize biometric processing.

A Sustainability assessment may create additional infrastructure obligations.

## Year 7

Powers cannot override binding preservation or disclosure orders.

A legal review may improve documentation and scrutiny.

A CTO veto cannot block mandatory legal compliance.

A CEO override cannot authorize unlawful disclosure.

## Year 8

Powers can affect commercial partnership choices.

Artist Relations may invoke a material change clause against an existing qualifying contract.

A CFO freeze may block a major expansion investment.

## Year 9

Powers can affect the company's strategic direction.

A work stoppage does not automatically prevent restructuring.

A CEO override cannot erase previously incurred obligations.

## Year 10

Powers can affect reporting strategy.

Legal review and Sustainability assessment may create additional evidence.

Marketing cannot falsify the responsibility report.

The CEO cannot override legally required disclosures.

All power effects appear in the final individual report.

---

# 11. DELAYED OBLIGATIONS

Power-created obligations carry forward until explicitly resolved.

Examples:

- Workforce negotiation.
- Contract renegotiation.
- Contract dispute.
- Sustainability follow-up.
- Communications scrutiny.
- Legal review findings.

A later decision may resolve an obligation only when its rules explicitly permit resolution.

Unresolved obligations appear in the Year 5 or Year 10 checkpoint as applicable.

Do not silently clear them.

---

# 12. FINAL REPORT

Each student's report must show:

1. Which executive power they possessed.
2. Whether they used it.
3. When they used it.
4. What they attempted to influence.
5. What actually happened.
6. Whether the company's final decision changed.
7. Immediate consequences.
8. Delayed consequences.
9. Outstanding obligations.
10. Relevant disagreements between their recommendation and the company decision.

Students who never used their power should see:

"You retained your executive power throughout the simulation."

Do not imply that unused power represents failure.

---

# 13. ACCEPTANCE TESTS

Verify:

1. Every student has exactly one executive power.
2. Each power can be activated only once.
3. Powers are unavailable during skipped years.
4. Recommendations are recorded before activation.
5. No power can be activated after decision lock.
6. CEO override locks a feasible option.
7. CEO override cannot bypass a valid veto.
8. CFO freeze blocks only discretionary expenditure.
9. CTO veto blocks only technically dependent proposals.
10. Legal review cannot authorize unlawful processing.
11. Marketing campaigns cannot erase documented harms.
12. Employee work stoppages create actual disruption.
13. Sustainability assessments create evidence and relevant obligations.
14. Material change clauses require a qualifying active contract.
15. Multiple powers resolve in deterministic order.
16. Power costs are charged once.
17. Unaffordable spending powers cannot activate.
18. Work stoppage liabilities do not create negative cash.
19. Power costs affect subsequent decision affordability.
20. Blocked options cannot be selected.
21. Financial fallbacks work when options become unavailable.
22. Powers cannot create unavailable technical capabilities.
23. Powers cannot override binding legal obligations.
24. Power consequences use actual company state.
25. Every activation appears on the company screen.
26. Private intelligence remains private.
27. Every power activation is preserved in the student report.
28. Power-related obligations persist until resolved.
29. Power use does not create a universal ethical score.
30. The simulation remains completable even when multiple powers conflict.

END OF EXECUTIVE POWERS SPECIFICATION.
