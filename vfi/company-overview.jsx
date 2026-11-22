import React from 'react';
import {Box,Paper,Typography,useMediaQuery} from '@mui/material';
import {euro} from './financial-ui';
import {CardPages} from './participant-ui';
export function CompanyOverview({c,content}){
 const compact=useMediaQuery('(max-width:48rem)'),overview=content.companyOverview,s=c.performance.state;
 return <CardPages className="company-overview-pages" label="Company introduction">
  <Paper component="section" variant="outlined" className="company-overview-panel company-history-panel" tabIndex={0} aria-label="Company history">
   <Typography component="h2" variant="h6">How it began</Typography>
   <Typography>{overview.history.replace('{company}',c.name)}</Typography>
   <Typography>{overview.business}</Typography>{overview.work&&<Typography>{overview.work}</Typography>}
  </Paper>
  <Paper component="section" variant="outlined" className="company-overview-panel company-today-panel" tabIndex={0} aria-label="Rollout division information">
   <Typography component="h2" variant="h6">The rollout division</Typography>
   <Box component="dl" className="company-facts">
    <Box><dt>Rollout team</dt><dd>{s.staff}</dd></Box>
    <Box><dt>{c.year===1?'Rollout venues':'Original rollout venues'}</dt><dd>{s.contracts}</dd></Box>
    <Box><dt>Cash available</dt><dd>{euro(c.financials.cash_now)}</dd></Box>
    <Box><dt>Debt</dt><dd>{euro(c.financials.debt_now)}</dd></Box>
   </Box>
   {s.new_partners>0&&<Typography>{s.new_partners} additional partnerships are recorded separately from your original venue clients.</Typography>}
  </Paper>
  {compact?overview.commitments.map(([title,description],index)=><Paper key={title} component="section" variant="outlined" className="company-overview-panel company-commitment-panel" tabIndex={0} aria-label={title}>
   <Typography component="h2" variant="h6">{title}</Typography>
   {index===0&&<Typography>{overview.commitmentsIntroduction}</Typography>}
   <Typography>{description}</Typography>
  </Paper>):(<Paper component="section" variant="outlined" className="company-overview-panel company-commitment-panel" tabIndex={0} aria-label="Company commitments">
   <Typography component="h2" variant="h6">Your commitments</Typography>
   <Typography>{overview.commitmentsIntroduction}</Typography>
   <Box component="dl" className="company-commitments">{overview.commitments.map(([title,description])=><Box key={title}><dt>{title}</dt><dd>{description}</dd></Box>)}</Box>
  </Paper>)}

 </CardPages>;
}
