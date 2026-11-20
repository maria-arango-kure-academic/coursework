
# FAIRPASS: THE VFI PLATFORM SHIFT
## Authoritative builder brief
### Year 5 commercial, Year 6 replacement, and Years 7–10 continuity

Implement this as an update to the existing FairPass simulation.

The central theme is POWER: who controls the infrastructure, who can change the rules, who benefits from the data, and who can afford to leave.

This specification supersedes the previous Year 6 "Beyond the Ticket" scenario and all previous FacePass product-offer mechanics.

Preserve Years 1–5 decisions, financial history, role intelligence, executive powers, stakeholder outcomes, and checkpoint records.

Do not reset company histories.

---

# 1. THE CENTRAL CHANGE

VFI is a fictional technology supplier.

Verified Fan Identity is its original identity verification product.

FacePass is the next generation of VFI's platform.

In 2032, VFI announces that its legacy verification infrastructure will be retired and replaced by a new platform incorporating facial-recognition capabilities.

Existing VFI customers cannot simply remain on the original product indefinitely.

They must decide whether to accept the migration, negotiate different terms, resist the change, or leave the supplier.

VFI can impose commercial and technical changes through its platform and contracts. It cannot independently authorize biometric processing by its customers.

A company may be contractually committed to a platform containing biometric functionality while remaining legally unable or unwilling to activate that functionality.

That distinction is essential.

Companies that built their own verification technology are unaffected by VFI's migration requirement. They can nevertheless develop competing biometric products and capture the associated commercial value.

Companies that never adopted verification can enter the market or position themselves as an alternative.

The same external shock produces different choices according to earlier company decisions.

---

# 2. YEAR 1 SUPPLIER MODEL

Use the following authoritative procurement interpretation.

| Year 1 choice | Technology ownership | VFI contract |
|---|---|---|
| A. Build in-house | Company-owned verification | No |
| B. License VFI | VFI-controlled core infrastructure | Yes |
| C. Hybrid with VFI | Company-owned services using VFI verification | Yes |
| D. Wait | Conventional ticketing | No |

Keep the existing Year 1 investment costs:

- Build: €2.8M
- License: €0.6M
- Hybrid: €1.6M
- Wait: €0.15M

Keep established recurring operating costs.

Initialize:

`identity_technology_provider = in_house | vfi | hybrid_vfi | none`

`vfi_supplier_contract = true | false`

`facepass_status = none`

Migrate legacy procurement states without repeating transactions.

---

# 3. YEAR 5 CHECKPOINT: SECOND COMMERCIAL

The Year 5 checkpoint remains synchronized and facilitator-controlled.

After displaying the five-year industry results, the facilitator plays the second VFI commercial.

The commercial is approximately 60 seconds long.

## Advertiser

VFI.

## Campaign

Smile and Pass.

## Commercial narrative

The advertisement begins by celebrating five years of verified ticketing.

It presents VFI as an established technology company that has helped transform live entertainment.

It then introduces the next generation of the VFI platform.

A concertgoer approaches a venue gate.

A camera identifies them.

The gate opens.

The fan walks inside without presenting a ticket or phone.

The advertisement emphasizes convenience, speed, security, and connected experiences.

Closing voiceover:

"Five years ago, we changed how fans get tickets.

Now we're changing how they experience everything beyond them.

The next generation of Verified Fan Identity.

VFI. Smile and Pass."

On-screen closing:

VFI
SMILE AND PASS
THE NEXT GENERATION IS HERE

The advertisement does not mention the Year 5 boycott or Alex Morgan.

The contrast with the students' recent experience is intentional.

## Immediate post-commercial announcement

Display:

# VFI Announces Mandatory Platform Migration

VFI has announced that its original verification infrastructure will be retired.

Existing customers will be migrated to the company's next-generation platform, which includes FacePass facial-recognition capabilities.

VFI says the upgrade will improve security, reduce entry times, and support new commercial services.

Customer companies have been given twelve months to transition.

VFI has not announced a general exemption for existing licensees.

The announcement is the same for every company.

Then release Year 6.

---

# 4. YEAR 6 · 2032
## Smile and Pass: Who Gets to Leave?

Year 6 remains optional for workshop pacing.

The fixed platform announcement occurs even when the year is skipped.

The decision options are determined by the company's Year 1 procurement strategy.

All companies receive the same external event.

Every company receives four options, A–D.

The options and consequences differ according to supplier relationship.

---

# 5. SHARED YEAR 6 INTRODUCTION

Display to every company:

# Smile and Pass

VFI has announced the retirement of its original verification platform.

The replacement includes facial-recognition entry technology and new commercial services.

Existing VFI customers face migration requirements, contract negotiations, and possible switching costs.

Independent ticketing providers are evaluating whether to compete with the new platform or offer alternatives.

Your company's earlier technology decisions now shape the options available.

**What will your company do?**

---

# 6. BRANCH A: LICENSED VFI COMPANIES

Applies when:

`identity_technology_provider = vfi`

These companies depend heavily on VFI's infrastructure.

## Decision options

### A. Accept the migration

Cost: €0.35M.

- Accept the next-generation platform.
- Continue the VFI supplier relationship.
- Gain access to FacePass capabilities.
- Increase supplier dependence.
- Biometric activation remains subject to authorization.

Effects:

- `facepass_status = pending`
- `supplier_dependence += 2`
- `commercial_opportunity += 2`
- `biometric_exposure += 2`
- `facepass_migration_accepted = true`

### B. Negotiate an exemption

Cost: €0.20M.

- Seek continued access to nonbiometric verification.
- Request revised licensing terms.
- Maintain the supplier relationship during negotiations.

Effects:

- `vfi_exemption_requested = true`
- `supplier_negotiation_pending = true`
- `assurance_evidence += 1`

Resolution:

If partnership standing is at least 72 OR assurance evidence is at least 3:

- VFI grants a two-year nonbiometric transition agreement.
- `vfi_exemption_granted = true`
- `facepass_status = rejected`
- Existing verification remains operational.

Otherwise:

- VFI refuses the exemption.
- `vfi_exemption_denied = true`
- Existing service remains available only during the twelve-month transition.
- Create `vfi_transition_deadline = year7`.

### C. Exit VFI

Base cost: €1.20M.

Additional switching cost:

`0.10M × max(0, supplier_dependence - 2)`

Total cost is calculated before the decision.

- Terminate the VFI supplier relationship.
- Migrate to independent verification infrastructure.
- Assume responsibility for technical development and continuity.

Effects if affordable:

- `vfi_supplier_contract = false`
- `identity_technology_provider = independent_migrated`
- `supplier_dependence = 0`
- `facepass_status = rejected`
- `migration_in_progress = true`
- `technical_reliability -= 1`
- `commercial_dependency = max(0, commercial_dependency - 1)`

Independent verification becomes operational at the beginning of Year 7 if the migration obligation is completed.

Do not automatically create facial-recognition capability.

### D. Resist the change

Cost: €0.10M.

- Refuse the upgrade.
- Continue using existing infrastructure during the transition.
- Formally challenge the supplier's unilateral change.

Effects:

- `vfi_supplier_contract = true`
- `facepass_status = rejected`
- `supplier_dispute_pending = true`
- `vfi_transition_deadline = year7`
- `partnership_standing -= 1`

VFI does not immediately shut down the service.

The unresolved dispute must be addressed in Year 7.

---

# 7. BRANCH B: HYBRID VFI COMPANIES

Applies when:

`identity_technology_provider = hybrid_vfi`

These companies own customer-facing components but depend on VFI's verification infrastructure.

## Decision options

### A. Accept the migration

Cost: €0.45M.

Effects:

- `facepass_status = pending`
- `supplier_dependence += 2`
- `commercial_opportunity += 2`
- `biometric_exposure += 2`
- `facepass_migration_accepted = true`

### B. Negotiate an exemption

Cost: €0.15M.

Effects:

- `vfi_exemption_requested = true`
- `supplier_negotiation_pending = true`
- `assurance_evidence += 1`

Resolution:

If internal capability is at least 1 OR partnership standing is at least 72:

- VFI grants a two-year nonbiometric transition agreement.
- `vfi_exemption_granted = true`
- `facepass_status = rejected`

Otherwise:

- Exemption denied.
- Transition deadline remains Year 7.

### C. Exit VFI

Base cost: €0.75M.

Additional switching cost:

`0.10M × max(0, supplier_dependence - 2)`

Effects if affordable:

- `vfi_supplier_contract = false`
- `identity_technology_provider = independent_migrated`
- `supplier_dependence = 0`
- `facepass_status = rejected`
- `migration_in_progress = true`
- `technical_reliability -= 1`

Independent verification becomes operational in Year 7 following successful migration.

### D. Resist the change

Cost: €0.10M.

Effects:

- `supplier_dispute_pending = true`
- `facepass_status = rejected`
- `vfi_transition_deadline = year7`
- `partnership_standing -= 1`

Existing verification continues temporarily.

---

# 8. BRANCH C: BUILT IN-HOUSE

Applies when:

`identity_technology_provider = in_house`

These companies have no VFI supplier contract.

They own their verification infrastructure.

They may now compete directly with VFI.

## Decision options

### A. Build proprietary biometric entry

Cost: €0.90M.

The company develops its own facial-recognition entry system.

It retains ownership of the technology and commercial infrastructure.

Potential value includes:

- Venue entry contracts.
- Licensing to other ticketing providers.
- Integrated customer services.
- Identity-linked commercial products, where lawful.

Effects:

- `facial_entry_selected = true`
- `facial_entry_provider = in_house`
- `proprietary_biometric_development = true`
- `biometric_exposure += 2`
- `technical_independence += 2`
- `commercial_opportunity += 3`
- `entry_compliance_review = true`

No immediate biometric deployment.

No automatic legal authorization.

Potential annual reported revenue from Year 8 if activated:

€1.60M.

This is deliberately higher than the standard licensed venue-entry opportunity because the company captures more of the product's commercial value.

### B. License an independent biometric supplier

Cost: €0.60M.

- Integrate an external biometric entry product.
- Preserve the existing in-house ticket verification system.
- Create a new supplier relationship.

Effects:

- `facial_entry_selected = true`
- `facial_entry_provider = independent_supplier`
- `supplier_dependence += 1`
- `commercial_opportunity += 2`
- `entry_compliance_review = true`

Potential annual reported revenue from Year 8 if activated:

€1.10M.

### C. Develop nonbiometric smart entry

Cost: €0.40M.

Effects:

- `smart_entry_selected = true`
- `entry_efficiency += 2`
- `entry_assistance += 1`
- `partnership_standing += 1`
- `entry_contract_active = true`

Annual reported revenue from Year 7:

€0.85M.

### D. Preserve existing services

Cost: €0.10M.

Effects:

- `customer_support_readiness += 1`
- `technical_reliability += 1`
- No new entry contract.

---

# 9. BRANCH D: NEVER ADOPTED VERIFICATION

Applies when:

`identity_technology_provider = none`

These companies have no identity-verification infrastructure or VFI contract.

## Decision options

### A. Enter the biometric market

Cost: €1.20M.

- Build or procure a new independent biometric entry system.
- Develop the necessary supporting infrastructure.
- Enter a new technology market.

Effects:

- `facial_entry_selected = true`
- `facial_entry_provider = independent_new`
- `biometric_exposure += 2`
- `commercial_opportunity += 3`
- `entry_compliance_review = true`

No immediate activation.

Potential annual reported revenue from Year 8 if authorized:

€1.20M.

### B. Build nonbiometric smart entry

Cost: €0.40M.

Effects:

- `smart_entry_selected = true`
- `entry_efficiency += 2`
- `entry_assistance += 1`
- `entry_contract_active = true`

Annual reported revenue from Year 7:

€0.85M.

### C. Expand staffed entry and accessible services

Cost: €0.45M.

Effects:

- `staffed_entry_selected = true`
- `entry_assistance += 3`
- `workforce_demand += 2`
- `community_access += 1`
- `entry_contract_active = true`

Annual reported revenue from Year 7:

€0.95M.

### D. Remain a conventional alternative

Cost: €0.10M.

Effects:

- `customer_support_readiness += 1`
- `partnership_standing += 1`
- `independent_market_positioning = true`

No new contract revenue.

---

# 10. YEAR 6 PRIVATE INTELLIGENCE

Each role receives one private message before the decision.

Messages must adapt to the company's supplier branch.

## CEO

VFI customer:
"The supplier's decision could determine your company's future. The board wants to know whether you can afford to leave and what would happen to existing clients."

In-house:
"Your earlier investment in independence now creates a new commercial opportunity. The board wants to know whether you should compete with VFI."

Non-adopter:
"The market is changing again. Your company can enter the new technology market or strengthen its position as an alternative."

## CFO

VFI customer:
"Switching costs depend on your supplier dependence and available cash. An option that exists contractually may be financially impossible."

In-house:
"Proprietary biometric development is expensive, but successful deployment could produce higher returns without VFI licensing fees."

Non-adopter:
"Entering biometric services requires substantial investment. Conventional entry services offer lower costs and more predictable obligations."

## CTO

VFI customer:
"VFI controls the infrastructure your company depends on. Migration or exit requires technical work, and the old platform has a fixed retirement timetable."

In-house:
"Your company owns its verification infrastructure. You could build a competing biometric system, but accuracy, security, and deployment remain your responsibility."

Non-adopter:
"You lack identity-verification infrastructure. Biometric entry would require new capabilities, while smart scanning can use existing ticketing systems."

## Marketing & PR

VFI customer:
"Some fans welcome faster entry, while others distrust VFI after the boycott. Your supplier's reputation may affect your company."

In-house:
"Owning the technology allows your company to create its own brand and customer proposition. It also makes the company directly accountable for failures."

Non-adopter:
"Some customers are actively looking for alternatives to mandatory verification. Others expect the convenience of connected entry systems."

## Head of Legal

VFI customer:
"Your supplier agreement may permit platform changes while limiting termination rights. Contractual migration does not establish a lawful basis for biometric processing."

In-house:
"Ownership of biometric technology does not grant unrestricted rights to process or monetize biometric information. Authorization and safeguards remain necessary."

Non-adopter:
"Entering biometric services creates new legal obligations. Conventional alternatives may involve fewer sensitive data-processing requirements."

## Employee Representative

VFI customer:
"Migration or supplier exit may require retraining, restructuring, and additional support work. Employees want to know whether their jobs are secure."

In-house:
"Building proprietary biometrics could create specialist jobs while changing existing operational roles."

Non-adopter:
"Staffed entry may create employment. Automated entry may reduce routine tasks, while creating new technical and support responsibilities."

## Head of Sustainability

VFI customer:
"Your company may be forced to fund infrastructure changes it did not choose. Accessibility and environmental impacts depend on how the migration is implemented."

In-house:
"Owning the technology gives your company control over infrastructure decisions and responsibility for their environmental and social impacts."

Non-adopter:
"Your choice affects accessibility, computing resources, staffing, and the ability of customers to enter without biometric identification."

## Head of Artist & Venue Relations

VFI customer:
"Several promoters expect continued compatibility with VFI. Leaving may threaten client relationships, while accepting the upgrade may concern artists."

In-house:
"Some venues want alternatives to VFI. Others want the same convenience without dependence on a single supplier."

Non-adopter:
"Independent artists may value nonbiometric services. Major venues are increasingly asking for faster and more integrated entry systems."

---

# 11. YEAR 6 POST-DECISION CONSEQUENCES

Display the selected option and actual resolved outcome.

## Licensed or hybrid VFI: Accept

"Your company accepts VFI's next-generation platform. The supplier relationship continues, but your dependence increases. FacePass capabilities become available for evaluation, subject to authorization."

## Licensed or hybrid VFI: Negotiate

"Your company requests an exemption from the mandatory migration. VFI reviews your contractual position and technical alternatives."

Append:

- Exemption granted: "VFI agrees to a temporary nonbiometric transition arrangement."
- Exemption denied: "VFI refuses the exemption. Your company must resolve its position before legacy support ends."

## Licensed or hybrid VFI: Exit

"Your company begins leaving VFI. The migration requires substantial expenditure and technical work. Your company gains a path toward independence but faces disruption risk."

## Licensed or hybrid VFI: Resist

"Your company refuses the migration and challenges VFI's contractual position. Existing services continue during the transition, but the dispute remains unresolved."

## In-house: Proprietary biometrics

"Your company begins developing a proprietary biometric entry product. It may capture substantial commercial value if the system succeeds, while assuming direct responsibility for its operation and impacts."

## In-house: Independent supplier

"Your company selects an external biometric supplier while retaining its existing verification infrastructure. The strategy reduces development demands but creates a new dependency."

## In-house: Smart entry

"Your company expands into nonbiometric venue entry. The system improves convenience without requiring facial recognition."

## In-house: Existing services

"Your company retains its current technology strategy and invests in service improvements."

## Non-adopter: Biometric entry

"Your company enters the biometric technology market. The investment creates new opportunities and responsibilities, but the system is not yet operational."

## Non-adopter: Smart entry

"Your company develops faster nonbiometric entry services."

## Non-adopter: Staffed entry

"Your company expands human assistance and staffed venue entry."

## Non-adopter: Conventional alternative

"Your company strengthens its position as a ticketing provider that does not require biometric identification."

---

# 12. YEAR 6 INTERNAL EVENTS

Resolve one primary event per company, in priority order.

## 1. VFI exit with low cash

Trigger:
- Exit selected.
- Cash below €1M after expenditure.

"Management warns that the migration has left the company financially vulnerable. Employees and clients request assurances about service continuity."

Effects:
- `financial_distress = true`
- `migration_financial_pressure = true`

## 2. VFI exemption granted

"Your company secures a temporary agreement allowing continued nonbiometric verification. The arrangement preserves service continuity but will require another decision before expiry."

Effects:
- `supplier_dependence = max(0, supplier_dependence - 1)`
- `vfi_exemption_expiry = year8`

## 3. VFI exemption denied or resistance

"VFI confirms that legacy infrastructure will lose support at the end of the transition. Your company must prepare for a technical or contractual resolution."

Effects:
- `legacy_support_at_risk = true`
- `vfi_transition_deadline = year7`

## 4. Proprietary biometric development

"A venue operator expresses interest in testing your independent biometric system. Artists request assurances about accessibility and data governance."

Effects:
- `proprietary_biometric_pilot_opportunity = true`
- No automatic contract revenue.

## 5. Independent nonbiometric entry

"A venue reports strong interest in entry systems that do not require facial recognition."

Effects:
- Partnership standing +1.

## 6. Otherwise

"The company completes its technology strategy review."

No additional effects.

---

# 13. YEAR 6 DEFAULTS

Defaults differ by branch.

## Licensed VFI

Default B: Negotiate an exemption.

Cost: €0.20M.

If unaffordable, default D: Resist.

Cost: €0.10M.

If also unaffordable, use a zero-cost formal objection with the same transition deadline and no cash effect.

## Hybrid VFI

Default B: Negotiate an exemption.

Cost: €0.15M.

If unaffordable, default D: Resist.

Cost: €0.10M.

If also unaffordable, use the zero-cost formal objection.

## In-house

Default D: Preserve existing services.

Cost: €0.10M.

If unaffordable, use zero-cost continuity.

## Non-adopter

Default D: Remain a conventional alternative.

Cost: €0.10M.

If unaffordable, use zero-cost continuity.

All defaults resolve the Year 6 external and internal events.

Record facilitator-skipped and expired decisions separately.

---

# 14. YEAR 7 TRANSITION RESOLUTION

Before the Year 7 safety dilemma, resolve outstanding VFI migration states.

## A. Accepted migration

The VFI supplier relationship continues.

FacePass remains subject to the established biometric authorization rules.

The company may operate identity verification without activating facial recognition, provided lawful nonbiometric alternatives remain available.

## B. Granted exemption

Continue nonbiometric verification.

The exemption expires in Year 8.

No biometric processing is created.

## C. Completed exit

If the exit investment was paid:

- Complete independent verification migration.
- Clear `migration_in_progress`.
- Preserve identity verification capability.
- Remove VFI supplier dependence.
- Apply no additional migration cost.

## D. Denied exemption or unresolved resistance

The original VFI infrastructure reaches its support deadline.

The company cannot continue treating unsupported infrastructure as fully operational.

Set:

- `legacy_vfi_support_expired = true`
- `vfi_operational = false`
- `mandatory_vfi_active = false`
- `supplier_dispute_pending = true` where applicable.

Existing ticket transaction records remain available for lawful retention and disclosure.

Do not delete historical data.

The company continues conventional ticketing where technically possible.

Create `verification_service_disruption = true`.

Effects:
- Technical reliability −1.
- Partnership standing −1.
- Customer trust −1.

Do not automatically bankrupt the company.

## E. Proprietary biometric development

Continue the established Year 7 compliance assessment.

Authorization requires the existing readiness, assurance, accessibility, and governance conditions.

If authorized:
- Activate proprietary biometric entry.
- Begin the specified contract revenue in Year 8.

If not authorized:
- Remain non-operational.
- No biometric contract revenue.

## F. Independent biometric supplier or new entrant

Apply the same compliance assessment.

No authorization is granted merely because the supplier claims its technology is compliant.

---

# 15. YEAR 8 EXEMPTION EXPIRY

At the beginning of Year 8, any temporary VFI exemption granted in Year 6 expires.

Resolve it deterministically:

If the company has sufficient cash to fund an independent migration using its branch's Year 6 exit-cost formula:

- Do not migrate automatically.
- Create `exemption_expiry_decision_required = true`.
- Make this obligation visible in Year 8.

If the company cannot afford migration:

- Create `supplier_lock_in_crisis = true`.
- Preserve the supplier relationship only under a temporary unsupported-service arrangement.
- Set `vfi_operational = false` until a lawful and technically supported solution is implemented.

The existing Year 8 commercial partnership scenario must acknowledge this condition.

Do not silently renew the exemption.

Do not invent a new VFI agreement.

---

# 16. YEARS 7–10 CONTINUITY

Update downstream scenarios and reports to distinguish:

- In-house verification.
- Licensed VFI verification.
- Hybrid VFI verification.
- Independent migrated verification.
- No identity verification.
- VFI FacePass.
- Proprietary biometric entry.
- Independent supplier biometric entry.
- Nonbiometric smart entry.
- Staffed entry.

## Year 7: Safety dilemma

A company can disclose only data it actually possesses.

VFI supplier relationships may create additional data-governance and contractual questions.

No company gains biometric records merely because it accepted a platform migration.

## Year 8: Commercial partnerships

Supplier lock-in and migration costs influence commercial dependence.

Companies with proprietary biometrics may attract new commercial partners.

Companies without biometric systems may attract artists and audiences seeking alternatives.

Preserve the existing Year 8 decisions while incorporating supplier-related obligations.

## Year 9: Strategic direction

Companies facing supplier dependence, expired support, or migration distress must retain those constraints.

The strategic decision cannot erase contractual obligations automatically.

## Year 10: Accountability

The final report must document:

- Original Year 1 procurement.
- Supplier dependence.
- VFI's mandatory migration announcement.
- The company's Year 6 response.
- Whether exit was financially feasible.
- Whether the company negotiated, resisted, accepted, or exited.
- Any supplier disruption.
- Whether biometric entry became operational.
- Commercial benefits captured.
- Customer, employee, and partner consequences.
- Unresolved obligations.

---

# 17. EXECUTIVE POWER INTERACTIONS

Preserve the established executive powers.

## CFO

Can freeze discretionary migration, development, or exit expenditure.

Cannot cancel an already binding supplier obligation.

## CTO

Can veto a technically dependent proposal, including biometric development or migration.

Cannot prevent a supplier from retiring its own infrastructure.

## Head of Legal

Can require review of supplier contracts, migration terms, biometric processing, and exit obligations.

The review may improve negotiating evidence but does not guarantee an exemption.

## Employee Representative

Can call a work stoppage in response to restructuring, migration pressure, or working conditions.

The action creates operational consequences but does not automatically reverse the decision.

## Head of Sustainability

Can require an impact assessment of biometric deployment, infrastructure changes, accessibility, and affected communities.

## Artist & Venue Relations

May invoke a material change clause in a qualifying active client contract affected by the supplier migration.

Cannot automatically invoke a client-contract clause against VFI's supplier agreement.

## Marketing & PR

Can communicate the company's position.

Cannot remove actual supplier dependence or conceal service disruptions.

## CEO

Can override the team's preferred option within legally, technically, and financially feasible choices.

Cannot force VFI to grant an exemption.

Cannot make an unaffordable exit feasible.

---

# 18. VALIDATION REQUIREMENTS

Test all Year 6 branches against reachable Years 1–5 company states.

Verify:

1. The Year 5 commercial is shown before Year 6.
2. VFI is a supplier, not a generic name for all verification.
3. Existing VFI customers face the mandatory migration.
4. In-house companies have no VFI migration obligation.
5. Non-adopters have no VFI migration obligation.
6. Licensed and hybrid companies have different exit costs.
7. Switching costs use actual supplier dependence.
8. Unaffordable exit options are disabled.
9. No company can spend more cash than it has.
10. Exemptions are resolved deterministically.
11. Exemption denial creates a Year 7 deadline.
12. Resistance creates a real supplier-dispute obligation.
13. Legacy infrastructure cannot operate indefinitely after support expiry.
14. In-house companies can build proprietary biometrics.
15. Proprietary biometric development has genuine commercial upside.
16. Biometric capability requires authorization before deployment.
17. Technology ownership does not automatically authorize personal data processing.
18. No biometric records are invented before deployment.
19. Non-adopters can pursue nonbiometric services.
20. Every branch has a defined default.
21. Every branch has private intelligence for all eight roles.
22. Every branch produces a resolved outcome.
23. Internal events depend on company state.
24. Year 7 receives the correct supplier and technology state.
25. Year 8 receives unresolved exemption and lock-in obligations.
26. Year 9 preserves supplier dependence and financial distress.
27. Year 10 reports actual supplier and technology history.
28. Executive powers remain functional.
29. Skipped years apply the correct branch-specific defaults.
30. All transactions remain idempotent.
31. Existing saved company histories migrate without data loss.
32. No universal ethics score is introduced.
33. Different procurement histories produce meaningfully different Year 6 choices.
34. Companies retain agency within their actual financial and contractual constraints.
35. The simulation remains completable even when a company cannot afford to exit.

## IMPLEMENTATION PRIORITY

1. Update VFI supplier model and legacy procurement mapping.
2. Add the Year 5 Smile and Pass commercial and migration announcement.
3. Replace the existing Year 6 scenario with the four procurement-dependent branches.
4. Implement switching costs and exemption resolution.
5. Implement Year 7 migration and support-expiry transitions.
6. Implement Year 8 exemption-expiry obligations.
7. Update Years 7–10 narratives and final reporting.
8. Test all branches and financial fallbacks.

The educational purpose is to make accumulated power and dependence visible through actual company constraints.

A company may possess a contractual right to exit while lacking the financial resources to exercise it.

A company that built independently may now use that freedom to develop and commercialize its own biometric technology.

A company that never adopted verification may gain new opportunities by remaining outside the supplier ecosystem.

Do not impose a preferred ethical outcome.

END OF AUTHORITATIVE PLATFORM SHIFT BRIEF.
