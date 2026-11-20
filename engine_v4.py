"""Authoritative 2027–2036 rules. Cash is in millions, with a deduplicated ledger."""
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import json
import rules_6_8 as later_rules
import rules_9_10 as closing_rules
import powers_v4 as powers
import platform_shift as platform

CONTENT=json.loads((Path(__file__).parent/'v4_scenarios.json').read_text(encoding='utf-8'))
VERSION=CONTENT['version']
DEFAULTS={int(y):s['default'] for y,s in CONTENT['years'].items()}
INITIAL=dict(cash=6.0,annual_baseline_revenue=24.0,employees=120,customer_trust=70,
 workforce_conditions=70,technical_reliability=70,sustainability=70,partnership_standing=70,
 technical_independence=0,supplier_dependence=0,internal_capability=0,reliability_readiness=0,
 customer_readiness=0,development_progress=0,assurance_evidence=0,workforce_pressure=0,
 labour_dispute_risk=0,legal_exposure=0,workforce_concerns=0,vfi_operational=False,
 procurement=None,northstar_contract=None,annual_vfi_cost=0,contract_revenue=0)
PROCUREMENT={
 'build':dict(cost=2.8,technical_independence=3,supplier_dependence=0,internal_capability=2,development_progress=0,annual_vfi_cost=.45),
 'license':dict(cost=.6,technical_independence=-2,supplier_dependence=3,internal_capability=0,development_progress=2,annual_vfi_cost=.9),
 'hybrid':dict(cost=1.6,technical_independence=1,supplier_dependence=2,internal_capability=1,development_progress=1,annual_vfi_cost=.65),
 'wait':dict(cost=.15,technical_independence=0,supplier_dependence=0,internal_capability=0,development_progress=0,annual_vfi_cost=0)}
TESTING={
 'stress':dict(cost=.30,reliability_readiness=2,customer_readiness=0,development_progress=0,assurance_evidence=1,workforce_pressure=1),
 'customer':dict(cost=.25,reliability_readiness=0,customer_readiness=2,development_progress=0,assurance_evidence=1,workforce_pressure=0),
 'accelerate':dict(cost=.15,reliability_readiness=-1,customer_readiness=-1,development_progress=2,assurance_evidence=0,workforce_pressure=2),
 'assessment':dict(cost=.35,reliability_readiness=1,customer_readiness=1,development_progress=-1,assurance_evidence=2,workforce_pressure=0)}
CONTRACTS={'full_awarded':(.6,2.4),'pilot_awarded':(.25,.8),'conventional_awarded':(.15,1),
 'full_conditional':(.05,0),'pilot_conditional':(.05,0),'unsuccessful':(.05,0),'declined':(0,0)}


FEATURES={
 'fan_rewards':dict(cost=.30,customer_convenience=1,customer_support_readiness=0,commercial_opportunity=2,support_workload=1),
 'payday_reservations':dict(cost=.35,customer_convenience=2,customer_support_readiness=0,commercial_opportunity=1,support_workload=1),
 'ticket_transfers':dict(cost=.40,customer_convenience=2,customer_support_readiness=0,commercial_opportunity=1,support_workload=1),
 'service_improvements':dict(cost=.20,customer_convenience=1,customer_support_readiness=2,commercial_opportunity=0,support_workload=-1)}
RESPONSES={
 'verification_suspended':dict(cost=.40,human_assistance_capacity=1,assurance_evidence=0,customer_support_readiness=1,workforce_demand=0),
 'independent_review':dict(cost=.30,human_assistance_capacity=0,assurance_evidence=2,customer_support_readiness=0,workforce_demand=0),
 'human_assistance_expanded':dict(cost=.50,human_assistance_capacity=3,assurance_evidence=0,customer_support_readiness=2,workforce_demand=2),
 'operations_defended':dict(cost=.15,human_assistance_capacity=0,assurance_evidence=0,customer_support_readiness=0,workforce_demand=0)}
for key in ('customer_convenience','customer_support_readiness','commercial_opportunity','support_workload','data_linkage_capability','human_assistance_capacity','commercial_continuity','workforce_demand','financial_pressure'):
    INITIAL[key]=0
for key in ('fan_rewards','payday_reservations','ticket_transfers','service_improvements','independent_festival_opportunity','reservation_terms_review','boycott_alternative_supplier_opportunity','boycott_customer_complaints','review_remediation_required','customer_compensation_review','staff_escalation_review','artist_collective_opportunity','mandatory_verification_suspended'):
    INITIAL[key]=False
later_rules.initialize(INITIAL)
closing_rules.initialize(INITIAL)
platform.initialize(INITIAL)
INITIAL.update(vfi_operating_payable_m=0,financial_distress=False,supplier_payment_at_risk=False,operating_payable_m=0)


def scenario(company,year):
    if year==6 and company.get('platform_shift_version')==1:
        original=company.get('decisions',{}).get('1',{}).get('option','wait')
        return CONTENT['platform_shift']['year6_branches'][original]
    original=CONTENT['years'][str(year)]
    recorded=company.get('decisions',{}).get(str(year))
    terminology=recorded.get('terminology_version',0) if recorded is not None else company.get('terminology_version',0)
    return platform.rename_terms(original) if year<=5 and terminology==1 else original


def scenario_for_state(state,year):
    if year==6 and state.get('platform_shift_applies'):
        return CONTENT['platform_shift']['year6_branches'][platform.branch(state)]
    return CONTENT['years'][str(year)]


def default_option(company,year):
    return scenario(company,year)['default']


def mandatory_verification(state):
    return state['vfi_operational'] and not state['mandatory_verification_suspended']


def apply_later_decision(result,year,option):
    state=result['state']
    rule=(FEATURES if year==4 else RESPONSES)[option]
    charge(result,year,'feature' if year==4 else 'boycott_response',rule['cost'])
    for key,value in rule.items():
        if key!='cost':state[key]+=value
    if year==4:
        state['selected_feature']=option
        state[option]=True
        if option in ('fan_rewards','ticket_transfers') and state['vfi_operational']:
            state['data_linkage_capability']+=1
    else:
        state['boycott_response']=option
        if option=='verification_suspended':
            if mandatory_verification(state):state['commercial_continuity']-=1
            state['mandatory_verification_suspended']=True
        elif option=='operations_defended':state['commercial_continuity']+=1
    if option in ('service_improvements','human_assistance_expanded'):
        if state.get('verification_remediation_required'):
            state['verification_remediation_required']=False
            if year==4:
                state['customer_trust']+=1;state['customer_support_readiness']+=1
        if state.get('support_training_outstanding'):
            state['support_training_outstanding']=False
            if year==4:state['workforce_pressure']=max(0,state['workforce_pressure']-1)
    if state['cash']>=2.5:state['restructuring_proposed_12']=False


def boycott_modifiers(state,option):
    definitions=CONTENT['boycott_modifiers'];messages=[]
    def add(number):
        key=next(k for k in definitions if k.startswith(str(number)+'.'))
        messages.append(definitions[key])
    if not mandatory_verification(state) and state['customer_trust']>=72:
        add(1);state['partnership_standing']+=2;state['boycott_alternative_supplier_opportunity']=True
    if state['vfi_operational'] and state['customer_support_readiness']>=2:
        add(2);state['customer_trust']+=1;state['partnership_standing']+=1
    if state['vfi_operational'] and readiness(state)['customer_readiness']<2 and not state['mandatory_verification_suspended']:
        add(3);state['customer_trust']-=2;state['partnership_standing']-=1;state['boycott_customer_complaints']=True
    weaknesses=state['customer_readiness']<2 or state.get('verification_remediation_required') or state.get('integration_governance_outstanding')
    if option=='independent_review':
        if weaknesses:
            add(4);state['review_remediation_required']=True;state['assurance_evidence']+=1
        else:
            add(5);state['customer_trust']+=1;state['assurance_evidence']+=1
    if state['cash']<1.5:
        add(6);state['financial_pressure']+=1;state['workforce_concerns']+=1
    if state['partnership_standing']>=73:
        add(7);state['partnership_standing']+=1
    return messages


def later_primary_event(state,year,option):
    definitions=CONTENT['internal'][str(year)]
    if year==4:
        if not state['vfi_operational'] and state['customer_trust']>=72:
            number=1;state['partnership_standing']+=1;state['independent_festival_opportunity']=True
        elif state['vfi_operational'] and readiness(state)['customer_readiness']>=2:
            number=2;state['customer_trust']+=1;state['partnership_standing']+=1
        elif option=='payday_reservations' and state['cash']<2.5:
            number=3;state['financial_pressure']+=1;state['reservation_terms_review']=True
        elif option=='fan_rewards' and state['workforce_pressure']>=2:
            number=4;state['customer_trust']-=1;state['workforce_pressure']+=1
        else:number=5
    else:
        if mandatory_verification(state) and state['customer_readiness']<2:
            number=1;state['customer_trust']-=1;state['customer_compensation_review']=True
        elif state['workforce_pressure']>=2:
            number=2;state['labour_dispute_risk']+=1;state['staff_escalation_review']=True
        elif not state['vfi_operational'] and state['partnership_standing']>=72:
            number=3;state['artist_collective_opportunity']=True
        elif state['customer_support_readiness']>=2:
            number=4;state['customer_trust']+=1
        else:number=5
    key=next(k for k in definitions if k.startswith(str(number)+'.'))
    return dict(id=f'I{year}',title='Company update',rule=key,text=definitions[key])


def charge(result,year,effect,amount):
    identifier=f"{result['session_id']}:{result['company_id']}:{year}:{effect}"
    if any(item['id']==identifier for item in result['ledger']):
        return
    cash=Decimal(str(result['state']['cash']))-Decimal(str(amount))
    if cash<0:
        raise ValueError('The company cannot afford this expenditure.')
    result['state']['cash']=float(cash)
    result['ledger'].append(dict(id=identifier,year=year,effect=effect,amount=-amount,balance=float(cash)))



VFI_PAYMENT_WARNING="Your company cannot cover its full VFI operating costs. The unpaid balance becomes an outstanding liability. The system remains operational for now, but suppliers are requesting a repayment plan, and future service continuity is uncertain."


def repay_payable(result,year,scope):
    identifier=f"{result['session_id']}:{result['company_id']}:{year}:repay_vfi_{scope}"
    if any(item['id']==identifier for item in result['ledger']):return
    state=result['state']
    due=state['vfi_operating_payable_m']
    payment=min(state['cash'],due)
    if payment:
        charge(result,year,'repay_vfi_'+scope,payment)
        state['vfi_operating_payable_m']=float(Decimal(str(due))-Decimal(str(payment)))
    if state['vfi_operating_payable_m']==0:state['supplier_payment_at_risk']=False
    other=state.get('operating_payable_m',0)
    paid=min(state['cash'],other)
    if paid:
        charge(result,year,'repay_operating_'+scope,paid)
        state['operating_payable_m']=float(Decimal(str(other))-Decimal(str(paid)))


def annual_vfi(result,year):
    identifier=f"{result['session_id']}:{result['company_id']}:{year}:annual_vfi_cost"
    if any(item['id']==identifier for item in result['ledger']):return
    state=result['state']
    repay_payable(result,year,'start')
    if not state['vfi_operational'] and not platform.supported_supplier_fee(state,year):return
    fee=state['annual_vfi_cost']
    paid=min(state['cash'],fee)
    charge(result,year,'annual_vfi_cost',paid)
    unpaid=float(Decimal(str(fee))-Decimal(str(paid)))
    if unpaid:
        state['vfi_operating_payable_m']=float(Decimal(str(state['vfi_operating_payable_m']))+Decimal(str(unpaid)))
        state.update(financial_distress=True,supplier_payment_at_risk=True)
        state['financial_pressure']+=1
        result.setdefault('annual_notices',{})[str(year)]=VFI_PAYMENT_WARNING.replace('VFI operating costs','verification operating costs') if year>=6 and state.get('platform_shift_applies') and not state.get('vfi_supplier_contract') else VFI_PAYMENT_WARNING
        result['ledger'].append(dict(id=f"{result['session_id']}:{result['company_id']}:{year}:unpaid_vfi",year=year,effect='unpaid_vfi_operating_cost',amount=0,liability_change=unpaid,balance=state['cash']))


def credit(result,year,effect,amount):
    identifier=f"{result['session_id']}:{result['company_id']}:{year}:{effect}"
    if any(item['id']==identifier for item in result['ledger']):return
    charge(result,year,effect,-amount)
    repay_payable(result,year,effect)


def option_definition(year,option,company=None,state=None):
    current=scenario(company,year) if company is not None else scenario_for_state(state,year) if state is not None else CONTENT['years'][str(year)]
    selected=next((o for o in current['options'] if o['id']==option),None)
    if selected:return selected
    if option in ('formal_objection','supplier_continuity'):
        text=('Your company files a formal objection without new expenditure. The supplier transition deadline remains in force.' if option=='formal_objection' else 'Your company makes no new investment and continues its existing services.')
        title='Zero-cost formal objection' if option=='formal_objection' else 'Zero-cost continuity'
    elif option=='continuity_fallback':
        text='No new investment. No restructuring. No layoffs. Existing contracts are preserved.'
        title='Continuity under financial constraint'
    elif option=='executive_conflict_fallback':
        text='The decision is deferred because executive blocks leave no feasible option. No new commitment is made. Binding legal obligations remain in force.'
        title='Decision deferred due to executive conflict'
    elif option=='mandatory_compliance_fallback':
        text='Preserve the records covered by the binding order. Disclose only the information required by the subsequent valid narrowed order. No optional legal services are purchased.'
        title='Mandatory compliance fallback'
    elif option=='maintenance_fallback':
        text='No new investment. No new contract. No additional state changes.'
        title='Zero-cost maintenance fallback'
    else:raise ValueError('Unknown decision option.')
    return dict(id=option,title=title,detail=text,outcome=text,private={role:text for role in current['info']})


def readiness(state):
    development=max(0,state['development_progress']-int(bool(state.get('recruitment_pressure'))))
    reliability=max(0,state['reliability_readiness']-int(bool(state.get('integration_responsibility_unresolved') or state.get('integration_governance_outstanding'))))
    customer=max(0,state['customer_readiness']-int(bool(state.get('support_training_needed') or state.get('support_training_outstanding'))))
    return dict(development_progress=development,reliability_readiness=reliability,customer_readiness=customer)


def start_year(result,year):
    state=result['state']
    if year==3:
        charge(result,3,'economic_shock',.24)
        state['annual_baseline_revenue']=21.6
        if state['procurement']!='wait':
            state['development_progress']=max(0,state['development_progress']+1)
        state['reliability_readiness']=max(0,state['reliability_readiness'])
        state['customer_readiness']=max(0,state['customer_readiness'])
        state['economic_shock_applied']=True
        state['effective_readiness']=readiness(state)
        effective=state['effective_readiness']
        state['vfi_operational']=state['procurement'] in ('build','license','hybrid') and effective['development_progress']>=2 and effective['reliability_readiness']>=1
    if year==4:
        state['annual_baseline_revenue']=24.0
        state['market_demand_multiplier']=1.0
        if state['procurement'] in ('build','license','hybrid'):
            state['development_progress']=max(0,state['development_progress']+1)
        state['recruitment_pressure_history']=bool(state.get('recruitment_pressure'))
        state['recruitment_pressure']=False
        state['support_training_outstanding']=state.pop('support_training_needed',False)
        state['integration_governance_outstanding']=state.pop('integration_responsibility_unresolved',False)
        state['effective_readiness']=readiness(state)
        effective=state['effective_readiness']
        state['vfi_operational']=state['procurement'] in ('build','license','hybrid') and effective['development_progress']>=2 and effective['reliability_readiness']>=1
        pending=state['northstar_contract']
        if pending in ('full_conditional','pilot_conditional'):
            full=pending=='full_conditional'
            cost=.55 if full else .20
            required=3 if full else 2
            if state['vfi_operational'] and effective['development_progress']>=required and state['cash']>=cost:
                charge(result,4,'northstar_activation',cost)
                state['northstar_contract']='full_awarded' if full else 'pilot_awarded'
                state['contract_revenue']=2.4 if full else .8
            else:
                state['northstar_contract']='expired'
                state['contract_revenue']=0
        if state['cash']>=2.5:
            state['restructuring_proposed_12']=False
        state['regional_opportunity_expires_after']=5 if state.get('regional_opportunity') else None
        state['reported_annual_revenue']=state['annual_baseline_revenue']+state['contract_revenue']
        annual_vfi(result,4)
        result['handoff']=deepcopy(state)
    if year==5:annual_vfi(result,5)
    if year>=6:
        state['regional_opportunity']=False
        if state.get('platform_shift_applies'):platform.before_annual(state,year)
        annual_vfi(result,year)
        if state.get('platform_shift_applies'):platform.after_annual(state,year)
        later_rules.start_year(state,year)


def contract_status(state,option):
    effective=readiness(state)
    development=effective['development_progress']
    reliability=effective['reliability_readiness']
    cash=state['cash']
    if option=='decline':return 'declined'
    if option=='conventional':return 'conventional_awarded' if state['technical_reliability']>=65 and cash>=.15 else 'unsuccessful'
    full=option=='full'
    required=3 if full else 2
    cost=.6 if full else .25
    if state['vfi_operational'] and development>=required and reliability>=1 and cash>=cost:
        return 'full_awarded' if full else 'pilot_awarded'
    if state['procurement'] in ('build','license','hybrid') and development>=1 and cash>=.05:
        return 'full_conditional' if full else 'pilot_conditional'
    return 'unsuccessful'


def cost(state,year,option):
    if option=='executive_conflict_fallback':return 0
    if year==6 and state.get('platform_shift_applies'):return platform.cost(state,option)
    if year>=9:return closing_rules.cost(state,year,option)
    if year==1:return PROCUREMENT[option]['cost']
    if year==2:return TESTING[option]['cost']
    if year==3:return CONTRACTS[contract_status(state,option)][0]
    if year>=6:return later_rules.cost(state,year,option)
    return (FEATURES if year==4 else RESPONSES)[option]['cost']


def available(state,year,option):
    return state['cash']>=cost(state,year,option)


def primary_event(result,year,option):
    state=result['state']
    if year==6 and state.get('platform_shift_applies'):return platform.primary(state,option,CONTENT['platform_shift'])
    if year>=9:return closing_rules.primary(state,year,option,CONTENT)
    if year>=6:return later_rules.primary(state,year,option,CONTENT)
    if year>=4:return later_primary_event(state,year,option)
    variants=CONTENT['internal'][str(year)]
    if year==1:
        key={'build':'Build','license':'License','hybrid':'Hybrid','wait':'Wait'}[option]
        if option=='build':
            state['workforce_pressure']+=1
            state['recruitment_pressure']=True
        elif option=='license':state['support_training_needed']=True
        elif option=='hybrid':state['integration_responsibility_unresolved']=True
        else:state.update(northstar_vfi_interest=True,conventional_market_opportunity=True)
    elif year==2:
        if state['cash']<2.5:
            key='1. Low reserves';state['restructuring_proposed_12']=True;state['workforce_concerns']+=1
        elif state['workforce_pressure']>=2:
            key='2. High workforce pressure';state['workforce_conditions']-=1;state['labour_dispute_risk']+=1
        elif state['customer_readiness']>=2:
            key='3. Strong customer readiness';state['customer_trust']+=1
        elif state['reliability_readiness']>=2:
            key='4. Strong reliability';state['partnership_standing']+=1
        else:key='5. Otherwise'
    else:
        status=state['northstar_contract']
        if status=='full_awarded':
            if readiness(state)['customer_readiness']<2:
                key='1. Full awarded + low customer readiness'
                state['customer_trust']-=1;state['workforce_pressure']+=1;state['verification_remediation_required']=True
            else:
                key='2. Full awarded + adequate customer readiness'
                state['customer_trust']+=1;state['partnership_standing']+=1
        elif status=='pilot_awarded':
            key='3. Pilot awarded';state['pilot_review_pending']=True;state['pilot_expansion_opportunity']=True
        elif status=='conventional_awarded':
            key='4. Conventional awarded';state['partnership_standing']+=1;state['scalping_concerns']=True
        elif state['cash']>=3:
            key='5. No active contract + cash at least €3M';state['regional_opportunity']=True
        else:key='6. Otherwise'
    return dict(id=f'I{year}',title='Company update',rule=key,text=variants[key])


def private_outcome(year,option,status,role,company=None,state=None):
    current=scenario(company,year) if company is not None else CONTENT['years'][str(year)]
    selected=option_definition(year,option,company,state)
    message=selected['private'][role]
    if year==3:
        if status=='unsuccessful':return current['unsuccessful_private']
        if status.endswith('_conditional'):return current['conditional_prefix']+' '+message
    return message


def replay(company):
    result=dict(session_id=company.get('session_id','test'),company_id=company.get('id','test'),state=deepcopy(INITIAL),ledger=[],timeline=[])
    state=result['state']
    state['platform_shift_applies']=company.get('platform_shift_version')==1
    if state['platform_shift_applies']:platform.initialize_data(state)
    last_year=0
    for year_text,decision in sorted(company.get('decisions',{}).items(),key=lambda entry:int(entry[0])):
        year=int(year_text)
        if year>10:break
        if year!=last_year+1:raise ValueError('Decisions must resolve in annual order.')
        start_year(result,year)
        current_scenario=scenario(company,year)
        state['active_terminology_version']=decision.get('terminology_version',0)
        round_powers=[i for i in company.get('interventions',[]) if i['year']==year and i.get('power_spec_version')==1]
        power_effects=powers.apply(result,year,round_powers,charge,CONTENT)
        for intervention in company.get('interventions',[]):
            if intervention['year']==year and not intervention.get('power_spec_version'):
                if intervention.get('cost') is not None:
                    charge(result,year,'power_'+intervention['role'],intervention['cost'])
        if year>=9:closing_rules.before_external(state,year)
        elif year>=6 and not (year==6 and state.get('platform_shift_applies')):later_rules.before_external(state,year)
        option=decision['option']
        resolution=decision.get('resolution_mode','student_decision')
        blocked={item.get('option') for item in company.get('interventions',[]) if item['year']==year and item['role'] in ('cfo','cto')}
        if option in blocked:
            if resolution=='student_decision':raise ValueError('The proposed option is blocked by an executive power.')
            feasible=[item['id'] for item in current_scenario['options'] if item['id'] not in blocked and available(state,year,item['id'])]
            if not feasible:
                option=platform.fallback(state,blocked) if year==6 and state.get('platform_shift_applies') else {7:'mandatory_compliance_fallback',8:'maintenance_fallback',9:'continuity_fallback'}.get(year,'executive_conflict_fallback')
                state['decision_deferred_due_to_executive_conflict']=True
            else:option=min(feasible,key=lambda candidate:cost(state,year,candidate))
        if not available(state,year,option):
            feasible=[item['id'] for item in current_scenario['options'] if item['id'] not in blocked and available(state,year,item['id'])]
            if not feasible:
                if year==6 and state.get('platform_shift_applies'):feasible=[platform.fallback(state,blocked)]
                elif year==7:feasible=['mandatory_compliance_fallback']
                elif year==8:feasible=['maintenance_fallback']
                elif year==9:feasible=['continuity_fallback']
                elif blocked or round_powers:feasible=['executive_conflict_fallback']
                else:raise ValueError('No affordable decision remains.')
            if resolution=='student_decision':raise ValueError('The company cannot afford this option.')
            if year==6 and state.get('platform_shift_applies'):option=platform.fallback(state,blocked)
            elif year==9:
                option=next((o for o in ('reinvest','specialize','restructure','continuity_fallback') if o in feasible),'continuity_fallback')
            elif year==10:option=next((o for o in ('detailed_report','focused_report','board_statement') if o in feasible),feasible[0])
            else:option=min(feasible,key=lambda candidate:cost(state,year,candidate))
            resolution='financial_fallback'
        current=current_scenario
        selected=option_definition(year,option,company,state)
        if option=='executive_conflict_fallback':
            state['decision_deferred_due_to_executive_conflict']=True
        elif year==1:
            rule=PROCUREMENT[option]
            charge(result,year,'procurement',rule['cost'])
            state.update({key:value for key,value in rule.items() if key!='cost'})
            state['procurement']=option
            platform.procurement(state,option)
        elif year==2:
            rule=TESTING[option]
            charge(result,year,'preparation',rule['cost'])
            for key,value in rule.items():
                if key!='cost':state[key]+=value
            if state['procurement']=='wait':state['development_progress']=0
            if state['procurement']=='build' and option=='stress':state['recruitment_pressure']=False
            if state['procurement']=='build' and option=='accelerate':state['workforce_pressure']+=1
            if state['procurement']=='license':
                if option in ('stress','assessment'):state['supplier_assessed']=True
                if option=='customer':state['support_training_needed']=False
            if state['procurement']=='hybrid' and option in ('stress','assessment'):state['integration_responsibility_unresolved']=False
            if state['procurement']=='wait' and option=='customer':state['customer_demand_evidence']=True
            if state['procurement']=='wait' and option=='assessment':state['supplier_evaluation_ready']=True
        elif year==3:
            status=contract_status(state,option)
            amount,revenue=CONTRACTS[status]
            charge(result,year,'northstar_bid',amount)
            state['northstar_contract']=status
            state['contract_revenue']=revenue
        elif year<=5:
            apply_later_decision(result,year,option)
        elif year==6 and state.get('platform_shift_applies'):
            state['year6_exit_cost_m']=platform.cost(state,'exit_supplier') if platform.branch(state) in ('license','hybrid') else None
            state['year6_exit_affordable']=state['cash']>=state['year6_exit_cost_m'] if state['year6_exit_cost_m'] is not None else None
            charge(result,year,'annual_decision',platform.cost(state,option))
            platform.apply(state,option,CONTENT['platform_shift'])
        elif year>=9:
            charge(result,year,'annual_decision',closing_rules.cost(state,year,option))
            closing_rules.apply(state,year,option)
        else:
            charge(result,year,'annual_decision',later_rules.cost(state,year,option))
            later_rules.apply(state,year,option)
        external=deepcopy(CONTENT['platform_shift']['external'] if year==6 and state.get('platform_shift_applies') else CONTENT['external'][str(year)])
        if year<=5 and state.get('active_terminology_version')==1:external=platform.rename_terms(external)
        external['id']=f'E{year}'
        if year==1:state.update(market_vfi_interest='growing',market_standardization='unsettled')
        elif year==2:state.update(year3_demand_multiplier=.9,year3_cash_shock_scheduled=.24)
        elif year==3:state.update(market_vfi_interest='mainstream',market_accessibility_scrutiny='elevated')
        elif year==4:state.update(market_demand_multiplier=1.0,annual_baseline_revenue=24.0)
        modifiers=closing_rules.conditional(state,year,option,CONTENT) if year>=9 else boycott_modifiers(state,option) if year==5 else later_rules.conditional(state,year,option,CONTENT) if year>=6 and not (year==6 and state.get('platform_shift_applies')) else []
        if year==8 and state.get('platform_shift_applies'):
            activation=platform.commercialize(state,option)
            if activation:modifiers.append(activation)
        internal=primary_event(result,year,option) if option!='executive_conflict_fallback' else dict(id=f'I{year}',title='Decision deferred',text='No new commitment is made while the executive conflict remains unresolved.')
        if year==7:
            if state.get('platform_shift_applies'):platform.authorize(state,later_rules.biometric_authorized)
            else:later_rules.facial_compliance(state)
        if year<=5 and state.get('active_terminology_version')==1:internal=platform.rename_terms(internal)
        state['financially_vulnerable']=state['cash']<1
        state['liquidity_distress']=state['cash']==0
        later_rules.clamp(state)
        status=state['northstar_contract'] or ''
        if year!=3 or option=='executive_conflict_fallback':outcome=selected['outcome']
        else:outcome=current['proposals'][['full','pilot','conventional','decline'].index(option)]+'\n\n'+current['resolved'][status]
        if year==6 and state.get('platform_shift_applies') and option=='negotiate_terms':outcome+='\n\n'+CONTENT['platform_shift']['exemption_granted' if state['vfi_exemption_granted'] else 'exemption_denied']
        if year==5 and not state['vfi_operational'] and option=='verification_suspended':outcome=current['nonadopter_suspend']
        if year==5 and decision.get('decision_source')=='expired_default':
            if option=='independent_review':outcome=current['expiry_announcement']+'\n\n'+outcome
            else:outcome='The independent review was unaffordable. Management applies the lowest-cost feasible response.\n\n'+outcome
        if year in (9,10) and decision.get('resolution_mode')=='deadline_expired':
            outcome=current['expiry_announcement']+'\n\n'+outcome
            if option!=DEFAULTS[year]:outcome+='\n\nApplied fallback: '+selected['title']
        if year==9 and option=='restructure':outcome+='\n\n'+current['layoffs_announcement' if state['year9_layoffs'] else 'no_layoffs_announcement']
        if year==2 and state['procurement']=='wait':
            outcome=outcome.replace('Your engineers','Your platform engineers').replace('The project','Work on your conventional platform').replace('launch','commercial delivery').replace('verification difficulties','difficulties using the existing platform')
        if year==7 and decision.get('resolution_mode')=='deadline_expired':outcome=current['expiry_announcement']+'\n\n'+outcome
        if year==8 and option=='independent' and state['independent_programme_pending']:outcome+='\n\n'+current['pending_announcement']
        if decision.get('resolution_mode')=='facilitator_skipped' and year<=4:
            announcements={1:'Management approves a hybrid VFI development programme, combining licensed verification technology with internally developed customer services. Initial investment: €1.6 million. Remaining cash: €4.4 million.',2:'Your company completes a routine technical testing and feasibility programme. The findings help prepare for future commercial decisions, although some questions remain unresolved.',3:'Your company submits a conventional ticketing proposal with enhanced fraud monitoring. Northstar evaluates the offer alongside competing providers.',4:'Management approves improvements to refunds, customer support and platform reliability. Customers benefit from faster assistance, while the company postpones major new commercial features.'}
            outcome=announcements[year]+('\n\n'+current['resolved'][status] if year==3 else '')
        if decision.get('resolution_mode')=='facilitator_skipped' and year in (6,8) and option==DEFAULTS[year] and not (year==6 and state.get('platform_shift_applies')):outcome=CONTENT['skipped_announcements'][str(year)]+'\n\n'+outcome
        result['timeline'].append(dict(year=year,option=option,resolution_mode=resolution,decision_source='financial_fallback' if resolution=='financial_fallback' and year>=6 else decision.get('decision_source',resolution),outcome=outcome,annual_notice=result.get('annual_notices',{}).get(str(year)),modifiers=modifiers,external_resolution=current.get('external_resolution'),external=external,internal=internal,private={role:private_outcome(year,option,status,role,company,state) for role in current['info']},state=deepcopy(state),power_effects=power_effects,scenario_title=current['title'],option_title=selected['title'],private_intelligence=deepcopy(current['info']),supplier_context=platform.context(state,year) if state.get('platform_shift_applies') else ''))
        last_year=year
    current_year=company.get('year',last_year)
    if current_year>last_year and current_year<=10:
        start_year(result,current_year)
        if current_year>=9:closing_rules.before_external(state,current_year)
        elif 6<=current_year<=8 and not (current_year==6 and state.get('platform_shift_applies')):later_rules.before_external(state,current_year)
    if current_year>last_year:state['active_terminology_version']=company.get('terminology_version',0)
    pending=[i for i in company.get('interventions',[]) if i['year']>last_year and i.get('power_spec_version')==1]
    result['pending_power_effects']=powers.apply(result,current_year,pending,charge,CONTENT) if pending else []
    for intervention in company.get('interventions',[]):
        if intervention['year']>last_year and intervention.get('cost') is not None and not intervention.get('power_spec_version'):
            charge(result,intervention['year'],'power_'+intervention['role'],intervention['cost'])
    return result
