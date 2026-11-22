import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import server as app


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        app.DB = Path(self.tmp.name) / 'test.sqlite3'
        app.TEACHER_KEY='local-test-teacher'
        app.initialise()
        self.s = self.call('POST', '/api/sessions', {'label':'Test','minutes':0,'role_count':8})
        self.base = '/api/sessions/' + self.s['id']
        self.c = self.call('POST', self.base+'/companies', {'name':'Example','country':'Sweden'})
        self.path = self.base+'/companies/'+self.c['id']
        teacher=self.call('GET',self.base,token=self.s['token'])
        self.password=teacher['password']
        self.join_token=self.call('POST',self.base+'/join',{'password':self.password})['token']
        self.tokens = {}
        for role in app.role_list(8):
            self.tokens[role] = self.call('POST',self.path+'/claim',{'role':role})['token']

    def test_company_context_tracks_late_acquisition(self):
        company={'year':3,'decisions':{'1':{'option':'wait'},'2':{'option':'late_buy'}},'interventions':[]}
        context=app.company_context(company,3)
        self.assertIn('Verity',context)
        self.assertNotIn('no buyer-verification prototype',context)
        self.assertIn('no new testing evidence',context)
        self.assertFalse(app.outcomes.replay(company)['state']['live'])

    def test_company_context_keeps_purchase_checks_separate_from_entry(self):
        choices=['hybrid','broad','broad','support','analytics','alternative']
        company={'year':7,'decisions':{str(n):{'option':v} for n,v in enumerate(choices,1)},'interventions':[]}
        context=app.company_context(company,7)
        self.assertIn('offline codes',context)
        self.assertIn('do not retain individual attendance records',context)
        self.assertNotIn('facial recognition',context)

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, method, path, body=None, token=''):

        if method=='POST' and path=='/api/sessions' and not token:token=app.TEACHER_KEY
        if method=='POST' and path.endswith('/companies') and not token:token=self.s['token']
        if method=='POST' and path.endswith('/claim'):
            if not token:token=self.join_token
            body={'name':'Test '+str((body or {}).get('role','student')),**(body or {})}
        return app.dispatch(method,path,body or {},token)

    def state(self, role=None):
        return self.call('GET',self.path,token=self.tokens[role] if role else self.c['token'])

    def act(self, action, role=None, **extra):
        c=self.state()['company']
        return self.call('POST',self.path+'/actions',{'action':action,'year':c['year'],'version':c['version'],**extra},self.tokens[role] if role else self.c['token'])

    def test_session_summaries_classify_completion_without_exposing_participants(self):
        with self.assertRaises(app.Problem):self.call('GET',self.base+'/summary')
        with self.assertRaises(app.Problem):self.call('GET',self.base+'/summary',token=self.c['token'])
        summary=self.call('GET',self.base+'/summary',token=self.s['token'])
        self.assertEqual(summary['status'],'active')
        self.assertEqual(summary['company_count'],1)
        self.assertEqual(set(summary),{'id','code','label','created','company_count','completed_count','status'})
        empty=self.call('POST','/api/sessions',{'label':'Empty class','minutes':0,'role_count':6})
        self.assertEqual(self.call('GET','/api/sessions/'+empty['id']+'/summary',token=empty['token'])['status'],'active')
        self.call('POST',self.base+'/control',{'action':'finish'},self.s['token'])
        complete=self.call('GET',self.base+'/summary',token=self.s['token'])
        self.assertEqual((complete['status'],complete['completed_count']),('past',1))

    def test_session_logs_are_isolated_and_include_saved_work(self):
        self.act('note',role='cfo',key='1:decision',note='A fictional contribution to the decision.')
        other=self.call('POST','/api/sessions',{'label':'Second class','minutes':0,'role_count':6})
        with self.assertRaises(app.Problem):
            self.call('GET',self.base+'/logs.pdf',token=other['token'])
        with self.assertRaises(app.Problem):
            self.call('GET',self.base+'/export',token=self.c['token'])
        pdf=self.call('GET',self.base+'/logs.pdf',token=self.s['token'])
        self.assertTrue(pdf.startswith(b'%PDF'))
        data=self.call('GET',self.base+'/export',token=self.s['token'])
        self.assertEqual(data['session_id'],self.s['id'])
        self.assertNotIn('password',data)
        company=data['companies'][self.c['id']]
        self.assertIn('performance',company)
        self.assertNotIn('secret',company)
        self.assertNotIn('phone_key',company)
        self.assertNotIn('secret',company['members']['cfo'])
        self.assertEqual(company['members']['cfo']['notes']['1:decision']['text'],'A fictional contribution to the decision.')
        separate=self.call('GET','/api/sessions/'+other['id']+'/export',token=other['token'])
        self.assertEqual(separate['companies'],{})

    def test_complete_ten_years_and_checkpoint(self):
        for year in range(1,11):
            self.assertEqual(self.state()['company']['year'],year)
            self.act('decide',option=app.DEFAULTS[year])
            self.act('advance')
            if year==5:
                self.assertEqual(self.state()['company']['phase'],'checkpoint')
                with self.assertRaises(app.Problem): self.act('advance')
                self.call('POST',self.base+'/control',{'action':'release5'},self.s['token'])
            if year<10: self.act('advance')
        c=self.state()['company']
        self.assertTrue(c['complete'])
        self.assertEqual(len(c['decisions']),10)
        self.assertEqual(len([h for h in c['history'] if h['type']=='event']),9)

    def test_financial_history_includes_interventions_before_a_decision(self):
        self.act('power','employee',reason='Cover the workload')
        f=self.state()['company']['financials']
        self.assertEqual(f['cash_now'],1520)
        self.assertEqual(f['cash_before_decision'],1520)
        self.assertEqual(f['history'][-1],{'year':1,'cash':1520,'current':True})

    def test_financial_comparison_is_before_operations_and_preserves_baseline(self):
        initial=self.state()['company']['financials']
        quotes={q['id']:q for q in initial['offers']}
        self.assertEqual(initial['cash_before_decision'],1600)
        self.assertEqual(quotes['build']['cash_after_upfront'],300)
        self.assertEqual(quotes['buy']['cash_after_upfront'],800)
        self.assertEqual(quotes['hybrid']['cash_after_upfront'],700)
        self.assertEqual(quotes['wait']['cash_after_upfront'],1600)
        self.act('decide',option='build')
        saved=self.state()['company']['financials']
        self.assertEqual(saved['cash_before_decision'],1600)
        self.assertEqual(saved['cash_now'],580)
        self.assertEqual(saved['history'],[{'year':0,'cash':1600},{'year':1,'cash':580}])
        self.assertNotIn('missions',saved)

    def test_private_notes_and_role_information(self):
        content=self.call('GET','/api/content')
        self.assertNotIn('info',content['years'][1])
        self.assertNotIn('stories',content)
        self.assertNotIn('mission',content['roles']['ceo'])
        with self.assertRaises(app.Problem): self.call('GET',self.base+'/content',token=self.tokens['ceo'])
        private=self.call('GET',self.base+'/content',token=self.s['token'])
        for year in range(1,11):
            self.assertEqual(set(private['years'][year]['info']),set(app.role_list(8)))
            for briefing in private['years'][year]['info'].values(): self.assertEqual(len(briefing),3)
        ceo=self.state('ceo');cfo=self.state('cfo')
        self.assertEqual(ceo['briefing_body'],app.CONTENT['years'][1]['info']['ceo'])
        self.assertEqual(cfo['briefing_body'],app.CONTENT['years'][1]['info']['cfo'])
        self.assertNotEqual(ceo['briefing_body'],cfo['briefing_body'])
        self.assertNotIn('briefing_body',self.state())
        self.act('note','ceo',key='1:decision',note='Private reflection')
        self.assertEqual(self.state('ceo')['notes']['1:decision']['text'],'Private reflection')
        self.assertEqual(self.state('cfo')['notes'],{})
        self.assertNotIn('notes',self.state())
        export=self.call('GET',self.base+'/export',token=self.s['token'])
        self.assertNotIn('secret',json.dumps(export))
        with self.assertRaises(app.Problem): self.call('GET',self.path)
        with self.assertRaises(app.Problem): self.act('decide','ceo',option='wait')

    def test_interventions_and_stale_decisions(self):
        old=self.state()['company']
        self.act('power','cto',option='buy',reason='Integration risk')
        self.assertIn('Integration risk',self.state()['company']['unavailable']['buy'])
        with self.assertRaises(app.Problem): self.act('decide',option='buy')
        with self.assertRaises(app.Problem):
            self.call('POST',self.path+'/actions',{'action':'decide','year':1,'version':old['version'],'option':'wait'},self.c['token'])
        self.act('power','legal',option='wait',reason='Review the contract')
        with self.assertRaises(app.Problem): self.act('decide',option='wait')
        self.assertIsNone(self.state()['company']['paused'])
        self.assertEqual(self.state()['company']['performance']['state']['cash'],1565)
        self.act('power','ceo',option='hybrid',reason='Proceed with integration')
        self.assertEqual(self.state()['company']['decisions']['1']['reason'],'executive_override')

    def test_teacher_student_and_projection_boundaries(self):
        with self.assertRaises(app.Problem): app.dispatch('POST','/api/sessions',{'label':'Student'},'')
        with self.assertRaises(app.Problem): self.call('POST',self.base+'/join',{'password':'incorrect'})
        with self.assertRaises(app.Problem): self.call('GET',self.base+'/projection',token=self.join_token)
        teacher=self.call('GET',self.base,token=self.s['token'])
        projected=self.call('GET',self.base+'/projection',token=teacher['projector'])
        self.assertEqual(projected['password'],self.password)
        self.assertNotIn('companies',projected)
        self.assertNotIn('password',self.call('GET',self.base))
        located=self.call('POST',self.base+'/locate',{'name':'Example'},self.join_token)
        self.assertEqual(located['id'],self.c['id'])
        with self.assertRaises(app.Problem): app.dispatch('POST',self.base+'/companies',{'name':'Intruder','country':'Sweden'},'')
        with self.assertRaises(app.Problem): app.dispatch('POST',self.path+'/claim',{'role':'ceo'},'')

    def test_single_role_claim_under_concurrency(self):
        c=self.call('POST',self.base+'/companies',{'name':'Second','country':'Finland'})
        path=self.base+'/companies/'+c['id']+'/claim'
        def claim(_):
            try: return self.call('POST',path,{'role':'ceo'})
            except app.Problem: return None
        with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(claim,range(2)))
        self.assertEqual(sum(r is not None for r in results),1)

    def test_named_roster_is_teacher_only_and_ids_are_unique(self):
        rows=self.call('GET',self.base,token=self.s['token'])['roster']
        self.assertEqual(len(rows),8)
        self.assertEqual(len({r['participant_id'] for r in rows}),8)
        self.assertTrue(all(r['company']==self.c['id'] or r['company_id']==self.c['id'] for r in rows))
        self.assertEqual(self.state('ceo')['participant']['name'],'Test ceo')
        self.assertNotIn('roster',self.call('GET',self.base))
        self.assertNotIn('Test ceo',json.dumps(self.state()))
        self.assertNotIn('Test ceo',json.dumps(self.state('cfo')))
        c=self.call('POST',self.base+'/companies',{'name':'Empty names','country':'Sweden'})
        with self.assertRaises(app.Problem):app.dispatch('POST',self.base+'/companies/'+c['id']+'/claim',{'role':'ceo','name':'  '},self.join_token)

    def test_session_archives_preserve_roster_and_notes_without_credentials(self):
        self.act('note','ceo',key='1:decision',note='A saved reflection')
        with self.assertRaises(app.Problem):self.call('GET',self.base+'/database',token=self.tokens['ceo'])
        data=self.call('GET',self.base+'/database',token=self.s['token'])
        with sqlite3.connect(':memory:') as archive:
            archive.deserialize(data)
            self.assertEqual(archive.execute('SELECT COUNT(*) FROM participants').fetchone()[0],8)
            row=archive.execute('SELECT p.name,c.name,p.role_id,n.text FROM participants p JOIN companies c ON c.id=p.company_id JOIN notes n ON n.participant_id=p.id').fetchone()
            self.assertEqual(row,('Test ceo','Example','ceo','A saved reflection'))
            self.assertEqual(archive.execute('PRAGMA foreign_key_check').fetchall(),[])
        self.assertNotIn(self.join_token.encode(),data)
        exported=self.call('GET',self.base+'/export',token=self.s['token'])
        self.assertEqual(exported['companies'][self.c['id']]['members']['ceo']['name'],'Test ceo')
        self.assertNotIn('phone_key',json.dumps(exported))

    def test_teacher_access_recovery_is_local_and_same_origin_only(self):
        self.assertTrue(app.local_teacher_request('127.0.0.1','127.0.0.1','localhost:8766','same-origin'))
        self.assertTrue(app.local_teacher_request('192.168.1.10','192.168.1.10','192.168.1.10:8766','same-origin'))
        self.assertFalse(app.local_teacher_request('192.168.1.20','192.168.1.10','192.168.1.10:8766','same-origin'))
        self.assertFalse(app.local_teacher_request('127.0.0.1','127.0.0.1','attacker.example:8766','same-origin'))
        self.assertFalse(app.local_teacher_request('127.0.0.1','127.0.0.1','localhost:8766','cross-site'))

    def test_additional_roles_wait_for_the_six_core_roles(self):
        c=self.call('POST',self.base+'/companies',{'name':'Core first','country':'European market'})
        path=self.base+'/companies/'+c['id']+'/claim'
        with self.assertRaises(app.Problem):self.call('POST',path,{'role':'sustainability'})
        for role in app.role_list(6):self.call('POST',path,{'role':role})
        self.assertEqual(self.call('POST',path,{'role':'sustainability'})['role'],'sustainability')

    def test_advance_to_checkpoint_decision_preserves_work_and_waits_for_choice(self):
        self.act('decide',option='hybrid')
        self.act('note',role='cfo',key='1:decision',note='Keep this reflection.')
        original=self.state()['company']['decisions']['1']
        control=lambda checkpoint:self.call('POST',self.base+'/control',{'action':'advance_decision','checkpoint':checkpoint},self.s['token'])
        with self.assertRaises(app.Problem):control(10)
        control(5)
        c=self.state()['company']
        self.assertEqual((c['year'],c['phase']),(5,'decision'))
        self.assertNotIn('5',c['decisions'])
        self.assertEqual(c['decisions']['1'],original)
        self.assertEqual(c['decisions']['4']['reason'],'facilitator_skip')
        self.assertEqual(self.state('cfo')['notes']['1:decision']['text'],'Keep this reflection.')
        version=c['version'];control(5)
        self.assertEqual(self.state()['company']['version'],version)
        self.act('decide',option=app.DEFAULTS[5]);self.act('advance')
        self.assertEqual(self.state()['company']['phase'],'checkpoint')
        self.call('POST',self.base+'/control',{'action':'release5'},self.s['token'])
        self.act('advance');control(10)
        c=self.state()['company']
        self.assertEqual((c['year'],c['phase']),(10,'decision'))
        self.assertNotIn('10',c['decisions'])
        self.assertFalse(c['complete'])
        self.act('decide',option=app.DEFAULTS[10]);self.act('advance')
        self.assertTrue(self.state()['company']['complete'])
        with self.assertRaises(app.Problem):control(5)

    def test_advance_uses_last_selected_year_and_keeps_sessions_separate(self):
        s=self.call('POST','/api/sessions',{'label':'Selected decisions','minutes':0,'role_count':6,'active_years':[1,3,7,9]})
        base='/api/sessions/'+s['id']
        c=self.call('POST',base+'/companies',{'name':'Selected Co','country':'European market'},s['token'])
        path=base+'/companies/'+c['id']
        control=lambda checkpoint:self.call('POST',base+'/control',{'action':'advance_decision','checkpoint':checkpoint},s['token'])
        control(5)
        current=self.call('GET',path,token=c['token'])['company']
        self.assertEqual((current['year'],current['phase']),(3,'decision'))
        self.assertNotIn('3',current['decisions'])
        self.assertEqual(self.state()['company']['year'],1)
        def act(action,**extra):
            current=self.call('GET',path,token=c['token'])['company']
            return self.call('POST',path+'/actions',{'action':action,'year':current['year'],'version':current['version'],**extra},c['token'])
        act('decide',option=app.DEFAULTS[3]);act('advance');act('advance')
        self.assertEqual(self.call('GET',path,token=c['token'])['company']['phase'],'checkpoint')
        self.call('POST',base+'/control',{'action':'release5'},s['token'])
        control(10)
        current=self.call('GET',path,token=c['token'])['company']
        self.assertEqual((current['year'],current['phase']),(9,'decision'))
        self.assertNotIn('9',current['decisions'])

    def test_repeating_advance_five_does_not_rewind_a_released_checkpoint(self):
        self.call('POST',self.base+'/control',{'action':'advance5'},self.s['token'])
        self.call('POST',self.base+'/control',{'action':'release5'},self.s['token'])
        self.assertEqual(self.state()['company']['phase'],'event')
        self.call('POST',self.base+'/control',{'action':'advance5'},self.s['token'])
        self.assertEqual(self.state()['company']['phase'],'event')
        self.act('advance')
        self.assertEqual(self.state()['company']['year'],6)

    def test_join_links_use_the_lan_interface_when_teacher_uses_localhost(self):
        from unittest.mock import patch
        with patch.object(app.socket,'gethostbyname_ex',return_value=('laptop',[],['127.0.0.1','192.168.1.10'])):
            self.assertEqual(app.network_join_origin('0.0.0.0',8766,'127.0.0.1'),'http://192.168.1.10:8766')
        self.assertEqual(app.network_join_origin('0.0.0.0',8766,'192.168.1.10'),'http://192.168.1.10:8766')
        self.assertIsNone(app.network_join_origin('127.0.0.1',8766,'127.0.0.1'))

    def test_company_qr_and_resume_follow_brewery_flow(self):
        phone_key=self.state()['join_token']
        self.assertNotIn('join_token',self.state('ceo'))
        roles=self.call('GET',self.path+'/roles',token=phone_key)
        self.assertEqual(roles['name'],'Example')
        second=self.call('POST',self.base+'/companies',{'name':'Another','country':'Finland'})
        with self.assertRaises(app.Problem):self.call('GET',self.base+'/companies/'+second['id']+'/roles',token=phone_key)
        self.act('decide',option='hybrid')
        resumed=self.call('POST',self.base+'/companies',{'name':'Example','country':'Sweden'},self.join_token)
        self.assertEqual(resumed['id'],self.c['id'])
        state=self.call('GET',self.path,token=resumed['token'])
        self.assertEqual(state['company']['decisions']['1']['option'],'hybrid')

    def test_printable_reports_and_participation_evidence(self):
        self.act('note','ceo',key='1:decision',note='We considered dependence on the supplier.')
        self.act('power','cfo',option='buy',reason='The contract leaves too little operating capacity.')
        rows=self.call('GET',self.base+'/participation',token=self.s['token'])['rows']
        ceo=next(r for r in rows if r['role_id']=='ceo')
        cfo=next(r for r in rows if r['role_id']=='cfo')
        self.assertEqual(ceo['reflections_saved'],1)
        self.assertEqual(ceo['reflections'][0]['text'],'We considered dependence on the supplier.')
        self.assertIn('operating capacity',cfo['actions'][0])
        with self.assertRaises(app.Problem):self.call('GET',self.base+'/participation',token=self.c['token'])
        with self.assertRaises(app.Problem):self.call('GET',self.base+'/participation.pdf',token=self.tokens['ceo'])
        with self.assertRaises(app.Problem):self.call('GET',self.path+'/personal.pdf',token=self.c['token'])
        for path,token in [(self.base+'/participation.pdf',self.s['token']),
                           (self.base+'/reports.pdf',self.s['token']),
                           (self.path+'/report.pdf',self.c['token']),
                           (self.path+'/report.pdf',self.tokens['employee']),
                           (self.path+'/personal.pdf',self.tokens['ceo'])]:
            report=self.call('GET',path,token=token)
            self.assertIsInstance(report,app.PDF)
            self.assertTrue(report.startswith(b'%PDF-'))

    def test_deadline_and_skips_remain_distinct(self):
        with app.transaction() as con:
            row,s=app.load(con,self.s['id']);s['companies'][self.c['id']]['deadline']=1;app.save(con,row['id'],s)
        self.assertEqual(self.state()['company']['decisions']['1']['reason'],'deadline')
        self.call('POST',self.base+'/control',{'action':'finish'},self.s['token'])
        c=self.state()['company']
        self.assertEqual(c['decisions']['1']['reason'],'deadline')
        self.assertEqual(c['decisions']['9']['option'],'continue')
        self.assertEqual(c['decisions']['10']['reason'],'facilitator_skip')
        self.assertTrue(c['complete'])

    def test_passive_years_reach_both_checkpoints(self):
        s=self.call('POST','/api/sessions',{'label':'Short','minutes':0,'role_count':6,'active_years':[1]})
        base='/api/sessions/'+s['id'];c=self.call('POST',base+'/companies',{'name':'Short Co','country':'Sweden'},s['token'])
        path=base+'/companies/'+c['id']
        def act(action,**extra):
            current=self.call('GET',path,token=c['token'])['company']
            return self.call('POST',path+'/actions',{'action':action,'year':current['year'],'version':current['version'],**extra},c['token'])
        act('decide',option='wait');act('advance');act('advance')
        self.assertEqual(self.call('GET',path,token=c['token'])['company']['phase'],'checkpoint')
        self.call('POST',base+'/control',{'action':'release5'},s['token'])
        result=self.call('GET',path,token=c['token'])['company']
        self.assertTrue(result['complete'])
        self.assertEqual(len(result['decisions']),10)


    def test_no_launch_without_acquisition(self):
        self.act('decide',option='wait');self.act('advance');self.act('advance')
        with self.assertRaises(app.Problem):self.act('decide',option='broad')
        self.act('decide',option='existing');self.act('advance');self.act('advance')
        with self.assertRaises(app.Problem):self.act('decide',option='broad')
        self.act('decide',option='late_buy')
        self.assertTrue(self.state()['company']['performance']['state']['prototype'])
        self.assertFalse(self.state()['company']['performance']['state']['live'])

    def test_tree_access_and_private_final_missions(self):
        with self.assertRaises(app.Problem):self.call('GET','/api/decision-tree',token=self.c['token'])
        tree=self.call('GET','/api/decision-tree',token=app.TEACHER_KEY)
        self.assertEqual(len(tree['model']['missions']),8)
        with self.assertRaises(app.Problem):self.call('POST','/api/decision-tree',{'choices':{'1':'wait','2':'existing','3':'broad'}},app.TEACHER_KEY)
        self.call('POST',self.base+'/control',{'action':'finish'},self.s['token'])
        self.assertNotIn('missions',self.state()['company']['performance'])
        own=self.state('ceo')
        self.assertIsInstance(own['mission_met'],bool)
        self.assertNotIn('missions',own['company']['performance'])
        self.assertEqual(own['mission_target'],tree['model']['missions']['ceo'])

    def test_powers_have_effects_and_do_not_need_teacher_resolution(self):
        self.act('power','employee',reason='Temporary cover')
        p=self.state()['company']['performance']['state']
        self.assertEqual(p['load'],25);self.assertEqual(p['cash'],1520)
        self.assertIsNone(self.state()['company']['paused'])
        with self.assertRaises(app.Problem):self.act('power','employee',reason='Again')

if __name__=='__main__': unittest.main()
