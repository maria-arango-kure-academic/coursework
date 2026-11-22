import {createTheme} from '@mui/material';

// Current interface.md: simulations use system fonts, small radii and washed selection states.
// FairPass keeps its explicitly requested light default and optional remembered dark mode.
export const palettes={
 light:{paper:'#f7faf2',surface:'#f7faf2',quiet:'#dcdfd8',ink:'#3a3b3a',title:'#041606',secondary:'#3a3b3a',line:'rgba(58,59,58,.12)',rule:'#7ca300',label:'#717271',selection:'rgba(209,247,141,.4)',selectionLine:'#1d3a09',primary:'#041606',onPrimary:'#f7faf2',hover:'#bdf520',onHover:'#041606',link:'#1d3a09'},
 dark:{paper:'#041606',surface:'#07210b',quiet:'#07210b',ink:'#f7faf2',title:'#dcdfd8',secondary:'#dcdfd8',line:'rgba(247,250,242,.12)',rule:'#aeaead',label:'#aeaead',selection:'rgba(29,58,9,.25)',selectionLine:'#7ca300',primary:'#f7faf2',onPrimary:'#041606',hover:'#bdf520',onHover:'#041606',link:'#bdf520'}
};
export const type={body:'1rem',support:'0.9375rem',section:'1.375rem'};
const fontStack='Arial, Helvetica, "Liberation Sans", sans-serif',labels=fontStack;

export function createFairPassTheme(dark){
 const c=palettes[dark?'dark':'light'];
 const focus={outline:`2px solid ${c.link}`,outlineOffset:2};
 const state='&:hover:not(.Mui-disabled), &.Mui-focusVisible:not(.Mui-disabled)';
 const semantic={main:c.ink,light:c.quiet,dark:c.ink,contrastText:c.paper};
 return createTheme({
  spacing:8,shape:{borderRadius:4},shadows:Array(25).fill('none'),
  transitions:{duration:{shortest:120,shorter:150,short:150,standard:150,complex:150,enteringScreen:150,leavingScreen:150}},
  palette:{mode:dark?'dark':'light',primary:{main:c.ink,contrastText:c.paper},background:{default:c.paper,paper:c.surface},text:{primary:c.ink,secondary:c.secondary,disabled:c.secondary},action:{disabled:c.secondary,disabledBackground:c.paper,disabledOpacity:1},divider:c.line,error:semantic,warning:semantic,info:semantic,success:semantic},
  typography:{
   fontFamily:fontStack,body1:{fontSize:type.body,fontWeight:400,lineHeight:1.5,letterSpacing:0},body2:{fontSize:'1rem',fontWeight:400,lineHeight:1.5,letterSpacing:0},
   h4:{color:c.title,fontFamily:fontStack,fontSize:'clamp(1.5rem, 3vw, 2rem)',fontWeight:700,lineHeight:1.1,letterSpacing:0},h5:{fontFamily:fontStack,fontSize:'2rem',fontWeight:700,lineHeight:1.2},h6:{color:c.title,fontFamily:fontStack,fontSize:type.section,fontWeight:700,lineHeight:1.25},
   subtitle2:{fontFamily:fontStack,fontSize:type.body,fontWeight:700,lineHeight:1.5},button:{fontFamily:fontStack,fontWeight:600,fontSize:'1rem',letterSpacing:'.04em',lineHeight:1.5},overline:{fontFamily:labels,fontWeight:600,fontSize:type.support,letterSpacing:'.06em',lineHeight:1.5,textTransform:'uppercase'}
  },
  components:{
   MuiCssBaseline:{styleOverrides:{body:{'--fairpass-bg':c.paper,'--fairpass-paper':c.paper,'--fairpass-surface':c.surface,'--fairpass-quiet':c.quiet,'--fairpass-line':c.line,'--fairpass-ink':c.ink,'--fairpass-secondary':c.secondary,'--fairpass-title':c.title,'--fairpass-rule':c.rule,'--fairpass-focus':c.link,'--fairpass-selection':c.selection,'--fairpass-selection-line':c.selectionLine,'--type-body':type.body,'--type-support':type.support,...Object.fromEntries([1,2,3,4,6,8,10,12,16].map(n=>['--space-'+n,n*4+'px']))}}},
   MuiTypography:{defaultProps:{variantMapping:{h1:'h1',h2:'h2',h3:'h3',h4:'h4',h5:'h5',h6:'p',subtitle1:'p',subtitle2:'p',body1:'p',body2:'p',inherit:'p'}}},
   MuiButtonBase:{styleOverrides:{root:{'&.Mui-focusVisible':focus}}},
   MuiButton:{defaultProps:{disableElevation:true},styleOverrides:{root:{textTransform:'uppercase',minHeight:44,minWidth:44,borderRadius:'0.25rem',padding:'8px 16px','&.Mui-disabled':{border:`1px solid ${c.line}`,backgroundColor:c.quiet,color:c.secondary},transition:'background-color 150ms ease, color 150ms ease, border-color 150ms ease'},outlined:{backgroundColor:c.surface,borderColor:c.ink,[state]:{backgroundColor:c.ink,color:c.paper,borderColor:c.ink}},text:{[state]:{backgroundColor:c.quiet,textDecoration:'underline',textUnderlineOffset:'.2em'}},contained:{backgroundColor:c.primary,color:c.onPrimary,border:`1px solid ${dark?c.primary:c.ink}`,[state]:{backgroundColor:c.hover,color:c.onHover,borderColor:dark?c.hover:c.primary}}}},
   MuiIconButton:{styleOverrides:{root:{minWidth:44,minHeight:44,borderRadius:'0.25rem',color:c.ink,[state]:{backgroundColor:c.ink,color:c.paper}}}},
   MuiCheckbox:{styleOverrides:{root:{minWidth:44,minHeight:44,color:c.ink,'&.Mui-checked':{color:c.ink}}}},
   MuiRadio:{styleOverrides:{root:{minWidth:44,minHeight:44,color:c.ink,'&.Mui-checked':{color:c.ink}}}},
   MuiTab:{styleOverrides:{root:{fontSize:'1rem',minHeight:48,minWidth:44,textTransform:'none',lineHeight:1.5,[state]:{backgroundColor:c.quiet,color:c.ink},'&.Mui-selected':{fontWeight:700,color:c.ink,backgroundColor:c.selection,boxShadow:`inset 0 0 0 1px ${c.selectionLine}`}}}},
   MuiTabScrollButton:{styleOverrides:{root:{width:44,minHeight:48,'&.Mui-disabled':{opacity:1,color:c.secondary},[state]:{backgroundColor:c.quiet}}}},
   MuiPaper:{styleOverrides:{root:{backgroundImage:'none',borderRadius:'0.25rem'}}},
   MuiOutlinedInput:{defaultProps:{notched:false},styleOverrides:{root:{backgroundColor:c.surface,borderRadius:'0.25rem','& .MuiOutlinedInput-notchedOutline':{borderColor:c.ink,borderWidth:1},'&:hover .MuiOutlinedInput-notchedOutline, &.Mui-focused .MuiOutlinedInput-notchedOutline, &.Mui-error .MuiOutlinedInput-notchedOutline':{borderColor:c.ink,borderWidth:2},'&.Mui-disabled .MuiOutlinedInput-notchedOutline':{borderColor:c.secondary}}}},
   MuiInputLabel:{defaultProps:{disableAnimation:true},styleOverrides:{root:{position:'static',transform:'none',maxWidth:'none',whiteSpace:'normal',overflow:'visible',marginBottom:8,lineHeight:1.5,color:c.label,fontFamily:labels,fontSize:type.support,fontWeight:600,letterSpacing:'.06em',textTransform:'uppercase','&.Mui-error, &.Mui-focused':{color:c.ink}},shrink:{transform:'none',maxWidth:'none'}}},
   MuiFormHelperText:{styleOverrides:{root:{margin:'8px 0 0',fontSize:type.support,lineHeight:1.5}}},
   MuiFormControlLabel:{styleOverrides:{label:{fontSize:'1rem',lineHeight:1.5}}},
   MuiTableCell:{styleOverrides:{root:{padding:16,fontSize:'1rem',lineHeight:1.6,verticalAlign:'top'},head:{fontFamily:labels,fontSize:type.support,fontWeight:600,lineHeight:1.5,letterSpacing:'.06em',textTransform:'uppercase'}}},
   MuiChip:{styleOverrides:{root:{borderRadius:'0.125rem',fontFamily:labels,fontSize:type.support,height:'auto',minHeight:32},label:{whiteSpace:'normal',padding:'4px 12px',lineHeight:1.5}}},
   MuiMenuItem:{styleOverrides:{root:{minHeight:44,whiteSpace:'normal',overflowWrap:'anywhere',lineHeight:1.5,'&.Mui-selected':{backgroundColor:c.selection,fontWeight:700,boxShadow:`inset 0 0 0 1px ${c.selectionLine}`},'&:hover':{backgroundColor:c.quiet}}}},
   MuiSelect:{styleOverrides:{select:{whiteSpace:'normal',overflowWrap:'anywhere',height:'auto',minHeight:24}},defaultProps:{MenuProps:{container:()=>document.activeElement?.closest('[role="dialog"]')||document.getElementById('main-content')||document.body}}},
   MuiPopover:{styleOverrides:{paper:{border:`1px solid ${c.ink}`}}},
   MuiDialog:{styleOverrides:{paper:{border:`1px solid ${c.ink}`,margin:16,maxHeight:'calc(100% - 32px)',width:'calc(100% - 32px)'}}},
   MuiDialogTitle:{styleOverrides:{root:{fontFamily:fontStack,fontWeight:700,fontSize:type.section,lineHeight:1.25,padding:24}}},
   MuiDialogContent:{styleOverrides:{root:{padding:24,'&:first-of-type':{paddingTop:24}}}},
   MuiDialogActions:{styleOverrides:{root:{padding:'16px 24px',gap:8,flexWrap:'wrap','& > :not(style) ~ :not(style)':{marginLeft:0}}}},
   MuiAccordion:{styleOverrides:{root:{background:c.paper,borderRadius:'0.25rem',border:`1px solid ${c.line}`,'&:before':{display:'none'}},heading:{margin:0}}},
   MuiAccordionSummary:{styleOverrides:{root:{minHeight:56,padding:'0 16px',backgroundColor:c.quiet,borderRadius:'0.25rem','&.Mui-expanded':{minHeight:56,borderBottom:`1px solid ${c.line}`},[state]:{backgroundColor:c.quiet,color:c.ink,boxShadow:`inset 0 0 0 1px ${c.ink}`}},content:{margin:'16px 0',paddingRight:16,'&.Mui-expanded':{margin:'16px 0'}},expandIconWrapper:{color:'inherit','&.Mui-expanded':{transform:'none'}}}},
   MuiAccordionDetails:{styleOverrides:{root:{display:'flex',flexDirection:'column',gap:16,padding:24,'& > .MuiStack-root':{paddingTop:0}}}},
   MuiStepIcon:{styleOverrides:{root:{color:c.secondary,'&.Mui-active, &.Mui-completed':{color:c.ink}},text:{fill:c.paper,fontSize:type.support,fontFamily:labels}}},
   MuiStepLabel:{styleOverrides:{iconContainer:{paddingRight:0},labelContainer:{height:0,margin:0}}},
   MuiStepConnector:{styleOverrides:{line:{borderTopWidth:1}}},
   MuiAlert:{styleOverrides:{root:{backgroundColor:c.paper,color:c.ink,border:`1px solid ${c.ink}`,borderRadius:'0.25rem',fontSize:'1rem',lineHeight:1.6},icon:{color:c.ink}}},
   MuiTooltip:{styleOverrides:{tooltip:{fontSize:type.support,backgroundColor:c.ink,color:c.paper,borderRadius:'0.25rem'}}}
  }
 });
}
