import itertools,unittest
from copy import deepcopy
import engine_v4 as e
from test_v4 import company,HttpAcceptance
import server

class Year45Acceptance(unittest.TestCase):
 def test_all_1024_five_year_paths(self):
  positive=negative=0
  for path in itertools.product(e.PROCUREMENT,e.TESTING,['full','pilot','conventional','decline'],e.FEATURES,e.RESPONSES):
   c=company(path,5);before=deepcopy(c);r=e.replay(c);s=r['state']
   self.assertEqual(c,before);self.assertEqual(r,e.replay(c))
   self.assertGreaterEqual(s['cash'],0)
   self.assertEqual(s['employees'],120)
   self.assertEqual(s['annual_baseline_revenue'],24)
   self.assertAlmostEqual(s['reported_annual_revenue'],24+s['contract_revenue'])
   self.assertAlmostEqual(s['cash'],6+sum(item['amount'] for item in r['ledger']))
   self.assertEqual(len({item['id'] for item in r['ledger']}),len(r['ledger']))
   self.assertEqual([step['external']['id'] for step in r['timeline']],['E1','E2','E3','E4','E5'])
   self.assertEqual(r['timeline'][4]['external'],e.CONTENT['external']['5']|{'id':'E5'})
   if not s['vfi_operational']:self.assertEqual(s['data_linkage_capability'],0)
   if s.get('boycott_customer_complaints'):negative+=1
   if s['customer_trust']>70:positive+=1
   if path[3]=='service_improvements':
    self.assertFalse(s.get('support_training_outstanding',False))
    self.assertFalse(s.get('verification_remediation_required',False))
  self.assertGreater(positive,0);self.assertGreater(negative,0)

 def test_year5_expired_review_and_financial_fallback(self):
  c=company(['hybrid','stress','conventional','service_improvements','independent_review'],5)
  c['decisions']['5'].update(resolution_mode='deadline_expired',decision_source='expired_default',actor='system')
  r=e.replay(c);last=r['timeline'][-1]
  self.assertEqual(last['decision_source'],'expired_default')
  self.assertIn(e.CONTENT['years']['5']['expiry_announcement'],last['outcome'])
  self.assertTrue(r['state']['review_remediation_required'])
  current=company(['hybrid','stress','conventional','service_improvements'],5)
  available=e.replay(current)['state']['cash']
  c['interventions']=[dict(role='marketing',year=5,cost=available-.2)]
  r=e.replay(c)
  self.assertEqual(r['timeline'][-1]['option'],'operations_defended')
  self.assertEqual(r['timeline'][-1]['resolution_mode'],'financial_fallback')
  self.assertEqual(r['timeline'][-1]['decision_source'],'expired_default')
  self.assertNotIn('commissions an independent review',r['timeline'][-1]['outcome'])

class MidpointAcceptance(HttpAcceptance):
 def test_reveal_waits_for_every_company_and_reset_retains_history(self):
  other=server.dispatch('POST',self.base+'/companies',{'name':'Fictional second company','country':'Finland'},self.join)
  server.dispatch('POST',self.base+'/control',{'action':'midpoint','warning_seconds':0},self.teacher)
  self.preferences('independent_review')
  self.action('decide',option='independent_review')
  for token in self.phones.values():self.action('reflection',token,text='Fictional reassessment.')
  with self.assertRaises(server.Problem):server.dispatch('POST',self.base+'/control',{'action':'reveal5'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'expire5','company':other['id']},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'reveal5'},self.teacher)
  state=server.dispatch('GET',self.base,{},self.teacher)
  self.assertEqual(len(state['comparison']),2)
  self.assertTrue(all(row['state']['employees']==120 for row in state['comparison']))
  server.dispatch('POST',self.base+'/control',{'action':'reset'},self.teacher)
  data=server.dispatch('GET',self.base+'/export',{},self.teacher)
  self.assertEqual(data['companies'],{})
  self.assertEqual(len(data['reset_history'][0]['companies']),2)
  for company in data['reset_history'][0]['companies'].values():
   self.assertNotIn('secret',company)
   self.assertNotIn('phone_key',company)

 def test_midpoint_defaults_reflection_gate_and_release(self):
  with self.assertRaises(server.Problem):server.dispatch('POST',self.base+'/control',{'action':'reveal5'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'midpoint','warning_seconds':0},self.teacher)
  c=self.state()['company']
  self.assertEqual(c['year'],5);self.assertEqual(c['phase'],'decision')
  self.assertEqual(len(c['history']),4)
  self.assertIn('external_announcement',c)
  self.assertNotIn('5',c['decisions'])
  self.preferences('human_assistance_expanded')
  server.dispatch('POST',self.base+'/control',{'action':'expire5','company':self.company['id']},self.teacher)
  c=self.state()['company']
  self.assertEqual(c['decisions']['5']['decision_source'],'expired_default')
  self.assertEqual(c['decisions']['5']['actor'],'system')
  self.assertEqual(c['decisions']['5']['option'],'independent_review')
  with self.assertRaises(server.Problem):self.action('advance')
  for token in self.phones.values():self.action('reflection',token,text='Fictional Year 5 reassessment.')
  c=self.state()['company']
  self.assertEqual(c['phase'],'checkpoint');self.assertTrue(c['checkpoint_saved'])
  server.dispatch('POST',self.base+'/control',{'action':'reveal5'},self.teacher)
  teacher=server.dispatch('GET',self.base,{},self.teacher)
  self.assertEqual(len(teacher['comparison']),1)
  self.assertEqual(teacher['comparison'][0]['state'],c['state'])
  before=c['state']
  server.dispatch('POST',self.base+'/control',{'action':'commercial'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'platform_announcement'},self.teacher)
  server.dispatch('POST',self.base+'/control',{'action':'release5'},self.teacher)
  after=self.state()['company']
  self.assertEqual(after['year'],6)
  self.assertAlmostEqual(after['state']['cash'],max(0,before['cash']-before['annual_vfi_cost']) if before['vfi_operational'] else before['cash'])
  data=server.dispatch('GET',self.base+'/export',{},self.teacher)
  self.assertIn('checkpoint5',data['companies'][self.company['id']])
  self.assertIn('industry_ranks',data['companies'][self.company['id']]['checkpoint5'])

if __name__=='__main__':unittest.main()
