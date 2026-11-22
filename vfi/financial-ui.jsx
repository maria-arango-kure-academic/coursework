import React,{useId,useState} from 'react';
import {Box,Button,FormControlLabel,MobileStepper,Paper,Radio,RadioGroup,Tab,Tabs,Typography,useMediaQuery} from '@mui/material';

export const euro=k=>`${k<0?'−':''}€${Math.abs(k)>=1000?(Math.abs(k)/1000).toLocaleString('en-GB',{maximumFractionDigits:3})+'m':Math.abs(k).toLocaleString('en-GB',{maximumFractionDigits:1})+'k'}`;

export const choiceTitle=option=>option?.display_title||option?.title||'';
const choiceNotice=reason=>reason?.startsWith('No verification technology was acquired.')?'Requires a verification prototype.':reason;
export function decisionOptions(c,y){
 const selected=c.decisions[String(c.year)]?.option;
 return y.options.filter(o=>o.id===selected||((!o.id.startsWith('late_')||!c.performance.state.prototype)&&(!o.id.startsWith('launch_')||(c.performance.state.prototype&&!c.performance.state.live))));
}

export function FinancialPanel({financials:f,options=[],history=false,panelId,labelledBy,paged=false}){
 const compact=useMediaQuery('(max-width:48rem)'),short=useMediaQuery('(max-height:700px)'),[page,setPage]=useState(0);
 if(!f)return <Paper variant="outlined" className="finance-panel"><Typography>Financial figures are loading.</Typography></Paper>;
 const allOffers=options.map(o=>({...f.offers.find(q=>q.id===o.id),title:choiceTitle(o)})).filter(q=>q.id);
 const size=paged?(compact?(short?1:2):(allOffers.length>4?3:4)):Math.max(1,allOffers.length),steps=Math.max(1,Math.ceil(allOffers.length/size)),active=Math.min(page,steps-1),offers=allOffers.slice(active*size,(active+1)*size);
 const cash=history?f.cash_now:f.cash_before_decision,debt=history?f.debt_now:f.debt_before_decision;
 const scale=Math.max(1,cash,...f.offers.map(o=>o.cash_after_upfront));
 const points=f.history||[],maxCash=Math.max(1,...points.map(p=>p.cash));
 const coordinates=points.map((p,i)=>[points.length===1?180:12+i*336/(points.length-1),128-p.cash/maxCash*112]);
 return <Paper component="section" tabIndex={0} aria-label={history?'Cash over time':'Cash after each option'} role={labelledBy?'tabpanel':undefined} id={panelId} aria-labelledby={labelledBy} variant="outlined" className={`finance-panel ${history?'finance-history-panel':''}`}>
  <Typography component="h2" variant="h6">{history?'Cash over time':'Cash after each option'}</Typography>
  <Box className="cash-totals"><Box><Typography>{history?'Cash now':'Cash before decision'}</Typography><Typography className="cash-number">{euro(cash)}</Typography></Box><Box><Typography>{history?'Debt now':'Debt before'}</Typography><Typography className="cash-number">{euro(debt)}</Typography></Box></Box>
  {history?<Box component="figure" className="cash-history">
   <Box className="cash-axis"><span>€0–{euro(maxCash)}</span><span>Cash available</span></Box>
   <svg preserveAspectRatio="none" viewBox="0 0 360 140" role="img" aria-label={`Cash from ${euro(points[0]?.cash||0)} at the start to ${euro(points.at(-1)?.cash||0)} after recorded activity.`}>
    <path d="M12 128H348 M12 72H348 M12 16H348" className="cash-grid"/>
    <polyline points={coordinates.map(p=>p.join(',')).join(' ')} className="cash-line"/>
    {coordinates.map(([cx,cy],i)=><circle key={i} cx={cx} cy={cy} r="4" className="cash-point"/>)}
   </svg>
   <Box className="cash-axis"><span>Start · {euro(points[0]?.cash||0)}</span><span>{points.length>1?` ${points.at(-1).current?'Now':'Year '+points.at(-1).year} · ${euro(points.at(-1).cash)}`:'No decision recorded'}</span></Box>
   <figcaption>Includes recorded decisions, operating results and other costs or income so far.</figcaption>
   <ul className="sr-only">{points.map(p=><li key={p.year}>{p.current?'Now':p.year===0?'Start':`Year ${p.year}`}: {euro(p.cash)}</li>)}</ul>
  </Box>:<Box component="figure" className="cash-options"><Box className="cash-axis" aria-hidden="true"><span>€0</span><span>{euro(scale/2)}</span><span>{euro(scale)}</span></Box>
   {offers.map(o=><Box key={o.id} className="cash-option">
    <Box className="cash-option-label"><Typography component="h3" variant="subtitle2">{o.title}</Typography><Typography>{o.upfront_change>0?'+':''}{euro(o.upfront_change)}</Typography></Box>
    <Box className="cash-option-track" aria-hidden="true"><span style={{width:`${Math.max(0,o.cash_after_upfront)/scale*100}%`}}/><i style={{left:`${Math.min(100,Math.max(0,cash/scale*100))}%`}}/></Box>
    <Typography>{o.cash_after_upfront>=0?`${euro(o.cash_after_upfront)} left`:`${euro(-o.cash_after_upfront)} funding gap`}</Typography>
   </Box>)}
   <figcaption>Shows the immediate cost or payment for each choice. Running costs, operating income and events are calculated later.</figcaption>
  </Box>}{!history&&steps>1&&<MobileStepper className="finance-pager" position="static" variant="text" steps={steps} activeStep={active} backButton={<Button disabled={!active} onClick={()=>setPage(active-1)}>Back</Button>} nextButton={<Button disabled={active===steps-1} onClick={()=>setPage(active+1)}>Next</Button>}/>}
 </Paper>;
}

export function DecisionWorkbench({c,y,options,choice,setChoice,busy,action}){
 const compact=useMediaQuery('(max-width:48rem)'),short=useMediaQuery('(max-height:700px)'),[page,setPage]=useState(0),[view,setView]=useState('options'),id=useId();
 const decision=c.decisions[String(c.year)],size=compact?(short?1:2):4,steps=Math.ceil(options.length/size),active=Math.min(page,steps-1),shown=options.slice(active*size,(active+1)*size);
 const labels=[['options','Options'],['money','Financials']];
 return <Box className="decision-workbench-shell">
  {compact&&<Tabs value={view} onChange={(_,v)=>setView(v)} aria-label="Decision workspace">{labels.map(([key,label])=><Tab id={`${id}-${key}-tab`} aria-controls={`${id}-${key}-panel`} key={key} value={key} label={label}/>)}</Tabs>}
  {compact&&labels.filter(([key])=>key!==view).map(([key])=><Box key={key} role="tabpanel" id={`${id}-${key}-panel`} aria-labelledby={`${id}-${key}-tab`} hidden/>)}<Box className="decision-workbench">
   {(!compact||view==='options')&&<Paper component="section" variant="outlined" className="decision-board" tabIndex={0} aria-label="Decision options" role={compact?'tabpanel':undefined} id={`${id}-options-panel`} aria-labelledby={compact?`${id}-options-tab`:undefined}>
    <RadioGroup name="company-decision" aria-label={y.question} value={choice||decision?.option||''} onChange={(_,v)=>setChoice(v)} className="choice-list">
     {shown.map(o=><FormControlLabel key={o.id} className="choice-row" control={<Radio value={o.id} disabled={!!decision||busy||!!c.paused||!!c.unavailable?.[o.id]}/>} label={<Box><Typography component="h2" variant="subtitle2">{choiceTitle(o)}</Typography><Typography>{o.summary||`${o.detail} ${o.consider}`}</Typography>{o.facts?.includes('months')&&<Typography className="choice-timing">{o.facts.split('·').slice(1).join('·').trim()}</Typography>}{c.unavailable?.[o.id]&&<Typography className="blocked-reason">{choiceNotice(c.unavailable[o.id])}</Typography>}</Box>}/>)}
    </RadioGroup>
   </Paper>}
   {(!compact||view==='money')&&<Box role={compact?'tabpanel':undefined} id={`${id}-money-panel`} aria-labelledby={compact?`${id}-money-tab`:undefined}><FinancialPanel financials={c.financials} options={shown}/></Box>}
  </Box>
  <Box className="decision-bottom">
   {steps>1&&<MobileStepper variant="text" position="static" steps={steps} activeStep={active} aria-label="Decision options" backButton={<Button disabled={!active} onClick={()=>setPage(active-1)}>Back</Button>} nextButton={<Button disabled={active===steps-1} onClick={()=>setPage(active+1)}>Next</Button>}/>}
   {compact&&view==='money'?<Button variant="outlined" onClick={()=>setView('options')}>Back to options</Button>:decision?<><Typography role="status">Decision saved{decision.reason==='deadline'?' after time expired; existing arrangements continued':''}.</Typography><Button variant="contained" disabled={busy} onClick={()=>action('advance')}>{c.year===10?'See outcomes':c.year===5?'Go to checkpoint':'See what happens'}</Button></>:<Button variant="contained" disabled={!choice||busy||!!c.paused||!!c.unavailable?.[choice]} onClick={()=>action('decide')}>Save decision</Button>}
  </Box>
 </Box>;
}

export function StageWorkbench({c,children,label='Update'}){
 const compact=useMediaQuery('(max-width:48rem)'),[view,setView]=useState('info'),id=useId();
 const labels=[['info',label],['money','Financials']];
 return <Box className="evidence-workbench-shell">{compact&&<Tabs value={view} onChange={(_,v)=>setView(v)} aria-label={`${label} workspace`}>{labels.map(([key,text])=><Tab key={key} id={`${id}-${key}-tab`} aria-controls={`${id}-${key}-panel`} value={key} label={text}/>)}</Tabs>}
  {compact&&labels.filter(([key])=>key!==view).map(([key])=><Box key={key} hidden role="tabpanel" id={`${id}-${key}-panel`} aria-labelledby={`${id}-${key}-tab`}/>)}
  <Box className="evidence-workbench">
   {(!compact||view==='info')&&<Box className="stage-primary" role={compact?'tabpanel':undefined} id={`${id}-info-panel`} aria-labelledby={compact?`${id}-info-tab`:undefined}>{children}</Box>}
   {(!compact||view==='money')&&<FinancialPanel financials={c.financials} history panelId={`${id}-money-panel`} labelledBy={compact?`${id}-money-tab`:undefined}/>}
  </Box>
 </Box>;
}
