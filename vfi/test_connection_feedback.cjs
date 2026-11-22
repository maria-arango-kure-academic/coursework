const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(__dirname+'/src.jsx','utf8');
const api=source.slice(source.indexOf('async function api('),source.indexOf('\nfunction link('));
const start=source.indexOf('function usePoll('),poll=source.slice(start,source.indexOf('\nfunction ',start+10));
function harness(){
 const state={values:[],effects:[],timer:null,requests:0,fail:true,error:'',cleared:false};
 const context=vm.createContext({token:'fictional',fetch:async()=>{state.requests++;if(state.fail)throw new TypeError('Failed to fetch');return {ok:true,status:200,json:async()=>({saved:true})};},useState:initial=>{const index=state.values.push(initial)-1;return [initial,value=>{state.values[index]=typeof value==='function'?value(state.values[index]):value;}];},useRef:value=>({current:value}),useEffect:callback=>state.effects.push(callback),setInterval:callback=>{state.timer=callback;return 1;},clearInterval:()=>{state.cleared=true;}});
 vm.runInContext(api+'\n'+poll,context);
 state.context=context;state.setError=value=>{state.error=typeof value==='function'?value(state.error):value;};return state;
}
async function flush(){await new Promise(resolve=>setImmediate(resolve));}
(async()=>{
 let state=harness();
 await assert.rejects(()=>state.context.api('/fictional/actions',{action:'preference'}),/Unable to confirm your submission/);
 assert.equal(state.requests,1,'Submission must never retry automatically.');
 state=harness();state.context.usePoll('/fictional',state.setError,'fictional');const stop=state.effects[0]();await flush();
 assert.match(state.error,/Reconnecting/);state.fail=false;await state.timer();
 assert.equal(state.error,'');assert.equal(state.values[1],'');assert.equal(state.values[0].saved,true);
 stop();const before=state.requests;await state.timer();assert.equal(state.requests,before);assert.equal(state.cleared,true);
 state=harness();state.context.usePoll('/fictional',state.setError,'fictional');state.effects[0]();await flush();
 state.error='An unrelated submission error';state.fail=false;await state.timer();assert.equal(state.error,'An unrelated submission error');
 process.stdout.write('Passed: recovery clears only the polling error; submission uncertainty remains visible; no automatic POST retry; cleanup stops polling.\n');
})().catch(error=>{process.stderr.write(error.stack+'\n');process.exitCode=1;});
