import sys, json, random, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import outcomes as o

def company(path, complete=True):
    return {'name':'Fictional company','decisions':{str(i+1):{'option':x,'reason':'decision'} for i,x in enumerate(path)},'interventions':[],'history':[],'year':min(len(path)+1,10),'phase':'report' if complete else 'decision','complete':complete}

class ModelTests(unittest.TestCase):
    def test_capabilities_cannot_appear(self):
        s=o.replay(company(['wait','existing'],False))['state']
        self.assertTrue(o.gate(3,'broad',s));self.assertTrue(o.gate(2,'broad',s))
        late=o.replay(company(['wait','late_buy'],False))['state']
        self.assertFalse(o.gate(3,'broad',late));self.assertEqual(late['maintenance'],280)

    def test_inaction_never_creates_contracts_or_disclosure(self):
        c=company(list(o.DEFAULTS.values()))
        for d in c['decisions'].values():d['reason']='deadline'
        s=o.replay(c)['state']
        self.assertFalse(s['prototype']);self.assertEqual(s['recurring'],0)
        self.assertEqual(s['entry'],'existing');self.assertEqual(s.get('disclosure','none'),'none')

    def test_missions_are_end_only_and_history_persists(self):
        path=['hybrid','broad','broad','support','analytics','alternative','expanded','maintain','restructure','full']
        self.assertEqual(o.replay(company(path[:5],False))['missions'],{})
        r=o.replay(company(path));self.assertFalse(r['missions']['legal']);self.assertFalse(r['missions']['employee'])
        self.assertGreater(r['state']['penalties'],0)

    def test_checkpoints_compare_the_same_instant(self):
        a=company(['hybrid','broad','broad','support','analytics'],False);b=company(['hybrid','broad','broad','support','analytics','alternative'],False)
        a['name']='A';a['year']=5;a['phase']='checkpoint';b['name']='B'
        rows=o.comparison([a,b]);self.assertEqual(rows[0]['growth'],rows[1]['growth']);self.assertEqual(rows[0]['growth_rank'],1)

    def test_role_powers_change_outcomes(self):
        c=company(['hybrid'],False);base=o.replay(c)['state'];c['interventions']=[{'year':2,'role':'sustainability'}]
        power=o.replay(c)['state'];self.assertEqual(base['footprint']-power['footprint'],12);self.assertEqual(base['cash']-power['cash'],60)

    def test_thousands_of_valid_paths_are_deterministic(self):
        random.seed(34);seen=set();mission_hits={k:0 for k in o.MODEL['missions']};max_goals=0
        for _ in range(2500):
            c=company([],False)
            for year in range(1,11):
                state=o.replay(c)['state']
                valid=[key for key in o.MODEL['rules'][str(year)] if not o.gate(year,key,state)]
                pick=random.choice(valid);seen.add((year,pick));c['decisions'][str(year)]={'option':pick,'reason':'decision'};c['year']=min(year+1,10)
            c['complete']=True;c['phase']='report'
            r=o.replay(c);self.assertEqual(r,o.replay(c));self.assertEqual(len(r['timeline']),10)
            self.assertGreaterEqual(r['state']['cash'],0)
            self.assertTrue(all(0<=r['state'][k]<=100 for k in ('trust','access','reliability','control')))
            max_goals=max(max_goals,sum(r['commitments'].values()))
            for k,v in r['missions'].items():mission_hits[k]+=v
        self.assertEqual(len(seen),sum(len(v) for v in o.MODEL['rules'].values()))
        self.assertEqual(max_goals,4)
        self.assertTrue(all(mission_hits.values()),mission_hits)
        print('2500 complete valid routes; all branches reached; each role can succeed; all four public goals attainable.',mission_hits)

if __name__=='__main__':unittest.main()
