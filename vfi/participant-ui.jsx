import React,{Children,useId,useState} from 'react';
import {Box,Button,Dialog,DialogActions,DialogContent,DialogTitle,MobileStepper,Paper,Stack,Tab,Tabs,Typography,useMediaQuery} from '@mui/material';
import {FinancialPanel,choiceTitle,decisionOptions} from './financial-ui';
import {StoryDocument} from './story-ui';

// The same cards reflow or page. No content is cut off to enforce viewport fit.
export function CardPages({children,label='Information',desktop=0,mobile=1,single=false,className=''}){
 const compact=useMediaQuery('(max-width:48rem)'),[page,setPage]=useState(0);
 const cards=Children.toArray(children),size=compact||single?mobile:desktop||cards.length;
 const steps=Math.max(1,Math.ceil(cards.length/size)),active=Math.min(page,steps-1);
 return <Box className={`card-pages ${className}`}>
  <Box className="card-page-grid">{cards.slice(active*size,(active+1)*size)}</Box>
  {steps>1&&<MobileStepper className="card-pager" variant="text" position="static" steps={steps} activeStep={active} aria-label={label}
   backButton={<Button size="small" disabled={active===0} onClick={()=>setPage(active-1)}>Back</Button>}
   nextButton={<Button size="small" disabled={active===steps-1} onClick={()=>setPage(active+1)}>Next</Button>}/>}
  {steps>1&&<span className="sr-only" role="status">{label}: page {active+1} of {steps}</span>}
 </Box>;
}

export function InfoCard({title,children,details}){
 const [source,setSource]=useState(false);
 return <Paper component="section" variant="outlined" className="briefing-card">{title&&<Typography component="h2" variant="h6">{title}</Typography>}{source?details:children}{details&&<Button variant="outlined" onClick={()=>setSource(!source)}>{source?'Back to summary':'Read full details'}</Button>}</Paper>;
}

export function CompanyBriefing({c,y,content,updates}){
 const compact=useMediaQuery('(max-width:48rem)'),[view,setView]=useState('situation'),[source,setSource]=useState('supplier'),[term,setTerm]=useState(0),id=useId();
 const sources=[['supplier','Offer'],['internal','Team'],['terms','Details']],first=c.year===1,d=content.docs[source];
 const options=decisionOptions(c,y),activeTerm=Math.min(term,options.length-1),selected=options[activeTerm];
 const title=source==='terms'?'Option details':first?content.companyDocuments[source].title:source==='supplier'?y.proposal[0]:y.team[0];
 const panels=[['situation','Situation'],['evidence','Information']];
 return <Box className="briefing-workbench-shell">
  {compact&&<Tabs value={view} onChange={(_,v)=>setView(v)} aria-label="Briefing sections">{panels.map(([key,label])=><Tab key={key} value={key} label={label} id={`${id}-${key}-tab`} aria-controls={`${id}-${key}-panel`}/>)}</Tabs>}
  {compact&&panels.filter(([key])=>key!==view).map(([key])=><Box key={key} role="tabpanel" id={`${id}-${key}-panel`} aria-labelledby={`${id}-${key}-tab`} hidden/>)}
  <Box className="briefing-workbench">
   {(!compact||view==='situation')&&<Paper variant="outlined" className="situation-board" role={compact?'tabpanel':undefined} id={`${id}-situation-panel`} aria-labelledby={compact?`${id}-situation-tab`:undefined}>
    <Box className="source-reading" tabIndex={0} role="region" aria-label="Situation"><StoryDocument y={y} year={c.year} c={c} content={content}/>{updates}</Box>
   </Paper>}
   {(!compact||view==='evidence')&&<Paper variant="outlined" className="situation-board" role={compact?'tabpanel':undefined} id={`${id}-evidence-panel`} aria-labelledby={compact?`${id}-evidence-tab`:undefined}>
    <Tabs className="source-tabs" variant="fullWidth" value={source} onChange={(_,v)=>setSource(v)} aria-label="Decision information">{sources.map(([key,label])=><Tab key={key} id={`${id}-${key}-tab`} aria-controls={`${id}-${key}-panel`} value={key} label={label}/>)}</Tabs>
    {sources.filter(([key])=>key!==source).map(([key])=><Box key={key} role="tabpanel" hidden id={`${id}-${key}-panel`} aria-labelledby={`${id}-${key}-tab`}/>)}
    <Box className="source-reading" role="tabpanel" id={`${id}-${source}-panel`} aria-labelledby={`${id}-${source}-tab`} tabIndex={0}>
     <Typography component="h2" variant="h6">{title}</Typography>
     {source==='terms'?<><Typography component="h3" variant="subtitle2">{selected.title}</Typography><Typography>{selected.detail}</Typography><Typography>{selected.consider}</Typography>{selected.facts&&<Typography>{selected.facts}</Typography>}{c.unavailable?.[selected.id]&&<Typography>{c.unavailable[selected.id]}</Typography>}</>:first?<>{content.companyDocuments[source].paragraphs.map((text,i)=><Typography key={i}>{text}</Typography>)}</>:<Typography>{source==='supplier'?y.proposal[1]:y.team[1]}</Typography>}
    </Box>
    {source==='terms'&&<MobileStepper className="terms-pager" variant="text" position="static" steps={options.length} activeStep={activeTerm} backButton={<Button disabled={!activeTerm} onClick={()=>setTerm(activeTerm-1)}>Back</Button>} nextButton={<Button disabled={activeTerm===options.length-1} onClick={()=>setTerm(activeTerm+1)}>Next</Button>}/>}
   </Paper>}
  </Box>
 </Box>;
}

const round=n=>Number(n.toFixed(1));
export function MetricCard({label,value,note,baseline,max=100,suffix=''}){
 const scale=Math.max(max,Number(value)||0,baseline||0);
 return <Paper variant="outlined" className="metric-card">
  <Typography component="h3" variant="subtitle2">{label}</Typography>
  <Typography className="metric-value">{typeof value==='number'?round(value):value}{suffix}</Typography>
  {typeof value==='number'&&baseline!==undefined&&<Box className="comparison-bars" aria-hidden="true">
   <Box className="bar-row"><span>Start</span><span className="bar-track"><span style={{width:`${Math.max(0,baseline/scale*100)}%`}}/></span><span>{baseline}</span></Box>
   <Box className="bar-row current"><span>Now</span><span className="bar-track"><span style={{width:`${Math.max(0,value/scale*100)}%`}}/></span><span>{round(value)}</span></Box>
  </Box>}
  {note&&<Typography className="metric-note">{note}</Typography>}
 </Paper>;
}
const money=n=>n>=1000?`€${(n/1000).toFixed(2).replace(/0$/,'').replace(/\.$/,'')}m`:`€${round(n)}k`;
export function RoleMetrics({role,state:s,financials}){
 if(role==='cfo'&&financials)return <FinancialPanel financials={financials} history/>;
 const items={
  ceo:[['Market presence',s.growth,'An index of business size, starting at 100. A value of 125 means 25% growth.',100,150]],
  cfo:[['Cash available',money(s.cash),'After recorded costs.'],['Debt',money(s.debt),s.emergency?'Emergency borrowing occurred.':'No emergency borrowing.']],
  cto:[['Reliability',s.reliability,'How reliably customers can buy tickets and enter events. Starts at 93%; your target is 97%.',93,100,'%'],['Technical control',s.control,'How much your team can maintain and change itself. Starts at 70/100; dependence on a supplier lowers the score.',70,100,'/100']],
  marketing:[['Trust',s.trust,'The simulation’s score for confidence in your company, starting at 60/100.',60,100,'/100'],['Market presence',s.growth,'An index of business size, starting at 100. A value of 125 means 25% growth.',100,150]],
  legal:[['Major penalties',s.penalties,'Major penalties upheld against the company during the exercise.'],['Serious complaint',s.complaint?'Open':'None open','An unresolved complaint can trigger a later penalty.']],
  employee:[['Jobs lost',s.redundancies,'Involuntary redundancies so far.']],
  sustainability:[['Operational footprint',s.footprint,'An index of resources used to run the service, starting at 100. A value of 90 means a 10% reduction. It does not measure carbon emissions.',100,150]],
  relations:[['Original venues',s.contracts,'How many of your first 10 venue customers still work with you.'],['New partnerships',s.new_partners,'Partnerships added during the exercise, counted separately from original venues.']]
 }[role]||[];
 return <Box className="role-metrics">{items.map(([label,value,note,baseline,max,suffix])=><MetricCard key={label} {...{label,value,note,baseline,max,suffix}}/>)}</Box>;
}

export function PositionCards({value,privateMission,missionMet,level=2,title='Company position',single=false,financials}){
 const s=value.state;
 const goals={
  'Fair access':`Resale abuse: ${round(s.fraud)}% (target 4% or less). Ticket fee level: ${round(s.fees)} (100 at start; target 110 or less).`,
  'Accessibility':`Customers able to complete a legitimate purchase or entry: ${round(s.access)}% (target at least 96%). Alternative entry: ${s.alternative_entry?'available':'unavailable'}.`,
  'Responsible data use':`${s.commercial_tracking?'Personalised tracking':'No personalised tracking'}; ${s.sharing==='expanded'?'broad screening':'no broad screening'}; attendance kept ${s.attendance_days} days (limit 30); ${s.complaint?'serious complaint open':'no serious complaint open'}.`,
  'Environmental impact':`Resource-use index ${round(s.footprint)}; start 100, target ≤90. Lower is better. Not a carbon estimate.`
 };
 return <Stack spacing={2} className="position-cards">
  {privateMission&&<Paper variant="outlined" className="briefing-card private-mission-result"><Typography component={`h${level}`} variant="h6">Your mission</Typography><Typography>{privateMission}</Typography><Typography variant="subtitle2">{value.final?(missionMet?'Mission achieved':'Mission not achieved'):'Evaluated after Year 10'}</Typography></Paper>}
  <Typography component={`h${level}`} variant="h6">{title}</Typography>
  <CardPages label="Company position" single={single} desktop={2} mobile={1} className="position-deck">
   <MetricCard label="Market presence" value={s.growth} baseline={100} max={150} note="An index of business size, starting at 100. A value of 125 means 25% growth."/>
   <MetricCard label="Trust" value={s.trust} baseline={60} max={100} suffix="/100" note="The simulation’s confidence score, starting at 60/100. The score is fictional; it does not come from a customer survey."/>

   <Paper variant="outlined" className="briefing-card"><Typography component="h3" variant="subtitle2">Partners and people</Typography><Box component="dl" className="compact-ledger"><dt>Original rollout venues</dt><dd>{s.contracts}/10</dd><dt>New partnerships</dt><dd>{s.new_partners}</dd><dt>Rollout jobs lost</dt><dd>{s.redundancies}</dd></Box><Typography>The case tracks compulsory redundancies in the rollout team, including through a merger or rescue.</Typography></Paper>
   {Object.entries(value.commitments).map(([name,met])=><Paper variant="outlined" className="briefing-card" key={name}><Typography component="h3" variant="subtitle2">{name}</Typography><Typography className="metric-value commitment-result">{met?(value.final?'Met':'Currently met'):(value.final?'Not met':'Not yet met')}</Typography><Typography>{goals[name]}</Typography></Paper>)}
  </CardPages>
  <Typography className="metric-note">These are fictional simulation measures. Company results and mission success do not determine your grade.</Typography>
 </Stack>;
}

export function SavedNotes({notes,label}){
 const [key,setKey]=useState(''),id=useId(),entries=Object.entries(notes),chosen=entries.find(([k])=>k===key)||entries.at(-1);
 return <Stack spacing={2}><Typography component="h2" variant="h6">Your saved notes</Typography>{chosen?<><Box component="label" htmlFor={id}>Choose a reflection</Box><Box component="select" id={id} value={chosen[0]} onChange={e=>setKey(e.target.value)} className="notes-stage-select">{entries.map(([k])=><option key={k} value={k}>{label(k)}</option>)}</Box><Typography sx={{whiteSpace:'pre-wrap'}}>{chosen[1].text}</Typography></>:<Typography>No notes saved yet.</Typography>}</Stack>;
}
