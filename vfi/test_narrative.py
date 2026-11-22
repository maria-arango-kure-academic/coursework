import copy
import json
from pathlib import Path
import random
import unittest
import narrative as n
import outcomes as o
from test_outcomes import company

GOOD=['hybrid','broad','limited','support','analytics','alternative','narrow','revise','specialise','full']
RISK=['buy','existing','broad','loyalty','sponsors','full','expanded','maintain','merge','summary']

class NarrativeTests(unittest.TestCase):
    def test_testing_changes_customer_incident_and_later_request(self):
        good=company(GOOD);risk=company(RISK)
        self.assertEqual(n.aftermath(good,3)['id'],'a3-limited')
        self.assertEqual(n.aftermath(risk,3)['id'],'a3-broad-failed')
        self.assertEqual(n.brief(risk,8)['id'],'b8-screening')
        self.assertEqual(n.brief(good,8)['id'],'b8-lowdata')
        self.assertEqual(n.aftermath(risk,10)['id'],'a10-summary-concealed')
        self.assertNotIn('failed',n.aftermath(good,6)['id'])

    def test_late_acquisition_never_claims_a_live_service(self):
        c=company(['wait','late_buy','limited'],False)
        self.assertEqual(n.brief(c,2)['id'],'b2-none')
        self.assertEqual(n.aftermath(c,2)['id'],'a2-late_buy')
        self.assertIn('still buy tickets through the existing service',n.aftermath(c,2)['body'][0])

    def test_review_score_does_not_invent_a_broader_customer_pilot(self):
        c=company(['hybrid','focused'],False)
        c.update(year=3,phase='decision')
        c['interventions']=[{'year':3,'role':'legal'}]
        self.assertEqual(n.at(c,3)['state']['evidence'],3)
        self.assertEqual(n.brief(c)['id'],'b3-focused')

    def test_hidden_events_are_not_in_current_year_record(self):
        c=company(GOOD[:5],False);c.update(year=5,phase='checkpoint')
        original=copy.deepcopy(c)
        story=n.company_story(c)
        self.assertNotIn('5',story['records'])
        self.assertIsNone(story['update'])
        self.assertEqual(c,original)
        c['phase']='event'
        self.assertEqual(n.company_story(c)['update']['id'],'a5-analytics')

    def test_checkpoint_private_position_includes_its_completed_decision(self):
        c=company(GOOD[:5],False);c.update(year=5,phase='checkpoint')
        content=json.loads((Path(__file__).parent/'content.json').read_text(encoding='utf-8'))
        doc=n.private_message(c,'cfo',content)
        self.assertIn(f"€{o.replay(c)['state']['cash']:,.0f}k",' '.join(doc['body']))

    def test_role_information_remains_private_and_final_record_is_personal(self):
        c=company(RISK)
        content=json.loads((Path(__file__).parent/'content.json').read_text(encoding='utf-8'))
        public=json.dumps(n.company_story(c),ensure_ascii=False)
        for role in content['roleKeys']:
            private=n.private_message(c,role,content)
            self.assertTrue(private['id'].endswith(role))
            self.assertNotIn(content['years'][10]['info'][role][0],public)

    def test_revision_only_ends_practices_the_company_adopted(self):
        for revenue,sharing,expected in [('analytics','narrow','existing-limits'),('sponsors','narrow','sponsorship'),('analytics','expanded','screening'),('sponsors','expanded',None)]:
            route=GOOD[:];route[4]=revenue;route[6]=sharing
            doc=n.aftermath(company(route),8)
            self.assertEqual(doc['id'],'a8-revise'+('-'+expected if expected else ''))
        route=GOOD[:];route[7]='negotiate'
        self.assertEqual(n.aftermath(company(route),8)['id'],'a8-negotiate-limits')

    def test_final_brief_remembers_each_previous_strategy(self):
        for strategy in ['expand','restructure','specialise','merge','continue']:
            route=GOOD[:];route[8]=strategy
            doc=n.brief(company(route),10)
            self.assertEqual(doc['id'],'b10-'+strategy)
            self.assertIn({'expand':'hired six','restructure':'cut six','specialise':'smaller accessible','merge':'cut eight','continue':'continued its existing'}[strategy],doc['callback'])

    def test_all_choices_and_generated_routes_have_valid_media_without_mutation(self):
        rng=random.Random(49);seen=set();media=set()
        for run in range(300):
            c=company([],False)
            for year in range(1,11):
                state=o.replay(c)['state']
                choices=[key for key in o.MODEL['rules'][str(year)] if not o.gate(year,key,state)]
                key=rng.choice(choices);seen.add((year,key))
                c['decisions'][str(year)]={'option':key,'reason':'deadline' if run%9==0 and key==o.DEFAULTS[year] else 'decision'}
                c.update(year=year,phase='event' if year<10 else 'report',complete=year==10)
                original=copy.deepcopy(c);baseline=o.replay(c)
                for doc in [n.brief(c),n.aftermath(c,year)]:
                    self.assertIn(doc['id'],n.CATALOGUE['assets']);media.add(doc['id'])
                    self.assertTrue(all(doc['body']))
                    self.assertNotIn('{company}',' '.join(doc['body']))
                self.assertEqual(c,original)
                self.assertEqual(o.replay(c),baseline)
                c.update(year=min(year+1,10),phase='decision',complete=False)
        self.assertEqual(len(seen),sum(len(v) for v in o.MODEL['rules'].values()))
        print(f'300 story routes: all {len(seen)} choices reached; {len(media)} distinct documents selected; no state mutations.')

if __name__=='__main__':unittest.main()
