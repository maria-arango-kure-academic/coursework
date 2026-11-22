"""Final checkpoint, factual reports and anonymous feedback for the ten-year specification."""
from copy import deepcopy
import json,secrets,time
import engine_v4 as engine
import rules_9_10 as rules

METRICS=('reported_annual_revenue','cash','employees','customer_trust','workforce_conditions','technical_reliability','sustainability','partnership_standing')
RANKED=tuple(k for k in METRICS if k!='employees')

def ready(c):
    return '10' in c['decisions'] and all(m.get('closing_reflection',{}).get('reconsider','').strip() and m.get('closing_reflection',{}).get('responsibility','').strip() for m in c['members'].values() if m.get('active',True))

def snapshot(c):
    if not ready(c):return
    c['phase']='final_checkpoint'
    if 'checkpoint10' not in c:
        result=engine.replay(c)
        c['checkpoint10']=dict(state=deepcopy(result['state']),ledger=deepcopy(result['ledger']),history=deepcopy(result['timeline']),decisions=deepcopy(c['decisions']),individual_histories={role:{k:deepcopy(m.get(k,{})) for k in ('preferences','preference_history','reflections','closing_reflection')} for role,m in c['members'].items()},interventions=deepcopy(c['interventions']),saved_at=time.time())
        base=c.get('checkpoint5',{}).get('state',{})
        c['checkpoint10']['comparison']={k:{'year5':base.get(k),'year10':result['state'].get(k),'change':round(result['state'][k]-base[k],10) if k in base else None} for k in METRICS}

def industry(session):
    rows=[]
    for c in session['companies'].values():
        if not c.get('active',True):continue
        if 'checkpoint10' not in c:continue
        snap=c['checkpoint10'];s=snap['state']
        rows.append(dict(id=c['id'],name=c['name'],country=c['country'],flag=c['flag'],state=deepcopy(s),comparison=deepcopy(snap['comparison']),history=[{**{k:deepcopy(step[k]) for k in ('year','option','outcome','resolution_mode','decision_source','internal','external')},'option_title':step.get('option_title',step['option'])} for step in snap['history']],obligations=rules.obligations(s),human_consequences=[step['internal']['text'] for step in snap['history'] if not step['internal'].get('rule','').endswith('Otherwise')][-3:]))
    for row in rows:row['ranks']={k:1+sum(o['state'][k]>row['state'][k] for o in rows) for k in RANKED}
    return rows

def synchronize(server,session,record):
    if not session.get('final_requested') or session.get('complete') or session.get('paused'):return
    expired=time.time()>=session['final_deadline']
    for c in session['companies'].values():
        if not c.get('active',True):continue
        while c['year']<=10 and c['phase'] not in ('final_checkpoint','complete'):
            year=c['year'];key=str(year)
            if key not in c['decisions']:
                if year not in session['active_years']:record(server,c,engine.default_option(c,year),'facilitator_skipped','system')
                elif expired:record(server,c,engine.default_option(c,year),'deadline_expired','system')
                else:
                    c['deadline']=session['final_deadline'];c['deadline_kind']='checkpoint_window';break
            if year==10:snapshot(c);break
            c['year']+=1;c['phase']='decision';c['version']+=1;c['deadline']=None

def mission(role,s,history,definitions,config):
    result=dict(definition=definitions[role][1],evaluated=False,met=None,reason='The configured measurable conditions are insufficient to evaluate this mission.',observed={k:s.get(k) for k in METRICS+('technical_independence','supplier_dependence','involuntary_layoffs','legal_exposure','financial_distress')})
    specification=config.get(role) if isinstance(config,dict) else None
    if isinstance(specification,dict):
        conditions=specification.get('conditions',[])
        required=3 if role=='ceo' else specification.get('required',len(conditions))
        operators={'gte':lambda a,b:a>=b,'lte':lambda a,b:a<=b,'gt':lambda a,b:a>b,'lt':lambda a,b:a<b,'eq':lambda a,b:a==b}
        valid=isinstance(conditions,list) and bool(conditions) and (role!='ceo' or len(conditions)==4) and type(required)==int and 1<=required<=len(conditions)
        valid=valid and all(isinstance(c,dict) and c.get('field') in s and c.get('op') in operators and type(c.get('value')) in (int,float,bool) and type(s[c['field']]) in (int,float,bool) for c in conditions)
        if valid:
            checks=[dict(**c,actual=s[c['field']],met=operators[c['op']](s[c['field']],c['value'])) for c in conditions]
            result.update(evaluated=True,met=sum(c['met'] for c in checks)>=required,reason='Evaluated against the explicitly configured mission conditions.',conditions=checks)
            return result
    if role=='cfo':result.update(evaluated=True,met=not s['financial_distress'] and s['cash']>0,reason='Based on recorded financial distress and final cash reserves.')
    if role=='employee' and s['involuntary_layoffs']>0:result.update(evaluated=True,met=False,reason='The recorded involuntary layoffs mean the no-layoff mission condition was not met.')
    return result

def report(c,session,role,missions,power_names):
    m=c['members'][role];r=engine.replay(c);steps=[]
    for step in r['timeline']:
        y=str(step['year']);pref=m.get('preferences',{}).get(y);record=c['decisions'][y]
        selected=engine.option_definition(step['year'],step['option'],c)
        recommend=next((o['title'] for o in engine.scenario(c,int(y))['options'] if o['id']==pref),None)
        source='ceo_override' if record.get('actor')=='ceo' else step['decision_source']
        steps.append(dict(year=step['year'],scenario=engine.scenario(c,int(y))['title'],recommendation=recommend,recommendation_status='submitted' if pref else 'not_required_skipped' if step['resolution_mode']=='facilitator_skipped' else 'not_submitted',recommendation_at=m.get('preference_history',{}).get(y,{}).get('at'),company_decision=selected['title'],source=source,resolution_mode=step['resolution_mode'],followed_recommendation=(pref==step['option']) if pref else None,intelligence=m.get('received',{}).get(y,{}).get('intelligence'),outcome=step['outcome'],supplier_context=step.get('supplier_context',''),private_consequence=step['private'][role],external=step['external'],external_resolution=step.get('external_resolution'),internal=step['internal'],modifiers=step['modifiers'],powers=[{k:deepcopy(v) for k,v in e.items() if k!='private' or e['role']==role} for e in step.get('power_effects',[])],reflection=m.get('reflections',{}).get(y)))
    own_powers=deepcopy([i for i in c['interventions'] if i['role']==role])
    for i in own_powers:
        i['target_title']=next((o['title'] for o in engine.scenario(c,i['year'])['options'] if o['id']==i.get('option')),'No specific option targeted')
        i['outcome_title']=next((o['title'] for o in engine.scenario(c,i['year'])['options'] if o['id']==i.get('decision_outcome')),i.get('decision_outcome','Pending'))
    return dict(name=m['name'],company=c['name'],country=c['country'],role=role,mission=mission(role,r['state'],r['timeline'],missions,session.get('mission_thresholds',{})),power=power_names[role][0],power_used=bool(own_powers),power_activations=deepcopy(own_powers),power_status='Executive power used in Year '+str(own_powers[0]['year'])+'.' if own_powers else 'You retained your executive power throughout the simulation.',years=steps,state=r['state'],ledger=r['ledger'],obligations=rules.obligations(r['state']),checkpoint5={k:deepcopy(v) for k,v in c.get('checkpoint5',{}).items() if k in ('state','ledger','saved_at','industry_ranks')},checkpoint10={k:deepcopy(v) for k,v in c.get('checkpoint10',{}).items() if k not in ('individual_histories','interventions','history','decisions')},closing_reflection=deepcopy(m.get('closing_reflection')),assignment=engine.CONTENT['closure']['assignment'])

def is_heading(text):
    return text.startswith('Year ') and ' · ' in text or text in ('Private intelligence','Outcome','Your reflection','Your executive-power activation','Outstanding obligations','Year 5 company performance','Year 10 company performance','Year 5 to Year 10 changes','Current company performance','Cash ledger (€M)','Role mission')

def report_text(data):
    lines=[data['name'],data['company']+' · '+data['country'],data['role'],data['mission']['definition'],data['power'],data['power_status']]
    for e in data['years']:
        lines += ['',f"Year {e['year']} · {e['scenario']}",'Your recommendation: '+(e['recommendation'] or ('No recommendation required for this skipped year.' if e['recommendation_status']=='not_required_skipped' else 'Not submitted')),'Company decision: '+e['company_decision'],'Decision source: '+e['source'],'Resolution: '+e['resolution_mode']]
        if e['followed_recommendation'] is not None:lines.append('Company followed your recommendation: '+('Yes' if e['followed_recommendation'] else 'No'))
        if e.get('supplier_context'):lines+=['Supplier and technology position',e['supplier_context']]
        if e['intelligence']:lines+=['Private intelligence',e['intelligence']]
        lines += ['Outcome',e['outcome'],e['private_consequence'],e['external']['text'],e['internal']['text']]+e['modifiers']
        if e['external_resolution']:lines += [e['external_resolution']['title'],e['external_resolution']['text']]
        for effect in e['powers']:
            changes='; '.join(k.replace('_',' ')+': '+str(v['before'])+' → '+str(v['after']) for k,v in effect['changes'].items() if isinstance(v['after'],(float,int)) and not isinstance(v['after'],bool))
            lines += [effect['power'],effect['announcement'],'Cash cost: €'+format(effect['cost']*1000000,',.0f'),'Effects: '+(changes or 'No additional indicator change.')]
        if e['reflection']:lines += ['Your reflection',e['reflection']]
    for activation in data['power_activations']:
        lines += ['', 'Your executive-power activation',activation['power_type'],'Year: '+str(activation['year']),'Target: '+activation['target_title'],'Company decision: '+activation['outcome_title'],'Whether the final choice changed: '+('Not established; no earlier team choice was recorded.' if activation.get('affected_final_choice') is None else 'Yes' if activation['affected_final_choice'] else 'No')]
    lines+=['','Outstanding obligations']+([k.replace('_',' ') for k in data['obligations']] or ['None recorded'])
    for key in ('checkpoint5','checkpoint10'):
        snap=data[key]
        if snap:
            lines += ['',key.replace('checkpoint','Year ')+' company performance']+[k.replace('_',' ')+': '+str(snap['state'].get(k)) for k in METRICS+('procurement','northstar_contract','entry_contract_active','commercial_partnership_active','independent_programme_active','facial_entry_operational','vfi_operating_payable_m','operating_payable_m')]
            if snap.get('comparison'):lines+=['Year 5 to Year 10 changes']+[k.replace('_',' ')+': '+str(v['year5'])+' → '+str(v['year10'])+' (change '+str(v['change'])+')' for k,v in snap['comparison'].items()]
    lines += ['', 'Current company performance']+[k.replace('_',' ')+': '+str(data['state'].get(k)) for k in METRICS+('vfi_operating_payable_m','operating_payable_m','financial_distress')]
    if data['state'].get('platform_shift_applies'):
        keys=('identity_technology_provider','vfi_supplier_contract','supplier_dependence','platform_response','year6_exit_cost_m','year6_exit_affordable','facepass_contract','supplier_data_rights','biometric_capability','ai_training_authorized','biometric_secondary_use_authorized','ai_training_performed','biometric_secondary_use_performed','company_data_control','data_governance_exposure','potential_biometric_revenue_m','biometric_venue_contract_active','biometric_venue_contract_value_m','biometric_venue_revenue_start_year','facepass_status','facial_entry_provider','facial_entry_authorized','facial_entry_operational','entry_contract_active','entry_contract_value_m','verification_service_disruption','vfi_exemption_expired','exemption_expiry_decision_required','supplier_lock_in_crisis')
        lines+=['Supplier and technology history','Contractual data-use claims do not establish that data was actually processed, shared or used for AI training.']+[k.replace('_',' ')+': '+str(data['state'].get(k,'Not applicable')) for k in keys]
    lines+=['Cash ledger (€M)']+[str(x['year'])+' · '+x['effect']+': '+str(x['amount']) for x in data['ledger']]
    lines += ['', 'Role mission',data['mission']['reason'],'Mission conditions: '+('Not fully evaluable from the defined conditions.' if data['mission']['met'] is None else 'Met' if data['mission']['met'] else 'Not met'),data['assignment']]
    return '\n\n'.join(lines)

def save_feedback(server,con,session_id,body):
    answers=body.get('ratings',{});text=body.get('text',{})
    if not isinstance(answers,dict) or any(k not in ('1','2','3','4') or type(v)!=int or not 1<=v<=5 for k,v in answers.items()):raise server.Problem('Choose a rating from 1 to 5.')
    if not isinstance(text,dict) or any(k not in ('5','6') or not isinstance(v,str) or len(v)>2000 for k,v in text.items()):raise server.Problem('Use short feedback text.')
    payload={'ratings':answers,'text':text}
    con.execute('CREATE TABLE IF NOT EXISTS anonymous_feedback (response_id TEXT PRIMARY KEY, session_id TEXT NOT NULL, payload TEXT NOT NULL)')
    con.execute('INSERT INTO anonymous_feedback VALUES (?,?,?)',(secrets.token_hex(16),session_id,json.dumps(payload)))
    return {'ok':True}

def feedback_summary(server,session_id,con=None):
    if con is None:
        with server.transaction() as opened:return feedback_summary(server,session_id,opened)
    if con is not None:
        con.execute('CREATE TABLE IF NOT EXISTS anonymous_feedback (response_id TEXT PRIMARY KEY, session_id TEXT NOT NULL, payload TEXT NOT NULL)')
        records=[json.loads(row[0]) for row in con.execute('SELECT payload FROM anonymous_feedback WHERE session_id=?',(session_id,))]
    return dict(count=len(records),ratings={k:{str(v):sum(r['ratings'].get(k)==v for r in records) for v in range(1,6)} for k in ('1','2','3','4')},responses=[r['text'] for r in records if any(r['text'].values())])
