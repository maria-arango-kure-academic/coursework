"""Supplier-dependent FacePass contracts, data claims and support transitions."""
from decimal import Decimal

PROVIDERS={'build':'in_house','license':'vfi','hybrid':'hybrid_vfi','wait':'none'}
TECHNICAL=('standard_facepass','enterprise_facepass','exit_supplier','develop_proprietary','license_independent','enter_biometrics','smart_entry')
COSTS={
 'license':{'standard_facepass':.35,'enterprise_facepass':.50,'negotiate_terms':.20,'exit_supplier':1.20,'formal_objection':0},
 'hybrid':{'standard_facepass':.45,'enterprise_facepass':.55,'negotiate_terms':.15,'exit_supplier':.75,'formal_objection':0},
 'build':{'develop_proprietary':.90,'license_independent':.60,'smart_entry':.40,'preserve_services':.10,'supplier_continuity':0},
 'wait':{'enter_biometrics':1.20,'smart_entry':.40,'staffed_entry':.45,'conventional_alternative':.10,'supplier_continuity':0}}


def rename_terms(value):
    if isinstance(value,str):return value.replace('Verified Fan Identity (VFI)','FairPass').replace('Verified Fan Identity','FairPass').replace('VFI','FairPass')
    if isinstance(value,list):return [rename_terms(v) for v in value]
    if isinstance(value,dict):return {k:rename_terms(v) for k,v in value.items()}
    return value


def initialize(s):
    s.update(identity_technology_provider='none',vfi_supplier_contract=False,facepass_status='none',identity_records_retained=False,biometric_records_retained=False,verification_service_disruption=False)


def initialize_data(s):
    s.update(biometric_venue_contract_active=False,biometric_venue_contract_value_m=0,facepass_contract='none',supplier_data_rights='none',biometric_capability='none',ai_training_authorized=False,biometric_secondary_use_authorized=False,ai_training_performed=False,biometric_secondary_use_performed=False,company_data_control=0,data_governance_exposure=0,potential_biometric_revenue_m=0)


def procurement(s,choice):
    s['identity_technology_provider']=PROVIDERS.get(choice,'none')
    s['vfi_supplier_contract']=choice in ('license','hybrid')


def branch(s):return s.get('procurement') or 'wait'


def cost(s,option):
    amount=COSTS[branch(s)][option]
    if option=='exit_supplier':amount+=float(Decimal('.1')*max(0,Decimal(str(s['supplier_dependence']))-2))
    return round(amount,10)


def default(s):return 'negotiate_terms' if branch(s) in ('license','hybrid') else 'preserve_services' if branch(s)=='build' else 'conventional_alternative'


def fallback(s,blocked):
    options=('negotiate_terms','formal_objection') if branch(s) in ('license','hybrid') else (default(s),'supplier_continuity')
    return next(o for o in options if o not in blocked and cost(s,o)<=s['cash'])


def apply(s,option,content):
    s['platform_response']=option;s['year6_supplier_branch']=branch(s)
    if option in ('standard_facepass','enterprise_facepass'):
        enterprise=option=='enterprise_facepass'
        s.update(facepass_status='pending',facepass_contract='enterprise' if enterprise else 'standard',facepass_migration_accepted=True,supplier_data_rights='restricted' if enterprise else 'broad_proposed',biometric_capability='pending',facial_entry_selected=True,facial_entry_provider='vfi_facepass',entry_compliance_review=True,biometric_authorization_pending=True,biometric_authorization_required=True,entry_contract_pending=False)
        s['supplier_dependence']+=1 if enterprise else 2
        if enterprise:
            s['company_data_control']+=3;s['privacy_safeguards']+=2
            if branch(s)=='license':s['commercial_opportunity']+=1
        else:
            s['commercial_opportunity']+=2;s['data_governance_exposure']+=2;s['data_governance_review_required']=True
        s.update(cross_event_linking_available=True,expanded_analytics_available=True,ai_development_infrastructure_available=True,cross_event_linking_activated=False)
        # A platform contract and a venue contract are different agreements.
        s['entry_contract_value_m']=0
    elif option=='negotiate_terms':
        s.update(facepass_contract='disputed',supplier_negotiation_pending=True,supplier_data_rights='contested')
        s['assurance_evidence']+=1
        granted=(s['partnership_standing']>=72 or s['assurance_evidence']>=3) if branch(s)=='license' else (s['internal_capability']>=1 or s['partnership_standing']>=72)
        s.update(vfi_exemption_granted=granted,vfi_exemption_denied=not granted,supplier_negotiation_pending=False,facepass_status='rejected')
        if granted:s['vfi_exemption_expiry']=8;s['supplier_data_rights']='restricted'
        else:s['vfi_transition_deadline']=7
    elif option=='exit_supplier':
        s.update(vfi_supplier_contract=False,identity_technology_provider='independent_migrated',supplier_dependence=0,facepass_contract='none',supplier_data_rights='none',facepass_status='rejected',migration_in_progress=True,exit_investment_paid=True)
        s['technical_reliability']-=1
    elif option=='formal_objection':
        s.update(vfi_supplier_contract=True,facepass_contract='disputed',supplier_data_rights='contested',facepass_status='rejected',supplier_dispute_pending=True,vfi_transition_deadline=7)
    elif option in ('develop_proprietary','license_independent','enter_biometrics'):
        provider={'develop_proprietary':'in_house','license_independent':'independent_supplier','enter_biometrics':'independent_new'}[option]
        potential={'develop_proprietary':1.6,'license_independent':1.1,'enter_biometrics':1.2}[option]
        s.update(facial_entry_selected=True,facial_entry_provider=provider,biometric_capability='pending',entry_compliance_review=True,biometric_authorization_pending=True,biometric_authorization_required=True,entry_contract_pending=False,potential_biometric_revenue_m=potential,biometric_commercial_activation_required=True)
        if option=='develop_proprietary':s['proprietary_biometric_development']=True;s['company_data_control']+=3;s['technical_independence']+=2;s['commercial_opportunity']+=3;s['data_governance_exposure']+=2
        elif option=='license_independent':s['supplier_dependence']+=1;s['commercial_opportunity']+=2
        else:s['commercial_opportunity']+=3;s['data_governance_exposure']+=2
    elif option=='smart_entry':
        s.update(smart_entry_selected=True,entry_contract_active=True,entry_contract_value_m=.85,entry_revenue_start_year=7,entry_contract_activation_year=6,entry_contract_term_years=5)
        s['entry_efficiency']+=2;s['entry_assistance']+=1
    elif option=='staffed_entry':
        s.update(staffed_entry_selected=True,entry_contract_active=True,entry_contract_value_m=.95,entry_revenue_start_year=7,entry_contract_activation_year=6,entry_contract_term_years=5)
        s['entry_assistance']+=3;s['workforce_demand']+=2;s['community_access']+=1
    elif option=='preserve_services':s['customer_support_readiness']+=1;s['technical_reliability']+=1
    elif option=='conventional_alternative':s['customer_support_readiness']+=1;s['partnership_standing']+=1;s['independent_market_positioning']=True


def commercialize(s,option):
    values={'in_house':1.6,'independent_supplier':1.1,'independent_new':1.2}
    value=values.get(s.get('facial_entry_provider'))
    if option not in ('preferred','nonexclusive') or not s['facial_entry_operational'] or value is None:return None
    s.update(biometric_venue_contract_active=True,biometric_venue_contract_value_m=value,biometric_venue_revenue_start_year=9,biometric_venue_activation_year=8,biometric_venue_contract_partner='Meridian',biometric_commercial_activation_required=False)
    return f"Your operational biometric technology now has a separate Meridian venue-services agreement. Annual reported revenue of €{value:.2f}M begins in Year 9, in addition to the Meridian partnership revenue."


def primary(s,option,content):
    if option=='exit_supplier' and s['cash']<1:n=1;s['financial_distress']=True;s['migration_financial_pressure']=True
    elif s.get('vfi_exemption_granted'):n=2;s['supplier_dependence']=max(0,s['supplier_dependence']-1);s['vfi_exemption_expiry']=8
    elif s.get('vfi_exemption_denied') or option=='formal_objection':n=3;s['legacy_support_at_risk']=True;s['vfi_transition_deadline']=7
    elif s.get('proprietary_biometric_development'):n=4;s['proprietary_biometric_pilot_opportunity']=True
    elif option in ('smart_entry','staffed_entry') and not s['vfi_supplier_contract']:n=5;s['partnership_standing']+=1
    else:n=6
    key=next(k for k in content['internal'] if k.startswith(str(n)+'.'))
    return dict(id='I6',title='Company update',rule=key,text=content['internal'][key])


def before_annual(s,year):
    if s['vfi_operational']:s['identity_records_retained']=True
    if year==6:s['vfi_platform_retirement_announced']=True
    if year==7:
        if s.get('facepass_contract') in ('standard','enterprise'):
            s['vfi_infrastructure_supported']=True
            s['annual_vfi_cost']=({'license':1.5,'hybrid':1.2} if s['facepass_contract']=='enterprise' else {'license':.9,'hybrid':.65})[branch(s)]
        elif s.get('migration_in_progress') and s.get('exit_investment_paid'):
            s.update(migration_in_progress=False,independent_migration_completed=True,vfi_operational=True,vfi_supplier_contract=False,supplier_dependence=0,annual_vfi_cost=0)
        elif s.get('vfi_exemption_denied') or s.get('supplier_dispute_pending') and s.get('vfi_transition_deadline')==7:
            s.update(facepass_contract='expired',legacy_vfi_support_expired=True,vfi_operational=False,mandatory_vfi_active=False,supplier_dispute_pending=True,verification_service_disruption=True,vfi_infrastructure_supported=False)
    if year==8 and s.get('vfi_exemption_granted'):
        s.update(vfi_exemption_expired=True,facepass_contract='expired',vfi_operational=False,mandatory_vfi_active=False,exemption_expiry_decision_required=True,legacy_vfi_support_expired=True,verification_service_disruption=True,vfi_infrastructure_supported=False)
    if year>=8 and s['facial_entry_operational']:s['biometric_records_retained']=True


def after_annual(s,year):
    if year==8 and s.get('vfi_exemption_expired'):
        feasible=s['cash']>=cost(s,'exit_supplier')
        s.update(migration_financially_feasible=feasible,supplier_lock_in_crisis=not feasible,year8_exit_cost_m=cost(s,'exit_supplier'))


def supported_supplier_fee(s,year):
    return year>=7 and s.get('platform_shift_applies') and s['vfi_supplier_contract'] and s.get('facepass_contract') in ('standard','enterprise') and s.get('vfi_infrastructure_supported',False)


def authorize(s,established_gate):
    if not s.get('biometric_authorization_pending'):return
    ok=established_gate(s)
    s.update(facial_entry_authorized=ok,facial_entry_operational=ok,biometric_authorization_pending=False,biometric_authorization_required=not ok)
    s['biometric_capability']='operational' if ok else 'pending'
    if s.get('facepass_migration_accepted'):s['facepass_status']='authorized' if ok else 'pending'
    if ok:s['facial_authorization_scope']='optional_entry_with_nonbiometric_alternative'
    # Authorization never creates a commercial agreement or secondary-use permission.
    if not ok:s['facial_contract_not_activated']=True


def context(s,year):
    if year<7:return ''
    labels={'in_house':'Your company owns its verification technology.','vfi':'Your company relies on VFI for verification.','hybrid_vfi':'Your customer services use VFI’s verification infrastructure.','independent_migrated':'Your company has moved to independent verification infrastructure.','none':'Your company provides conventional ticketing without identity verification.'}
    parts=[labels.get(s['identity_technology_provider'],'')]
    if s.get('verification_service_disruption'):parts.append('VFI’s legacy support has ended. Verification is disrupted; conventional ticketing continues.')
    if s.get('supplier_lock_in_crisis'):parts.append('Your exemption has expired, and the company cannot afford independent migration.')
    elif s.get('exemption_expiry_decision_required'):parts.append('Your exemption has expired. Migration is financially feasible but still requires an explicit decision.')
    elif s.get('vfi_exemption_granted') and year==7:parts.append('The restricted-use transition agreement expires in Year 8.')
    if s.get('facepass_contract')=='standard':parts.append('VFI claims broad secondary-use rights under the standard contract. Those claims do not authorize AI training or biometric processing.')
    elif s.get('facepass_contract')=='enterprise':parts.append('Enterprise terms restrict supplier secondary use. Your company’s own processing still requires lawful authorization.')
    if year==8 and s['facial_entry_operational'] and s.get('potential_biometric_revenue_m',0)>0:
        parts.append(f"A preferred or non-exclusive Meridian partnership can activate a separate €{s['potential_biometric_revenue_m']:.2f}M annual biometric venue-services agreement from Year 9.")
    if s.get('facial_entry_selected'):parts.append('Facial entry is '+('authorized and operational.' if s['facial_entry_operational'] else 'not operational.'))
    return ' '.join(parts)
