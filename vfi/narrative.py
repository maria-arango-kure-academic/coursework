"""Present the fictional case through documents selected from actual decisions.

This module reads the existing model. It never records decisions or changes state.
"""
from copy import deepcopy
from pathlib import Path
import json
import outcomes

CATALOGUE=json.loads((Path(__file__).parent/'story.json').read_text(encoding='utf-8'))

def at(company, year, after=False, event=True):
    record=deepcopy(company)
    record.update(year=year,phase=('event' if event and year<10 else 'report') if after else 'decision')
    record['decisions']={k:v for k,v in company['decisions'].items() if int(k)<year or after and int(k)==year}
    record['interventions']=[i for i in company.get('interventions',[]) if i['year']<=year]
    record['history']=[h for h in company.get('history',[]) if h['year']<year or after and event and h['year']==year]
    return outcomes.replay(record)

def document(key,company):
    doc=deepcopy(CATALOGUE['assets'][key])
    doc.pop('voice',None)
    doc['notice']=CATALOGUE['notice']
    doc['company']=company['name']
    return doc

def brief_key(y,s,company):
    if y==1:return 'b1'
    if y==2:return 'b2-'+s['architecture']
    if y==3:
        investigation=company['decisions'].get('2',{}).get('option')
        return 'b3-none' if not s['prototype'] else 'b3-tested' if investigation=='broad' else 'b3-focused' if investigation=='focused' else 'b3-thin'
    if y==4:return 'b4-live' if s['live'] else 'b4-conventional'
    if y==5:return 'b5-'+s.get('feature','basic')
    if y==6:return 'b6-'+(s.get('revenue') if s.get('revenue') in ('fees','sponsors') else 'other')
    if y==7:return 'b7-'+(s['entry'] if s['entry'] in ('full','selective') else 'lowdata')
    if y==8:return 'b8-screening' if s['sharing']=='expanded' else 'b8-tracking' if s['commercial_tracking'] else 'b8-lowdata'
    if y==9:
        choice=company['decisions'].get('8',{}).get('option')
        return {'revise':'b9-revised','separate':'b9-separate','negotiate':'b9-targeted'}.get(choice,'b9-maintain')
    if s['penalties']:return 'b10-penalty'
    previous=company['decisions'].get('9',{})
    strategy=previous.get('option') if previous.get('reason') not in ('deadline','facilitator_skip') else None
    if strategy in ('restructure','merge'):return 'b10-'+strategy
    if s['redundancies']:return 'b10-jobs'
    return 'b10-'+strategy if strategy in ('expand','specialise','continue') else 'b10-clean'

def callback(y,s):
    key=None
    if y in (2,3,4):key=s['architecture']
    elif y==5:key=s.get('feature','basic')
    elif y==6:key=s.get('revenue','retain')
    elif y==7:key=s['entry'] if s['entry']!='existing' else s['architecture']
    elif y==8:key='sponsors' if s['commercial_tracking'] else s['sharing']
    elif y==9:key=s.get('feature','basic')
    elif y==10:key='sponsors' if s['commercial_tracking'] else s['architecture']
    return CATALOGUE['callbacks'].get(key,'')

def brief(company,year=None):
    y=year or company['year'];s=at(company,y)['state']
    doc=document(brief_key(y,s,company),company)
    doc['callback']=callback(y,s)
    if y==10:
        previous=company['decisions'].get('9',{})
        strategy=previous.get('option') if previous.get('reason') not in ('deadline','facilitator_skip') else 'continue'
        action={'expand':'The company expanded and hired six people.', 'restructure':'The company rebuilt operations and cut six jobs.', 'specialise':'The company focused on smaller accessible venues.', 'merge':'The company accepted a controlling investor and cut eight jobs.', 'continue':'The company continued its existing business.'}.get(strategy,'The existing business continued.')
        doc['callback']=action+f" The record includes {s['redundancies']} compulsory redundancies in the rollout team and {s['penalties']} upheld major penalties across the decade."
        if s['sharing']=='expanded' and s['entry']=='full':
            doc['callback']='A breach exposed records linking names, billing addresses and face templates to events across several venues. Organisers want attendees warned and told who received the records. '+doc['callback']
    return doc

def aftermath(company,y):
    decision=company['decisions'].get(str(y))
    if not decision:return None
    passive=decision.get('reason') in ('deadline','facilitator_skip')
    choice=decision['option'];before=at(company,y)['state'];result=at(company,y,True)
    s=result['state'];pre_event=result['snapshots'][str(y)]
    key=f'a{y}-'+('passive' if passive else choice)
    if not passive and y==3 and choice=='broad':key='a3-broad-'+('failed' if before['evidence']<2 else 'tested')
    if y==4 and pre_event['load']>65:key='a4-overload'
    if y==6:
        if s['entry']=='full':key='a6-full-'+('failed' if pre_event['evidence']<3 else 'tested')
        elif s['entry']=='selective':key='a6-selective'
        elif choice=='launch_broad' and not passive and before['evidence']<2:key='a6-launch-failed'
        elif pre_event['reliability']<95:key='a6-disruption'
    if y==8 and not passive:
        if choice=='negotiate' and before['sharing']!='expanded':key='a8-negotiate-limits'
        if choice=='revise':
            screening=before['sharing']=='expanded';tracking=before['commercial_tracking']
            if not screening and not tracking:key='a8-revise-existing-limits'
            elif screening and not tracking:key='a8-revise-screening'
            elif tracking and not screening:key='a8-revise-sponsorship'
    if not passive and y==10 and choice=='summary':key='a10-summary-'+('concealed' if before['complaint'] or before['penalties'] else 'clear')
    doc=document(key,company)
    doc['callback']=callback(y,s)
    doc['follow_up']=[]
    if y==2 and passive:doc['follow_up'].append('A customer has delayed its €220k payment until Year 4. The company must fund its current commitments while waiting.')
    if y==4 and passive and key!='a4-overload':doc['follow_up'].append('The delayed €220k customer payment has arrived. Existing support work and service obligations continue.')
    if y==5 and passive:doc['follow_up'].append('Entertainment spending has fallen. The company must keep providing the service while ticket demand weakens.')
    if y==7:
        doc['follow_up'].append('The coalition challenges the company’s broad screening or personalised tracking, reducing trust.' if s['commercial_tracking'] or s['sharing']=='expanded' else 'The company’s low-data practices attract support during the industry campaign.')
    if y==7 and s['sharing']=='expanded':
        if s['entry']=='full':
            doc['follow_up'].insert(0,'The live feed correctly identifies an attendee arriving at a union meeting and gives police their name, location and arrival time. The same agreement covers a political talk and an LGBTQ+ night. People are being identified because they attended, even when nobody disputes who they are.')
        elif s['entry']=='selective':
            doc['follow_up'].insert(0,'Police receive live identity matches for fans who used facial entry. The staffed lane produces no face match to send.')
        else:
            doc['follow_up'].insert(0,'The screening agreement gives police access to named ticket records where available. The entry system produces no live face match.')
    if y==6 and key=='a6-launch-failed' and pre_event['reliability']<95:
        doc['follow_up'].append('The busy event also disrupted the existing entry arrangement. Additional support cost €70k and trust fell further.')
    if y==8:
        lost=max(0,before['contracts']-s['contracts']);gained=max(0,s['new_partners']-before['new_partners'])
        doc['follow_up'].append(f'{lost} original venue'+('s have' if lost!=1 else ' has')+' declined renewal after the company’s access or trust fell below their requirements.' if lost else 'The original venues still working with the company have renewed their agreements.')
        doc['follow_up'].append(f'The negotiations also produced {gained} new partnership'+('s.' if gained!=1 else '.'))
    if y==9:
        if s['sharing']=='expanded' and s['entry']=='full':
            doc['title']='Attendee records from multiple venues exposed'
            doc['follow_up'].insert(0,'A breach makes attendee records from multiple venues public. The files link names, billing addresses and facial templates to the events people attended. An LGBTQ+ night attendee asks the organiser to remove their home address. A union member says their employer has been sent a list of names from a meeting. Copies are already circulating.')
        doc['follow_up'].append('The independent review upheld the unresolved screening complaint. The company receives a €300k penalty and loses trust.' if s['penalties']>before['penalties'] else 'The independent review found no unresolved broad-screening complaint requiring a new penalty.')
    if s['emergency'] and not before['emergency']:
        doc['follow_up'].append('Finance arranged emergency borrowing when cash ran out. That borrowing stays in the record even if the debt is repaid.')
    if s.get('rescued') and not before.get('rescued'):
        doc['follow_up'].append('An asset-sale rescue repaid €600k of debt and caused six additional job losses. Those employees remain part of the company’s history.')
    if y==10:
        year_seven = at(company, 7, after=True)['state']
        if year_seven['sharing']=='expanded':
            if s['sharing']=='expanded' and s['entry']=='full':
                doc['title']='The leaked attendee records are still circulating'
                doc['follow_up'].insert(0,'Copies of the leaked attendee records are still circulating. People can use the records to out attendees, identify workers who attended a union meeting or target people associated with a political event. Publishing the company’s account cannot recall the copies.')
            elif s['sharing']!='expanded':
                doc['follow_up'].insert(0,'The broad screening arrangement has ended. The event organiser still wants to know who kept copies of the records already shared. People who stayed home missed the event.')
            else:
                doc['follow_up'].insert(0,'Police access continues. People linked to sensitive events through ticket records still face exposure. Those who stayed home missed the event.')
        elif s['entry']=='alternative':
            doc['follow_up'].insert(0,'At participating venues, people can use staffed gates and offline codes. The gates create no face record and the company never opened an ongoing police feed. The lower-power equipment also reduces the resources needed to run entry.')
        goals=outcomes.commitments(s)
        doc['follow_up'].append('Lina, from the first festival: '+('Your record meets the fair-access commitment that helped start our relationship. We will still judge the service by what happens when people try to buy.' if goals['Fair access'] else 'We first asked for ticketing that our festival could afford. Your record still falls short of the fair-access commitment; our customers will need the company to keep working on it.'))
        doc['rows']=[['Original rollout venues remaining',f"{s['contracts']} of 10"],['New partnerships',str(s['new_partners'])],['Rollout jobs lost',str(s['redundancies'])],['Public commitments met',f"{sum(goals.values())} of 4"]]
    return doc

def company_story(company):
    y=company['year']
    seen=lambda year: year<y or year==y and (company['phase']=='event' or year==10 and company.get('complete')) or any(h['year']==year and h['type']=='event' for h in company.get('history',[]))
    return dict(version=CATALOGUE['version'],brief=brief(company),update=aftermath(company,y) if company['phase']=='event' else None,
        records={str(year):aftermath(company,year) for year in range(1,y+1) if str(year) in company['decisions'] and seen(year)})

def private_message(company,role,content):
    y=company['year'];event=company['phase']=='event'
    if company['phase']=='report':
        result=outcomes.replay(company);s=result['state'];goals=result['commitments']
        summaries={
            'ceo':[f"The company finishes with {sum(goals.values())} of four public commitments met and a market presence index of {s['growth']:.1f}.", 'Finance records the company as '+('operational at the end of the exercise.' if result['viable'] else 'unable to meet the financial operating conditions at the end of the exercise.')],
            'cfo':[f"The final account records €{s['cash']:,.0f}k cash, €{s['debt']:,.0f}k debt and market presence of {s['growth']:.1f}.", 'Emergency borrowing occurred during the exercise and remains in the record even if debt was later repaid.' if s['emergency'] else 'The company reached the end without emergency borrowing.'],
            'cto':[f"Reliability finishes at {s['reliability']:.1f}%, and technical control at {s['control']:.1f} out of 100.",callback(3,s)],
            'marketing':[f"Trust finishes at {s['trust']:.1f} out of 100 and market presence at {s['growth']:.1f}, compared with 100 at the start.", 'Customers and partners have experienced the service, its changes and the company’s final account across the decade.'],
            'legal':[f"The record contains {s['penalties']} upheld major penalties. "+('A serious complaint remains unresolved.' if s['complaint'] else 'No serious complaint remains unresolved.'), 'A later remedy or publication leaves earlier upheld penalties in the record.'],
            'employee':[f"The rollout team finishes with {s['staff']} staff. It recorded {s['redundancies']} compulsory redundancies across the exercise.", 'The staffing total includes later hiring; it does not remove earlier employees’ redundancies.'],
            'sustainability':[f"The final operational-footprint index is {s['footprint']:.1f}, compared with 100 at the start.", 'This records resources used to run the company’s service, including the effect of business growth. It is a fictional index, without measured carbon emissions.'],
            'relations':[f"The company retains {s['contracts']} of its ten original venues and has gained {s['new_partners']} additional partnerships.", 'Those new agreements are counted separately from the original customers whose relationships you were asked to protect.']
        }
        return dict(id=f'private-final-{role}',kind='memo',sender=CATALOGUE['role_senders'][role],title='Your part in the company’s record',body=[p for p in summaries[role] if p],notice='Private fictional case message',company=company['name'])
    if event:
        public=aftermath(company,y)
        body=[f'Forwarded from {public["sender"]}: “{public["body"][0]}”'] if public else [content['events'][y]['impacts'][role]]
    else:
        body=[content['years'][y]['info'][role][0]]
    s=at(company,y,after=event or company['phase'] in ('checkpoint','report'),event=event)['state']
    history={
        'ceo':f"The division is responsible for its {s['staff']}-person rollout team and the venues that still use the service.",
        'cfo':f"Finance currently records €{s['cash']:,.0f}k in cash and €{s['debt']:,.0f}k of debt.",
        'cto':callback(y,s),
        'marketing':'The company still uses personalised sponsorship, so claims about its data practices need to account for that agreement.' if s['commercial_tracking'] else 'The current service does not use personalised commercial tracking.',
        'legal':'The screening complaint is still unresolved.' if s['complaint'] else ('An earlier upheld penalty remains in the record.' if s['penalties'] else 'Any new agreement needs to account for the company’s current service and duties.'),
        'employee':f"The record includes {s['redundancies']} compulsory redundancies in the rollout team so far; hiring later does not remove them." if s['redundancies'] else f"The rollout team currently has {s['staff']} staff and has made no compulsory redundancies.",
        'sustainability':f"The current resource-use index is {s['footprint']:.1f}, compared with 100 at the start. It includes the effect of business growth.",
        'relations':f"The company still serves {s['contracts']} original venues and has {s['new_partners']} additional partnerships."
    }[role]
    if history:body.append(history)
    return dict(id=f'private-{y}-{role}-{company["phase"]}',kind='email',sender=CATALOGUE['role_senders'][role],
        title=CATALOGUE['role_subjects'][role][y-1],body=body,notice='Private fictional case message',company=company['name'])
