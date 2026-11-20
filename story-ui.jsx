import React from 'react';
import {Box,Typography} from '@mui/material';

const formats={email:'Email',memo:'Internal memo',chat:'Team conversation','test-log':'Test record','support-ticket':'Customer support record',contract:'Agreement extract',letter:'Letter',voice:'Audio message',bulletin:'Investigation bulletin',incident:'Event report',receipt:'Fee notice',subscription:'Subscription offer',report:'Report extract',complaint:'Complaint'};

// Case media occupies the existing reading surface. The transcript is always
// present, including when audio is unavailable or somebody prefers to read.
export function CaseMedia({document:d,level=2}){
 if(!d)return null;
 return <Box component="article" className={`case-document case-document-${d.kind}`} data-case-id={d.id} aria-label={`${formats[d.kind]||'Case document'}: ${d.title}`}>
  <Box className="case-document-source"><Typography component="p">{formats[d.kind]||'Case document'}</Typography><Typography component="p">{d.sender}</Typography></Box>
  <Typography component={`h${level}`} variant="h6">{d.title}</Typography>
  {d.audio&&<Box className="case-audio"><audio controls preload="none" src={d.audio} aria-label={`Listen: ${d.title}`}/><Typography className="sr-only">Message transcript</Typography></Box>}
  <Box className="case-document-body">{d.body.map((text,i)=><Typography component="p" className="case-line" key={i}>{text}</Typography>)}</Box>
  {d.rows&&<Box component="dl" className="case-document-terms">{d.rows.map(([label,value])=><Box key={label}><dt>{label}</dt><dd>{value}</dd></Box>)}</Box>}
  {d.follow_up?.map((text,i)=><Typography key={i} className="case-follow-up">{text}</Typography>)}
  {d.callback&&<Typography className="case-callback">{d.callback}</Typography>}
  <Typography className="case-document-notice">{d.audio?'Fictional case material · synthetic narration':'Fictional case material'}</Typography>
 </Box>;
}

export function StoryDocument({y,year,c}){
 return <Box component="section" className="company-situation" aria-label="This year's situation">
  {c.story?.brief?<CaseMedia document={c.story.brief}/>:<><Typography component="h2" variant="h6">The proposal</Typography><Typography>{y.story}</Typography></>}
  <Typography>{y.decision_scope}</Typography>
 </Box>;
}

export function PrivateMessage({year,role,children,document}){
 return <Box className="private-message" aria-label={`Private briefing for ${role}`}>
  {document?<CaseMedia document={document}/>:<><Typography component="h2" variant="subtitle2">Private briefing · Year {year}</Typography><Typography>{children}</Typography></>}
 </Box>;
}
