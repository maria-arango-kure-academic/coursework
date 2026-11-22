import itertools,unittest
from copy import deepcopy
import engine_v4 as e
import rules_6_8 as rules
from test_v4 import company

class Years68Acceptance(unittest.TestCase):
 def test_64_combinations_against_representative_reachable_states(self):
  stems=list(itertools.product(e.PROCUREMENT,e.TESTING,['full','pilot','conventional','decline'],e.FEATURES,e.RESPONSES))[::32]
  tested=0;distress=0
  for stem in stems:
   for tail in itertools.product(rules.ENTRY, list(rules.POLICE)[:4],list(rules.PARTNERSHIPS)[:4]):
    c=company(stem,6)
    for year,option in zip((6,7,8),tail):
     c['year']=year
     before=e.replay(c)['state']
     if e.available(before,year,option):mode='student_decision'
     else:mode='deadline_expired';option=e.DEFAULTS[year]
     c['decisions'][str(year)]={'option':option,'resolution_mode':mode,'decision_source':'expired_default' if mode=='deadline_expired' else mode,'actor':'system' if mode=='deadline_expired' else 'company'}
     r=e.replay(c);s=r['state'];step=r['timeline'][-1]
     self.assertGreaterEqual(s['cash'],0)
     self.assertEqual(r,e.replay(c))
     self.assertEqual(len({x['id'] for x in r['ledger']}),len(r['ledger']))
     self.assertAlmostEqual(s['cash'],6+sum(x['amount'] for x in r['ledger']))
     self.assertTrue(all(0<=s[key]<=100 for key in rules.SCORES))
     if year==6:self.assertFalse(s['facial_entry_operational'])
     if year==7:
      self.assertTrue(s['law_enforcement_request_resolved'])
      self.assertTrue(s['law_enforcement_data_preserved'])
      self.assertFalse(s['law_enforcement_deadline_pending'])
      self.assertTrue(set(s['disclosed_data_categories']).issubset(s['available_data_categories']))
      self.assertNotIn('biometric_records',s['disclosed_data_categories'])
      self.assertEqual(step['external_resolution'],e.CONTENT['years']['7']['external_resolution'])
     if s['procurement']=='wait':self.assertNotIn('identity_linked_account_records',s.get('available_data_categories',[]))
     if s['mandatory_verification_suspended']:self.assertFalse(s['mandatory_vfi_active'])
     if s['facial_entry_selected'] and not s['facial_entry_authorized']:self.assertFalse(s['entry_contract_active'])
     if year==8:
      expected=24+s['contract_revenue']+(s['entry_contract_value_m'] if s['entry_contract_active'] else 0)
      self.assertAlmostEqual(s['reported_annual_revenue'],expected)
      c['year']=9;nine=e.replay(c)['state']
      expected+=nine['meridian_revenue_m'] if nine['commercial_partnership_active'] else 0
      expected+=nine['independent_revenue_m'] if nine['independent_programme_active'] else 0
      self.assertAlmostEqual(nine['reported_annual_revenue'],expected)
     distress+=int(s['financial_distress'])
    tested+=1
  self.assertEqual(tested,2048)
  self.assertGreater(distress,0)
  print('2,048 representative Year 6–8 combinations checked, including affordability fallbacks.')

 def test_facial_compliance_both_results_and_no_early_records(self):
  state=deepcopy(e.INITIAL)
  state.update(facial_entry_selected=True,entry_contract_pending=True,entry_compliance_review=True,assurance_evidence=3,human_assistance_capacity=2)
  rules.facial_compliance(state)
  self.assertTrue(state['facial_entry_authorized'])
  self.assertEqual(state['entry_revenue_start_year'],8)
  bad=deepcopy(e.INITIAL)
  bad.update(facial_entry_selected=True,entry_contract_pending=True,entry_compliance_review=True,assurance_evidence=3,human_assistance_capacity=2,integration_governance_outstanding=True)
  rules.facial_compliance(bad)
  self.assertFalse(bad['facial_entry_operational']);self.assertTrue(bad['facial_contract_not_activated'])
  pending=deepcopy(e.INITIAL);pending['facial_entry_selected']=True
  self.assertNotIn('biometric_records',rules.available_data(pending))

 def test_unpaid_operating_cost_and_repayment(self):
  r=dict(state=deepcopy(e.INITIAL),ledger=[],session_id='s',company_id='c')
  r['state'].update(cash=.2,vfi_operational=True,annual_vfi_cost=.9)
  e.annual_vfi(r,6)
  self.assertEqual(r['state']['cash'],0)
  self.assertAlmostEqual(r['state']['vfi_operating_payable_m'],.7)
  self.assertTrue(r['state']['financial_distress']);self.assertTrue(r['state']['vfi_operational'])
  first=deepcopy(r)
  e.annual_vfi(r,6)
  self.assertEqual(r,first)
  e.credit(r,7,'specified_future_receipt',1.0)
  self.assertAlmostEqual(r['state']['cash'],.3)
  self.assertEqual(r['state']['vfi_operating_payable_m'],0)
  self.assertFalse(r['state']['supplier_payment_at_risk'])
  first=deepcopy(r)
  e.credit(r,7,'specified_future_receipt',1.0)
  self.assertEqual(r,first)

 def test_annual_arrears_accumulate_from_year_four_and_partial_receipts_repay_first(self):
  r=dict(state=deepcopy(e.INITIAL),ledger=[],session_id='arrears',company_id='c')
  r['state'].update(cash=.2,vfi_operational=True,annual_vfi_cost=.9)
  e.annual_vfi(r,4)
  self.assertAlmostEqual(r['state']['vfi_operating_payable_m'],.7)
  self.assertEqual(r['annual_notices']['4'],e.VFI_PAYMENT_WARNING)
  e.annual_vfi(r,5)
  self.assertAlmostEqual(r['state']['vfi_operating_payable_m'],1.6)
  before=deepcopy(r)
  e.annual_vfi(r,5)
  self.assertEqual(r,before)
  e.credit(r,5,'partial_receipt',.4)
  self.assertEqual(r['state']['cash'],0)
  self.assertAlmostEqual(r['state']['vfi_operating_payable_m'],1.2)
  self.assertTrue(r['state']['supplier_payment_at_risk'])
  self.assertTrue(r['state']['financial_distress'])
  self.assertTrue(r['state']['vfi_operational'])
  e.credit(r,6,'later_receipt',2)
  self.assertAlmostEqual(r['state']['cash'],.8)
  self.assertEqual(r['state']['vfi_operating_payable_m'],0)
  self.assertFalse(r['state']['supplier_payment_at_risk'])
  self.assertAlmostEqual(r['state']['cash'],.2+sum(x['amount'] for x in r['ledger']))

if __name__=='__main__':unittest.main()
