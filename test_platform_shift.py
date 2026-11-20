"""Behavioral coverage for supplier branches, processing permissions and revenue timing."""
import itertools,json,unittest
from copy import deepcopy
import engine_v4 as e
import platform_shift as p
import test_v4

class PlatformRules(unittest.TestCase):
 def company(self,path,year=6):
  c=test_v4.company(path,year,'deadline_expired');c['platform_shift_version']=1;return c

 def test_all_4096_year_six_choices_against_reachable_first_five_years(self):
  count=0
  for stem in itertools.product(e.PROCUREMENT,e.TESTING,['full','pilot','conventional','decline'],e.FEATURES,e.RESPONSES):
   baseline=e.replay(test_v4.company(stem,5));c=self.company(stem)
   options=e.scenario(c,6)['options'];self.assertEqual(len(options),4)
   for option in options:
    chosen=deepcopy(c);chosen['decisions']['6']={'option':option['id'],'resolution_mode':'deadline_expired','decision_source':'expired_default'}
    result=e.replay(chosen);s=result['state'];step=result['timeline'][-1]
    self.assertGreaterEqual(s['cash'],0);self.assertEqual(result,e.replay(chosen))
    self.assertEqual([x for x in result['ledger'] if x['year']<=5],baseline['ledger'])
    self.assertEqual([x['outcome'] for x in result['timeline'][:5]],[x['outcome'] for x in baseline['timeline']])
    self.assertEqual(len(result['ledger']),len({x['id'] for x in result['ledger']}))
    self.assertAlmostEqual(s['cash'],6+sum(x['amount'] for x in result['ledger']))
    self.assertFalse(s['facial_entry_operational']);self.assertFalse(s['ai_training_authorized']);self.assertFalse(s['biometric_secondary_use_authorized'])
    self.assertEqual(set(step['private_intelligence']),set(e.CONTENT['years']['1']['info']))
    self.assertEqual(step['external']['text'],e.CONTENT['platform_shift']['external']['text'])
    if stem[0] in ('build','wait'):self.assertFalse(s['vfi_supplier_contract'])
    if step['option']=='exit_supplier':self.assertFalse(s['vfi_supplier_contract']);self.assertTrue(s['migration_in_progress']);self.assertEqual(s['supplier_dependence'],0)
    if step['option']=='standard_facepass':self.assertEqual(s['supplier_data_rights'],'broad_proposed');self.assertEqual(s['facepass_contract'],'standard')
    if step['option']=='enterprise_facepass':self.assertEqual(s['supplier_data_rights'],'restricted');self.assertEqual(s['company_data_control'],3)
    count+=1
  self.assertEqual(count,4096);print('4,096 Year 6 branches verified against all reachable first-five-year histories.')

 def test_negotiation_expiry_stops_support_and_retains_historical_records(self):
  for procurement in ('license','hybrid'):
   c=self.company([procurement,'assessment','decline','service_improvements','independent_review','negotiate_terms'],7)
   r=e.replay(c);s=r['state'];self.assertTrue(s['vfi_exemption_granted']);self.assertTrue(s['identity_records_retained'])
   c['decisions']['7']={'option':'require_order','resolution_mode':'deadline_expired'};c['year']=8
   r=e.replay(c);s=r['state'];self.assertFalse(s['vfi_operational']);self.assertFalse(s['mandatory_vfi_active']);self.assertTrue(s['exemption_expiry_decision_required'])
   self.assertEqual(s['supplier_lock_in_crisis'],not s['migration_financially_feasible'])
   self.assertIn('identity_linked_account_records',s['available_data_categories']);self.assertNotIn('biometric_entry_records',s['available_data_categories'])
   self.assertEqual(s['facepass_contract'],'expired')

 def test_standard_and_enterprise_fees_are_charged_once_from_year_seven(self):
  for procurement,standard,enterprise in [('license',.9,1.5),('hybrid',.65,1.2)]:
   for response,fee in [('standard_facepass',standard),('enterprise_facepass',enterprise)]:
    c=self.company([procurement,'assessment','decline','service_improvements','independent_review',response],7)
    r=e.replay(c);paid=[x for x in r['ledger'] if x['year']==7 and x['effect']=='annual_vfi_cost'];unpaid=[x for x in r['ledger'] if x['year']==7 and x['effect']=='unpaid_vfi_operating_cost']
    self.assertEqual(len(paid),1);self.assertAlmostEqual(-paid[0]['amount']+sum(x['liability_change'] for x in unpaid),fee)
    self.assertEqual(r['state']['annual_vfi_cost'],fee);self.assertFalse(r['state']['facial_entry_operational']);self.assertFalse(r['state']['ai_training_performed'])

 def test_exit_prices_and_funded_migration(self):
  for procurement,amount in [('license',1.3),('hybrid',.75)]:
   c=self.company([procurement,'assessment','decline','service_improvements','operations_defended'],6)
   s=e.replay(c)['state'];self.assertAlmostEqual(p.cost(s,'exit_supplier'),amount)
   c['decisions']['6']={'option':'exit_supplier','resolution_mode':'deadline_expired'};c['year']=7
   r=e.replay(c);self.assertTrue(r['state']['independent_migration_completed']);self.assertFalse(r['state']['vfi_supplier_contract']);self.assertFalse(r['state']['facial_entry_operational']);self.assertEqual(r['state']['annual_vfi_cost'],0)
   self.assertEqual(sum(x['effect']=='annual_decision' and x['year']==6 for x in r['ledger']),1)

 def test_biometric_authorization_is_not_commercial_activation(self):
  c=self.company(['build','accelerate','decline','service_improvements','human_assistance_expanded','develop_proprietary','independent_legal'],7)
  c['interventions']=[dict(role='legal',year=6,option='develop_proprietary',power_spec_version=1)]
  r=e.replay(c);s=r['state'];self.assertTrue(s['facial_entry_operational']);self.assertEqual(s['potential_biometric_revenue_m'],1.6);self.assertFalse(s['biometric_venue_contract_active']);self.assertFalse(s['entry_contract_active'])
  self.assertFalse(s['ai_training_authorized']);self.assertFalse(s['biometric_secondary_use_authorized']);self.assertNotIn('biometric_entry_records',s['available_data_categories'])
  for option in ('preferred','nonexclusive','independent','services'):
   trial=deepcopy(c);trial['decisions']['8']={'option':option,'resolution_mode':'deadline_expired'};trial['year']=8
   eight=e.replay(trial);self.assertEqual(eight['state']['reported_annual_revenue'],24)
   trial['year']=9;nine=e.replay(trial);s=nine['state']
   value=1.6 if option in ('preferred','nonexclusive') else 0
   self.assertEqual(s['biometric_venue_contract_active'],bool(value))
   self.assertEqual(s['reported_annual_revenue'],24+s['meridian_revenue_m']+s['independent_revenue_m']*s['independent_programme_active']+value)
   self.assertEqual(nine,e.replay(trial))

 def test_three_biometric_contract_values_and_no_unauthorized_contracts(self):
  for provider,value in [('in_house',1.6),('independent_supplier',1.1),('independent_new',1.2)]:
   for operational,option in itertools.product((True,False),('preferred','nonexclusive','independent','services')):
    s=deepcopy(e.INITIAL);p.initialize_data(s);s.update(facial_entry_provider=provider,facial_entry_operational=operational)
    p.commercialize(s,option);self.assertEqual(s['biometric_venue_contract_active'],operational and option in ('preferred','nonexclusive'))
    if s['biometric_venue_contract_active']:self.assertEqual(s['biometric_venue_contract_value_m'],value);self.assertEqual(s['biometric_venue_revenue_start_year'],9)

if __name__=='__main__':unittest.main()
