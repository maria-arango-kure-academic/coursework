"""Acceptance checks for recommendations, final years, executive powers and closure."""
import itertools,json,unittest
from copy import deepcopy
import engine_v4 as e
import rules_9_10 as rules
import powers_v4 as powers
import server,service_v4 as service
import test_v4

class ClosingRules(unittest.TestCase):
 def test_all_final_choices_against_representative_reachable_histories(self):
  starts=list(itertools.product(e.PROCUREMENT,e.TESTING,['full','pilot','conventional','decline'],e.FEATURES,e.RESPONSES))[::73]
  count=0
  for stem in starts:
   c=test_v4.company(stem,6)
   for y,o in [(6,'smart'),(7,'require_order'),(8,'services')]:
    c['year']=y;c['decisions'][str(y)]=dict(option=o,resolution_mode='deadline_expired',decision_source='expired_default')
   for a,b in itertools.product(rules.STRATEGY.keys()-{'continuity_fallback'},rules.REPORTS):
    trial=deepcopy(c)
    for y,o in [(9,a),(10,b)]:
     trial['year']=y;trial['decisions'][str(y)]=dict(option=o,resolution_mode='deadline_expired',decision_source='expired_default')
    result=e.replay(trial);s=result['state'];ledger=result['ledger']
    self.assertGreaterEqual(s['cash'],0);self.assertEqual(result,e.replay(trial))
    self.assertEqual(len(ledger),len({x['id'] for x in ledger}))
    self.assertAlmostEqual(s['cash'],6+sum(x['amount'] for x in ledger))
    self.assertIn(s['employees'],(108,120));self.assertNotIn('ethics_score',s)
    self.assertEqual(s['reported_annual_revenue'],24+s['contract_revenue']+(s['entry_contract_value_m'] if s['entry_contract_active'] else 0)+(s['meridian_revenue_m'] if s['commercial_partnership_active'] else 0)+(s['independent_revenue_m'] if s['independent_programme_active'] else 0))
    count+=1
  self.assertGreater(count,200)
  print(f'{count} complete final-year combinations verified.')

 def test_missions_require_defined_conditions(self):
  import closure_v4
  s=deepcopy(e.INITIAL)
  result=closure_v4.mission('ceo',s,[],service.MISSIONS,{})
  self.assertIsNone(result['met'])
  config={'ceo':{'conditions':[{'field':k,'op':'gte','value':value} for k,value in [('cash',1),('employees',100),('customer_trust',70),('partnership_standing',72)]]}}
  self.assertTrue(closure_v4.mission('ceo',s,[],service.MISSIONS,config)['met'])

 def test_reinvestment_resolves_two_and_restructure_requires_proposal(self):
  s=deepcopy(e.INITIAL);s.update(staff_escalation_review=True,support_training_outstanding=True,verification_remediation_required=True,legal_exposure=3)
  rules.apply(s,9,'reinvest');self.assertFalse(s['staff_escalation_review']);self.assertFalse(s['support_training_outstanding']);self.assertTrue(s['verification_remediation_required']);self.assertEqual(s['legal_exposure'],3)
  s=deepcopy(e.INITIAL);rules.apply(s,9,'restructure');self.assertEqual(s['employees'],120)
  s['restructuring_proposed_12']=True;rules.apply(s,9,'restructure');self.assertEqual(s['employees'],108);self.assertEqual(s['involuntary_layoffs'],12)
  for o in rules.REPORTS:
   t=deepcopy(s);t['data_handling_review_required']=True;rules.apply(t,10,o);self.assertTrue(t['data_handling_review_required']);self.assertEqual(t['legal_exposure'],s['legal_exposure'])

 def test_power_order_and_partial_work_stoppage(self):
  c=test_v4.company(['wait'],2)
  c['interventions']=[dict(role=role,year=2,option='accelerate',power_spec_version=1) for role in ('marketing','employee','sustainability','legal','cto','cfo')]
  r=e.replay(c);self.assertEqual([p['role'] for p in r['pending_power_effects']],['cfo','cto','legal','sustainability','employee','marketing'])
  self.assertAlmostEqual(r['state']['cash'],5.3)
  r=dict(state=deepcopy(e.INITIAL),session_id='test',company_id='low',ledger=[]);r['state']['cash']=.05
  result=powers.apply(r,9,[dict(role='employee',year=9)],e.charge,e.CONTENT)
  self.assertEqual(r['state']['cash'],0);self.assertAlmostEqual(r['state']['operating_payable_m'],.15);self.assertTrue(r['state']['financial_distress']);self.assertEqual(result[0]['unpaid'],.15)
  self.assertIsNotNone(powers.validate(r['state'],10,'cto','board_statement',0))
  self.assertIsNotNone(powers.validate(e.INITIAL,3,'relations','full',.6))

class PowersAcceptance(unittest.TestCase):
 def result(self,role,year=9,option='reinvest'):
  state=deepcopy(e.INITIAL);state.update(cash=3,procurement='hybrid',development_progress=2,northstar_contract='full_awarded',contract_revenue=2.4,workforce_conditions=67,customer_trust=68,verification_remediation_required=True)
  result=dict(state=state,ledger=[],session_id='power-test',company_id='fictional')
  effects=powers.apply(result,year,[dict(role=role,year=year,option=option,power_spec_version=1,governance_conflict=role=='ceo')],e.charge,e.CONTENT)
  return result,effects
 def test_all_eight_powers_have_specified_real_effects(self):
  for role in powers.ORDER:
   r,effects=self.result(role,6,'facial')
   self.assertEqual(len(effects),1);self.assertTrue(r['state'][powers.FLAGS[role]])
   self.assertAlmostEqual(r['state']['cash'],3-powers.COSTS[role]);self.assertTrue(effects[0]['changes'])
   self.assertFalse(r['state']['facial_entry_operational'])
  r,_=self.result('employee');self.assertTrue(r['state']['workforce_negotiation_required'])
  r,_=self.result('sustainability',6,'facial');self.assertTrue(r['state']['sustainability_followup_required'])
  r,_=self.result('legal');self.assertTrue(r['state']['verification_remediation_required']);self.assertTrue(r['state']['formally_reviewed_obligations'])
  r,_=self.result('ceo');self.assertEqual(r['state']['workforce_conditions'],66)
 def test_sorted_powers_preserve_committed_spending_and_record_disruption_arrears(self):
  r=dict(state=deepcopy(e.INITIAL),ledger=[],session_id='test',company_id='c');r['state']['cash']=.2
  effects=powers.apply(r,10,[dict(role='marketing',year=10),dict(role='employee',year=10)],e.charge,e.CONTENT)
  self.assertEqual([x['role'] for x in effects],['employee','marketing']);self.assertEqual(r['state']['cash'],0);self.assertAlmostEqual(r['state']['operating_payable_m'],.15)
 def test_facial_authorization_is_reachable_with_legal_review_and_assistance(self):
  c=test_v4.company(['hybrid','assessment','pilot','service_improvements','human_assistance_expanded'],6)
  c['interventions']=[dict(role='legal',year=6,option='facial',power_spec_version=1)]
  for y,o in [(6,'facial'),(7,'require_order')]:c['decisions'][str(y)]={'option':o,'resolution_mode':'deadline_expired','decision_source':'expired_default'}
  c['year']=7;s=e.replay(c)['state'];self.assertTrue(s['facial_entry_authorized']);self.assertTrue(s['facial_entry_operational']);self.assertEqual(s['entry_revenue_start_year'],8)

 def test_final_default_fallback_order(self):
  s=deepcopy(e.INITIAL)
  self.assertEqual(rules.cost(s,9,'specialize'),.3);self.assertEqual(rules.cost(s,10,'board_statement'),0)
  c=test_v4.company(['build','stress','full','ticket_transfers','human_assistance_expanded'],6)
  for y,o in [(6,'smart'),(7,'independent_legal'),(8,'services'),(9,'reinvest'),(10,'detailed_report')]:c['decisions'][str(y)]={'option':o,'resolution_mode':'deadline_expired','decision_source':'expired_default'}
  c['year']=10;r=e.replay(c)
  self.assertEqual(r['timeline'][-2]['option'],'continuity_fallback');self.assertEqual(r['timeline'][-1]['option'],'board_statement')
  self.assertEqual(r['state']['cash'],0);self.assertTrue(r['state']['vfi_operational'])

class ClosureHttp(test_v4.HttpAcceptance):
 def play(self,year,option):
  if year==6 and option=='smart':option='smart_entry'
  self.assertEqual(self.state()['company']['year'],year)
  self.preferences(option);self.action('decide',option=option)
  if year in (1,5):
   for token in self.phones.values():self.action('reflection',token,text=f'Original Year {year} reflection.')
  if year!=5:self.action('advance')

 def midpoint(self):
  for y,o in [(1,'wait'),(2,'assessment'),(3,'conventional'),(4,'service_improvements'),(5,'independent_review')]:self.play(y,o)
  server.dispatch('POST',self.base+'/control',{'action':'reveal5'},self.teacher)
  before=deepcopy(server.dispatch('GET',self.base+'/export',{},self.teacher)['companies'][self.company['id']]['checkpoint5'])
  server.dispatch('POST',self.base+'/control',{'action':'commercial'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'platform_announcement'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'release5'},self.teacher)
  return before

 def test_recommendations_are_private_immutable_and_required_before_power(self):
  with self.assertRaises(server.Problem):self.action('power',self.phones['cfo'],option='license')
  self.action('preference',self.phones['cfo'],option='hybrid')
  with self.assertRaises(server.Problem):self.action('preference',self.phones['cfo'],option='wait')
  self.assertEqual(self.state(self.phones['cfo'])['preferences']['1'],'hybrid')
  self.assertNotIn('preferences',self.state());self.assertNotIn('preferences',self.state(self.phones['legal'])['company'])
  self.action('power',self.phones['cfo'],option='license')
  option=next(o for o in self.state()['company']['scenario']['options'] if o['id']=='license')
  self.assertTrue(option['unavailable']);self.assertEqual(option['blocked_by'],'cfo')
  with self.assertRaises(server.Problem):self.action('power',self.phones['cfo'],option='build')

 def test_full_ten_year_closure_reports_feedback_and_locked_results(self):
  before=self.midpoint()
  for y,o in [(6,'smart'),(7,'independent_legal'),(8,'independent'),(9,'reinvest')]:self.play(y,o)
  self.preferences('independent_review');self.action('decide',option='independent_review')
  with self.assertRaises(server.Problem):server.dispatch('POST',self.base+'/control',{'action':'reveal10'},self.teacher)
  for i,token in enumerate(self.phones.values()):
   with self.assertRaises(server.Problem):self.action('reflection',token,reconsider='First answer only.')
   self.action('reflection',token,reconsider=f'Original reconsideration {i}.',responsibility=f'Original responsibility {i}.')
  teacher=server.dispatch('GET',self.base,{},self.teacher)
  self.assertTrue(teacher['companies'][0]['final_ready']);self.assertFalse(teacher['final_revealed'])
  server.dispatch('POST',self.base+'/control',{'action':'reveal10'},self.teacher)
  export=server.dispatch('GET',self.base+'/export',{},self.teacher);company=export['companies'][self.company['id']]
  self.assertEqual(before,company['checkpoint5']);self.assertTrue(export['complete']);self.assertEqual(company['phase'],'complete')
  snap=deepcopy(company['checkpoint10']);self.state()
  self.assertEqual(snap,server.dispatch('GET',self.base+'/export',{},self.teacher)['companies'][self.company['id']]['checkpoint10'])
  report=server.dispatch('GET',self.path+'/personal-report',{},self.phones['cfo'])
  self.assertEqual(len(report['years']),10);self.assertIn('Original Year 1 reflection.',report['text']);self.assertIn('Original Year 5 reflection.',report['text']);self.assertIn('Original reconsideration 1.',report['text']);self.assertNotIn('Original responsibility 0.',report['text']);self.assertNotIn('history',report['checkpoint5']);self.assertNotIn(e.CONTENT['years']['10']['info']['ceo'],json.dumps(report));self.assertNotIn(e.CONTENT['years']['5']['info']['ceo'],json.dumps(report))
  self.assertTrue(server.dispatch('GET',self.path+'/personal.pdf',{},self.phones['cfo']).startswith(b'%PDF'))
  with self.assertRaises(server.Problem):self.action('preference',self.phones['cfo'],option='board_statement')
  self.assertNotIn('feedback',report)
  server.dispatch('POST',self.base+'/feedback',{'ratings':{'1':5},'text':{'5':'Fictional anonymous response.'},'student_id':'SHOULD NOT BE STORED'},self.phones['cfo'])
  with server.transaction() as con:
   records=con.execute('SELECT * FROM anonymous_feedback').fetchall();raw=json.dumps([tuple(row) for row in records])
  self.assertNotIn('SHOULD NOT BE STORED',raw);self.assertNotIn('Fictional cfo',raw);self.assertNotIn(self.company['id'],raw)
  self.assertEqual(server.dispatch('GET',self.base,{},self.teacher)['feedback_summary']['count'],1)
  server.dispatch('POST',self.base+'/control',{'action':'debrief'},self.teacher)
  self.assertTrue(server.dispatch('GET',self.base+'/projection',{},self.teacher)['debrief_visible'])

 def test_final_reveal_waits_for_two_companies(self):
  other=server.dispatch('POST',self.base+'/companies',{'name':'Fictional Second Company','country':'Finland'},self.join)
  other_path=self.base+'/companies/'+other['id']
  other_phones={r:server.dispatch('POST',other_path+'/claim',{'role':r,'name':'Other fictional '+r},self.join)['token'] for r in server.role_list(6)}
  server.dispatch('POST',self.base+'/control',{'action':'midpoint','warning_seconds':0},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'expire5'},self.teacher)
  for token in self.phones.values():self.action('reflection',token,text='First company midpoint.')
  for token in other_phones.values():server.dispatch('POST',other_path+'/actions',{'action':'reflection','year':5,'text':'Second company midpoint.'},token)
  server.dispatch('POST',self.base+'/control',{'action':'reveal5'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'commercial'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'platform_announcement'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'release5'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'final','warning_seconds':0},self.teacher)
  for token in self.phones.values():self.action('reflection',token,reconsider='First company closing.',responsibility='First company responsibility.')
  with self.assertRaises(server.Problem):server.dispatch('POST',self.base+'/control',{'action':'reveal10'},self.teacher)
  for role,token in other_phones.items():
   if role=='legal':server.dispatch('POST',other_path+'/actions',{'action':'reflection','year':10,'reconsider':'Second closing.','responsibility':'Second responsibility.'},token)
   else:server.dispatch('POST',self.base+'/control',{'action':'participant','company':other['id'],'role':role,'active':False},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'reveal10'},self.teacher)
  projection=server.dispatch('GET',self.base+'/projection',{},self.teacher)
  self.assertEqual(len(projection['comparison']),2)
  self.assertTrue(all(row['ranks']['cash']==1 for row in projection['comparison']))

 def test_force_final_defaults_missing_recommendations_and_inactive_students(self):
  self.midpoint()
  server.dispatch('POST',self.base+'/control',{'action':'final','warning_seconds':0},self.teacher)
  c=self.state()['company'];self.assertEqual(c['year'],10);self.assertEqual(c['phase'],'event')
  self.assertEqual(c['decisions']['6']['resolution_mode'],'deadline_expired');self.assertEqual(c['decisions']['9']['actor'],'system')
  with self.assertRaises(server.Problem):self.action('preference',self.phones['cfo'],option='board_statement')
  server.dispatch('POST',self.base+'/control',{'action':'participant','company':c['id'],'role':'cfo','active':False},self.teacher)
  for role,token in self.phones.items():
   if role!='cfo':self.action('reflection',token,reconsider='Fictional closing reflection.',responsibility='Fictional responsibility response.')
  server.dispatch('POST',self.base+'/control',{'action':'reveal10'},self.teacher)
  report=server.dispatch('GET',self.path+'/personal-report',{},self.phones['cfo'])
  self.assertIsNone(report['years'][-1]['recommendation']);self.assertEqual(report['years'][-1]['recommendation_status'],'not_submitted')

if __name__=='__main__':unittest.main()
