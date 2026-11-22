"""Acceptance checks for the supplied Years 1–3 v4 rules and normal HTTP actions."""
import itertools,json,tempfile,unittest
from pathlib import Path
from copy import deepcopy
import engine_v4 as engine
import server


def company(path,year=3,mode='student_decision'):
    return dict(id='company',session_id='session',year=year,decisions={str(i+1):dict(option=option,resolution_mode=mode) for i,option in enumerate(path)},interventions=[])


class EngineAcceptance(unittest.TestCase):
    def test_all_64_paths_and_year_four(self):
        for procurement,testing,bid in itertools.product(engine.PROCUREMENT,engine.TESTING,['full','pilot','conventional','decline']):
            with self.subTest(procurement=procurement,testing=testing,bid=bid):
                c=company([procurement,testing,bid]);unchanged=deepcopy(c)
                result=engine.replay(c);state=result['state'];ledger=result['ledger']
                status=state['northstar_contract']
                expected=6-engine.PROCUREMENT[procurement]['cost']-engine.TESTING[testing]['cost']-.24-engine.CONTRACTS[status][0]
                self.assertAlmostEqual(state['cash'],expected)
                self.assertEqual(state['annual_baseline_revenue'],21.6)
                self.assertEqual(state['employees'],120)
                self.assertEqual(len({item['id'] for item in ledger}),len(ledger))
                self.assertEqual(len(ledger),4)
                self.assertEqual(result,engine.replay(c));self.assertEqual(c,unchanged)
                self.assertEqual(len(result['timeline']),3)
                self.assertTrue(all('external' in row and 'internal' in row and len(row['private'])==8 for row in result['timeline']))
                self.assertTrue(all(value>=0 for value in engine.readiness(state).values()))
                if procurement=='wait':self.assertFalse(state['vfi_operational'])
                if not status.endswith('_awarded'):self.assertEqual(state['contract_revenue'],0)
                c['year']=4;handoff=engine.replay(c)
                self.assertNotIn(handoff['state']['northstar_contract'],('full_conditional','pilot_conditional'))
                self.assertFalse(handoff['state'].get('recruitment_pressure'))
                self.assertEqual(handoff['state']['employees'],120)
                self.assertEqual(handoff,engine.replay(c))
                annual=[item for item in handoff['ledger'] if item['effect']=='annual_vfi_cost']
                self.assertEqual(len(annual),int(handoff['state']['vfi_operational']))

    def test_all_paths_under_expiry_and_skip_modes(self):
        for mode in ('deadline_expired','facilitator_skipped'):
            for options in itertools.product(engine.PROCUREMENT,engine.TESTING,['full','pilot','conventional','decline']):
                c=company(options,3,mode)
                first=engine.replay(c)
                self.assertEqual(first,engine.replay(c))
                self.assertEqual(len(first['ledger']),4)
                self.assertEqual(len({e['id'] for e in first['ledger']}),4)

    def test_review_costs_and_restructuring_proposal(self):
        c=company(['build','stress'],2)
        c['interventions']=[dict(role='legal',year=2,cost=.6)]
        r=engine.replay(c)
        self.assertTrue(r['state']['restructuring_proposed_12'])
        self.assertEqual(r['state']['employees'],120)
        self.assertEqual(r,engine.replay(c))
        self.assertEqual(sum(e['effect']=='power_legal' for e in r['ledger']),1)

    def test_starting_cash_and_defaults(self):
        for option,expected in [('build',3.2),('license',5.4),('hybrid',4.4),('wait',5.85)]:
            r=engine.replay(company([option],1))
            self.assertAlmostEqual(r['state']['cash'],expected)
            self.assertFalse(r['state']['vfi_operational'])
        for mode in ('deadline_expired','facilitator_skipped'):
            r=engine.replay(company(['hybrid','stress','conventional'],3,mode))
            self.assertEqual([s['resolution_mode'] for s in r['timeline']],[mode]*3)
            self.assertAlmostEqual(r['state']['cash'],3.71)

    def test_obligations_and_activation(self):
        c=company(['hybrid','stress','full'])
        r=engine.replay(c)
        self.assertEqual(r['state']['northstar_contract'],'full_conditional')
        c['year']=4;r=engine.replay(c)
        self.assertEqual(r['state']['northstar_contract'],'full_awarded')
        self.assertAlmostEqual(next(item['amount'] for item in r['ledger'] if item['effect']=='northstar_activation'),-.55)
        self.assertEqual(r['state']['contract_revenue'],2.4)
        c=company(['license','stress','full'])
        r=engine.replay(c)
        self.assertTrue(r['state']['support_training_needed'])
        self.assertTrue(r['state']['verification_remediation_required'])
        self.assertEqual(r['timeline'][-1]['internal']['rule'],'1. Full awarded + low customer readiness')
        c['year']=4
        self.assertTrue(engine.replay(c)['state']['support_training_outstanding'])


class HttpAcceptance(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.old_db,self.old_key=server.DB,server.TEACHER_KEY
        server.DB=Path(self.directory.name)/'test.sqlite3';server.TEACHER_KEY='fictional-v4-test'
        server.initialise()
        session=server.dispatch('POST','/api/sessions',{'rules_version':engine.VERSION,'label':'Fictional v4 class','minutes':0,'role_count':6,'active_years':[1,2,3,4,5,6,7,8,9,10]},server.TEACHER_KEY)
        self.session=session;self.base='/api/sessions/'+session['id'];self.teacher=session['token']
        state=server.dispatch('GET',self.base,{},self.teacher)
        self.join=server.dispatch('POST',self.base+'/join',{'password':state['password']},'')['token']
        self.company=server.dispatch('POST',self.base+'/companies',{'name':'Fictional Company','country':'Sweden'},self.join)
        self.path=self.base+'/companies/'+self.company['id'];self.shared=self.company['token']
        roles=server.role_list(6)
        self.phones={role:server.dispatch('POST',self.path+'/claim',{'role':role,'name':'Fictional '+role},self.join)['token'] for role in roles}
        self.action('start')

    def tearDown(self):
        server.DB,self.old_db=self.old_db,server.DB;server.TEACHER_KEY=self.old_key
        self.directory.cleanup()

    def state(self,token=None):return server.dispatch('GET',self.path,{},token or self.shared)

    def action(self,action,token=None,**extra):
        c=self.state()['company']
        return server.dispatch('POST',self.path+'/actions',{'action':action,'year':c['year'],'version':c['version'],**extra},token or self.shared)

    def preferences(self,option):
        for token in self.phones.values():self.action('preference',token,option=option)

    def test_three_session_pacing_values_are_saved(self):
        created=server.dispatch('POST','/api/sessions',{'rules_version':engine.VERSION,'label':'Fictional pacing check','minutes':4,'checkpoint_minute':40,'end_minute':85},server.TEACHER_KEY)
        saved=server.dispatch('GET','/api/sessions/'+created['id'],{},created['token'])
        self.assertEqual((saved['minutes'],saved['checkpoint_minute'],saved['end_minute']),(4,40,85))
        with self.assertRaises(server.Problem):server.dispatch('POST','/api/sessions',{'rules_version':engine.VERSION,'label':'Invalid targets','checkpoint_minute':90,'end_minute':45},server.TEACHER_KEY)

    def test_discussion_estimates_and_targets_never_expire_a_decision(self):
        with server.transaction() as con:
            row,session=server.load(con,self.session['id'])
            session['minutes']=1
            session['checkpoint_minute']=2;session['end_minute']=3
            session['workshop_started']=1
            session['companies'][self.company['id']]['deadline']=1
            server.save(con,row['id'],session)
        state=self.state()['company']
        self.assertEqual(state['phase'],'decision')
        self.assertIsNone(state['deadline']);self.assertEqual(state['decisions'],{})

    def test_full_normal_flow_and_private_reports(self):
        for year,option in [(1,'hybrid'),(2,'stress'),(3,'full')]:
            with self.assertRaises(server.Problem):self.action('decide',option=option)
            self.preferences(option)
            self.action('decide',option=option)
            with self.assertRaises(server.Problem):self.action('decide',option=option)
            public=self.state()
            self.assertNotIn('private',json.dumps(public['company']['history']))
            if year==1:
                with self.assertRaises(server.Problem):self.action('advance')
                for token in self.phones.values():self.action('reflection',token,text='Fictional one-sentence reflection.')
            else:
                with self.assertRaises(server.Problem):self.action('reflection',self.phones['cfo'],text='Not a reflection year')
            self.action('advance')
        end=self.state()['company']
        self.assertEqual(end['year'],4);self.assertEqual(end['phase'],'decision')
        self.assertEqual(end['state']['northstar_contract'],'full_awarded')
        for token in self.phones.values():
            pdf=server.dispatch('GET',self.path+'/personal.pdf',{},token)
            self.assertTrue(pdf.startswith(b'%PDF'))
        exported=server.dispatch('GET',self.base+'/export',{},self.teacher)
        c=exported['companies'][self.company['id']]
        self.assertNotIn('secret',c)
        self.assertTrue(all('secret' not in member for member in c['members'].values()))
        self.assertTrue(server.dispatch('GET',self.base+'/logs.pdf',{},self.teacher).startswith(b'%PDF'))

    def test_deadline_locks_missing_recommendations_without_blocking_reflections(self):
        with server.transaction() as con:
            row,session=server.load(con,self.session['id'])
            session['companies'][self.company['id']]['deadline']=1
            session['companies'][self.company['id']]['deadline_kind']='checkpoint_window'
            server.save(con,row['id'],session)
        state=self.state()['company']
        self.assertEqual(state['decisions']['1']['resolution_mode'],'deadline_expired')
        with self.assertRaises(server.Problem):self.action('preference',self.phones['cfo'],option='wait')
        self.assertEqual(self.state(self.phones['cfo'])['preferences'],{})
        for token in self.phones.values():self.action('reflection',token,text='Fictional reflection after the default.')
        self.action('advance')
        self.assertEqual(self.state()['company']['year'],2)

    def test_skipped_optional_year_resolves_without_submissions(self):
        with server.transaction() as con:
            row,session=server.load(con,self.session['id'])
            session['active_years']=[1,3]
            server.save(con,row['id'],session)
        self.preferences('hybrid');self.action('decide',option='hybrid')
        for token in self.phones.values():self.action('reflection',token,text='Fictional reflection.')
        self.action('advance')
        c=self.state()['company']
        self.assertEqual(c['year'],3)
        self.assertEqual(c['decisions']['2']['resolution_mode'],'facilitator_skipped')
        self.assertEqual(c['decisions']['2']['option'],'stress')
        self.assertEqual(len(c['history']),2)
        self.assertAlmostEqual(c['state']['cash'],3.86)

    def test_override_once_and_disconnected_member(self):
        self.preferences('wait')
        self.action('power',self.phones['ceo'],option='license',reason='Fictional executive decision')
        self.assertEqual(self.state()['company']['decisions']['1']['actor'],'ceo')
        for role,token in self.phones.items():
            if role!='cfo':self.action('reflection',token,text='Fictional reflection.')
        server.dispatch('POST',self.base+'/control',{'action':'participant','company':self.company['id'],'role':'cfo','active':False},self.teacher)
        self.action('advance')
        with self.assertRaises(server.Problem):self.action('power',self.phones['ceo'],option='stress',reason='Second attempt')

    def test_power_requires_recommendation_and_respects_pause(self):
        with self.assertRaises(server.Problem):self.action('power',self.phones['employee'],reason='Fictional strike')
        self.assertFalse(self.state(self.phones['employee'])['power_used'])
        server.dispatch('POST',self.base+'/control',{'action':'pause'},self.teacher)
        self.preferences('hybrid')
        with self.assertRaises(server.Problem):self.action('decide',option='hybrid')
        server.dispatch('POST',self.base+'/control',{'action':'resume'},self.teacher)
        self.action('decide',option='hybrid')


if __name__=='__main__':unittest.main()
