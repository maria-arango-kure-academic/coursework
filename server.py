"""VFI simulation classroom server. Python standard library and transactional SQLite."""
from contextlib import contextmanager, closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import argparse
import copy
import hashlib
import ipaddress
import json
import os
import secrets
import socket
import sqlite3
import time
import outcomes
import narrative

ROOT = Path(__file__).resolve().parent
CONTENT = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
DB = Path(os.environ.get('FAIRPASS_DB', str(ROOT / 'fairpass.sqlite3')))
DEFAULTS = outcomes.DEFAULTS
TEACHER_KEY = os.environ.get('FAIRPASS_TEACHER_KEY', '')
KEY_FILE = ROOT / '.teacher-key'

def teacher_key():
    if TEACHER_KEY:return TEACHER_KEY
    if not KEY_FILE.exists():KEY_FILE.write_text(secrets.token_urlsafe(32),encoding='utf-8')
    return KEY_FILE.read_text(encoding='utf-8').strip()

def group_joined(session, company, token):
    return joined(session,token) or (bool(token) and secrets.compare_digest(token,company.get('phone_key','!')))

def joined(session, token):
    return bool(token) and digest(token) in session.get('join_keys',[])

PAUSING = set()

class Problem(Exception):
    def __init__(self, message, status=400):
        self.message, self.status = message, status

def digest(token):
    return hashlib.sha256(token.encode()).hexdigest()

def initialise():
    teacher_key()
    DB.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB)) as con:
        con.execute('PRAGMA journal_mode=WAL')
        con.execute('CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, code TEXT UNIQUE, secret TEXT, state TEXT)')
        con.commit()

@contextmanager
def transaction():
    con = sqlite3.connect(DB, timeout=15)
    con.row_factory = sqlite3.Row
    try:
        con.execute('BEGIN IMMEDIATE')
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def load(con, identity):
    row = con.execute('SELECT * FROM sessions WHERE id=? OR code=?', (identity,identity.upper())).fetchone()
    if not row:
        raise Problem('Session not found. Check the code.',404)
    state=json.loads(row['state'])
    if 'password' not in state:
        state.update(password=''.join(secrets.choice('23456789') for _ in range(6)),projector=secrets.token_urlsafe(32),join_keys=[])
        save(con,row['id'],state)
    changed=False
    for c in state['companies'].values():
        if 'phone_key' not in c:c['phone_key']=secrets.token_urlsafe(32);changed=True
    if changed:save(con,row['id'],state)
    return row, state

def save(con, identity, state):
    con.execute('UPDATE sessions SET state=? WHERE id=?',(json.dumps(state,ensure_ascii=False),identity))

def text(value, label, maximum=200):
    if not isinstance(value,str) or not value.strip() or len(value)>maximum:
        raise Problem(f'Enter {label} using at most {maximum} characters.')
    return value.strip()

def role_list(count):
    keys=CONTENT['roleKeys']
    return keys[:count]

def company_by_id(state, identity):
    if identity not in state['companies']:
        raise Problem('Company not found.',404)
    return state['companies'][identity]

def authority(row, company, token):
    token_hash=digest(token)
    if secrets.compare_digest(token_hash,row['secret']):
        return 'facilitator', None
    if secrets.compare_digest(token_hash,company['secret']) or token_hash in company.get('resume_secrets',[]):
        return 'company', None
    for role, member in company['members'].items():
        if secrets.compare_digest(token_hash,member['secret']) or token_hash in member.get('resume_secrets',[]):
            return 'student', role
    raise Problem('This link cannot access that company. Use your saved join link.',403)

def record(company, year, option, reason='decision', actor='company'):
    key=str(year)
    if key in company['decisions']:
        return
    company['decisions'][key]={'option':option,'reason':reason,'actor':actor,'at':time.time()}
    company['history'].append({'year':year,'type':'decision','option':option,'reason':reason,'actor':actor})
    company['version']+=1

def current_choice(company, year):
    return company['decisions'].get(str(year),{}).get('option')

def company_context(company, year, state=None):
    s=state if state is not None else outcomes.replay(company)['state']
    architecture={'build':'Your engineers have built a verification prototype that the company owns.',
        'buy':'Your company has licensed a verification prototype from Verity.',
        'hybrid':'Your team has connected Verity’s verification to the company’s software.'}
    project=architecture.get(s['architecture'],'Your company has continued ticket sales without acquiring a buyer-verification prototype.')
    service=('Buyer verification is live '+('at selected venues with staffed recovery.' if s.get('launch')=='limited' else 'across your service.')) if s['live'] else 'Customers still use conventional ticket sales; buyer verification is not live.'
    if year==1:return 'Your company employs thousands across markets. The rollout starts with ten venue partners and a 40-person team. Existing ticket sales and customer support must keep running.'
    if year==2:return project+' '+service
    if year==3:
        evidence='You have no new testing evidence.' if not s['evidence'] else {'broad':'Your pilot covered varied customers, devices and failures.','focused':'Your team investigated accessibility and the connection between systems.','explore':'You investigated designs and supplier exit terms.'}.get(current_choice(company,2),'Your team has existing records and commissioned reviews to inform its decision.')
        return project+' '+evidence
    if year==4:return service+' Your team must maintain the current service while developing the next improvement.'
    if year==5:
        feature={'loyalty':'You introduced rewards for repeat customers.', 'reservations':'Customers can reserve until payday and transfer tickets under the company’s rules.', 'support':'You invested in accessible booking, account recovery and staffed alternatives.', 'basic':'You kept the existing feature set.'}.get(s.get('feature'),'You kept the existing feature set.')
        return service+' '+feature
    if year==6:return service+' '+('An acquired prototype remains available to launch.' if s['prototype'] and not s['live'] else 'Entry equipment would add another service for your company to maintain alongside ticket sales.')
    if year==7:
        entry={'full':'Your entry system uses facial recognition, movement tracking and temperature checks.', 'selective':'You offer optional facial entry with staffed alternatives.', 'alternative':'Your entry arrangements use offline codes, accessible gates and staffed checks.', 'existing':'You kept your existing entry arrangements.'}[s['entry']]
        records=f"Your company keeps individual attendance records for {s['attendance_days']} days." if s['attendance_days'] else 'You do not retain individual attendance records.'
        return entry+' '+records
    if year==8:
        screening='Your company uses broad watchlist screening and has an unresolved serious complaint.' if s['sharing']=='expanded' else 'Your current service operates without broad watchlist screening.'
        tracking='You also use personalised sponsored rewards.' if s['commercial_tracking'] else 'Your company does not use personalised sponsored rewards.'
        return screening+' '+tracking
    if year==9:
        partners=f"You have also added {s['new_partners']} new partnerships." if s['new_partners'] else 'You have not added any new partnerships.'
        jobs=f"{s['redundancies']} people have already lost their jobs." if s['redundancies'] else 'No staff have been made redundant.'
        return f"You still work with {s['contracts']} of your ten original venue customers. "+partners+f" Your {s['staff']}-person rollout team keeps those services running. "+jobs
    if year==10:
        complaints='A serious complaint remains unresolved.' if s['complaint'] else 'No serious complaint remains unresolved.'
        return f"Your record includes {s['penalties']} upheld major penalties and {s['redundancies']} involuntary job losses. "+complaints
    return service


def event_context(company, year):
    preview=copy.deepcopy(company)
    preview['year']=year;preview['phase']='event'
    timeline=outcomes.replay(preview)['timeline']
    rule=outcomes.MODEL['rules'][str(year)].get(current_choice(company,year),{}).get('consequence')
    return ' '.join(line for line in timeline[-1]['log'] if not line.startswith('Year-end cash movement') and line!=rule) if timeline else outcomes.MODEL['events'].get(str(year),'Review the current company record.')


def resolve_passive_years(session, company):
    while company['year'] not in session['active_years'] and not company['complete']:
        y=company['year']
        record(company,y,DEFAULTS[y],'facilitator_skip','facilitator')
        if y<10:
            company['history'].append({'year':y,'type':'event','title':CONTENT['events'][y]['title'], 'update':event_context(company,y)})
        # Checkpoints apply even when their decision was skipped.
        if y==5 and not session['released5']:
            company['phase']='checkpoint'
            return
        if y==10:
            company['complete']=True
            company['phase']='report'
            return
        company['year']+=1
        company['phase']='decision'
    company['deadline']=time.time()+session['minutes']*60 if session['minutes'] else None

def tick(session, company):
    if company['phase']=='decision' and not company['paused'] and str(company['year']) not in company['decisions']:
        deadline=company.get('deadline')
        if deadline and time.time()>=deadline:
            # Timeout is an outcome of inaction, not an instructor skip.
            year=company['year']
            record(company,year,DEFAULTS[year],'deadline','system')

def public_company(company):
    safe={key:copy.deepcopy(company[key]) for key in ['id','name','country','year','phase','version','decisions','history','deadline','paused','interventions','complete']}
    safe['roles_taken']=list(company['members'])
    safe['performance']=outcomes.replay(company)
    before=copy.deepcopy(company)
    before['decisions'].pop(str(company['year']),None)
    state=outcomes.replay(before)['state']
    safe['financials']={
        'cash_before_decision':state['cash'],'debt_before_decision':state['debt'],
        'cash_now':safe['performance']['state']['cash'],'debt_now':safe['performance']['state']['debt'],
        'history':[{'year':0,'cash':outcomes.MODEL['initial']['cash']}]+[
            {'year':step['year'],'cash':step['state']['cash']} for step in safe['performance']['timeline']],
        'offers':[{ 'id':option['id'],
            'upfront_change':outcomes.MODEL['rules'][str(company['year'])][option['id']]['changes'].get('cash',0),
            'cash_after_upfront':state['cash']+outcomes.MODEL['rules'][str(company['year'])][option['id']]['changes'].get('cash',0)
        } for option in CONTENT['years'][company['year']]['options']]
    }
    if safe['financials']['history'][-1]['cash']!=safe['financials']['cash_now']:
        safe['financials']['history'].append({'year':company['year'],'cash':safe['financials']['cash_now'],'current':True})
    safe['unavailable']={o['id']:outcomes.gate(company['year'],o['id'],state) for o in CONTENT['years'][company['year']]['options'] if outcomes.gate(company['year'],o['id'],state)}
    for action in company['interventions']:
        if action['year']==company['year'] and action['role'] in ('cfo','cto','legal'):
            safe['unavailable'][action['option']]=CONTENT['roles'][action['role']][0]+': '+action['reason']
    if safe['performance']['timeline']:
        safe['context']=' '.join(safe['performance']['timeline'][-1]['log'][:1])
    safe['context']=company_context(company,company['year'],safe['performance']['state'])
    safe['event_context']=event_context(company,company['year']) if company['phase']=='event' else None
    safe['story']=narrative.company_story(company)
    return safe

class PDF(bytes):
    pass

def participant_roster(session, detailed=False):
    rows=[]
    for c in session['companies'].values():
        for role, member in c['members'].items():
            notes=[{'stage':key,**note} for key,note in member.get('notes',{}).items() if note['text'].strip()]
            notes.sort(key=lambda note:(int(note['stage'].split(':')[0]),note['saved']))
            actions=[f'Year {action["year"]} - {CONTENT["roles"][role][3]}: {action["reason"]}'
                     for action in c['interventions'] if action['role']==role]
            row={'participant_id':member.get('participant_id',''),'name':member.get('name','Name not provided'),
                 'company_id':c['id'],'company':c['name'],'role_id':role,'role':CONTENT['roles'][role][0],
                 'reflections_saved':len(notes),'years':sorted({int(note['stage'].split(':')[0]) for note in notes}), 'actions':actions}
            if detailed:row['reflections']=notes
            rows.append(row)
    return rows

def report_company(company):
    result=public_company(company)
    if company['phase']=='event':
        year=company['year']
        result['current_event']={'year':year,'type':'event','title':CONTENT['events'][year]['title'],'update':event_context(company,year)}
    return result


def public_content():
    c=copy.deepcopy(CONTENT)
    for y in c['years'][1:]:
        y.pop('info',None)
    for e in c['events'][1:]:
        e.pop('impacts',None)
    c['roles']={key:{'title':value[0]} for key,value in c['roles'].items()}
    c.pop('stories',None)
    return c

def response_state(row, session, company, access, role):
    result={'session':{'id':row['id'],'code':row['code'],'label':session['label'],'roles':role_list(session['role_count']),
        'active_years':session['active_years'],'minutes':session['minutes'],'released5':session['released5']},'company':public_company(company),'access':access}
    if access in ('company','facilitator'):result['join_token']=company['phone_key']
    if access!='facilitator':result['company']['performance'].pop('missions',None)
    if role:
        result['mission_target']=outcomes.MODEL['missions'][role]
        result['mission_met']=outcomes.replay(company)['missions'].get(role)
        result['role']={'id':role,'title':CONTENT['roles'][role][0],'mission':CONTENT['roles'][role][1],
            'power':CONTENT['roles'][role][3], 'power_description':CONTENT['roles'][role][4], 'story':CONTENT['stories'][role].replace('{company}',company['name'])}
        if company['phase']=='event':
            e=CONTENT['events'][company['year']]
            result['briefing']=[e['story'],e['impacts'][role],'What does this update mean for your mission, and what would you discuss with the team?']
        else:
            result['briefing']=list(CONTENT['years'][company['year']]['info'][role])
            position=outcomes.replay(company)['state']
            observation={'ceo':f"Market presence is {position['growth']:.0f}, from 100 at the start.",'cfo':f"Cash is EUR {position['cash']:,.0f}k; debt is EUR {position['debt']:,.0f}k.",'cto':f"Reliability is {position['reliability']:.0f}%; technical control is {position['control']:.0f}/100.",'marketing':f"Trust is {position['trust']:.0f}/100 and market presence is {position['growth']:.0f}.",'legal':f"Upheld major penalties: {position['penalties']}; unresolved serious complaint: {'yes' if position['complaint'] else 'no'}.",'employee':f"Involuntary redundancies so far: {position['redundancies']}.",'sustainability':f"Operational footprint index: {position['footprint']:.0f}, from 100 at the start.",'relations':f"Original venues retained: {position['contracts']}/10; new partnerships: {position['new_partners']}."}[role]
            result['briefing_body']=list(result['briefing'])
            result['briefing'][0]=observation+' '+result['briefing'][0]
        result['participant']={k:company['members'][role].get(k,'') for k in ('name','participant_id')}
        result['notes']=company['members'][role].get('notes',{})
        result['power_used']=company['members'][role].get('power_used',False)
        result['role_message']=narrative.private_message(company,role,CONTENT)
    return result

def sqlite_archive(session, identity, code):
    with closing(sqlite3.connect(':memory:')) as archive:
        archive.executescript('''
            CREATE TABLE session(id TEXT PRIMARY KEY, code TEXT, label TEXT, settings_json TEXT);
            CREATE TABLE companies(id TEXT PRIMARY KEY, session_id TEXT REFERENCES session(id), name TEXT, country TEXT, year INTEGER, phase TEXT);
            CREATE TABLE participants(id TEXT PRIMARY KEY, company_id TEXT REFERENCES companies(id), name TEXT, role_id TEXT, role_title TEXT);
            CREATE TABLE decisions(company_id TEXT REFERENCES companies(id), year INTEGER, option TEXT, reason TEXT, actor TEXT, recorded_at REAL, PRIMARY KEY(company_id,year));
            CREATE TABLE notes(participant_id TEXT REFERENCES participants(id), stage TEXT, text TEXT, saved_at REAL, PRIMARY KEY(participant_id,stage));
            CREATE TABLE history(company_id TEXT REFERENCES companies(id), position INTEGER, year INTEGER, type TEXT, detail_json TEXT, PRIMARY KEY(company_id,position));
        ''')
        settings={k:session[k] for k in ('minutes','role_count','active_years')}
        archive.execute('INSERT INTO session VALUES (?,?,?,?)',(identity,code,session['label'],json.dumps(settings)))
        for c in session['companies'].values():
            archive.execute('INSERT INTO companies VALUES (?,?,?,?,?,?)',(c['id'],identity,c['name'],c['country'],c['year'],c['phase']))
            for r,m in c['members'].items():
                participant=m.get('participant_id') or c['id']+':'+r
                archive.execute('INSERT INTO participants VALUES (?,?,?,?,?)',(participant,c['id'],m.get('name','Name not provided'),r,CONTENT['roles'][r][0]))
                for stage,n in m.get('notes',{}).items():
                    archive.execute('INSERT INTO notes VALUES (?,?,?,?)',(participant,stage,n['text'],n['saved']))
            for year,d in c['decisions'].items():
                archive.execute('INSERT INTO decisions VALUES (?,?,?,?,?,?)',(c['id'],int(year),d['option'],d['reason'],d['actor'],d['at']))
            for i,h in enumerate(c['history']):
                archive.execute('INSERT INTO history VALUES (?,?,?,?,?)',(c['id'],i,h['year'],h['type'],json.dumps(h,ensure_ascii=False)))
        archive.commit()
        return archive.serialize()

def dispatch(method, path, body, token):
    import sys
    import service_v4
    application=sys.modules[__name__]
    if service_v4.handles(application,method,path,body):
        return service_v4.dispatch(application,method,path,body,token)
    pieces=[p for p in path.split('/') if p]
    if path=='/api/decision-tree':
        if not token or not secrets.compare_digest(token,teacher_key()):raise Problem('Open teacher setup on this laptop first.',403)
        if method=='GET':return {'model':outcomes.MODEL,'content':CONTENT}
        choices=body.get('choices',{})
        if not isinstance(choices,dict):raise Problem('Choose a path through the tree.')
        for year,option in choices.items():
            if year not in outcomes.MODEL['rules'] or option not in outcomes.MODEL['rules'][year]:raise Problem('Unknown branch.')
        company={'decisions':{k:{'option':v,'reason':'decision'} for k,v in choices.items()},'interventions':[],'history':[], 'year':min(10,len(choices)+1),'phase':'report' if len(choices)==10 else 'decision','complete':len(choices)==10}
        for year in sorted(choices,key=int):
            if list(sorted(int(k) for k in choices))!=list(range(1,len(choices)+1)):raise Problem('Choose a continuous path from Year 1.')
            prefix=copy.deepcopy(company);prefix['decisions']={k:v for k,v in company['decisions'].items() if int(k)<int(year)}
            prefix['year']=int(year);prefix['phase']='decision';prefix['complete']=False
            problem=outcomes.gate(int(year),choices[year],outcomes.replay(prefix)['state'])
            if problem:raise Problem(problem,409)
        return outcomes.replay(company)
    if method=='GET' and path=='/api/health':
        return {'status':'ok'}
    if method=='GET' and path=='/api/content':
        return public_content()
    if method=='POST' and path=='/api/sessions':
        if not token or not secrets.compare_digest(token,teacher_key()):raise Problem('Open the teacher setup screen on the laptop running VFI simulation.',403)
        label=text(body.get('label'),'a session name',80)
        minutes=body.get('minutes',5)
        count=body.get('role_count',6)
        active=body.get('active_years',list(range(1,11)))
        if type(minutes) not in (int,float) or not 0<=minutes<=30 or type(count) is not int or count not in (6,7,8):
            raise Problem('Choose 6–8 roles and 0–30 minutes per decision.')
        if not isinstance(active,list) or not active or any(type(y) is not int or not 1<=y<=10 for y in active):
            raise Problem('Choose at least one decision year.')
        secret=secrets.token_urlsafe(32)
        identity=secrets.token_hex(12)
        session={'label':label,'minutes':minutes,'role_count':count,'active_years':sorted(set(active)),
                 'released5':False,'companies':{},'created':time.time(),
                 'password':''.join(secrets.choice('23456789') for _ in range(6)),
                 'projector':secrets.token_urlsafe(32),'join_keys':[]}
        with transaction() as con:
            for _ in range(10):
                code=''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(6))
                try:
                    con.execute('INSERT INTO sessions VALUES (?,?,?,?)',(identity,code,digest(secret),json.dumps(session)))
                    break
                except sqlite3.IntegrityError:
                    continue
            else:
                raise Problem('Could not create a code. Try again.',503)
        return {'id':identity,'code':code,'token':secret}
    if len(pieces)<3 or pieces[:2]!=['api','sessions']:
        raise Problem('Not found.',404)
    identity=pieces[2]
    with transaction() as con:
        row,session=load(con,identity)
        if len(pieces)==4 and pieces[3]=='join' and method=='POST':
            if not secrets.compare_digest(str(body.get('password','')),session.get('password','!')):
                raise Problem('The session password is incorrect.',403)
            join_token=secrets.token_urlsafe(32)
            session.setdefault('join_keys',[]).append(digest(join_token))
            save(con,row['id'],session)
            return {'id':row['id'],'code':row['code'],'token':join_token}
        if len(pieces)==4 and pieces[3]=='summary' and method=='GET':
            if not token or not secrets.compare_digest(digest(token),row['secret']):raise Problem('Teacher access required.',403)
            companies=list(session['companies'].values())
            completed=sum(bool(c['complete']) for c in companies)
            return {'id':row['id'],'code':row['code'],'label':session['label'],'created':session['created'],
                    'company_count':len(companies),'completed_count':completed,
                    'status':'past' if companies and completed==len(companies) else 'active'}
        if len(pieces)==4 and pieces[3]=='projection' and method=='GET':
            if not token or not (secrets.compare_digest(token,session.get('projector','!')) or secrets.compare_digest(digest(token),row['secret'])):
                raise Problem('Projection access required.',403)
            return {'id':row['id'],'code':row['code'],'label':session['label'],'password':session.get('password',''),'comparison':outcomes.comparison(list(session['companies'].values()))}
        if len(pieces)==4 and pieces[3]=='locate' and method=='POST':
            if not joined(session,token):raise Problem('Enter the session password first.',403)
            name=text(body.get('name'),'your company name',60)
            for c in session['companies'].values():
                if c['name'].casefold()==name.casefold():return {'id':c['id']}
            raise Problem('That company has not joined yet. Start on the shared company laptop first.',404)
        if len(pieces)==3 and method=='GET':
            is_teacher=token and secrets.compare_digest(digest(token),row['secret'])
            if is_teacher:
                for c in session['companies'].values():tick(session,c)
                save(con,row['id'],session)
                return {'id':row['id'],'code':row['code'],**{k:session[k] for k in ['label','minutes','role_count','active_years','released5','password','projector']},
                    'companies':[public_company(c) for c in session['companies'].values()], 'comparison':outcomes.comparison(list(session['companies'].values())), 'roster':participant_roster(session)}
            if token:
                raise Problem('This teacher link is not recognised. Reopen the saved link for this session.',403)
            return {'id':row['id'],'code':row['code'],'label':session['label'],'roles':role_list(session['role_count'])}
        if len(pieces)==4 and pieces[3]=='companies' and method=='POST':
            if not joined(session,token) and not secrets.compare_digest(digest(token),row['secret']):raise Problem('Enter the session password first.',403)
            name=text(body.get('name'),'a company name',60)
            for existing in session['companies'].values():
                if existing['name'].casefold()==name.casefold():
                    secret=secrets.token_urlsafe(32)
                    existing.setdefault('resume_secrets',[]).append(digest(secret))
                    save(con,row['id'],session)
                    return {'session_id':row['id'],'id':existing['id'],'token':secret}
            country=text(body.get('country'),'an EU country',40)
            if any(c['name'].casefold()==name.casefold() for c in session['companies'].values()):
                raise Problem('That company name is in use. Reopen its saved link or choose another name.',409)
            if len(session['companies'])>=20:raise Problem('This session already has 20 companies.',409)
            cid=secrets.token_hex(10);secret=secrets.token_urlsafe(32)
            c={'id':cid,'name':name,'country':country,'secret':digest(secret),'phone_key':secrets.token_urlsafe(32),'year':1,'phase':'decision','version':0,
               'decisions':{},'history':[],'members':{},'interventions':[],'paused':None,'complete':False}
            resolve_passive_years(session,c)
            c['deadline']=None
            c['started']=False
            session['companies'][cid]=c
            save(con,row['id'],session)
            return {'session_id':row['id'],'id':cid,'token':secret}
        if len(pieces)==4 and pieces[3] in ('participation','participation.pdf','reports.pdf','logs.pdf') and method=='GET':
            if not token or not secrets.compare_digest(digest(token),row['secret']):raise Problem('Teacher access required.',403)
            if pieces[3]=='participation':return {'rows':participant_roster(session,True)}
            import reports
            for company in session['companies'].values():tick(session,company)
            save(con,row['id'],session)
            if pieces[3]=='participation.pdf':return PDF(reports.participation_pdf(participant_roster(session,True),session['label']))
            return PDF(reports.company_pdf([report_company(c) for c in session['companies'].values()],session['label'],CONTENT,participants=participant_roster(session,True) if pieces[3]=='logs.pdf' else None))
        if len(pieces)==4 and pieces[3]=='content' and method=='GET':
            if not token or not secrets.compare_digest(digest(token),row['secret']):raise Problem('This action needs the teacher’s session link.',403)
            return CONTENT
        if len(pieces)==4 and pieces[3] in ('control','export','database'):
            if not token or not secrets.compare_digest(digest(token),row['secret']):raise Problem('This action needs the teacher’s session link.',403)
            if pieces[3]=='database' and method=='GET':return sqlite_archive(session,row['id'],row['code'])
            if pieces[3]=='export' and method=='GET':
                exported=copy.deepcopy(session)
                for key in ('password','projector','join_keys'):exported.pop(key,None)
                for c in exported['companies'].values():
                    c['performance']=outcomes.replay(c)
                    c['story']=narrative.company_story(c)
                    for key in ('secret','phone_key','resume_secrets'):c.pop(key,None)
                    for member in c['members'].values():member.pop('secret',None)
                return {'schema':'fairpass.session.v1','session_id':row['id'],'code':row['code'],**exported}
            if method!='POST':raise Problem('Method not allowed.',405)
            action=body.get('action')
            if action=='release5':
                companies=list(session['companies'].values())
                if not companies:raise Problem('No companies have joined yet.',409)
                if not all(str(5) in c['decisions'] for c in companies) and not body.get('force'):
                    raise Problem('Some teams have not reached Year 5. The advance control can move them to the last selected decision before the checkpoint.',409)
                session['released5']=True
                for c in companies:
                    if c['phase']=='checkpoint':
                        if 5 not in session['active_years']:
                            c['year']=6;c['phase']='decision';resolve_passive_years(session,c)
                        else:c['phase']='event'
                        c['version']+=1
            elif action=='advance_decision':
                checkpoint=body.get('checkpoint')
                if type(checkpoint) is not int or checkpoint not in (5,10):raise Problem('Choose the Year 5 or final checkpoint.')
                if checkpoint==5 and session['released5']:raise Problem('The Year 5 checkpoint has already been released.',409)
                if checkpoint==10 and not session['released5']:raise Problem('Release the Year 5 checkpoint before advancing the second part.',409)
                active=[y for y in session['active_years'] if (0 if checkpoint==5 else 5)<y<=checkpoint]
                if not active:raise Problem('No team decision is selected before this checkpoint.',409)
                target=max(active)
                for c in session['companies'].values():
                    # Already-arrived teams retain their decision, phase, timer and any intervention.
                    if c['complete'] or c['year']>=target:continue
                    for year in range(c['year'],target):
                        record(c,year,DEFAULTS[year],'facilitator_skip','facilitator')
                        if not any(h['type']=='event' and h['year']==year for h in c['history']):
                            c['history'].append({'year':year,'type':'event','title':CONTENT['events'][year]['title'],'update':event_context(c,year)})
                    c['year']=target;c['phase']='decision';c['paused']=None
                    c['deadline']=time.time()+session['minutes']*60 if session['minutes'] and c.get('started') else None
                    c['version']+=1
            elif action in ('advance5','finish'):
                target=5 if action=='advance5' else 10
                for c in session['companies'].values():
                    if c['complete'] or c['year']>target:continue
                    if action=='advance5' and c['year']==5 and session['released5'] and '5' in c['decisions']:continue
                    for year in range(c['year'],target+1):
                        record(c,year,DEFAULTS[year],'facilitator_skip','facilitator')
                        if year<target:c['history'].append({'year':year,'type':'event','title':CONTENT['events'][year]['title'],'update':event_context(c,year)})
                    c['year']=target;c['paused']=None;c['deadline']=None
                    c['phase']='checkpoint' if target==5 else 'report';c['complete']=target==10;c['version']+=1
            elif action=='resume':
                c=company_by_id(session,body.get('company'))
                c['paused']=None;c['deadline']=time.time()+session['minutes']*60 if session['minutes'] else None;c['version']+=1
                c['history'].append({'year':c['year'],'type':'facilitator_review','note':text(body.get('note'),'a short review outcome',500)})
            else:raise Problem('Unknown facilitator action.')
            save(con,row['id'],session)
            return {'ok':True}
        if len(pieces)<5 or pieces[3]!='companies':raise Problem('Not found.',404)
        c=company_by_id(session,pieces[4])
        if len(pieces)==6 and pieces[5]=='claim' and method=='POST':
            if not group_joined(session,c,token):raise Problem('Use the company QR code or enter the session password.',403)
            role=body.get('role')
            if role not in role_list(session['role_count']):raise Problem('This role is not available in this session.')
            if role in role_list(session['role_count'])[6:] and any(core not in c['members'] for core in role_list(6)):
                raise Problem('The six core roles must be chosen before the additional roles.',409)
            if role in c['members']:raise Problem('That role has already been chosen. Choose another.',409)
            name=text(body.get('name'),'your name',100)
            secret=secrets.token_urlsafe(32)
            c['members'][role]={'name':name,'participant_id':secrets.token_hex(12),'secret':digest(secret),'notes':{},'power_used':False};c['version']+=1
            save(con,row['id'],session)
            return {'token':secret,'role':role,'session_id':row['id'],'company_id':c['id']}
        if len(pieces)==6 and pieces[5]=='roles' and method=='GET':
            if not group_joined(session,c,token):raise Problem('Use the company QR code or enter the session password.',403)
            return {'name':c['name'],'roles':role_list(session['role_count']),'taken':list(c['members'])}
        access,role=authority(row,c,token)
        tick(session,c)
        if len(pieces)==6 and pieces[5] in ('report.pdf','personal.pdf') and method=='GET':
            import reports
            if pieces[5]=='personal.pdf' and not role:raise Problem('Use your private role link for your reflections.',403)
            personal=None
            if pieces[5]=='personal.pdf':
                member=c['members'][role]
                personal={'closing_message':narrative.private_message(c,role,CONTENT),'name':member.get('name',''),'role':CONTENT['roles'][role][0],'notes':member['notes'],'mission':outcomes.MODEL['missions'][role],'mission_outcome':('Mission achieved' if outcomes.replay(c)['missions'].get(role) else 'Mission not achieved') if c['complete'] else 'Your mission is evaluated after Year 10.'}
            save(con,row['id'],session)
            return PDF(reports.company_pdf([report_company(c)],session['label'],CONTENT,personal))
        if len(pieces)==5 and method=='GET':
            save(con,row['id'],session)
            return response_state(row,session,c,access,role)
        if len(pieces)==6 and pieces[5]=='actions' and method=='POST':
            action=body.get('action');year=c['year']
            if action=='start':
                if access not in ('company','facilitator'):raise Problem('Start on the shared company laptop.',403)
                if not c.get('started'):
                    c['started']=True
                    c['deadline']=time.time()+session['minutes']*60 if session['minutes'] and c['phase']=='decision' else None
                    c['version']+=1
            elif action=='note':
                if not role:raise Problem('A student role is required to save individual notes.',403)
                key=body.get('key')
                if not isinstance(key,str) or key not in [f'{y}:{phase}' for y in range(1,11) for phase in ('decision','event','checkpoint','report')]:raise Problem('Invalid note location.')
                note=body.get('note','')
                if not isinstance(note,str) or len(note)>4000:raise Problem('Keep notes within 4,000 characters.')
                c['members'][role]['notes'][key]={'text':note,'saved':time.time()}
            elif action=='power':
                if not role:raise Problem('Choose your own role to use a power.',403)
                if c['phase']!='decision' or str(year) in c['decisions']:raise Problem('The current decision has already closed.',409)
                member=c['members'][role]
                if member['power_used'] and role!='ceo':raise Problem('Your intervention has already been used.',409)
                if body.get('year')!=year:raise Problem('The company has moved to another year. Refresh first.',409)
                explanation=text(body.get('reason'),'a reason for the intervention',500)
                option=body.get('option')
                available={o['id'] for o in CONTENT['years'][year]['options']}
                if role in ('ceo','cto','cfo','legal') and option not in available:raise Problem('Choose the option affected by the intervention.')
                if role=='ceo':
                    validate_decision(c,option)
                    record(c,year,option,'executive_override','ceo')
                elif role in ('cfo','cto','legal'):
                    before=outcomes.replay(c)['state']
                    candidates=[o['id'] for o in CONTENT['years'][year]['options'] if o['id']!=option and not outcomes.gate(year,o['id'],before)]
                    blocked={i['option'] for i in c['interventions'] if i['year']==year and i['role'] in ('cfo','cto','legal')}
                    if not set(candidates)-blocked:raise Problem('At least one feasible option must remain.',409)
                member['power_used']=True
                c['interventions'].append({'role':role,'year':year,'reason':explanation,'option':option,'at':time.time()})
                c['history'].append({'year':year,'type':'intervention','role':role,'reason':explanation,'option':option});c['version']+=1
            elif action=='decide':
                if access not in ('company','facilitator'):raise Problem('Record company decisions on the company screen.',403)
                if body.get('year')!=year or body.get('version')!=c['version']:raise Problem('The company has an update. Read it before saving your decision.',409)
                if c['phase']!='decision' or str(year) in c['decisions']:raise Problem('This decision has already been recorded.',409)
                option=body.get('option')
                if option not in {o['id'] for o in CONTENT['years'][year]['options']}:raise Problem('Choose an available option.')
                validate_decision(c,option)
                record(c,year,option)
            elif action=='advance':
                if access not in ('company','facilitator'):raise Problem('Continue on the company screen.',403)
                if body.get('year')!=year or body.get('version')!=c['version']:raise Problem('The company has an update. Refresh the page before continuing.',409)
                if c['phase']=='decision':
                    if str(year) not in c['decisions']:raise Problem('Record the decision first.')
                    if year==10:c['phase']='report';c['complete']=True
                    elif year==5 and not session['released5']:c['phase']='checkpoint'
                    else:c['phase']='event'
                elif c['phase']=='event':
                    c['history'].append({'year':year,'type':'event','title':CONTENT['events'][year]['title'],'update':event_context(c,year)})
                    c['year']+=1;c['phase']='decision';resolve_passive_years(session,c)
                elif c['phase']=='checkpoint':raise Problem('Your teacher will open the next part after the Year 5 discussion.',409)
                else:raise Problem('The company has completed the simulation.',409)
                c['version']+=1
            else:raise Problem('Unknown company action.')
            save(con,row['id'],session)
            return response_state(row,session,c,access,role)
        raise Problem('Not found.',404)

def validate_decision(company,option):
    if company['paused']:raise Problem('A role action has paused this decision. Your teacher needs to review it before the team continues.',409)
    state=outcomes.replay(company)['state']
    problem=outcomes.gate(company['year'],option,state)
    if problem:raise Problem(problem,409)
    blocked=[i for i in company['interventions'] if i['year']==company['year'] and i['role'] in ('cto','cfo','legal') and i['option']==option]
    if blocked:raise Problem('That option is blocked by a recorded intervention. Consider another option.',409)

def network_join_origin(bound_host, port, local_ip):
    configured=os.environ.get('FAIRPASS_PUBLIC_ORIGIN','').rstrip('/')
    if configured:
        parsed=urlparse(configured)
        if parsed.scheme in ('https','http') and parsed.netloc and not parsed.username and not parsed.password and parsed.path=='' and not parsed.query and not parsed.fragment:return configured
    if bound_host in ('127.0.0.1','localhost','::1'):return None
    candidates=[local_ip]
    if local_ip.startswith('127.'):
        try:candidates=socket.gethostbyname_ex(socket.gethostname())[2]
        except OSError:return None
    for address in candidates:
        try:ip=ipaddress.ip_address(address)
        except ValueError:continue
        if ip.version==4 and ip.is_private and not ip.is_loopback and not ip.is_link_local:
            return f'http://{address}:{port}'
    return None

def local_teacher_request(client, local, host, fetch_site=''):
    # Only the computer running the preview can recover its existing teacher access.
    # A student's phone, cross-site request or arbitrary rebinding hostname cannot.
    try:
        client_ip=ipaddress.ip_address(client)
        local_ip=ipaddress.ip_address(local)
        hostname=urlparse('http://'+host).hostname
        host_ok=hostname=='localhost' or ipaddress.ip_address(hostname) in (local_ip,ipaddress.ip_address('127.0.0.1'))
        return (client_ip.is_loopback or client_ip==local_ip) and host_ok and fetch_site in ('','none','same-origin')
    except ValueError:
        return False

class Handler(BaseHTTPRequestHandler):
    server_version='VFI simulation'
    def log_message(self,*args):
        pass  # Do not log bearer links, individual notes or student request paths.
    def do_GET(self):self.handle_request('GET')
    def do_POST(self):self.handle_request('POST')
    def handle_request(self,method):
        path=urlparse(self.path).path
        if path.startswith('/api/'):
            try:
                body={}
                if method=='POST':
                    length=int(self.headers.get('Content-Length','0'))
                    if length<0 or length>50000:raise Problem('Request is too large.',413)
                    body=json.loads(self.rfile.read(length) or b'{}')
                    if not isinstance(body,dict):raise Problem('Expected a JSON object.')
                    origin=self.headers.get('Origin')
                    if origin and urlparse(origin).netloc!=self.headers.get('Host'):raise Problem('Use this server’s own page to make changes.',403)
                if path=='/api/connection' and method=='GET':
                    self.json_response({'join_origin':network_join_origin(self.server.server_address[0],self.server.server_address[1],self.connection.getsockname()[0])});return
                if path=='/api/teacher-access' and method=='GET':
                    if not local_teacher_request(self.client_address[0],self.connection.getsockname()[0],self.headers.get('Host',''),self.headers.get('Sec-Fetch-Site','')):
                        raise Problem('Open teacher setup on the laptop running VFI simulation, or use your saved teacher link.',403)
                    self.json_response({'token':teacher_key()});return
                auth=self.headers.get('Authorization','')
                result=dispatch(method,path,body,auth.removeprefix('Bearer '))
                if isinstance(result,bytes):
                    self.send_response(200);self.common_headers();self.send_header('Content-Type','application/pdf' if isinstance(result,PDF) else 'application/vnd.sqlite3');self.send_header('Content-Disposition','inline; filename="fairpass-report.pdf"' if isinstance(result,PDF) else 'attachment; filename="fairpass-session.sqlite3"');self.send_header('Content-Length',str(len(result)));self.end_headers();self.wfile.write(result)
                else:self.json_response(result)
            except Problem as e:self.json_response({'error':e.message},e.status)
            except (ValueError,TypeError):self.json_response({'error':'Invalid request data.'},400)
            except Exception:
                self.json_response({'error':'The server could not complete the request. Your saved work has not been replaced.'},500)
            return
        if method!='GET':self.json_response({'error':'Not found.'},404);return
        dist=ROOT/'dist'
        relative=path.lstrip('/') or 'index.html'
        target=(dist/relative).resolve()
        if not target.is_relative_to(dist.resolve()):self.json_response({'error':'Not found.'},404);return
        if not target.is_file():
            if '.' not in Path(relative).name:target=dist/'index.html'
            else:self.json_response({'error':'Not found.'},404);return
        if not target.is_file():self.json_response({'error':'Build the interface with npm run build first.'},503);return
        types={'.mp4':'video/mp4','.vtt':'text/vtt; charset=utf-8','.mp3':'audio/mpeg','.wav':'audio/wav','.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.woff':'font/woff','.woff2':'font/woff2'}
        data=target.read_bytes();self.send_response(200);self.common_headers();self.send_header('Content-Type',types.get(target.suffix,'application/octet-stream'));self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def common_headers(self):
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'")
    def json_response(self,value,status=200):
        data=json.dumps(value,ensure_ascii=False).encode();self.send_response(status);self.common_headers();self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--host',default='127.0.0.1');parser.add_argument('--port',type=int,default=8766);args=parser.parse_args()
    initialise();print(f'VFI simulation is running at http://{args.host}:{args.port}',flush=True)
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
