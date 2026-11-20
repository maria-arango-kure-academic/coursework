"""Specified strategy and accountability effects for Years 9–10."""
STRATEGY={'scale':.5,'reinvest':.4,'restructure':.2,'specialize':.3,'continuity_fallback':0}
REPORTS={'independent_review':.35,'detailed_report':.2,'focused_report':.1,'board_statement':0}
OBLIGATIONS=('data_governance_review_required','biometric_authorization_required','supplier_dispute_pending','supplier_negotiation_pending','migration_in_progress','exemption_expiry_decision_required','supplier_lock_in_crisis','verification_service_disruption','restructuring_proposed_12','verification_remediation_required','support_training_outstanding','integration_governance_outstanding','review_remediation_required','customer_compensation_review','staff_escalation_review','staff_restructuring_dispute','data_handling_review_required','year9_contract_review_required','partnership_conditions_disputed','entry_remediation_required','independent_programme_pending','workforce_negotiation_required','workforce_consultation_required','major_contract_renegotiation_pending','contract_dispute_pending','sustainability_followup_required','communications_scrutiny','financial_recovery_plan_required')

def obligations(s):
    values=[k for k in OBLIGATIONS if s.get(k)]
    for k in ('vfi_operating_payable_m','operating_payable_m'):
        if s.get(k,0)>0:values.append(k)
    return values

def initialize(s):
    for k in ('involuntary_layoffs','report_transparency'):s[k]=0
    for k in ('strategic_direction','report_scope','report_verification'):s[k]=None
    s['resolved_obligations']=[]

def before_external(s,y):
    if y==9:s.update(market_consolidation_pressure='high',investor_strategy_review=True)
    if y==10:s['industry_accountability_review']=True

def cost(s,y,o):return (STRATEGY if y==9 else REPORTS)[o]

def apply(s,y,o):
    if y==9:
        s['year9_layoffs']=0
        s['year9_prior_workforce_pressure']=s['workforce_pressure']
        if o=='scale':
            s['commercial_opportunity']+=3;s['commercial_dependency']+=2;s['partnership_standing']+=1;s['workforce_pressure']+=1
            s['strategic_direction']='major_partnership_growth'
            if s['commercial_partnership_active']:s['meridian_expansion_option']=True
            else:s['major_partner_search']=True
            if s['partnership_conditions_disputed']:s['stakeholder_conflict']+=1
        elif o=='reinvest':
            s['workforce_conditions']+=3;s['customer_trust']+=2;s['customer_support_readiness']+=2;s['technical_reliability']+=1
            s['workforce_pressure']=max(0,s['workforce_pressure']-2);s['strategic_direction']='service_and_workforce_investment'
            resolved=[]
            for k in ('staff_escalation_review','support_training_outstanding','verification_remediation_required','customer_compensation_review','review_remediation_required'):
                if s.get(k):s[k]=False;resolved.append(k)
                if len(resolved)==2:break
            s['resolved_obligations']+= [{'year':9,'obligation':k} for k in resolved]
        elif o=='restructure':
            s['technical_reliability']+=1;s['financial_pressure']=max(0,s['financial_pressure']-1)
            s['workforce_conditions']-=2;s['workforce_pressure']+=1;s['strategic_direction']='operational_restructuring'
            if s.get('restructuring_proposed_12'):
                s['employees']=max(0,s['employees']-12);s['restructuring_proposed_12']=False
                s['year9_layoffs']=12;s['involuntary_layoffs']+=12;s['workforce_conditions']-=3;s['labour_dispute_risk']+=1
            else:s['process_reorganization']=True
        elif o=='specialize':
            s['artist_autonomy']+=2;s['community_access']+=2;s['partnership_standing']+=2
            s['commercial_dependency']=max(0,s['commercial_dependency']-1);s['strategic_direction']='independent_specialization'
            if s['independent_programme_active']:s['commercial_opportunity']+=2;s['independent_expansion_option']=True
            elif s['independent_programme_pending']:
                if s['partnership_standing']>=72:s['independent_programme_active']=True;s['independent_programme_pending']=False
            else:s['independent_partner_recruitment']=True
        else:s['strategic_direction']='continuity_under_constraint'
    else:
        s['reporting_choice']=o
        values={'independent_review':(3,'comprehensive','independent',3),'detailed_report':(2,'comprehensive','internal',1),'focused_report':(1,'limited','internal',0),'board_statement':(0,'minimal','none',0)}
        transparency,scope,verification,evidence=values[o]
        s.update(report_transparency=transparency,report_scope=scope,report_verification=verification)
        s['assurance_evidence']+=evidence
        if o=='independent_review':s['independent_accountability_review']=True

def conditional(s,y,o,content):
    messages=[];defs=content['strategy_modifiers' if y==9 else 'reporting_modifiers']
    def add(i):messages.append(defs[str(i)])
    if y==9:
        if o=='scale' and s['partnership_standing']>=73:add(1);s['commercial_opportunity']+=1
        if o=='scale' and s['partnership_conditions_disputed']:add(2);s['stakeholder_conflict']+=1;s['customer_trust']-=1
        if o=='reinvest' and s['year9_prior_workforce_pressure']>=2:add(3);s['workforce_conditions']+=1;s['labour_dispute_risk']=max(0,s['labour_dispute_risk']-1)
        if o=='restructure' and s['year9_layoffs']:add(4);s['staff_restructuring_dispute']=True
        if o=='specialize' and any(s.get(k) for k in ('independent_festival_opportunity','artist_collective_opportunity','boycott_alternative_supplier_opportunity','independent_expansion_option')):add(5);s['partnership_standing']+=1;s['independent_expansion_option']=True
    else:
        if s['report_transparency']>=2 and s['customer_trust']>=72 and s['workforce_conditions']>=70 and s['partnership_standing']>=72:add(1);s['customer_trust']+=1;s['partnership_standing']+=1
        if s['report_transparency']>=2 and obligations(s):add(2);s['public_remediation_commitment']=True
        if o=='independent_review' and (s['workforce_conditions']<68 or s['involuntary_layoffs']>0):add(3);s['workforce_accountability_finding']=True
        disputes=('customer_compensation_review','boycott_customer_complaints','data_handling_review_required','staff_escalation_review','staff_restructuring_dispute','workforce_negotiation_required','partnership_conditions_disputed','contract_dispute_pending')
        if s['report_transparency']<=1 and any(s.get(k) for k in disputes):add(4);s['customer_trust']-=1;s['reporting_criticism']=True
        if o=='independent_review' and s['cash']>=2:add(5);s['partnership_standing']+=1
        if s['cash']<1:add(6);s['financial_recovery_plan_required']=True
    return messages

def primary(s,y,o,content):
    if y==9:
        if s['cash']<1:n=1;s['financial_recovery_plan_required']=True;s['workforce_concerns']+=1
        elif s['year9_layoffs']>0:n=2;s['workforce_conditions']-=1;s['labour_dispute_risk']+=1
        elif o=='reinvest' and s['customer_support_readiness']>=3:n=3;s['customer_trust']+=1;s['partnership_standing']+=1
        elif o=='specialize' and s['partnership_standing']>=73:n=4;s['independent_network_opportunity']=True;s['partnership_standing']+=1
        else:n=5
    else:
        if len(obligations(s))>=2:n=1;s['post_simulation_accountability_plan_required']=True
        elif s['workforce_conditions']>=72 and s['customer_trust']>=72:n=2;s['partnership_standing']+=1
        elif s['cash']<1:n=3;s['financial_recovery_plan_required']=True
        elif s['artist_autonomy']>=3 and s['partnership_standing']>=73:n=4;s['partnership_standing']+=1
        else:n=5
    key=next(k for k in content['internal'][str(y)] if k.startswith(str(n)+'.'))
    return dict(id=f'I{y}',title='Company update',rule=key,text=content['internal'][str(y)][key])
