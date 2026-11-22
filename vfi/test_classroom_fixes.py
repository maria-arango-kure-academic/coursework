import unittest,json
from copy import deepcopy
from unittest.mock import patch
import server,engine_v4 as engine
from test_v4 import HttpAcceptance

class ClassroomFixes(unittest.TestCase):
 setUp=HttpAcceptance.setUp
 tearDown=HttpAcceptance.tearDown
 state=HttpAcceptance.state
 action=HttpAcceptance.action
 preferences=HttpAcceptance.preferences
 def control(self,action,**kw):return server.dispatch('POST',self.base+'/control',dict(action=action,**kw),self.teacher)
 def raw(self):
  with server.transaction() as con:return server.load(con,self.session['id'])[1]
 def test_cross_device_company_and_role_rejoin_preserves_every_record(self):
  self.preferences('hybrid')
  before=deepcopy(self.raw()['companies'][self.company['id']])
  joined=server.dispatch('POST',self.base+'/join',{'password':self.raw()['password']},'')
  resumed=server.dispatch('POST',self.base+'/companies',{'name':'fictional company','resume_only':True},joined['token'])
  self.assertEqual(resumed['id'],self.company['id'])
  self.assertEqual(server.dispatch('GET',self.path,{},resumed['token'])['company']['id'],self.company['id'])
  for role in self.phones:
   r=server.dispatch('POST',self.path+'/claim',{'role':role,'name':'Fictional '+role,'resume':True},self.state()['join_token'])
   own=server.dispatch('GET',self.path,{},r['token'])
   self.assertEqual(own['preferences']['1'],'hybrid');self.assertEqual(own['role']['id'],role)
   self.assertEqual(self.raw()['companies'][self.company['id']]['members'][role]['participant_id'],before['members'][role]['participant_id'])
   self.assertEqual(self.state(self.phones[role])['preferences']['1'],'hybrid')
  self.assertEqual(len(self.raw()['companies']),1)
  exported=server.dispatch('GET',self.base+'/export',{},self.teacher)
  self.assertNotIn('resume_secrets',json.dumps(exported))
 def midpoint(self):
  self.control('move',year=5)
  self.control('expire5',company=self.company['id'])
  for token in self.phones.values():self.action('reflection',token,text='Fictional midpoint reflection')
 def test_release_six_needs_no_hidden_video_flags(self):
  self.midpoint();self.control('release5')
  self.assertEqual(self.state()['company']['year'],6)
  self.assertFalse(self.raw().get('commercial_shown',False))
 def test_jump_ten_keeps_target_open_and_preserves_midpoint(self):
  self.midpoint();self.control('release5');before=deepcopy(self.raw()['companies'][self.company['id']])
  self.control('move',year=10)
  c=self.state()['company'];self.assertEqual(c['year'],10);self.assertEqual(c['phase'],'decision');self.assertNotIn('10',c['decisions'])
  for y in range(1,6):self.assertEqual(c['decisions'][str(y)],before['decisions'][str(y)])
  for token in self.phones.values():
   state=self.state(token);self.assertNotIn('10',state['preferences']);self.assertTrue(state['reflections']['5'])
  choice=next(o['id'] for o in c['scenario']['options'] if not o['unavailable'])
  self.preferences(choice);self.action('decide',option=choice)
  for token in self.phones.values():self.action('reflection',token,reconsider='Fictional reconsideration',responsibility='Fictional responsibility')
  self.assertTrue(self.state()['company']['final_ready'])
  self.control('reveal10')
  self.assertTrue(server.dispatch('GET',self.path+'/personal.pdf',{},self.phones['cfo']).startswith(b'%PDF'))
  resumed=server.dispatch('POST',self.path+'/claim',{'role':'cfo','name':'Fictional cfo','resume':True},self.state()['join_token'])
  self.assertTrue(server.dispatch('GET',self.path+'/personal.pdf',{},resumed['token']).startswith(b'%PDF'))
 def test_single_company_jump_does_not_move_other_team(self):
  other=server.dispatch('POST',self.base+'/companies',{'name':'Other team','country':'France'},self.join)
  self.control('move',company=self.company['id'],year=5)
  s=self.raw();self.assertEqual(s['companies'][other['id']]['year'],1);self.assertEqual(s['companies'][self.company['id']]['year'],5)
 def test_power_undo_refunds_and_keeps_recommendations(self):
  self.preferences('hybrid');before=self.state()['company']['state']
  self.action('power',self.phones['cfo'],option='build')
  self.assertTrue(next(o for o in self.state()['company']['scenario']['options'] if o['id']=='build')['unavailable'])
  self.action('undo_power',self.phones['cfo'])
  self.assertFalse(self.state(self.phones['cfo'])['power_used']);self.assertEqual(self.state()['company']['state'],before)
  self.assertEqual(self.state(self.phones['cfo'])['preferences']['1'],'hybrid')
 def test_ceo_accidental_override_can_be_reopened_before_reflections(self):
  self.preferences('hybrid');self.action('power',self.phones['ceo'],option='license')
  self.action('undo_power',self.phones['ceo'])
  self.assertNotIn('1',self.state()['company']['decisions']);self.assertEqual(self.state()['company']['phase'],'decision')
  self.action('decide',option='hybrid');self.action('reflection',self.phones['cfo'],text='Fictional reflection')
  self.assertEqual(len(self.raw()['companies'][self.company['id']]['correction_history']),1)
 def test_inspection_is_private_and_readonly(self):
  before=deepcopy(self.raw())
  for year in range(1,11):
   result=server.dispatch('GET',self.base+f'/inspect/{self.company["id"]}/{year}',{},self.teacher)
   self.assertTrue(result['scenario']['options']);self.assertIn('cfo',result['roles'])
  self.assertEqual(before,self.raw())
  with self.assertRaises(server.Problem):server.dispatch('GET',self.base+f'/inspect/{self.company["id"]}/1',{},self.shared)
 def test_settings_and_withdrawal_preserve_export(self):
  self.control('settings',active_years=[1,5,10],minutes=4,checkpoint_minute=30,end_minute=60,registration_open=False)
  with self.assertRaises(server.Problem):server.dispatch('POST',self.base+'/companies',{'name':'Closed','country':'Sweden'},self.join)
  self.control('company_participation',company=self.company['id'],active=False)
  self.assertFalse(self.state()['company']['active'])
  exported=server.dispatch('GET',self.base+'/export',{},self.teacher)
  self.assertIn(self.company['id'],exported['companies'])

if __name__=='__main__':unittest.main()
