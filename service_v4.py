"""Versioned HTTP adapter using VFI simulation's existing SQLite and access controls."""
from copy import deepcopy
from pathlib import Path
import json,secrets,time
import engine_v4 as engine
import closure_v4 as closure
import powers_v4 as powers
import platform_shift as platform

COUNTRIES=['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czechia','Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia','Spain','Sweden']
CODES=['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE']
MISSIONS={
 'ceo':('Board Confidence','Achieve at least three of four board objectives covering financial viability, market position, organizational stability, and industry commitments.'),
 'cfo':('Financial Resilience','Avoid financial distress and finish Year 10 with positive cash reserves.'),
 'cto':('Technical Independence','Maintain sufficient control over critical infrastructure and avoid excessive dependence on a single external provider.'),
 'marketing':('Market Recognition','Finish among the leading companies for customer trust and maintain a competitive market position.'),
 'legal':('Legal Resilience','Avoid major unresolved legal liabilities and serious regulatory penalties.'),
 'employee':('Protect the Workforce','Avoid involuntary layoffs and maintain acceptable working conditions.'),
 'sustainability':('Sustainable Operations','Meet environmental targets while supporting accessible and responsible services.'),
 'relations':('Preferred Partner','Maintain strong commercial partnerships and high satisfaction among artists, promoters, and venues.')}
POWERS={role:(value['name'],value['description']) for role,value in engine.CONTENT['powers'].items()}


def flag(country):
    code=CODES[COUNTRIES.index(country)]
    return ''.join(chr(127397+ord(letter)) for letter in code)


def handles(server,method,path,body):
    if path=='/api/v4/content':return True
    if path=='/api/sessions' and method=='POST':return body.get('rules_version')==engine.VERSION
    parts=path.split('/')
    if len(parts)<4 or parts[1:3]!=['api','sessions']:return False
    with server.transaction() as con:
        try:row,session=server.load(con,parts[3])
        except server.Problem:return False
    return session.get('rules_version')==engine.VERSION



def participating_companies(session):
    return [c for c in session['companies'].values() if c.get('active',True)]


def checkpoint_ready(company):
    submitted=progress(company)
    return company['year']==5 and '5' in company['decisions'] and submitted['reflections']==submitted['active']


def snapshot_checkpoint(company):
    if not checkpoint_ready(company):return
    company['phase']='checkpoint'
    if 'checkpoint5' not in company:
        result=engine.replay(company)
        company['checkpoint5']={'state':deepcopy(result['state']),'ledger':deepcopy(result['ledger']),'history':deepcopy(result['timeline']),'saved_at':time.time()}


def industry(session):
    rows=[]
    for company in participating_companies(session):
        state=company['checkpoint5']['state']
        rows.append(dict(id=company['id'],name=company['name'],country=company['country'],flag=company['flag'],state=deepcopy(state)))
    for metric in ('cash','reported_annual_revenue','customer_trust','workforce_conditions','technical_reliability','sustainability','partnership_standing'):
        for row in rows:
            row.setdefault('ranks',{})[metric]=1+sum(other['state'][metric]>row['state'][metric] for other in rows)
    obligation_keys=('support_training_outstanding','integration_governance_outstanding','restructuring_proposed_12','verification_remediation_required','pilot_review_pending','reservation_terms_review','review_remediation_required','customer_compensation_review','staff_escalation_review')
    for row in rows:row['obligations']=[key.replace('_',' ').capitalize() for key in obligation_keys if row['state'].get(key)]
    for row in rows:
        if row['state'].get('vfi_operating_payable_m'):row['obligations'].append(f"Unpaid VFI operating costs: EUR {row['state']['vfi_operating_payable_m']:.2f}M")
    return rows


def synchronize_midpoint(server,session):
    until=session.get('midpoint_deadline')
    if not until or session.get('paused') or time.time()<until:return
    for company in participating_companies(session):
        while company['year']<5:
            year=company['year']
            if str(year) not in company['decisions']:
                record(server,company,engine.default_option(company,year),'facilitator_skipped','system')
            company['year']+=1;company['phase']='decision';company['version']+=1
        if '5' not in company['decisions']:
            company['deadline']=time.time()+decision_seconds(session,company['year']) if decision_seconds(session,company['year']) else None
        company.pop('midpoint_warning_until',None)
    session['midpoint_deadline']=None
    session['midpoint_triggered']=True


def decision_seconds(session,year):
    # Annual durations are discussion estimates, never automatic deadlines.
    return 0


def active_members(company):
    return {role:member for role,member in company['members'].items() if member.get('active',True)}


def progress(company):
    year=str(company['year'])
    members=active_members(company)
    preferences=sum(year in member.get('preferences',{}) for member in members.values())
    reflections=sum(bool(member.get('reflections',{}).get(year,'').strip()) if year!='10' else bool(member.get('closing_reflection',{}).get('reconsider','').strip() and member.get('closing_reflection',{}).get('responsibility','').strip()) for member in members.values())
    return dict(active=len(members),preferences=preferences,reflections=reflections,reflection_required=company['year'] in (1,5,10))


def record(server,company,option,mode='student_decision',actor='company'):
    year=company['year'];key=str(year)
    if key in company['decisions']:return
    company['decisions'][key]=dict(option=option,resolution_mode=mode,decision_source='ceo_override' if actor=='ceo' else 'expired_default' if mode=='deadline_expired' else mode,reason=mode,actor=actor,at=time.time(),terminology_version=company.get('terminology_version',0))
    result=engine.replay(company)
    step=result['timeline'][-1]
    company['decisions'][key].update(option=step['option'],resolution_mode=step['resolution_mode'],decision_source=step['decision_source'])
    company['history'].append(deepcopy(step))
    for item in company['interventions']:
        if item['year']==year:
            effect=next((e for e in step.get('power_effects',[]) if e['role']==item['role']),None)
            if effect:item.update(immediate_effect=deepcopy(effect),decision_outcome=step['option'],affected_final_choice=(item.get('proposed_option_before')!=step['option']) if item.get('proposed_option_before') else None,blocked_option_unselected=(item.get('option')!=step['option']) if item['role'] in ('cfo','cto') else None,final_decision_locked=item['role']=='ceo')
    company['phase']='event';company['deadline']=None;company['version']+=1
    for role,member in company['members'].items():
        received=member.setdefault('received',{}).setdefault(key,{})
        received.setdefault('intelligence',engine.scenario(company,int(key))['info'][role])
        received['consequence']=step['private'][role]


def enter_year(server,session,company):
    while company['year']<=10 and company['year'] not in session['active_years']:
        record(server,company,engine.default_option(company,company['year']),'facilitator_skipped','system')
        if company['year'] in (1,5,10):return
        company['year']+=1;company['phase']='decision'
    company['deadline']=time.time()+decision_seconds(session,company['year']) if company.get('started') and decision_seconds(session,company['year']) else None


def tick(server,session,company):
    if session.get('complete') or not company.get('active',True):return
    if company['phase']=='decision' and company.get('deadline') and not session.get('paused') and time.time()>=company['deadline']:
        default=session.get('year5_default','independent_review') if company['year']==5 else engine.default_option(company,company['year'])
        if default is None:
            company['deadline']=None
            company['default_awaiting_specification']=True
            return
        record(server,company,default,'deadline_expired','system')
    if company['year']==5:snapshot_checkpoint(company)
    if company['year']==5 and session.get('released5') and checkpoint_ready(company):
        company['year']=6;company['phase']='decision';company['version']+=1;enter_year(server,session,company)
    if company['year']==10:closure.snapshot(company)



def move_to_decision(server,session,company,target):
    if type(target)!=int or not 1<=target<=10:raise server.Problem('Choose a year from 1 to 10.')
    if target<company['year']:raise server.Problem('Moving backwards would alter recorded history. Choose the current year or a later year.',409)
    if not company.get('active',True):raise server.Problem('Restore this company before moving it.',409)
    if target>5 and company['year']<=5 and not checkpoint_ready(company):raise server.Problem('Complete the Year 5 decision and active students’ reflections before moving beyond the midpoint.',409)
    if str(target) in company['decisions']:return  # Preserve completed teams at the target.
    before=company['year']
    while company['year']<target:
        year=company['year']
        if str(year) not in company['decisions']:record(server,company,engine.default_option(company,year),'facilitator_skipped','system')
        company['year']+=1
    company.update(phase='decision',deadline=None,started=True)
    company.pop('deadline_kind',None);company.pop('midpoint_warning_until',None)
    company['version']+=1
    session['active_years']=sorted(set(session['active_years']+[target]))
    session.setdefault('moderator_history',[]).append(dict(action='move_to_decision',company=company['id'],from_year=before,to_year=target,at=time.time()))

def undo_power(server,company,role,teacher=False):
    item=next((i for i in company['interventions'] if i['role']==role),None)
    if not item:raise server.Problem('There is no active power to undo.',409)
    year=item['year'];key=str(year)
    if company['year']!=year or company.get('checkpoint5') and year==5 or company.get('checkpoint10'):raise server.Problem('This power is part of a completed year and cannot be undone without altering later work.',409)
    decision=company['decisions'].get(key)
    if decision:
        if role!='ceo' or decision.get('actor')!='ceo':raise server.Problem('The company has already decided. This power is now part of its recorded outcome.',409)
        if any(m.get('reflections',{}).get(key) for m in company['members'].values()):raise server.Problem('Reflections already refer to this outcome. It cannot be reopened automatically.',409)
        company.setdefault('correction_history',[]).append(dict(kind='withdrawn_ceo_decision',decision=deepcopy(decision),at=time.time()))
        del company['decisions'][key]
        company['history']=[step for step in company['history'] if step['year']!=year]
        for member in company['members'].values():member.get('received',{}).get(key,{}).pop('consequence',None)
        company.update(phase='decision',deadline=None)
    company.setdefault('power_corrections',[]).append(dict(action='undo',activation=deepcopy(item),by='teacher' if teacher else role,at=time.time()))
    company['interventions'].remove(item);company['members'][role]['power_used']=False;company['version']+=1

def public_company(company):
    result=engine.replay(company)
    current=engine.scenario(company,company['year'])
    safe={key:deepcopy(company.get(key)) for key in ('id','name','country','flag','year','phase','version','decisions','deadline','started','midpoint_warning_until')}
    safe.update(active=company.get('active',True),rules_version=engine.VERSION,roles_taken=list(company['members']),state=result['state'],ledger=result['ledger'],progress=progress(company),scenario=None,history=[])
    for step in result['timeline']:
        public=deepcopy(step);public.pop('private',None);public.pop('private_intelligence',None)
        for effect in public.get('power_effects',[]):effect.pop('private',None)
        safe['history'].append(public)
    if current:
        safe['scenario']={key:deepcopy(current[key]) for key in ('title','story','question','calendar_year')}
        safe['scenario']['supplier_context']=platform.context(result['state'],company['year']) if company.get('platform_shift_version')==1 else ''
        state=result['state']
        if company['year'] in (5,6,7,8,9,10) and str(company['year']) not in company['decisions']:safe['external_announcement']=deepcopy(engine.CONTENT['platform_shift']['external'] if company['year']==6 and company.get('platform_shift_version')==1 else engine.CONTENT['external'][str(company['year'])])
        blocked={item.get('option') for item in company['interventions'] if item['year']==company['year'] and item['role'] in ('cfo','cto')}
        safe['scenario']['options']=[dict(id=o['id'],title=o['title'],detail=o['detail'],cost=engine.cost(state,company['year'],o['id']),blocked_by=next((i['role'] for i in company['interventions'] if i['year']==company['year'] and i['role'] in ('cfo','cto') and i.get('option')==o['id']),None),unavailable=o['id'] in blocked or not engine.available(state,company['year'],o['id'])) for o in current['options']]
    safe['supplier_context']=platform.context(result['state'],company['year']) if company.get('platform_shift_version')==1 else ''
    safe['annual_notice']=result.get('annual_notices',{}).get(str(company['year']))
    safe['checkpoint_ready']=checkpoint_ready(company)
    safe['final_ready']=closure.ready(company)
    safe['power_announcements']=deepcopy([{k:v for k,v in effect.items() if k!='private'} for effect in (result.get('pending_power_effects',[]) or (result['timeline'][-1].get('power_effects',[]) if str(company['year']) in company['decisions'] else []))])
    safe['complete']=company.get('complete',False)
    safe['deadline_kind']=company.get('deadline_kind')
    safe['checkpoint_saved']='checkpoint5' in company
    safe['participants']=[dict(role=role,name=m['name'],active=m.get('active',True),power_used=m.get('power_used',False)) for role,m in company['members'].items()]
    return safe


def response(server,row,session,company,access,role):
    result={'rules_version':engine.VERSION,'session':{'id':row['id'],'code':row['code'],'label':session['label'],'roles':server.role_list(session['role_count']),'active_years':session['active_years'],'minutes':session['minutes']},'company':public_company(company),'access':access}
    if access in ('company','facilitator'):result['join_token']=company['phone_key']
    result['session'].update(complete=session.get('complete',False),final_revealed=session.get('final_revealed',False),debrief=engine.CONTENT['closure']['debrief_questions'] if session.get('final_revealed') else None,feedback_questions=engine.CONTENT['closure']['feedback_questions'] if session.get('final_revealed') else None)
    if role:
        member=company['members'][role]
        if company['phase']=='decision' and member.get('active',True):member.setdefault('received',{}).setdefault(str(company['year']),{}).setdefault('intelligence',engine.scenario(company,company['year'])['info'][role])
        current=engine.scenario(company,company['year'])
        result.update(role={'id':role,'title':server.CONTENT['roles'][role][0],'mission':MISSIONS[role][1],'mission_title':MISSIONS[role][0],'power':POWERS[role][0],'power_description':POWERS[role][1]},participant={'name':member['name'],'active':member.get('active',True)},preferences=deepcopy(member.get('preferences',{})),reflections=deepcopy(member.get('reflections',{})),received=deepcopy(member.get('received',{})),notes={},power_used=member.get('power_used',False),reflection_prompt=engine.CONTENT['reflections'].get(str(company['year'])),intelligence=current['info'][role] if current else None,private_consequence=member.get('received',{}).get(str(company['year']),{}).get('consequence'),power_configured=True,closing_reflection=deepcopy(member.get('closing_reflection')),closing_questions=engine.CONTENT['closure']['reflection_questions'],closing_intro=engine.CONTENT['closure']['closing_intro'],power_activation=next((deepcopy(i) for i in company['interventions'] if i['role']==role),None),power_effect=next((deepcopy(e) for e in engine.replay(company).get('pending_power_effects',[]) if e['role']==role),None))
        computed=engine.replay(company)
        effects=computed.get('pending_power_effects',[])+[e for step in computed['timeline'] for e in step.get('power_effects',[])]
        result['power_result']=next((deepcopy(e) for e in effects if e['role']==role),None)
        result['technical_options']=list(powers.technical_options(computed['state'],company['year']))
        state=computed['state']
        result['power_unavailable_reason']=('The company cannot afford this executive power.' if role in ('marketing','legal','sustainability','relations') and state['cash']<powers.COSTS[role] else 'No qualifying active contract and material change are available this year.' if role=='relations' and (not powers.contracts(state) or company['year'] not in (4,5,6,7,8,9)) else 'No qualifying technical proposal is available to veto this year.' if role=='cto' and not result['technical_options'] else None)
        result['individual_history']=[dict(year=step['year'],company_option=engine.option_definition(step['year'],step['option'],company)['title'],preferred_option=next((o['title'] for o in engine.scenario(company,step['year'])['options'] if o['id']==member.get('preferences',{}).get(str(step['year']))),'No submission required' if step['resolution_mode']=='facilitator_skipped' else 'Not submitted'),intelligence=engine.scenario(company,step['year'])['info'][role],consequence=step['private'][role],reflection=member.get('reflections',{}).get(str(step['year'])),ceo_override=company['decisions'][str(step['year'])].get('actor')=='ceo') for step in engine.replay(company)['timeline']]
    return result


def export(session):
    data=deepcopy(session)
    for key in ('password','projector','join_keys'):data.pop(key,None)
    for company in data['companies'].values():
        for key in ('secret','phone_key','resume_secrets'):company.pop(key,None)
        for member in company['members'].values():
            member.pop('secret',None);member.pop('resume_secrets',None)
        company['computed']=engine.replay(company)
    return data


def report_pdf(server,company,session,role=None):
    import reports
    roles=[role] if role else list(company['members'])
    story=[]
    for member_role in roles:
        data=closure.report(company,session,member_role,MISSIONS,POWERS)
        story.extend(reports.paragraph(text,'ReportHeading' if closure.is_heading(text) else 'ReportBody') for text in closure.report_text(data).split('\n\n') if text)
    if not story:story=[reports.paragraph(company['name'],'ReportTitle')]
    return server.PDF(reports.build(story,session['label']))


def company_report_pdf(server,company,session):
    """Shared decisions and outcomes; private student records stay in personal/teacher reports."""
    import reports
    result=engine.replay(company)
    story=[reports.paragraph(company['name'],'ReportTitle'),reports.paragraph(company['country'])]
    def heading(text):story.append(reports.paragraph(text,'ReportHeading'))
    def paragraph(text):
        if text:story.append(reports.paragraph(str(text)))
    for step in result['timeline']:
        heading(f"Year {step['year']} · {step['scenario_title']}")
        paragraph('Company decision: '+step['option_title'])
        paragraph('Decision source: '+step['decision_source'])
        paragraph(step['outcome'])
        for event in ('external','internal'):
            paragraph(step[event]['title']);paragraph(step[event]['text'])
        for message in step.get('modifiers',[]):paragraph(message)
        if step.get('external_resolution'):
            paragraph(step['external_resolution']['title']);paragraph(step['external_resolution']['text'])
        for effect in step.get('power_effects',[]):paragraph(effect['announcement'])
    for label,state in [('Year 5 company performance',company.get('checkpoint5',{}).get('state')),('Current company performance',result['state'])]:
        if state:
            heading(label)
            for key in closure.METRICS:
                value=state.get(key)
                if value is not None:paragraph(key.replace('_',' ').capitalize()+': '+(f'€{value*1000000:,.0f}' if key in ('cash','reported_annual_revenue') else str(value)))
    heading('Outstanding obligations')
    for obligation in closure.rules.obligations(result['state']):paragraph(obligation.replace('_',' '))
    heading('Cash ledger (€M)')
    for item in result['ledger']:paragraph(f"Year {item['year']} · {item['effect'].replace('_',' ')} · {item['amount']:+.2f} · Cash {item['balance']:.2f}")
    return server.PDF(reports.build(story,session['label']))


def projection_data(server,row,session,preview_year=None):
    if preview_year:
        session=deepcopy(session)
        session.update(revealed5=preview_year==5,final_revealed=preview_year==10,debrief_visible=False,released5=True,midpoint_presentation='results')
        if preview_year==5:session['companies']={key:c for key,c in session['companies'].items() if c.get('checkpoint5')}
    result=dict(id=row['id'],code=row['code'],label=session['label'],password=session['password'],intro_video_src='/media/vfi/intro.mp4' if (server.ROOT/'dist/media/vfi/intro.mp4').is_file() else None,closing_video_src='/media/vfi/year-10.mp4' if (server.ROOT/'dist/media/vfi/year-10.mp4').is_file() else None,comparison=closure.industry(session) if session.get('final_revealed') else industry(session) if session.get('revealed5') else [],rules_version=engine.VERSION,final_revealed=session.get('final_revealed',False),complete=session.get('complete',False),debrief_visible=session.get('debrief_visible',False),platform_presentation=session.get('midpoint_presentation','results') if not session.get('released5') else 'results',platform_commercial={**engine.CONTENT['platform_shift']['commercial'],'video_src':'/media/vfi/smile-and-pass.mp4' if (server.ROOT/'dist/media/vfi/smile-and-pass.mp4').is_file() else None},platform_announcement=engine.CONTENT['platform_shift']['external'],debrief_questions=engine.CONTENT['closure']['debrief_questions'],debrief_statement=engine.CONTENT['closure']['G4'],checkpoint_text={'announcement':engine.CONTENT['closure']['final_announcement']} if session.get('final_revealed') else platform.rename_terms(engine.CONTENT['checkpoint']) if session.get('revealed5') else None)
    if preview_year:
        result.update(preview_year=preview_year,preview_video_src=result['platform_commercial']['video_src'] if preview_year==5 else result['closing_video_src'])
    return result


def dispatch(server,method,path,body,token):
    parts=[part for part in path.split('/') if part]
    if path=='/api/v4/content':
        return {'rules_version':engine.VERSION,'introduction':platform.rename_terms(engine.CONTENT['introduction']),'countries':COUNTRIES,'roles':{r:{'title':v[0]} for r,v in server.CONTENT['roles'].items()}}
    if path=='/api/sessions':
        if not token or not secrets.compare_digest(token,server.teacher_key()):raise server.Problem('Teacher access required.',403)
        active=body.get('active_years',list(range(1,11)))
        if not isinstance(active,list) or any(type(y)!=int or not 1<=y<=10 for y in active) :raise server.Problem('Choose decision years from 1 to 10.')
        count=body.get('role_count',6);minutes=body.get('minutes',5)
        if count not in (6,7,8) or not isinstance(minutes,(float,int)) or not 0<=minutes<=30:raise server.Problem('Choose 6–8 roles and 0–30 minutes.')
        decision_minutes=body.get('decision_minutes',{})
        if not isinstance(decision_minutes,dict) or any(k not in tuple(str(y) for y in range(1,11)) or type(v) not in (int,float) or not 0<=v<=30 for k,v in decision_minutes.items()):raise server.Problem('Choose 0–30 minutes for each year.')
        checkpoint_minute=body.get('checkpoint_minute',45);end_minute=body.get('end_minute',90)
        if type(checkpoint_minute) not in (int,float) or type(end_minute) not in (int,float) or not 0<checkpoint_minute<end_minute<=600:raise server.Problem('Set a checkpoint time before the session finish time, within 600 minutes.')
        company_count=None  # Company registration is not capped, including older sessions.
        identity=secrets.token_hex(12);secret=secrets.token_urlsafe(32)
        session=dict(rules_version=engine.VERSION,label=server.text(body.get('label'),'a session name',80),minutes=minutes,role_count=count,active_years=sorted(set(active)),companies={},created=time.time(),released5=False,password=''.join(secrets.choice('23456789') for _ in range(6)),projector=secrets.token_urlsafe(32),join_keys=[],paused=False,power_effects=body.get('power_effects',{}),mission_thresholds=body.get('mission_thresholds',{}),year5_default=body.get('year5_default','independent_review'),revealed5=False,company_count=company_count,decision_minutes=decision_minutes,checkpoint_minute=checkpoint_minute,end_minute=end_minute,timing_mode='estimates')
        code=''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(6))
        with server.transaction() as con:con.execute('INSERT INTO sessions VALUES (?,?,?,?)',(identity,code,server.digest(secret),json.dumps(session)))
        return dict(id=identity,code=code,token=secret)
    with server.transaction() as con:
        row,session=server.load(con,parts[2])
        teacher=bool(token) and secrets.compare_digest(server.digest(token),row['secret'])
        def save(value):
            server.save(con,row['id'],session)
            return value
        # Preview requests bypass ticking, checkpoint synchronization and all writes.
        if len(parts)==5 and parts[3]=='projection':
            if method!='GET' or parts[4] not in ('preview5','preview10'):raise server.Problem('Not found.',404)
            if not teacher:raise server.Problem('Teacher access required.',403)
            return projection_data(server,row,session,int(parts[4].replace('preview','')))
        # Inspection is teacher-only and returns before any ticking or writes.
        if len(parts)==6 and parts[3]=='inspect':
            if not teacher:raise server.Problem('Teacher access required.',403)
            if method!='GET':raise server.Problem('Use GET.',405)
            try:year=int(parts[5])
            except ValueError:raise server.Problem('Choose a year from 1 to 10.')
            if not 1<=year<=10:raise server.Problem('Choose a year from 1 to 10.')
            original=server.company_by_id(session,parts[4]);copy=deepcopy(original)
            # Reconstruct the state they had on entering that year.
            copy['decisions']={k:v for k,v in copy['decisions'].items() if int(k)<year}
            copy['interventions']=[i for i in copy['interventions'] if i['year']<year]
            copy.update(year=year,phase='decision')
            scenario=engine.scenario(copy,year)
            return dict(views={r:{**response(server,row,deepcopy(session),deepcopy(original if year==original['year'] else copy),'student',r), 'read_only':True} for r in original['members']},company_view={**response(server,row,deepcopy(session),deepcopy(original if year==original['year'] else copy),'company',None),'read_only':True},company=public_company(copy),scenario=scenario,roles={r:dict(title=server.CONTENT['roles'][r][0],mission=MISSIONS[r][1],intelligence=scenario['info'][r]) for r in server.role_list(session['role_count'])},recorded_decision=deepcopy(original['decisions'].get(str(year))))
        session.setdefault('year5_default','independent_review')
        if session['year5_default'] is None:session['year5_default']='independent_review'
        for company in session['companies'].values():
            company.setdefault('terminology_version',1)
            company.setdefault('platform_shift_version',0 if '6' in company['decisions'] else 1)
            if company['year'] in (4,9) and company['phase']=='handoff':
                company['phase']='decision'
                enter_year(server,session,company)
        session['timing_mode']='estimates'
        for company in session['companies'].values():
            if company.get('deadline_kind')!='checkpoint_window':company['deadline']=None
        synchronize_midpoint(server,session)
        for company in session['companies'].values():tick(server,session,company)
        closure.synchronize(server,session,record)
        server.save(con,row['id'],session)
        operation=parts[3] if len(parts)>3 else ''
        if operation=='join' and method=='POST':
            if not secrets.compare_digest(str(body.get('password','')),session['password']):raise server.Problem('The session password is incorrect.',403)
            secret=secrets.token_urlsafe(32);session['join_keys'].append(server.digest(secret))
            return save(dict(id=row['id'],code=row['code'],token=secret))
        if operation=='locate':
            if not server.joined(session,token):raise server.Problem('Enter the session password first.',403)
            name=server.text(body.get('name'),'a company name',60)
            for c in session['companies'].values():
                if c['name'].casefold()==name.casefold():return dict(id=c['id'])
            raise server.Problem('Company not found.',404)
        if operation=='summary':
            if not teacher:raise server.Problem('Teacher access required.',403)
            return dict(id=row['id'],code=row['code'],label=session['label'],created=session['created'],company_count=len(session['companies']),completed_count=sum(c.get('complete',False) for c in session['companies'].values()),status='complete' if session.get('complete') else 'active')
        if operation=='projection':
            if not teacher and not secrets.compare_digest(token,session['projector']):raise server.Problem('Projection access required.',403)
            return projection_data(server,row,session)
        if operation=='feedback' and method=='POST':
            if not session.get('final_revealed'):raise server.Problem('Feedback opens after the final checkpoint.',409)
            if not any(any((secrets.compare_digest(server.digest(token),m['secret']) or server.digest(token) in m.get('resume_secrets',[])) for m in c['members'].values()) for c in session['companies'].values()):raise server.Problem('Use your student session.',403)
            return closure.save_feedback(server,con,row['id'],body)
        if operation=='export':
            if not teacher:raise server.Problem('Teacher access required.',403)
            return export(session)
        if operation=='logs.pdf':
            if not teacher:raise server.Problem('Teacher access required.',403)
            import reports
            story=[]
            for company in session['companies'].values():
                for role in company['members']:
                    data=closure.report(company,session,role,MISSIONS,POWERS)
                    story.extend(reports.paragraph(text,'ReportHeading' if closure.is_heading(text) else 'ReportBody') for text in closure.report_text(data).split('\n\n') if text)
            return server.PDF(reports.build(story or [reports.paragraph('No companies have joined yet.')],session['label']))
        if operation=='control':
            if not teacher:raise server.Problem('Teacher access required.',403)
            action=body.get('action')
            if session.get('complete') and action not in ('reset','debrief'):raise server.Problem('This simulation is complete. Company decisions and state are locked.',409)
            if action=='reset':
                archived=export(session);archived.pop('reset_history',None)
                session.setdefault('reset_history',[]).append(archived)
                session.update(companies={},released5=False,revealed5=False,final_requested=False,final_revealed=False,complete=False,debrief_visible=False,commercial_shown=False,migration_announced=False,midpoint_presentation='results',midpoint_deadline=None,midpoint_triggered=False,paused=False)
                session.pop('workshop_started',None)
            elif action=='settings':
                if session.get('complete'):raise server.Problem('Final results are locked.',409)
                years=body.get('active_years',session['active_years'])
                if not isinstance(years,list) or any(type(y)!=int or not 1<=y<=10 for y in years):raise server.Problem('Choose decision years from 1 to 10.')
                minutes=body.get('minutes',session['minutes']);checkpoint=body.get('checkpoint_minute',session.get('checkpoint_minute',45));finish=body.get('end_minute',session.get('end_minute',90))
                if type(minutes) not in (int,float) or not 0<=minutes<=30 or type(checkpoint) not in (int,float) or type(finish) not in (int,float) or not 0<checkpoint<finish<=600:raise server.Problem('Choose valid discussion and checkpoint estimates.')
                registration=body.get('registration_open',session.get('registration_open',True))
                if type(registration)!=bool:raise server.Problem('Choose whether new companies may join.')
                before={k:deepcopy(session.get(k)) for k in ('active_years','minutes','checkpoint_minute','end_minute','registration_open')}
                session.update(active_years=sorted(set(years)),minutes=minutes,checkpoint_minute=checkpoint,end_minute=finish,registration_open=registration)
                session.setdefault('moderator_history',[]).append(dict(action='settings',at=time.time(),before=before,after={k:deepcopy(session[k]) for k in before}))
                for company in participating_companies(session):
                    if company['phase']=='decision' and company['year'] not in session['active_years']:enter_year(server,session,company)
            elif action=='company_participation':
                if session.get('complete'):raise server.Problem('Final results are locked.',409)
                company=server.company_by_id(session,body.get('company'));active=body.get('active')
                if type(active)!=bool:raise server.Problem('Choose whether the company is participating.')
                before=company.get('active',True);company['active']=active;company['version']+=1
                session.setdefault('moderator_history',[]).append(dict(action='company_participation',company=company['id'],before=before,after=active,at=time.time()))
            elif action=='move':
                target=body.get('year')
                companies=[server.company_by_id(session,body['company'])] if body.get('company') else participating_companies(session)
                if not companies:raise server.Problem('No participating companies to move.',409)
                # Validate on copies first: either every selected team moves, or none.
                trial=deepcopy(session)
                for company in companies:move_to_decision(server,trial,trial['companies'][company['id']],target)
                for company in companies:move_to_decision(server,session,company,target)
                session.update(final_requested=False,final_deadline=None,midpoint_deadline=None)
                if target>5:session['released5']=True
            elif action=='undo_power':
                company=server.company_by_id(session,body.get('company'))
                undo_power(server,company,body.get('role'),True)
            elif action=='final':
                if not session['released5']:raise server.Problem('Complete and release the Year 5 checkpoint first.',409)
                seconds=body.get('warning_seconds',30)
                if type(seconds) not in (int,float) or not 0<=seconds<=300:raise server.Problem('Choose 0–300 seconds for the final submission window.')
                if not session.get('final_requested'):
                    session['final_requested']=True;session['final_deadline']=time.time()+seconds
                closure.synchronize(server,session,record)
            elif action=='reveal10':
                if not participating_companies(session) or not all(closure.ready(c) for c in participating_companies(session)):raise server.Problem('Every active student must complete both closing reflection answers first.',409)
                if not session.get('final_revealed'):
                    for c in participating_companies(session):closure.snapshot(c)
                    for item in closure.industry(session):session['companies'][item['id']]['checkpoint10']['industry_ranks']=item['ranks']
                    session.update(final_revealed=True,complete=True,paused=False)
                    for c in participating_companies(session):c.update(complete=True,phase='complete',deadline=None)
            elif action=='debrief':
                if not session.get('final_revealed'):raise server.Problem('Release the final checkpoint first.',409)
                session['debrief_visible']=True
            elif action=='expire5':
                companies=[server.company_by_id(session,body['company'])] if body.get('company') else participating_companies(session)
                for company in companies:
                    if company['year']==5 and '5' not in company['decisions']:
                        record(server,company,'independent_review','deadline_expired','system')
            elif action=='midpoint':
                seconds=body.get('warning_seconds',30)
                if not isinstance(seconds,(int,float)) or not 0<=seconds<=300:raise server.Problem('Choose a final submission window between 0 and 300 seconds.')
                if not session.get('midpoint_triggered') and not session.get('midpoint_deadline'):
                    session['midpoint_deadline']=time.time()+seconds
                    for c in participating_companies(session):
                        if c['year']<5:c['midpoint_warning_until']=session['midpoint_deadline']
                synchronize_midpoint(server,session)
            elif action=='reveal5':
                if not participating_companies(session) or not all(checkpoint_ready(c) for c in participating_companies(session)):raise server.Problem('Every company must complete Year 5 and all active submissions first.',409)
                for c in participating_companies(session):snapshot_checkpoint(c)
                session['revealed5']=True
                for row_result in industry(session):session['companies'][row_result['id']]['checkpoint5']['industry_ranks']=row_result['ranks']
            elif action=='commercial':
                session.update(midpoint_presentation='commercial',commercial_shown=True)
            elif action=='platform_announcement':
                session.update(midpoint_presentation='announcement',migration_announced=True)
            elif action=='release5':
                # Presentation is independent of progression. The announcement is
                # also delivered in each company's Year 6 briefing.
                if not all(checkpoint_ready(c) for c in participating_companies(session)):raise server.Problem('Every active participant must complete the checkpoint before release.',409)
                if not session['released5']:
                    for c in participating_companies(session):
                        c['year']=6;c['phase']='decision';c['version']+=1
                        enter_year(server,session,c)
                    session['released5']=True
            elif action in ('pause','resume'):
                now=time.time()
                if action=='pause':session['pause_started_at']=now
                else:
                    duration=max(0,now-session.pop('pause_started_at',now))
                    for field in ('final_deadline','midpoint_deadline'):
                        if session.get(field):session[field]+=duration
                session['paused']=action=='pause'
                for c in participating_companies(session):
                    if action=='pause':c['remaining_seconds']=max(0,(c.get('deadline') or now)-now);c['deadline']=None
                    elif c['phase']=='decision':c['deadline']=now+c.pop('remaining_seconds',0) if c.get('deadline_kind')=='checkpoint_window' else None
            elif action=='participant':
                c=server.company_by_id(session,body.get('company'))
                if body.get('active') and c.get('checkpoint10') and not c['members'][body['role']].get('closing_reflection'):raise server.Problem('This company has completed its immutable closing checkpoint.',409)
                c['members'][body['role']]['active']=bool(body['active']);c['version']+=1
            else:raise server.Problem('This control needs an annual checkpoint specification.')
            return save({'ok':True})
        if len(parts)==3:
            if not teacher:raise server.Problem('Teacher access required.',403)
            for c in session['companies'].values():tick(server,session,c)
            return save(dict(id=row['id'],code=row['code'],rules_version=engine.VERSION,**{k:session[k] for k in ('label','minutes','role_count','active_years','released5','password','projector','paused')},companies=[public_company(c) for c in session['companies'].values()],comparison=closure.industry(session) if session.get('final_revealed') else industry(session) if session.get('revealed5') else [],revealed5=session.get('revealed5',False),final_revealed=session.get('final_revealed',False),complete=session.get('complete',False),final_requested=session.get('final_requested',False),commercial_shown=session.get('commercial_shown',False),migration_announced=session.get('migration_announced',False),feedback_summary=closure.feedback_summary(server,row['id'],con) if session.get('complete') else None,registration_open=session.get('registration_open',True),workshop_started=session.get('workshop_started'),checkpoint_minute=session.get('checkpoint_minute',45),end_minute=session.get('end_minute',90),roster=[]))
        if operation=='companies' and len(parts)==4:
            if not teacher and not server.joined(session,token):raise server.Problem('Enter the session password first.',403)
            name=server.text(body.get('name'),'a company name',60);country=body.get('country')
            for c in session['companies'].values():
                if c['name'].casefold()==name.casefold():
                    # Restore the established brewery flow: the class password and
                    # existing company name reopen that company, even at capacity.
                    secret=secrets.token_urlsafe(32)
                    c.setdefault('resume_secrets',[]).append(server.digest(secret))
                    return save(dict(session_id=row['id'],id=c['id'],token=secret,resumed=True))
            if body.get('resume_only'):raise server.Problem('No saved company matches that name in this session. Check the name or session code.',404)
            if session.get('complete') or not teacher and not session.get('registration_open',True):raise server.Problem('New company registration is closed. Existing companies can still return.',409)
            if country not in COUNTRIES:raise server.Problem('Choose an EU headquarters country.')
            identity=secrets.token_hex(10);secret=secrets.token_urlsafe(32)
            c=dict(id=identity,session_id=row['id'],rules_version=engine.VERSION,platform_shift_version=1,terminology_version=1,name=name,country=country,flag=flag(country),secret=server.digest(secret),phone_key=secrets.token_urlsafe(32),year=1,phase='decision',version=0,decisions={},history=[],members={},interventions=[],deadline=None,started=False,paused=None,complete=False)
            session['companies'][identity]=c
            enter_year(server,session,c)
            return save(dict(session_id=row['id'],id=identity,token=secret))
        if operation!='companies' or len(parts)<5 or len(parts)>6:raise server.Problem('Not found.',404)
        c=server.company_by_id(session,parts[4])
        endpoint=parts[5] if len(parts)>5 else ''
        if endpoint in ('roles','claim'):
            if not c.get('active',True):raise server.Problem('Your company is withdrawn. Ask your teacher to restore it.',409)
            if not server.group_joined(session,c,token):raise server.Problem('Use the company QR code.',403)
            roles=server.role_list(session['role_count'])
            if endpoint=='roles':return dict(name=c['name'],roles=roles,taken=list(c['members']))
            role=body.get('role')
            if role not in roles:raise server.Problem('Role unavailable.')
            if role in c['members']:
                member=c['members'][role]
                if not body.get('resume') or str(body.get('name','')).strip().casefold()!=member['name'].casefold():raise server.Problem('Role already taken. To return, use the same role and name.',409)
                secret=secrets.token_urlsafe(32)
                member.setdefault('resume_secrets',[]).append(server.digest(secret))
                return save(dict(token=secret,role=role,session_id=row['id'],company_id=c['id'],resumed=True))
            secret=secrets.token_urlsafe(32)
            c['members'][role]=dict(name=server.text(body.get('name'),'your name',100),participant_id=secrets.token_hex(12),secret=server.digest(secret),preferences={},reflections={},received={},notes={},active=True,power_used=False)
            c['version']+=1
            return save(dict(token=secret,role=role,session_id=row['id'],company_id=c['id']))
        access,role=server.authority(row,c,token)
        tick(server,session,c)
        if endpoint=='personal-report':
            if not role:raise server.Problem('Use your private role link.',403)
            data=closure.report(c,session,role,MISSIONS,POWERS)
            data['text']=closure.report_text(data)
            return save(data)
        if endpoint in ('report.pdf','personal.pdf'):
            if endpoint=='personal.pdf' and not role:raise server.Problem('Use your private role link.',403)
            return save(report_pdf(server,c,session,role) if role or access=='facilitator' else company_report_pdf(server,c,session))
        if not endpoint:return save(response(server,row,session,c,access,role))
        if endpoint!='actions' or method!='POST':raise server.Problem('Not found.',404)
        action=body.get('action');year=c['year'];key=str(year)
        if not c.get('active',True):raise server.Problem('Your company is withdrawn from this session. Ask your teacher to restore it.',409)
        if action in ('preference','power','decide') and not c.get('started'):raise server.Problem('Start the company from Team QR before making recommendations or decisions.',409)
        if session.get('complete'):raise server.Problem('This simulation is complete. Decisions and reflections are locked.',409)
        if action=='start':
            if access not in ('company','facilitator'):raise server.Problem('Start on the company laptop.',403)
            if not c['started']:
                c['started']=True
                session.setdefault('workshop_started',time.time())
                if c['phase']=='decision' and decision_seconds(session,c['year']):c['deadline']=time.time()+decision_seconds(session,c['year'])
        elif action in ('preference','reflection'):
            if not role or not c['members'][role].get('active',True):raise server.Problem('An active student role is required.',403)
            if body.get('year')!=year:raise server.Problem('The company moved to another year.',409)
            if year not in session['active_years'] and action=='preference':raise server.Problem('This year does not require a recommendation.')
            if action=='preference':
                if c['phase']!='decision' or key in c['members'][role].get('preferences',{}):raise server.Problem('Recommendations cannot be changed after submission or recorded after the company decision is locked.',409)
                option=body.get('option')
                if option not in [o['id'] for o in engine.scenario(c,year)['options']]:raise server.Problem('Choose an option.')
                c['members'][role]['preferences'][key]=option
                c['members'][role].setdefault('preference_history',{})[key]={'option':option,'at':time.time(),'after_resolution':False}
            else:
                if year not in (1,5,10):raise server.Problem('No written reflection is required this year.')
                if c['phase'] not in ('event','checkpoint'):raise server.Problem('Write your reflection after the decision.',409)
                if year==10:
                    if c.get('checkpoint10'):raise server.Problem('The closing reflection has been saved in the final checkpoint.',409)
                    answers={k:server.text(body.get(k),k,4000) for k in ('reconsider','responsibility')}
                    c['members'][role]['closing_reflection']=dict(**answers,submitted_at=time.time(),recommendation=c['members'][role]['preferences'].get('10'),company_decision=c['decisions']['10']['option'])
                    c['members'][role]['reflections'][key]='\n\n'.join(answers.values())
                else:c['members'][role]['reflections'][key]=server.text(body.get('text'),'one or two sentences',4000)
        elif action=='undo_power':
            if not role:raise server.Problem('Use your private role link.',403)
            undo_power(server,c,role)
        elif action=='power':
            if not role:raise server.Problem('Use your private role link.',403)
            member=c['members'][role]
            if not member.get('active',True):raise server.Problem('This participant is inactive.',409)
            if member['power_used']:raise server.Problem('Your executive power has already been used.',409)
            if c['phase']!='decision' or session['paused']:raise server.Problem('This decision is closed or paused.',409)
            if body.get('year')!=year:raise server.Problem('The company moved to another year.',409)
            if year not in session['active_years']:raise server.Problem('Powers cannot be used during skipped years.',409)
            if key not in member.get('preferences',{}):raise server.Problem('Submit your private recommendation before activating your power.',409)
            option=body.get('option')
            options=[o['id'] for o in engine.scenario(c,year)['options']]
            if role in ('ceo','cfo','cto','sustainability','relations') and option not in options:raise server.Problem('Choose the proposal your power concerns.')
            state=engine.replay(c)['state']
            error=powers.validate(state,year,role,option,engine.cost(state,year,option) if option in options else 0)
            if error:raise server.Problem(error,409)
            if role=='ceo':
                if any(key not in m.get('preferences',{}) for m in active_members(c).values()):raise server.Problem('Every active member must submit a recommendation first.',409)
                selected=next(o for o in public_company(c)['scenario']['options'] if o['id']==option)
                if selected['unavailable']:raise server.Problem('That option is unavailable.')
            others=[m for r,m in active_members(c).items() if r!='ceo']
            conflict=role=='ceo' and bool(others) and sum(m['preferences'].get(key)!=option for m in others)*2>=len(others)
            intervention=dict(session_id=row['id'],company_id=c['id'],student_id=member['participant_id'],role=role,year=year,power_type=POWERS[role][0],reason=str(body.get('reason','')).strip()[:500],option=option,cost=powers.COSTS[role],at=time.time(),state_at_activation=deepcopy(state),power_spec_version=1,governance_conflict=conflict)
            c['interventions'].append(intervention);member['power_used']=True
            try:engine.replay(c)
            except ValueError as error:raise server.Problem(str(error),409)
            if role=='ceo':record(server,c,option,'student_decision','ceo')
        elif action=='decide':
            if access not in ('company','facilitator'):raise server.Problem('Use the shared company screen.',403)
            if c['phase']!='decision' or session['paused']:raise server.Problem('The decision is closed or paused.',409)
            if body.get('year')!=year or body.get('version')!=c['version']:raise server.Problem('The company has updated. Refresh first.',409)
            if any(key not in m.get('preferences',{}) for m in active_members(c).values()):raise server.Problem('Every active member must submit a recommendation first.',409)
            option=body.get('option')
            selected=next((o for o in public_company(c)['scenario']['options'] if o['id']==option),None)
            if not selected or selected['unavailable']:raise server.Problem('Choose a feasible option.')
            record(server,c,option)
        elif action=='advance':
            if access not in ('company','facilitator'):raise server.Problem('Use the shared company screen.',403)
            if session['paused']:raise server.Problem('The session is paused.',409)
            if body.get('year')!=year or c['phase']!='event':raise server.Problem('This stage has already advanced.',409)
            p=progress(c)
            if p['reflection_required'] and p['reflections']<p['active']:raise server.Problem('Wait for all active members to submit.',409)
            if year==10:closure.snapshot(c)
            elif year==5:
                snapshot_checkpoint(c)
            else:
                c['year']+=1;c['phase']='decision';enter_year(server,session,c)
        else:raise server.Problem('Unknown action.')
        if year==5:snapshot_checkpoint(c)
        if year==10:closure.snapshot(c)
        c['version']+=1
        return save(response(server,row,session,c,access,role))
