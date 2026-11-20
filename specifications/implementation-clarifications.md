# Approved implementation clarifications

## Annual VFI operating fees, from Year 4 onward

Pay as much of the annual VFI operating fee as available cash permits. Record the unpaid balance as `vfi_operating_payable_m`, set `financial_distress = true` and `supplier_payment_at_risk = true`, and keep VFI operational. Carry the liability forward and prioritize repayment when cash becomes available. Do not automatically shut down VFI, borrow, declare bankruptcy or charge the same liability twice.

Student-facing notice:

> Your company cannot cover its full VFI operating costs. The unpaid balance becomes an outstanding liability. The system remains operational for now, but suppliers are requesting a repayment plan, and future service continuity is uncertain.

## Year 5 expiry

Default: B, Independent review (€300K). Apply the review cost and state changes, resolve findings from actual safeguards and outstanding obligations, and apply boycott modifiers and the internal event normally. Record `decision_source = expired_default` without attributing the decision to a student. If unaffordable, use the established lowest-cost feasible fallback, normally D. All active students must complete their Year 5 reflection before the mandatory midpoint checkpoint. Facilitator-forced expiry uses the same rules.

Student-facing announcement:

> With no executive decision submitted before the deadline, management commissions an independent review of the company's ticketing systems and customer access procedures. Existing operations continue while the findings are prepared.

## Individual recommendations

One mandatory private multiple-choice recommendation per student per active year, after confidential intelligence and before company decision lock. A submitted recommendation cannot be edited. No recommendation is invented for a skipped year or inactive student. Written reflections remain in Years 1, 5 and 10 and contain no duplicate multiple-choice preference question. Reports compare recommendations with actual company decisions and executive-power use.

Maria explicitly selected: if time expires before everyone recommends, apply the existing default and mark missing recommendations as not submitted. Do not collect retrospective recommendations after the decision locks; missing recommendations do not prevent the required written reflections or checkpoint progression.

The Year 10 specification's duplicate Question 1 is replaced by the single pre-decision recommendation step. Its two written questions remain mandatory and retain their supplied wording.

## Session pacing

Maria clarified on 20 November: setup has estimated minutes per decision, time to the first checkpoint, and time to finish. The decision duration is an estimate; companies can be faster or slower. These settings do not automatically lock decisions or trigger defaults. Existing facilitator controls open explicit submission windows and trigger synchronized checkpoints; their default-resolution rules remain in force.
