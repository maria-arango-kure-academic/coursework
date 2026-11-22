"""Specified entry, disclosure and partnership rules for Years 6–8."""
ENTRY={
 'facial':dict(cost=.7,entry_efficiency=3,biometric_exposure=2,commercial_opportunity=2),
 'smart':dict(cost=.4,entry_efficiency=2,entry_assistance=1,partnership_standing=1),
 'staffed':dict(cost=.45,entry_efficiency=1,entry_assistance=3,workforce_demand=2,partnership_standing=1),
 'decline':dict(cost=0)}
POLICE={
 'cooperate':dict(cost=.20,security_cooperation=2),
 'require_order':dict(cost=.15,privacy_safeguards=2,security_cooperation=1),
 'independent_legal':dict(cost=.25,privacy_safeguards=2,security_cooperation=1,assurance_evidence=2),
 'contest':dict(cost=.10,privacy_safeguards=2),
 'mandatory_compliance_fallback':dict(cost=0)}
PARTNERSHIPS={
 'preferred':dict(cost=.30,commercial_dependency=3,commercial_opportunity=3,artist_autonomy=-2,partnership_standing=1),
 'nonexclusive':dict(cost=.25,commercial_dependency=1,commercial_opportunity=2,artist_autonomy=1,partnership_standing=1),
 'independent':dict(cost=.35,artist_autonomy=3,community_access=2,commercial_opportunity=1,partnership_standing=2),
 'services':dict(cost=.10,customer_support_readiness=1,technical_reliability=1),
 'maintenance_fallback':dict(cost=0)}
SCORES=('customer_trust','workforce_conditions','technical_reliability','sustainability','partnership_standing')


def initialize(state):
    for key in ('entry_efficiency','entry_assistance','biometric_capability','biometric_exposure','entry_contract_value_m','security_cooperation','privacy_safeguards','data_disclosure_exposure','stakeholder_conflict','commercial_dependency','artist_autonomy','community_access','security_assurance','regulatory_scrutiny','meridian_revenue_m','independent_revenue_m'):
        state[key]=0
    for key in ('facial_entry_selected','facial_entry_authorized','facial_entry_operational','smart_entry_selected','staffed_entry_selected','entry_contract_active','entry_contract_pending','entry_compliance_review','entry_remediation_required','law_enforcement_request_received','law_enforcement_request_resolved','law_enforcement_disclosure_made','law_enforcement_data_preserved','law_enforcement_legal_review','law_enforcement_request_contested','law_enforcement_deadline_pending','data_minimization_completed','artist_partnership_active','commercial_partnership_active','partnership_conditions_disputed','community_program_active','year9_contract_review_required','independent_programme_pending','independent_programme_active','data_handling_review_required','artist_privacy_dialogue','facial_contract_not_activated','mandatory_vfi_active'):
        state[key]=False


def clamp(state):
    for key in SCORES:state[key]=max(0,min(100,state[key]))


def available_data(state):
    categories=['ticket_purchases','account_and_contact_details','transaction_history']
    if state['vfi_operational'] or state.get('identity_records_retained'):categories+=['verification_status','identity_linked_account_records']
    if state['data_linkage_capability']>0:categories.append('additional_account_purchase_links')
    if state.get('biometric_records_retained'):categories.append('biometric_entry_records')
    return categories


def start_year(state,year):
    if year==6:state['mandatory_vfi_active']=state['vfi_operational'] and not state['mandatory_verification_suspended']
    if year==7:state['available_data_categories']=available_data(state)
    state['annual_baseline_revenue']=24.0
    venue=state['entry_contract_value_m'] if state['entry_contract_active'] and year>=state.get('entry_revenue_start_year',99) else 0
    meridian=state['meridian_revenue_m'] if year>=9 and state['commercial_partnership_active'] else 0
    independent=state['independent_revenue_m'] if year>=9 and state['independent_programme_active'] else 0
    biometric=state.get('biometric_venue_contract_value_m',0) if state.get('biometric_venue_contract_active') and year>=state.get('biometric_venue_revenue_start_year',99) else 0
    state['reported_annual_revenue']=24+state['contract_revenue']+venue+meridian+independent+biometric


def before_external(state,year):
    if year==6:state.update(market_entry_technology_interest='high',regulatory_scrutiny=state['regulatory_scrutiny']+1)
    elif year==7:state['law_enforcement_request_received']=True
    elif year==8:state['market_consolidation_pressure']='high'


def cost(state,year,option):
    rule=ENTRY if year==6 else POLICE if year==7 else PARTNERSHIPS
    amount=rule[option]['cost']
    if year==6 and option=='facial' and not state['vfi_operational']:amount+=.3
    return amount


def apply(state,year,option):
    rule=(ENTRY if year==6 else POLICE if year==7 else PARTNERSHIPS)[option]
    for key,value in rule.items():
        if key!='cost':state[key]+=value
    if year==6:
        state['selected_entry']=option
        if option=='facial':
            state.update(facial_entry_selected=True,entry_contract_pending=True,entry_compliance_review=True,facial_entry_authorized=False,facial_entry_operational=False,entry_contract_value_m=1.4)
            if state.get('integration_governance_outstanding'):state['entry_governance_finding']=True
            if state['assurance_evidence']>=3:state['security_assurance']+=1
        elif option in ('smart','staffed'):
            state[option+'_entry_selected']=True
            state.update(entry_contract_active=True,entry_contract_value_m=.85 if option=='smart' else .95,entry_revenue_start_year=7,entry_contract_activation_year=6,entry_contract_term_years=5)
            if option=='smart' and state['technical_reliability']>=70:state['partnership_standing']+=1
            if option=='staffed':
                if state.get('support_training_outstanding'):
                    state['support_training_outstanding']=False;state['workforce_pressure']=max(0,state['workforce_pressure']-1)
                if state.get('verification_remediation_required'):
                    state['verification_remediation_required']=False;state['customer_trust']+=1
    elif year==7:
        state['law_enforcement_data_preserved']=True
        state['law_enforcement_legal_review']=option!='mandatory_compliance_fallback'
        if option=='cooperate':state['law_enforcement_deadline_pending']=True
        if option=='contest':state['law_enforcement_request_contested']=True
        if option=='mandatory_compliance_fallback':state['mandatory_compliance_fallback']=True
    else:
        state['partnership_choice']=option
        if option in ('preferred','nonexclusive'):
            state['commercial_partnership_active']=True
            state['meridian_revenue_m']=2.0 if option=='preferred' else 1.1
            state['meridian_revenue_start_year']=9
            if option=='preferred':state['year9_contract_review_required']=True
        elif option=='independent':
            state['artist_partnership_active']=True
            state['independent_revenue_m']=.65
            state['independent_programme_active']=state['partnership_standing']>=72
            state['independent_programme_pending']=not state['independent_programme_active']
    clamp(state)


def conditional(state,year,option,content):
    messages=[]
    if year==7:
        state.update(law_enforcement_request_resolved=True,law_enforcement_disclosure_made=True,law_enforcement_deadline_pending=False)
        state['disclosed_data_categories']=list(state['available_data_categories'])
        state['disclosure_scope']='authorized_transactions_and_accounts_only'
        defs=content['disclosure_modifiers']
        if state['vfi_operational']:
            messages.append(defs['1']);state['security_cooperation']+=1;state['data_disclosure_exposure']+=1
        else:messages.append(defs['2'])
        if state['data_linkage_capability']>0:
            messages.append(defs['3']);state['security_assurance']+=1;state['data_disclosure_exposure']+=1
        if state['privacy_safeguards']>=2:
            messages.append(defs['4']);state['customer_trust']+=1
        if state['assurance_evidence']<2 and state['privacy_safeguards']<2:
            messages.append(defs['5']);state['legal_exposure']+=1;state['data_handling_review_required']=True
    if year==8:
        defs=content['partnership_modifiers']
        if option=='preferred':
            if state['commercial_dependency']>=3:
                messages.append(defs['1']);state['stakeholder_conflict']+=1;state['partnership_conditions_disputed']=True
            if state['financial_pressure']>=1:
                messages.append(defs['2']);state['workforce_concerns']=max(0,state['workforce_concerns']-1)
        if option=='nonexclusive' and state['partnership_standing']>=73:
            messages.append(defs['3']);state['partnership_standing']+=1;state['customer_trust']+=1
        if option=='independent' and any(state.get(key) for key in ('independent_festival_opportunity','artist_collective_opportunity','boycott_alternative_supplier_opportunity')):
            messages.append(defs['4']);state['independent_programme_active']=True;state['independent_programme_pending']=False;state['partnership_standing']+=1
        if option=='services':
            for key in ('customer_compensation_review','review_remediation_required','data_handling_review_required'):
                if state.get(key):
                    messages.append(defs['5']);state[key]=False;state['customer_trust']+=1;break
    clamp(state)
    return messages


def primary(state,year,option,content):
    if year==6:
        if option=='facial' and state['assurance_evidence']<3:
            number=1;state['entry_remediation_required']=True
        elif option=='facial':number=2;state['security_assurance']+=1
        elif option=='smart' and state['technical_reliability']>=70:
            number=3;state['partnership_standing']+=1;state['customer_trust']+=1
        elif option=='staffed' and state['cash']<2:
            number=4;state['financial_pressure']+=1;state['workforce_concerns']+=1
        elif not state['entry_contract_active'] and not state['entry_contract_pending'] and state['customer_trust']>=72:
            number=5;state['independent_festival_opportunity']=True
        else:number=6
    elif year==7:
        if state['data_linkage_capability']>0 and state['privacy_safeguards']<2:
            number=1;state['customer_trust']-=1;state['data_handling_review_required']=True
        elif state['privacy_safeguards']>=2:
            number=2;state['customer_trust']+=1;state['partnership_standing']+=1
        elif state['workforce_pressure']>=2:
            number=3;state['labour_dispute_risk']+=1;state['staff_escalation_review']=True
        elif state['partnership_standing']>=73:
            number=4;state['artist_privacy_dialogue']=True;state['partnership_standing']+=1
        else:number=5
    else:
        if option=='preferred' and state['commercial_dependency']>=3:
            number=1;state['partnership_conditions_disputed']=True;state['partnership_standing']-=1;state['year9_contract_review_required']=True
        elif state['artist_partnership_active'] and not state['independent_programme_pending']:
            number=2;state['partnership_standing']+=1;state['customer_trust']+=1
        elif option=='nonexclusive' and state['technical_reliability']>=70:
            number=3;state['partnership_standing']+=1;state['commercial_opportunity']+=1
        elif state['workforce_pressure']>=2:
            number=4;state['workforce_conditions']-=1;state['labour_dispute_risk']+=1
        else:number=5
    clamp(state)
    definitions=content['internal'][str(year)]
    key=next(k for k in definitions if k.startswith(str(number)+'.'))
    return dict(id=f'I{year}',title='Company update',rule=key,text=definitions[key])


def biometric_authorized(state):
    return bool(state['entry_compliance_review'] and state['assurance_evidence']>=3 and not state['entry_remediation_required'] and (state['entry_assistance']>=1 or state['human_assistance_capacity']>=2) and not state.get('integration_governance_outstanding'))


def facial_compliance(state):
    if not state['facial_entry_selected'] or not state['entry_contract_pending']:return
    authorized=biometric_authorized(state)
    state.update(facial_entry_authorized=bool(authorized),facial_entry_operational=bool(authorized),entry_contract_active=bool(authorized),entry_contract_pending=False)
    if authorized:
        state.update(entry_revenue_start_year=8,entry_contract_activation_year=7,entry_contract_term_years=5,facial_authorization_scope='optional_entry_with_nonbiometric_alternative')
        state['biometric_capability']=1
    else:state['facial_contract_not_activated']=True
