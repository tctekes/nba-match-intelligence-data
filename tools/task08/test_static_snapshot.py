"""Synthetic fixtures only. Run: python -m unittest -v test_static_snapshot."""
import copy,csv,datetime as dt,io,unittest
import static_snapshot as s

def csvtext(records):
    out=io.StringIO(); w=csv.DictWriter(out,fieldnames=list(records[0])); w.writeheader();w.writerows(records);return out.getvalue()
def fixture():
    games=[]; standings=[]; events=[]
    for i in range(0,30,2):
        a,b=s.model.TEAMS[i:i+2]
        for team,opp,points,allowed in [(a,b,100,90),(b,a,90,100)]:
            r={k:0 for k in s.model.FIELDS}
            r.update(season=s.SEASON,team=team,opponent=opp,game_date='2026-11-10',points=points,opponent_points=allowed,point_diff=points-allowed,result='W' if points>allowed else 'L',field_goals_made=points//2,field_goal_attempts=90,turnovers=10)
            games.append(r);standings.append(dict(season=s.SEASON,team=team,games=1,wins=int(points>allowed),losses=int(points<allowed),off_rating_est=points,def_rating_est=allowed,pace=100))
        events.append(dict(id=str(i),date='2026-11-10T23:00:00Z',season={'type':2},status={'type':{'completed':True,'name':'STATUS_FINAL'}},competitions=[{'competitors':[{'team':{'abbreviation':a},'score':'100'},{'team':{'abbreviation':b},'score':'90'}]}]))
    start=dt.date(2026,10,1); cutoff=dt.datetime(2026,11,11,15,tzinfo=dt.timezone.utc)
    docs={(start+dt.timedelta(days=i)).isoformat():{'events':[],'leagues':[{'calendar':[]}]} for i in range(42)}
    docs['2026-11-10']['events']=events
    return games,standings,docs,cutoff

class Gate(unittest.TestCase):
    def setUp(self): self.g,self.st,self.docs,self.cutoff=fixture()
    def data(self): return s.reconstruct(csvtext(self.g),csvtext(self.st))
    def test_30_team_success(self):
        d=self.data();self.assertEqual(len(d['teams']),30);self.assertEqual(s.coverage(d,self.docs,self.cutoff),15)
    def test_missing_team(self):
        self.g=self.g[2:]
        with self.assertRaises(AssertionError):self.data()
    def test_duplicate(self):
        self.g.append(self.g[0])
        with self.assertRaises(ValueError):self.data()
    def test_stale(self):
        for day in ('2026-11-12','2026-11-13','2026-11-14'):self.docs[day]={'events':[],'leagues':[{'calendar':[]}]}
        with self.assertRaisesRegex(AssertionError,'Stale'):s.coverage(self.data(),self.docs,self.cutoff+dt.timedelta(days=3))
    def test_missing_completed_game(self):
        d=self.data();d['scores'].pop(next(iter(d['scores'])))
        with self.assertRaisesRegex(AssertionError,'Missing completed'):s.coverage(d,self.docs,self.cutoff)
    def test_wl_mismatch(self):
        self.st[0]['wins']=0;self.st[0]['losses']=1
        with self.assertRaisesRegex(AssertionError,'W/L'):self.data()
    def test_parity(self):
        d=self.data();self.assertEqual(d['standings_max_abs_difference'],0)
        for t in d['teams'].values():self.assertEqual(t['pace'],100);self.assertEqual(t['ortg']+t['drtg'],190)
    def test_schema_and_attribution(self):
        d=self.data();p=dict(validation='PASS',data_through=d['latest'],cutoff=self.cutoff.isoformat(),game_count=15,build='SYNTHETIC',teams=d['teams'],receipts={})
        text=s.render(p);self.assertEqual(text.count('| '),31*7);self.assertIn('CC BY 4.0',text);self.assertIn('SHA-256',text)
        p.update(validation='FAIL',reason='test');self.assertNotIn('| Team |',s.render(p))
    def test_partial_day(self):
        e=copy.deepcopy(self.docs['2026-11-10']['events'][0]);e['id']='unfinished';e['status']['type']['completed']=False
        self.docs['2026-11-10']['events'].append(e)
        with self.assertRaisesRegex(AssertionError,'Partial'):s.coverage(self.data(),self.docs,self.cutoff)
if __name__=='__main__':unittest.main()