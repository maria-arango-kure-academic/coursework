
# FAIRPASS: FACEPASS PLATFORM AND DATA ECONOMY
## Authoritative implementation update for the simulation builder

**Status:** Replace the previous Year 6 VFI migration decision model with this specification.

Preserve the existing FairPass simulation, Years 1–5 history, executive powers, company indicators, and financial ledger.

The central educational theme is power: who controls technological infrastructure, who captures the value of customer data, and who can afford to refuse a supplier's terms.

---

# 1. THE PLATFORM SHIFT

VFI is a fictional technology supplier.

Its original product, Verified Fan Identity, was introduced in 2027 to limit ticket purchases to five tickets per verified person, per event.

In 2032, VFI announces that its original verification infrastructure will be retired.

Its replacement is FacePass.

FacePass is the standard next generation of the VFI platform. It is not an optional facial-recognition product sold separately.

The new platform includes:

- Biometric identity verification capabilities.
- Facial-recognition venue entry.
- Cross-event identity linking.
- Expanded customer analytics.
- Infrastructure for AI model development and training.

VFI's standard licensing agreement introduces broad contractual rights to use data processed through the platform for product development, commercial analytics, and AI training.

VFI also offers a more expensive enterprise arrangement with dedicated hosting and restrictions on supplier secondary data use.

Existing VFI customers must choose how to respond before the legacy platform is retired.

## Critical distinction

VFI can impose commercial terms and technical migration requirements.

VFI cannot make biometric processing or AI training lawful merely by including them in a contract.

A company may accept FacePass infrastructure without being legally authorized to activate every capability.

A contractual right claimed by VFI does not override data protection law, customer rights, or the company's own responsibilities.

Do not automatically collect, disclose, monetize, or train AI on biometric data merely because a company accepts standard FacePass terms.

---

# 2. YEAR 5 CHECKPOINT

Keep the synchronized Year 5 checkpoint.

After displaying the five-year industry results, play the second VFI commercial.

## Commercial

Advertiser: VFI.

Campaign: Smile and Pass.

The advertisement celebrates five years of verified ticketing.

It introduces the next generation of connected fan experiences.

A fan approaches a venue gate.

A camera recognizes them.

The gate opens.

The fan walks inside.

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

## Post-commercial announcement

Display:

# VFI Announces New Platform Terms

VFI is retiring its original verification infrastructure.

All existing customers must migrate to FacePass or make alternative arrangements.

The new platform includes biometric entry capabilities and expanded customer analytics.

Under VFI's proposed standard terms, the supplier claims rights to use platform data for commercial analytics, product development, and AI training.

Customers wanting dedicated data controls and restrictions on supplier secondary use must purchase an enterprise agreement.

The legacy platform will lose support in twelve months.

Then release Year 6.

---

# 3. YEAR 6: SMILE AND PASS
## Who Controls the Data?

Year 6 remains optional.

The fixed external event occurs for every company, including when Year 6 is skipped.

Companies receive different decision options according to their Year 1 procurement strategy.

## Shared scenario

# Smile and Pass

VFI has announced the retirement of its original identity verification platform.

Its replacement includes facial-recognition capabilities, expanded customer analytics, and new contractual data-use terms.

VFI says the platform will improve convenience, security, and service innovation.

Customer organizations question who will control the information generated through the system.

Existing VFI customers face a choice between accepting the new terms, paying for greater control, challenging the changes, or leaving.

Independent providers face a different opportunity: they may build competing technology and capture the commercial value themselves.

**What will your company do?**

---

# 4. BRANCH A: LICENSED VFI COMPANIES

Applies when:

`identity_technology_provider = vfi`

## A. Accept standard FacePass

Immediate migration cost: €0.35M.

Annual VFI fee remains €0.90M.

The company accepts the standard platform and proposed supplier data-use terms.

Effects:

- `facepass_contract = standard`
- `facepass_migration_accepted = true`
- `supplier_dependence += 2`
- `supplier_data_rights = broad_proposed`
- `biometric_capability = pending`
- `commercial_opportunity += 2`
- `data_governance_exposure += 2`

The company does not gain automatic authorization for biometric processing or AI training.

## B. Purchase enterprise FacePass

Immediate migration cost: €0.50M.

Annual VFI fee becomes €1.50M from Year 7.

The company obtains dedicated hosting and contractual restrictions on VFI's secondary use of customer data.

Effects:

- `facepass_contract = enterprise`
- `facepass_migration_accepted = true`
- `supplier_dependence += 1`
- `supplier_data_rights = restricted`
- `company_data_control += 3`
- `privacy_safeguards += 2`
- `biometric_capability = pending`
- `commercial_opportunity += 1`

Enterprise licensing does not automatically make the company's own biometric processing or data monetization lawful.

## C. Negotiate or resist

Immediate cost: €0.20M.

The company challenges VFI's expanded data-use terms and seeks continued nonbiometric verification.

Effects:

- `facepass_contract = disputed`
- `supplier_negotiation_pending = true`
- `supplier_data_rights = contested`
- `assurance_evidence += 1`

Resolution:

If partnership standing is at least 72 OR assurance evidence is at least 3:

- VFI grants a two-year restricted-use transition agreement.
- `vfi_exemption_granted = true`
- Existing verification continues.
- `vfi_exemption_expiry = year8`

Otherwise:

- VFI refuses.
- `vfi_exemption_denied = true`
- `vfi_transition_deadline = year7`
- Existing verification continues only during the transition period.

## D. Exit VFI

Base migration cost: €1.20M.

Additional switching cost:

`0.10M × max(0, supplier_dependence - 2)`

Calculate the full cost before presenting affordability.

If affordable:

- Terminate the VFI supplier relationship.
- Begin migration to independent verification.
- Set `identity_technology_provider = independent_migrated`.
- Set `vfi_supplier_contract = false`.
- Set `supplier_dependence = 0`.
- Set `facepass_contract = none`.
- Set `migration_in_progress = true`.
- Technical reliability −1.

Independent verification becomes operational at the beginning of Year 7 if migration completes.

No biometric capability is automatically created.

---

# 5. BRANCH B: HYBRID VFI COMPANIES

Applies when:

`identity_technology_provider = hybrid_vfi`

## A. Accept standard FacePass

Immediate cost: €0.45M.

Annual VFI fee remains €0.65M.

Effects:

- `facepass_contract = standard`
- `supplier_dependence += 2`
- `supplier_data_rights = broad_proposed`
- `biometric_capability = pending`
- `commercial_opportunity += 2`
- `data_governance_exposure += 2`

## B. Purchase enterprise FacePass

Immediate cost: €0.55M.

Annual VFI fee becomes €1.20M from Year 7.

Effects:

- `facepass_contract = enterprise`
- `supplier_dependence += 1`
- `supplier_data_rights = restricted`
- `company_data_control += 3`
- `privacy_safeguards += 2`
- `biometric_capability = pending`

## C. Negotiate or resist

Immediate cost: €0.15M.

Effects:

- `facepass_contract = disputed`
- `supplier_negotiation_pending = true`
- `supplier_data_rights = contested`
- `assurance_evidence += 1`

Resolution:

If internal capability is at least 1 OR partnership standing is at least 72:

- Grant a two-year restricted-use transition.
- `vfi_exemption_granted = true`
- `vfi_exemption_expiry = year8`

Otherwise:

- Exemption denied.
- Legacy support expires in Year 7.

## D. Exit VFI

Base cost: €0.75M.

Additional switching cost:

`0.10M × max(0, supplier_dependence - 2)`

If affordable:

- Terminate the VFI supplier relationship.
- Migrate to independent verification.
- Set `supplier_dependence = 0`.
- Set `identity_technology_provider = independent_migrated`.
- Set `migration_in_progress = true`.
- Technical reliability −1.

---

# 6. BRANCH C: BUILT IN-HOUSE

Applies when:

`identity_technology_provider = in_house`

These companies have no VFI supplier contract.

They own their verification infrastructure.

## A. Build proprietary biometric technology

Cost: €0.90M.

The company develops its own facial-recognition infrastructure.

It may capture commercial value from venue contracts, licensing, and lawful data-enabled services.

Effects:

- `proprietary_biometric_development = true`
- `biometric_capability = pending`
- `company_data_control += 3`
- `technical_independence += 2`
- `commercial_opportunity += 3`
- `data_governance_exposure += 2`
- `entry_compliance_review = true`

Potential annual reported revenue from Year 8, only if authorized and commercially activated:

€1.60M.

The company cannot automatically use biometric information for unrelated AI training or commercial analytics.

## B. License independent biometric infrastructure

Cost: €0.60M.

Effects:

- `biometric_capability = pending`
- `facial_entry_provider = independent_supplier`
- `supplier_dependence += 1`
- `commercial_opportunity += 2`
- `entry_compliance_review = true`

Potential annual reported revenue from Year 8, if authorized and commercially activated:

€1.10M.

## C. Build nonbiometric smart entry

Cost: €0.40M.

Effects:

- `smart_entry_selected = true`
- `entry_efficiency += 2`
- `entry_assistance += 1`
- `entry_contract_active = true`

Annual reported contract revenue from Year 7:

€0.85M.

## D. Preserve existing services

Cost: €0.10M.

Effects:

- `customer_support_readiness += 1`
- `technical_reliability += 1`

No new contract revenue.

---

# 7. BRANCH D: NEVER ADOPTED VERIFICATION

Applies when:

`identity_technology_provider = none`

## A. Enter the biometric market

Cost: €1.20M.

Effects:

- `biometric_capability = pending`
- `facial_entry_provider = independent_new`
- `commercial_opportunity += 3`
- `data_governance_exposure += 2`
- `entry_compliance_review = true`

Potential annual reported revenue from Year 8, if authorized and commercially activated:

€1.20M.

## B. Develop nonbiometric smart entry

Cost: €0.40M.

Effects:

- `smart_entry_selected = true`
- `entry_efficiency += 2`
- `entry_assistance += 1`
- `entry_contract_active = true`

Annual reported revenue from Year 7:

€0.85M.

## C. Expand staffed entry

Cost: €0.45M.

Effects:

- `staffed_entry_selected = true`
- `entry_assistance += 3`
- `workforce_demand += 2`
- `community_access += 1`
- `entry_contract_active = true`

Annual reported revenue from Year 7:

€0.95M.

## D. Remain a conventional alternative

Cost: €0.10M.

Effects:

- `customer_support_readiness += 1`
- `partnership_standing += 1`
- `independent_market_positioning = true`

No new contract revenue.

---

# 8. PRIVATE INTELLIGENCE

Preserve the eight-role private intelligence structure.

Update Year 6 messages to reflect the data-economy dilemma.

## CEO

VFI customer:
"VFI has changed the terms of a relationship your company depends on. The board wants to know whether you can afford greater control or afford to leave."

In-house:
"Your company owns its infrastructure. You can now compete with VFI and potentially capture the value of biometric services yourself."

Non-adopter:
"Some promoters want biometric entry, while others are looking for alternatives. Your earlier decision has left you outside VFI's contractual changes."

## CFO

VFI customer:
"VFI's standard price assumes the supplier can derive additional value from customer data. Restricting that use requires a more expensive enterprise agreement. Leaving may cost even more."

In-house:
"Proprietary biometric development is expensive, but ownership could allow the company to capture more commercial revenue."

Non-adopter:
"Entering biometric services requires major investment. Nonbiometric alternatives have lower costs and fewer new data obligations."

## CTO

VFI customer:
"The new platform bundles biometric capabilities with existing verification infrastructure. Your engineers cannot simply remove supplier-controlled components."

In-house:
"Your team can design proprietary biometric technology, including data architecture and retention rules. You also bear responsibility for reliability and security."

Non-adopter:
"You have no existing identity-verification infrastructure. Biometric entry requires new technical capabilities."

## Marketing & PR

VFI customer:
"VFI promotes Smile and Pass as effortless convenience. Customer organizations are questioning the expanded data-use terms."

In-house:
"Your company could market an independent alternative to VFI. Customers may also question how you intend to use the data yourself."

Non-adopter:
"Some fans value convenience. Others are actively seeking services that do not require biometric identification."

## Head of Legal

VFI customer:
"VFI's standard contract claims rights to use customer data for AI training and commercial analytics. These terms do not establish a lawful basis for every proposed use. Your company remains responsible for evaluating what processing is permitted."

In-house:
"Owning biometric infrastructure does not grant unrestricted rights to process or monetize biometric data. Purpose limitation, necessity, lawful basis, and safeguards remain relevant."

Non-adopter:
"Entering biometric services creates substantial new legal obligations. Conventional services can continue under existing data practices."

## Employee Representative

VFI customer:
"Migration may increase support demands and change technical responsibilities. Enterprise fees or switching costs may compete with staffing budgets."

In-house:
"Building proprietary technology could create specialist jobs while changing existing work and support roles."

Non-adopter:
"Staffed services may create employment, while automated entry changes the work required at venues."

## Head of Sustainability

VFI customer:
"The new platform may increase computing demands and data collection. Your company has limited control over supplier infrastructure under standard terms."

In-house:
"Owning the infrastructure gives your company more control over environmental and social impacts, including decisions about data retention."

Non-adopter:
"Your choice affects accessibility, computing resources, and opportunities for people who cannot or do not wish to use biometric identification."

## Head of Artist & Venue Relations

VFI customer:
"Some promoters want FacePass compatibility. Others are concerned about the supplier's data-use terms and their implications for audiences."

In-house:
"Venues are interested in alternatives to VFI. Some want equivalent biometric capabilities without supplier dependence."

Non-adopter:
"Independent artists may prefer nonbiometric services. Major venues increasingly expect integrated entry systems."

---

# 9. DATA RIGHTS AND LEGAL STATUS

Use separate variables for contractual claims and actual authorized processing.

`facepass_contract = none | standard | enterprise | disputed | expired`

`supplier_data_rights = none | broad_proposed | restricted | contested`

`biometric_capability = none | pending | authorized | operational`

`ai_training_authorized = false`

`biometric_secondary_use_authorized = false`

Accepting standard FacePass:

- Creates a contractual claim by VFI.
- Does not automatically authorize AI training.
- Does not automatically authorize biometric processing.
- Does not create biometric records before lawful deployment.

Enterprise FacePass:

- Restricts VFI's contractual secondary-use rights.
- Gives the company greater control over its data arrangements.
- Does not automatically authorize the company's own secondary uses.

In-house biometric development:

- Gives the company ownership of its technology.
- Does not grant ownership of people's personal data.
- Does not automatically authorize AI training or unrelated commercial exploitation.

Do not model unlawful data processing as an automatic consequence of selecting a contract.

Instead, record the resulting governance exposure, commercial incentives, and unresolved authorization requirements.

---

# 10. ANNUAL LICENSING AND FINANCIAL DISTRESS

Standard FacePass retains the existing annual VFI fee:

- Licensed: €0.90M.
- Hybrid: €0.65M.

Enterprise FacePass increases annual fees from Year 7:

- Licensed: €1.50M.
- Hybrid: €1.20M.

Use the existing annual operating-fee ledger.

If a company cannot pay the full fee:

1. Deduct available cash.
2. Record the unpaid balance as `vfi_operating_payable_m`.
3. Set `financial_distress = true`.
4. Set `supplier_payment_at_risk = true`.
5. Preserve operational status temporarily if the infrastructure remains supported.
6. Do not automatically borrow, bankrupt the company, or terminate services.
7. Carry the liability forward without duplicate charging.

At the next annual transition, address outstanding liabilities according to the established financial rules.

Do not charge both the old and new VFI annual fee in the same year.

---

# 11. YEAR 6 DEFAULTS

## Licensed VFI

Default C: Negotiate or resist.

Cost: €0.20M.

If unaffordable, use zero-cost formal objection and preserve the transition deadline.

## Hybrid VFI

Default C: Negotiate or resist.

Cost: €0.15M.

If unaffordable, use zero-cost formal objection.

## In-house

Default D: Preserve existing services.

Cost: €0.10M.

If unaffordable, use zero-cost continuity.

## Non-adopter

Default D: Remain a conventional alternative.

Cost: €0.10M.

If unaffordable, use zero-cost continuity.

Record expired decisions and facilitator-skipped decisions separately.

---

# 12. YEAR 7 TRANSITIONS

At the start of Year 7:

## Standard FacePass

The next-generation platform becomes the supported VFI infrastructure.

Existing identity verification may continue.

Biometric capabilities remain inactive until authorized.

The supplier's broad contractual data-use claims remain subject to applicable law.

## Enterprise FacePass

The next-generation platform becomes supported.

Dedicated hosting and contractual data-use restrictions take effect.

Biometric capabilities remain inactive until authorized.

Charge the enterprise annual fee once.

## Negotiated exemption granted

Continue restricted-use nonbiometric verification.

The exemption expires in Year 8.

## Negotiation denied

Legacy VFI support expires.

Set:

- `vfi_operational = false`
- `mandatory_vfi_active = false`
- `verification_service_disruption = true`

Conventional ticketing continues.

## Completed supplier exit

Independent verification becomes operational after the funded migration.

Remove VFI supplier dependence.

No FacePass capability is created.

## Proprietary biometric development

Apply the established technical, accessibility, and legal authorization assessment.

If authorized, mark the technology operational.

Commercial revenue still requires an activated contract or programme.

Do not automatically award a venue contract merely because biometric technology is authorized.

---

# 13. YEAR 8 EXEMPTION EXPIRY

When a restricted-use VFI exemption expires:

- Stop unsupported VFI verification.
- Set `vfi_operational = false`.
- Set `mandatory_vfi_active = false`.
- Create `exemption_expiry_decision_required = true`.
- Preserve conventional ticketing.
- Record the company's financial ability to migrate.
- Do not automatically complete migration.

If the company cannot afford migration:

- Create `supplier_lock_in_crisis = true`.

If it can afford migration:

- Record `migration_financially_feasible = true`.

The company must still make an explicit future decision before migration occurs.

Do not silently renew the exemption.

---

# 14. YEARS 8–10 CONTINUITY

Update downstream consequences and reporting to distinguish:

- VFI standard FacePass.
- VFI enterprise FacePass.
- Disputed or expired VFI agreements.
- In-house biometric development.
- Independent biometric suppliers.
- Nonbiometric entry services.
- Supplier-controlled data rights.
- Company-controlled infrastructure.
- Actual lawful processing authorization.
- Unresolved data-governance obligations.

## Year 9

Supplier dependence, enterprise licensing costs, switching costs, and data-governance obligations must influence strategic choices.

Do not erase supplier obligations through generic restructuring.

## Year 10

The accountability report must include:

- Original Year 1 procurement strategy.
- Year 6 FacePass response.
- Standard or enterprise contract choice.
- Supplier data-use terms.
- Actual biometric deployment status.
- Whether AI training or secondary use was authorized.
- Financial consequences of licensing or exit.
- Outstanding supplier liabilities.
- Customer, employee, and partner consequences.
- Whether the company could afford to refuse VFI's terms.

Do not describe contractual claims as proof that data was actually processed or monetized.

---

# 15. STUDENT-FACING CONSEQUENCES

Use actual resolved outcomes.

Examples:

## Standard FacePass

"Your company accepts VFI's standard next-generation platform. Licensing costs remain unchanged, but the supplier claims broader rights to use data for analytics and AI development. Your company must determine which processing activities can lawfully proceed."

## Enterprise FacePass

"Your company pays higher licensing fees for dedicated data controls and restrictions on VFI's secondary use of customer information. The arrangement increases costs while giving your company greater contractual control."

## Negotiation

"Your company challenges VFI's new terms and seeks continued nonbiometric verification. Its future depends on the supplier's response and your company's contractual position."

## Exit

"Your company begins leaving VFI. The migration is expensive and technically demanding, but it offers a path toward greater independence."

## Proprietary biometrics

"Your company invests in its own biometric entry technology. It may capture the commercial value of future services, while assuming direct responsibility for the system and its data practices."

## Nonbiometric alternative

"Your company develops or maintains entry services without facial recognition. Some customers and artists value this approach, while others prefer the convenience of biometric entry."

---

# 16. ACCEPTANCE TESTS

Verify:

1. FacePass is a mandatory next-generation platform for existing VFI customers.
2. It is not presented as an optional standalone product.
3. Standard FacePass retains existing licensing fees.
4. Enterprise FacePass increases annual licensing fees.
5. Standard terms create proposed supplier data-use rights.
6. Enterprise terms restrict supplier secondary use.
7. Neither contract automatically authorizes biometric processing.
8. Neither contract automatically authorizes AI training.
9. In-house technology ownership does not create unrestricted rights over personal data.
10. Licensed and hybrid companies receive different costs.
11. In-house companies can develop proprietary biometrics.
12. Non-adopters can enter the biometric market or remain conventional.
13. Exit costs depend on existing supplier dependence.
14. Unaffordable exits are disabled.
15. Negotiation outcomes are deterministic.
16. Every procurement branch has a defined default.
17. No company can spend more cash than available.
18. Unpaid operating fees become liabilities without duplicate charges.
19. Supported verification may continue during financial distress.
20. Unsupported verification stops after the relevant transition deadline.
21. No biometric records are created before lawful activation.
22. No AI training occurs without explicit authorization.
23. No venue contract is automatically awarded through biometric authorization.
24. Year 8 exemption expiry stops unsupported verification.
25. Year 9 preserves supplier dependence and financial consequences.
26. Year 10 accurately reports the company's data-governance history.
27. All eight roles receive relevant private intelligence.
28. Executive powers remain functional.
29. Skipped years use branch-specific defaults.
30. Existing company histories and financial records remain intact.
31. The Year 5 commercial precedes the Year 6 decision.
32. The Year 5 boycott remains a separate external event.
33. No universal ethics score is introduced.
34. The simulation remains completable for financially distressed companies.
35. All effects are deterministic and idempotent.

## IMPLEMENTATION PRIORITY

1. Replace the existing FacePass contract model.
2. Update the Year 5 commercial and supplier announcement.
3. Replace Year 6 decision branches and private intelligence.
4. Implement standard versus enterprise licensing.
5. Implement contractual data rights separately from lawful processing authorization.
6. Update financial distress and recurring-fee handling.
7. Update Year 7 migration transitions.
8. Update Year 8 exemption expiry.
9. Update Years 9–10 reporting and consequences.
10. Run full regression tests.

The central question is:

**Who controls the infrastructure, who captures the value, and who can afford to refuse?**

END OF AUTHORITATIVE FACEPASS DATA ECONOMY UPDATE.
