export function companySubmissionReason({busy,started,choice,progress,options=[],companyActive=true}) {
 if(!companyActive)return 'Your company is withdrawn. Ask your teacher to restore it.';
 if(busy)return 'Saving. Please wait.';
 if(!started)return 'Start the year from Team QR before submitting a decision.';
 if(!choice)return 'Choose the option your company has agreed on.';
 const selected=options.find(option=>option.id===choice);
 if(selected?.unavailable)return selected.blocked_by?`This option has been blocked by the ${selected.blocked_by.toUpperCase()}. Choose another option.`:'Your company cannot afford this option. Choose an available option.';
 const missing=progress.active-progress.preferences;
 if(missing>0)return `Waiting for ${missing} ${missing===1?'teammate':'teammates'} to submit a private recommendation on their phone. The company can submit once everyone has recommended.`;
 return '';
}
export function recommendationReason({busy,active,closed,recommendation,choice,started=true,companyActive=true}) {
 if(!companyActive)return 'Your company is withdrawn. Ask your teacher to restore it.';
 if(!started&&!closed)return 'Waiting for the company laptop to start the year from Team QR.';
 if(busy)return 'Saving. Please wait.';
 if(!active)return 'Your teacher has marked your participation inactive.';
 if(recommendation)return 'Your recommendation is saved and cannot be changed.';
 if(closed)return 'The company decision is locked. Recommendations are closed for this year.';
 if(!choice)return 'Choose the option you recommend before submitting.';
 return '';
}
export function reflectionReason({busy,final,year,finalReady,phase,text,responsibility,companyActive=true}) {
 if(!companyActive)return 'Your company is withdrawn. Ask your teacher to restore it.';
 if(busy)return 'Saving. Please wait.';
 if(final)return 'Final results have been released. Reflections are locked.';
 if(String(year)==='10'&&finalReady)return 'The closing reflections are complete. Your response is saved.';
 if(!['event','checkpoint','final_checkpoint'].includes(phase))return 'Written reflections open after your company submits its decision.';
 if(!text.trim())return 'Write your reflection before submitting.';
 if(String(year)==='10'&&!responsibility.trim())return 'Answer both closing questions before submitting.';
 return '';
}
