"""Deterministic fictional teaching model. Replay saved decisions; never grade students."""
from pathlib import Path
from copy import deepcopy
import json

MODEL = json.loads((Path(__file__).parent / 'decision-model.json').read_text(encoding='utf-8'))
DEFAULTS = {1:'wait',2:'existing',3:'conventional',4:'basic',5:'retain',6:'decline',7:'refuse',8:'maintain',9:'continue',10:'none'}

def change(s, changes):
    for key, value in changes.items():
        s[key] += value
    s['footprint'] += max(0, changes.get('growth',0)) * .2
    for key, lo, hi in [('trust',0,100),('access',70,100),('reliability',70,100),('fraud',0,20),('control',0,100),('load',0,100),('footprint',20,250),('growth',20,300),('staff',0,100),('contracts',0,10)]:
        s[key] = max(lo,min(hi,s[key]))

def gate(year, option, s):
    if year in (2,3) and option in ('late_build','late_buy','late_hybrid'):
        return '' if not s['prototype'] else 'A prototype has already been acquired.'
    if year==2 and option=='broad' and not s['prototype']:
        return 'You need a prototype to test buyer verification. You can still investigate access and integration in conventional ticketing.'
    if year==3 and option in ('broad','limited','delay') and not s['prototype']:
        return 'No verification technology was acquired. You can acquire a prototype now or continue conventional sales.'
    if year==6 and option in ('launch_broad','launch_limited'):
        return '' if s['prototype'] and not s['live'] else 'You need a verification prototype that has not already launched.'
    return ''

def operate(s):
    return 280 + 6*(s['growth']-100) + s['recurring'] - s['maintenance']

def settle(s, log):
    if s['cash'] < 0:
        missing=-s['cash'];s['debt']+=missing;s['cash']=0;s['emergency']=True
        log.append(f'Emergency borrowing: €{missing:,.0f}k. The company remains in the exercise.')
    if s['debt']>800 and not s.get('rescued'):
        s['rescued']=True;s['cash']+=600
        payment=min(s['cash'],s['debt']);s['cash']-=payment;s['debt']-=payment
        change(s,dict(growth=-15,staff=-6,redundancies=6,load=-10))
        log.append('The company sells assets to repay €600k of debt. Six people lose their jobs, and market presence falls by 15 points.')

def apply_power(s, action, log):
    role=action['role']
    if role=='legal':change(s,{'cash':-35});s['evidence']=min(3,s['evidence']+1)
    elif role=='employee':change(s,{'cash':-80,'load':-15,'growth':-2})
    elif role=='sustainability':change(s,{'cash':-60,'footprint':-12})
    elif role=='marketing':change(s,{'cash':-80,'trust':6 if s['evidence']>=2 or not s['live'] else -3})
    elif role=='relations':
        change(s,{'cash':-70})
        if s['access']>=94 and s['reliability']>=95:s['new_partners']+=1
    log.append({'ceo':'The CEO used an executive override.', 'cfo':'Finance blocked an option for this year.', 'cto':'The CTO blocked an option for this year.', 'legal':'The company spent €35k on a legal review and blocked an option for this year. The evidence level improved.', 'employee':'A strike settlement provided €80k of temporary cover. Workload fell by 15 points, while delivery delays reduced market presence by 2.', 'sustainability':'The company spent €60k assessing operations and making changes. The footprint index fell by 12.', 'marketing':'The company spent €80k on a campaign. '+('Trust rose by 6 points.' if s['evidence']>=2 or not s['live'] else 'Challenged claims reduced trust by 3 points.'), 'relations':'The company spent €70k negotiating a venue agreement. '+('It gained a new partnership.' if s['access']>=94 and s['reliability']>=95 else 'The negotiation did not secure a new partnership.')}[role])

def event(s,y,log):
    story=MODEL['events'][str(y)]
    if y==2:
        story='A customer has delayed its €220k payment until Year 4. The company must fund its existing commitments while waiting for the money.'
        change(s,{'cash':-220})
        if s['prototype'] and s['evidence']==3 and s.get('acquired_year',10)<2:
            change(s,{'cash':150});log.append('The promoter invests €150k after seeing the working, broadly tested prototype.')
    elif y==3:
        story='The consumer investigation examines your current service. The testing provides evidence for the release arrangements you chose.' if s['live'] else 'The consumer investigation examines your conventional ticket sales. Staff still handle resale abuse and customer appeals manually.'
        if s.get('launch')=='broad' and s['evidence']<2:
            change(s,{'cash':-180,'trust':-8,'access':-4,'reliability':-4,'contracts':-1,'growth':-3})
            log.append('The investigation confirms failures after the broad launch. The company pays refunds, loses trust and loses one original venue customer.')
    elif y==4:
        story='The delayed €220k payment has arrived. Support staff can manage current demand without additional temporary cover.'
        change(s,{'cash':220})
        if s['load']>65:
            change(s,{'cash':-90,'reliability':-3,'trust':-3,'load':-10})
            log.append('Support staff cannot manage all the requests. Temporary cover is needed, and the service becomes less reliable.')
            story='The delayed customer payment has arrived, while support requests have exceeded what staff can manage.'
    elif y==5:
        story='Fans are spending less on entertainment. Demand has fallen, with further effects on income depending on how the company funds its service.'
        change(s,{'growth':-8-(4 if s.get('revenue')=='fees' else 0)})
        if s.get('revenue') in ('premium','sponsors'):change(s,{'recurring':-40})
    elif y==6:
        story='The company’s entry arrangements coped with the busy event without needing major corrections.'
        if s['entry']=='full' and s['evidence']<3:
            change(s,{'cash':-160,'trust':-5,'access':-2});log.append('Failed biometric checks at the busy event require corrections to the entry system.')
            story='During the busiest arrivals, staff struggled to help customers rejected by biometric checks.'
        elif s['entry']=='selective':
            change(s,{'cash':-50});story='Both optional facial entry and staffed alternatives worked. Helping people switch between them required €50k in additional staffing.'
        elif s['reliability']<95:
            change(s,{'cash':-70,'trust':-2});story='Entry was disrupted during the event. Additional support cost €70k, and trust fell after customers experienced problems.'
    elif y==7:
        exposed=s['commercial_tracking'] or s['sharing']=='expanded'
        change(s,{'trust':-8 if exposed else 3})
        log.append('The coalition challenges the company’s data practices.' if exposed else 'The company’s low-data service attracts support during the industry campaign.')
        story='Artists and fans want the company to explain its current practices. Your team will decide how to respond next year.'
    elif y==8:
        before_partners=s['new_partners']
        if s['access']<92 or s['trust']<50:
            lost=min(2,s['contracts']);change(s,{'contracts':-lost,'growth':-4*lost});log.append(f'{lost} original venues do not renew.')
        else:log.append('The original venue customers still working with the company renew their agreements.')
        if s['trust']>=65 and s['access']>=94:s['new_partners']+=1;change(s,{'growth':4})
        if s['entry'] in ('selective','alternative') and s['reliability']>=95:s['new_partners']+=1;change(s,{'growth':4})
        story=f"Partner negotiations produce {s['new_partners']-before_partners} new agreements. New partnerships are counted separately from the original venue customers that remain."
    elif y==9:
        story='The independent review finds no unresolved broad-screening complaint that would lead to a new penalty.'
        if s['complaint']:
            change(s,{'cash':-300,'trust':-10});s['penalties']+=1
            log.append('The independent review upholds the screening complaint, resulting in a €300k penalty.')
            story='The company remains responsible for the screening complaint. The penalty will remain in its history when it publishes next year’s report.'
        if s.get('specialist') and s['trust']>=65:s['new_partners']+=1;change(s,{'growth':4})
    log.append(story)
    settle(s,log)

def commitments(s):
    return {
        'Fair access':s['fraud']<=4 and s['fees']<=110,
        'Accessibility':s['access']>=96 and s['alternative_entry'],
        'Responsible data use':not s['commercial_tracking'] and s['sharing']!='expanded' and s['attendance_days']<=30 and not s['complaint'],
        'Environmental impact':s['footprint']<=90,
    }

def evaluate(s):
    viable=s['cash']>=0 and s['debt']<=800 and operate(s)>=0
    goals=commitments(s)
    missions=dict(ceo=viable and s['growth']>=125 and sum(goals.values())>=3,
        cfo=viable and s['growth']>=125 and not s['emergency'],
        cto=s['reliability']>=97 and s['control']>=60,
        marketing=s['trust']>=75 and s['growth']>=120,
        legal=s['penalties']==0 and not s['complaint'],employee=s['redundancies']==0,
        sustainability=s['footprint']<=90,relations=s['contracts']>=8 and s['new_partners']>=2)
    return goals,missions,viable

def replay(company, through=None):
    s=deepcopy(MODEL['initial']);timeline=[];snapshots={}
    decisions=company.get('decisions',{})
    last=max([int(k) for k in decisions],default=0)
    for y in range(1,min(through or 10,last)+1):
        if str(y) not in decisions:break
        log=[];before=deepcopy(s)
        for action in company.get('interventions',[]):
            if action['year']==y:apply_power(s,action,log)
        choice=decisions[str(y)]['option']
        rule=MODEL['rules'][str(y)].get(choice)
        if not rule:raise ValueError(f'Unknown Year {y} choice: {choice}')
        problem=gate(y,choice,s)
        # Legacy records remain printable, but cannot manufacture technology.
        passive=decisions[str(y)].get('reason') in ('deadline','facilitator_skip')
        if passive:
            log.append('The team agreed no new action this year. The company continues its existing service, prices, contracts and duties.')
        elif problem:
            log.append('Legacy choice could not be enacted: '+problem)
        else:
            old_maintenance=s['maintenance']
            if y==8 and choice in ('negotiate','revise') and s['sharing']=='expanded':s['recurring']-=140
            if y==8 and choice=='revise' and s['commercial_tracking']:s['recurring']-=120
            change(s,rule['changes']);s.update(rule['flags']);log.append(rule['consequence'])
            if choice.startswith('late_') or y==1 and choice!='wait':s['acquired_year']=y
            if y==3 and choice in ('broad','limited'):
                s['access']+=min(s['evidence'],2);s['reliability']+=min(s['evidence'],2)
            if y==6 and choice in ('launch_broad','launch_limited'):
                if choice=='launch_broad' and s['evidence']<2:
                    change(s,{'cash':-180,'access':-4,'reliability':-4,'trust':-8,'contracts':-1})
                    log.append('The late broad launch reaches customers with limited testing. Failures add the same costs as they would have at an earlier launch.')
            if y==10 and choice=='summary':change(s,{'trust':-6 if s['complaint'] or s['penalties'] else 1})
        change(s,{})
        maintenance=s['maintenance'] if s.get('acquired_year',0)<y else 0
        surplus=280+6*(s['growth']-100)+s['recurring']-maintenance-.1*s['debt']
        s['cash']+=surplus
        log.append(f'Year-end cash movement from operations: €{surplus:,.0f}k, after recurring costs and debt interest.')
        settle(s,log)
        snapshots[str(y)]=deepcopy(s)
        # Year 5 ranking is before its external event for every group.
        seen_event=(y<company.get('year',1) or any(h.get('type')=='event' and h.get('year')==y for h in company.get('history',[])) or y==company.get('year') and company.get('phase')=='event')
        if y<10 and seen_event:event(s,y,log)
        delta={k:round(s[k]-before[k],2) for k in s if isinstance(s[k],(int,float)) and not isinstance(s[k],bool) and k in before and s[k]!=before[k]}
        timeline.append(dict(year=y,option=choice,log=log,changes=delta,state=deepcopy(s)))
    # Powers happen immediately, even before the year's company decision.
    for action in company.get('interventions',[]):
        if action['year']>last:apply_power(s,action,[])
    goals,missions,viable=evaluate(s)
    return dict(version=MODEL['version'],state=s,commitments=goals,targets=MODEL['targets'],viable=viable,
        timeline=timeline,snapshots=snapshots,missions=missions if company.get('complete') else {},final=bool(company.get('complete')))

def comparison(companies):
    if not companies:return []
    year=10 if all(c.get('complete') for c in companies) else 5
    rows=[]
    for c in companies:
        result=replay(c);s=result['snapshots'].get(str(year))
        if s is None:return []
        rows.append(dict(name=c['name'],year=year,growth=round(s['growth'],1),trust=round(s['trust'],1),commitments=commitments(s)))
    for row in rows:
        row['growth_rank']=1+sum(other['growth']>row['growth'] for other in rows)
        row['trust_rank']=1+sum(other['trust']>row['trust'] for other in rows)
    return sorted(rows,key=lambda r:(r['growth_rank'],r['name']))
