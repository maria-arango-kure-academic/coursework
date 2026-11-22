"""Shared company PDFs must never expose confidential individual records."""
import unittest
from unittest.mock import patch
import server
from test_v4 import HttpAcceptance

class ReportBoundaries(unittest.TestCase):
 setUp=HttpAcceptance.setUp
 tearDown=HttpAcceptance.tearDown
 state=HttpAcceptance.state
 action=HttpAcceptance.action
 preferences=HttpAcceptance.preferences

 def test_shared_private_and_teacher_pdf_boundaries(self):
  self.preferences('hybrid');self.action('decide',option='hybrid')
  for role,token in self.phones.items():self.action('reflection',token,text='CONFIDENTIAL-'+role)
  captured=[]
  def capture(story,title):
   captured.append('\n'.join(item.getPlainText() for item in story if hasattr(item,'getPlainText')))
   return b'%PDF-audit'
  with patch('reports.build',side_effect=capture):
   server.dispatch('GET',self.path+'/report.pdf',{},self.shared)
   shared=captured[-1]
   self.assertIn('Company decision:',shared);self.assertIn('Cash ledger',shared)
   self.assertNotIn('CONFIDENTIAL-',shared);self.assertNotIn('Your recommendation:',shared);self.assertNotIn('Private intelligence',shared)
   server.dispatch('GET',self.path+'/personal.pdf',{},self.phones['cfo'])
   own=captured[-1];self.assertIn('CONFIDENTIAL-cfo',own);self.assertNotIn('CONFIDENTIAL-ceo',own)
   server.dispatch('GET',self.path+'/report.pdf',{},self.teacher)
   teacher=captured[-1]
   for role in self.phones:self.assertIn('CONFIDENTIAL-'+role,teacher)
   server.dispatch('GET',self.base+'/logs.pdf',{},self.teacher)
   for role in self.phones:self.assertIn('CONFIDENTIAL-'+role,captured[-1])
  self.assertTrue(server.dispatch('GET',self.path+'/report.pdf',{},self.shared).startswith(b'%PDF'))

 def test_public_join_links_use_the_configured_https_origin(self):
  with patch.dict('os.environ',{'FAIRPASS_PUBLIC_ORIGIN':'https://vfi.coursework.live/'}):
   self.assertEqual(server.network_join_origin('0.0.0.0',8766,'172.18.0.2'),'https://vfi.coursework.live')
  with patch.dict('os.environ',{'FAIRPASS_PUBLIC_ORIGIN':'javascript:invalid'}):
   self.assertEqual(server.network_join_origin('127.0.0.1',8766,'127.0.0.1'),None)

 def test_lecturer_projection_video_slots_and_access(self):
  from pathlib import Path
  import tempfile
  with tempfile.TemporaryDirectory() as directory,patch.object(server,'ROOT',Path(directory)):
   before=server.dispatch('GET',self.base+'/projection',{},self.teacher)
   self.assertIsNone(before['intro_video_src']);self.assertIsNone(before['closing_video_src']);self.assertIsNone(before['platform_commercial']['video_src'])
   media=Path(directory)/'dist/media/vfi';media.mkdir(parents=True)
   for name in ('intro.mp4','smile-and-pass.mp4','year-10.mp4'):(media/name).write_bytes(b'fictional-media-path-test')
   after=server.dispatch('GET',self.base+'/projection',{},self.teacher)
   self.assertEqual(after['intro_video_src'],'/media/vfi/intro.mp4')
   self.assertEqual(after['closing_video_src'],'/media/vfi/year-10.mp4')
   self.assertEqual(after['platform_commercial']['video_src'],'/media/vfi/smile-and-pass.mp4')
   with self.assertRaises(server.Problem):server.dispatch('GET',self.base+'/projection',{},self.shared)

 def test_checkpoint_previews_are_teacher_only_and_do_not_tick_or_write(self):
  with server.transaction() as con:
   row,saved=server.load(con,self.session['id'])
   saved['companies'][self.company['id']].update(deadline=1,deadline_kind='checkpoint_window')
   server.save(con,row['id'],saved)
   before=con.execute('SELECT state FROM sessions WHERE id=?',(self.session['id'],)).fetchone()['state']
   projector=saved['projector']
  for year in (5,10):
   result=server.dispatch('GET',self.base+'/projection/preview'+str(year),{},self.teacher)
   self.assertEqual(result['preview_year'],year);self.assertEqual(result['comparison'],[])
   self.assertEqual(result['final_revealed'],year==10);self.assertIsNotNone(result['checkpoint_text'])
   for token in (self.shared,self.join,self.phones['cfo'],projector):
    with self.assertRaises(server.Problem) as error:server.dispatch('GET',self.base+'/projection/preview'+str(year),{},token)
    self.assertEqual(error.exception.status,403)
  with server.transaction() as con:
   after=con.execute('SELECT state FROM sessions WHERE id=?',(self.session['id'],)).fetchone()['state']
  self.assertEqual(before,after)

 def test_checkpoint_previews_use_only_saved_checkpoint_results(self):
  from copy import deepcopy
  import engine_v4 as engine
  import closure_v4 as closure
  from test_v4 import company
  path=['wait','assessment','conventional','service_improvements','independent_review','smart_entry','independent_legal','independent','reinvest','independent_review']
  final_company=company(path,10,'deadline_expired');final_company['platform_shift_version']=1
  midpoint_company=deepcopy(final_company);midpoint_company['decisions']={k:v for k,v in midpoint_company['decisions'].items() if int(k)<=5};midpoint_company['year']=5
  midpoint=engine.replay(midpoint_company);final=engine.replay(final_company)
  with server.transaction() as con:
   row,saved=server.load(con,self.session['id']);c=saved['companies'][self.company['id']]
   c['checkpoint5']={'state':midpoint['state']}
   c['checkpoint10']={'state':final['state'],'history':final['timeline'],'comparison':{k:{'year5':midpoint['state'][k],'year10':final['state'][k],'change':final['state'][k]-midpoint['state'][k]} for k in closure.METRICS}}
   server.save(con,row['id'],saved)
  five=server.dispatch('GET',self.base+'/projection/preview5',{},self.teacher)
  ten=server.dispatch('GET',self.base+'/projection/preview10',{},self.teacher)
  self.assertEqual(five['comparison'][0]['state'],midpoint['state'])
  self.assertEqual(ten['comparison'][0]['state'],final['state'])
  self.assertNotIn('private_intelligence',str(ten['comparison']))
  normal=server.dispatch('GET',self.base+'/projection',{},self.teacher)
  self.assertIsNone(normal['checkpoint_text']);self.assertFalse(normal['final_revealed'])

 def test_existing_company_can_reopen_at_capacity_without_losing_work(self):
  from copy import deepcopy
  self.preferences('hybrid');self.action('decide',option='hybrid')
  with server.transaction() as con:
   row,saved=server.load(con,self.session['id']);saved['company_count']=1
   original=deepcopy(saved['companies'][self.company['id']]);server.save(con,row['id'],saved)
  reopened=server.dispatch('POST',self.base+'/companies',{'name':'fictional company','country':'Finland'},self.join)
  self.assertEqual(reopened['id'],self.company['id']);self.assertTrue(reopened['resumed'])
  self.assertEqual(self.state(reopened['token'])['access'],'company')
  self.assertEqual(self.state()['access'],'company')
  with server.transaction() as con:
   row,saved=server.load(con,self.session['id']);current=saved['companies'][self.company['id']]
   self.assertEqual(len(saved['companies']),1)
   for key in ('name','country','decisions','history','members','phone_key','secret'):self.assertEqual(current[key],original[key])
  extra=server.dispatch('POST',self.base+'/companies',{'name':'Extra company','country':'Sweden'},self.join)
  self.assertNotEqual(extra['id'],self.company['id'])
  with self.assertRaises(server.Problem):server.dispatch('POST',self.base+'/companies',{'name':'Fictional Company','country':'Sweden'},'invalid')

 def test_no_company_cap_and_return_only_never_creates_a_company(self):
  with server.transaction() as con:
   row,saved=server.load(con,self.session['id']);saved['company_count']=8;password=saved['password'];server.save(con,row['id'],saved)
  for index in range(25):server.dispatch('POST',self.base+'/companies',{'name':f'Additional company {index}','country':'Sweden'},self.join)
  fresh_join=server.dispatch('POST',self.base+'/join',{'password':password},'')['token']
  recovered=server.dispatch('POST',self.base+'/companies',{'name':'Fictional Company','resume_only':True},fresh_join)
  self.assertEqual(recovered['id'],self.company['id'])
  self.assertEqual(self.state(recovered['token'])['company']['name'],'Fictional Company')
  with self.assertRaises(server.Problem) as error:server.dispatch('POST',self.base+'/companies',{'name':'Mistyped name','resume_only':True},fresh_join)
  self.assertEqual(error.exception.status,404)
  with server.transaction() as con:
   row,saved=server.load(con,self.session['id']);self.assertEqual(len(saved['companies']),26)
  self.assertEqual(saved['companies'][self.company['id']]['country'],'Sweden')

 def test_forced_year5_reflections_work_with_seven_and_eight_roles(self):
  for size in (7,8):
   with self.subTest(size=size):
    if size==8:self.tearDown();self.setUp()
    with server.transaction() as con:
     row,saved=server.load(con,self.session['id']);saved['role_count']=size;server.save(con,row['id'],saved)
    phones=dict(self.phones)
    for role in server.role_list(size)[6:]:phones[role]=server.dispatch('POST',self.path+'/claim',{'role':role,'name':'Fictional '+role},self.join)['token']
    server.dispatch('POST',self.base+'/control',{'action':'midpoint','warning_seconds':0},self.teacher)
    server.dispatch('POST',self.base+'/control',{'action':'expire5','company':self.company['id']},self.teacher)
    self.assertEqual(self.state()['company']['phase'],'event')
    for role,token in phones.items():self.action('reflection',token,text='Fictional Year 5 reflection '+role)
    result=self.state()['company']
    self.assertTrue(result['checkpoint_ready']);self.assertEqual(result['progress']['reflections'],size)

 def test_malformed_session_paths_return_404(self):
  for path in (self.base+'/report.pdf',self.base+'/unknown',self.path+'/actions/extra'):
   with self.assertRaises(server.Problem) as error:server.dispatch('GET',path,{},self.teacher)
   self.assertEqual(error.exception.status,404)

if __name__=='__main__':unittest.main()
