import unittest,json
import server
from test_v4 import HttpAcceptance as Base
class SkipCatchUp(unittest.TestCase):
 setUp=Base.setUp
 tearDown=Base.tearDown
 state=Base.state
 action=Base.action
 preferences=Base.preferences
 def control(self,action,**kw):return server.dispatch('POST',self.base+'/control',dict(action=action,**kw),self.teacher)
 def test_teacher_jump_reports_actual_defaults_without_private_data(self):
  self.control('move',year=5)
  c=self.state()['company'];updates=c['catch_up']
  self.assertEqual([u['year'] for u in updates],[1,2,3,4])
  self.assertNotIn('5',c['decisions'])
  for update in updates:
   step=next(s for s in c['history'] if s['year']==update['year'])
   self.assertEqual(update['choice'],step['option_title'])
   self.assertEqual(update['outcome'],step['outcome'])
   self.assertEqual(update['cash'],step['state']['cash'])
   self.assertNotIn('private',update);self.assertNotIn('private_intelligence',update)
  for token in self.phones.values():self.assertEqual(self.state(token)['preferences'],{})
 def test_removed_years_show_after_manual_decision(self):
  self.control('settings',active_years=[1,5,6,7,8,9,10])
  self.preferences('hybrid');self.action('decide',option='hybrid')
  for token in self.phones.values():self.action('reflection',token,text='Fictional reflection')
  self.action('advance')
  c=self.state()['company'];self.assertEqual(c['year'],5)
  self.assertEqual([u['year'] for u in c['catch_up']],[2,3,4])
  self.assertEqual(c['decisions']['1']['actor'],'company')
 def test_midpoint_and_final_countdown_have_catch_up(self):
  self.control('midpoint',warning_seconds=0)
  self.assertEqual([u['year'] for u in self.state()['company']['catch_up']],[1,2,3,4])
  self.control('expire5',company=self.company['id'])
  for token in self.phones.values():self.action('reflection',token,text='Fictional midpoint response')
  self.control('release5');self.control('final',warning_seconds=0)
  c=self.state()['company']
  self.assertEqual(c['year'],10)
  self.assertEqual([u['year'] for u in c['catch_up']],[6,7,8,9,10])
 def test_normal_years_do_not_get_a_skip_notice(self):
  self.assertEqual(self.state()['company']['catch_up'],[])
  self.preferences('hybrid');self.action('decide',option='hybrid')
  self.assertEqual(self.state()['company']['catch_up'],[])
if __name__=='__main__':unittest.main()
