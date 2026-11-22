"""Once-per-student executive powers, resolved in the supplied priority order."""
from copy import deepcopy
import platform_shift as platform
ORDER=('cfo','cto','legal','sustainability','relations','employee','marketing','ceo')
COSTS={'ceo':0,'cfo':0,'cto':0,'legal':.1,'sustainability':.1,'relations':.1,'employee':.2,'marketing':.15}
TECHNICAL={1:('build','license','hybrid'),2:('accelerate',),3:('full','pilot'),4:('fan_rewards','payday_reservations','ticket_transfers','service_improvements'),5:(),6:('facial','smart'),7:(),8:(),9:(),10:()}
FLAGS={'ceo':'ceo_override_used','cfo':'cfo_spending_freeze_used','cto':'cto_technical_veto_used','legal':'legal_review_used','sustainability':'sustainability_assessment_used','relations':'material_change_clause_used','employee':'employee_work_stoppage_used','marketing':'marketing_campaign_used'}

def technical_options(state,year):
    return platform.TECHNICAL if year==6 and state.get('platform_shift_applies') else TECHNICAL.get(year,())


def contracts(s):
    values=[]
    if s.get('northstar_contract') in ('full_awarded','pilot_awarded','conventional_awarded'):values.append(('Northstar',s['contract_revenue']))
    if s.get('entry_contract_active'):values.append(('Venue entry',s['entry_contract_value_m']))
    if s.get('biometric_venue_contract_active'):values.append(('Meridian biometric venue services',s['biometric_venue_contract_value_m']))
    if s.get('commercial_partnership_active'):values.append(('Meridian',s['meridian_revenue_m']))
    return values

def validate(s,y,role,option,decision_cost):
    if role=='cfo' and decision_cost<=0:return 'Choose an option with a positive discretionary expenditure.'
    if role=='cto' and option not in technical_options(s,y):return 'This option has no qualifying technical deployment or integration to veto.'
    if role in ('marketing','legal','sustainability','relations') and s['cash']<COSTS[role]:return 'The company cannot afford this executive power.'
    if role=='relations' and (not contracts(s) or y not in (4,5,6,7,8,9)):return 'A qualifying active contract and a documented material change are required.'
    return None

def apply(result,year,interventions,charge,content):
    import rules_9_10 as closing
    s=result['state'];effects=[]
    sequence=sorted(interventions,key=lambda i:ORDER.index(i['role']))
    for index,item in enumerate(sequence):
        role=item['role']
        if any(x['id']==f"{result['session_id']}:{result['company_id']}:{year}:power_{role}" for x in result['ledger']):continue
        before=deepcopy(s);due=COSTS[role];unpaid=0
        if role=='employee':
            reserved=sum(COSTS[i['role']] for i in sequence[index+1:] if i['role']!='employee')
            due=round(min(.2,max(0,s['cash']-reserved)),10);unpaid=round(.2-due,10)
        charge(result,year,'power_'+role,due)
        s[FLAGS[role]]=True
        if role=='cfo':
            s['financial_pressure']=max(0,s['financial_pressure']-1)
            if year in (3,6) and item.get('option') not in ('decline',):s['partnership_standing']-=1
        elif role=='cto':
            s['technical_reliability']+=1
            if s.get('procurement') not in (None,'wait') and not s['vfi_operational']:s['development_progress']=max(0,s['development_progress']-1)
            if contracts(s) and year in (4,6):s['partnership_standing']-=1
        elif role=='legal':
            s['assurance_evidence']+=1;s['legal_review_current_year']=True
            relevant=closing.obligations(s)
            if relevant:s.setdefault('formally_reviewed_obligations',[]).append({'year':year,'obligation':relevant[0]})
        elif role=='sustainability':
            s['assurance_evidence']+=1
            technical=item.get('option') in technical_options(s,year)
            if technical:s['sustainability_followup_required']=True
            s.setdefault('impact_assessments',[]).append({'year':year,'option':item.get('option'),'scope':['accessibility','resource use','workers','customers','local communities']})
        elif role=='relations':
            largest=max(contracts(s),key=lambda c:c[1]);s['partnership_standing']-=1;s['major_contract_renegotiation_pending']=True
            s['renegotiated_contract']=largest[0]
            if s['partnership_standing']>=73:s['contract_renegotiation_open']=True
            else:s['contract_dispute_pending']=True
        elif role=='employee':
            s['workforce_pressure']+=1;s['labour_dispute_risk']+=1;s['work_stoppage_current_year']=True
            if unpaid:
                s['operating_payable_m']=round(s.get('operating_payable_m',0)+unpaid,10);s['financial_distress']=True
                result['ledger'].append(dict(id=f"{result['session_id']}:{result['company_id']}:{year}:unpaid_work_stoppage",year=year,effect='unpaid_work_stoppage_cost',amount=0,liability_change=unpaid,balance=s['cash']))
            if s['workforce_conditions']<70:s['partnership_standing']-=1;s['workforce_negotiation_required']=True
            else:s['workforce_consultation_required']=True
        elif role=='marketing':
            if s['customer_trust']<70:s['customer_trust']+=1
            else:s['partnership_standing']+=1
            if any(s.get(k) for k in ('boycott_customer_complaints','customer_compensation_review')):s['communications_scrutiny']=True
        elif role=='ceo' and item.get('governance_conflict'):
            s['workforce_conditions']-=1;s['executive_governance_conflict']=True
        created=[k for k in closing.obligations(s) if k not in closing.obligations(before)]
        effects.append(dict(role=role,year=year,power=content['powers'][role]['name'],cost=due,unpaid=unpaid,announcement=content['powers'][role]['announcement'].replace('[option]',(platform.rename_terms if year<=5 and s.get('active_terminology_version')==1 else lambda x:x)(next((o['title'] for o in (content['platform_shift']['year6_branches'][platform.branch(s)] if year==6 and s.get('platform_shift_applies') else content['years'][str(year)])['options'] if o['id']==item.get('option')),item.get('option') or ''))),private=content['powers'][role]['private'],changes={k:{'before':before.get(k),'after':v} for k,v in s.items() if before.get(k)!=v},obligations_created=created))
    return effects
