/* Portable progress data, intentionally independent of DOM/storage availability. */
(function(host,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else host.ARM_WORKSTATION_STATE=api;})(typeof window==='object'?window:this,function(){
  'use strict';
  const steps=['confirm','prepare','read','order','contract','implement','test','submit','preserve'];
  const lengths=[3,3,3,3,4,4,5,4,3];
  const allowedChecks=new Set(steps.flatMap((s,i)=>Array.from({length:lengths[i]},(_,j)=>s+'-'+j)));
  const fieldNames=['materials','duration','template','destination','order','notes'];
  const empty=()=>({version:1,completed:[],exam:{step:0,full:false,fields:{},checks:[]}});
  function validate(value){
    if(!value||value.version!==1||!Array.isArray(value.completed)||!value.exam||typeof value.exam!=='object')throw Error('This is not a supported progress file.');
    const result=empty();
    result.completed=[...new Set(value.completed.filter(v=>typeof v==='string'&&/^(c|arm|board|project|practice)-[a-z0-9-]{1,60}$/.test(v)))].slice(0,200);
    const exam=value.exam;
    if(!Number.isInteger(exam.step)||exam.step<0||exam.step>=steps.length)throw Error('Invalid exam step.');
    result.exam.step=exam.step;result.exam.full=exam.full===true;
    if(!Array.isArray(exam.checks))throw Error('Invalid checklist data.');
    result.exam.checks=[...new Set(exam.checks.filter(v=>allowedChecks.has(v)))];
    for(const key of fieldNames){
      const raw=exam.fields&&Object.prototype.hasOwnProperty.call(exam.fields,key)?exam.fields[key]:'';
      if(typeof raw!=='string')throw Error('Invalid sitting field.');
      if(raw.length>(key==='notes'?20000:500))throw Error('A saved field is too long.');
      if(key==='duration'&&raw!==''&&(!/^\d+$/.test(raw)||Number(raw)<1||Number(raw)>1440))throw Error('Duration must be 1 to 1440 minutes, or blank.');
      if(key==='order'&&!['','assembly','board'].includes(raw))throw Error('Invalid implementation order.');
      result.exam.fields[key]=raw;
    }
    return result;
  }
  function budget(minutes){
    const n=Number(minutes);
    if(!Number.isFinite(n)||n<1||n>1440)return null;
    const setup=Math.max(1,Math.round(n*.1)),test=Math.max(1,Math.round(n*.15)),submit=Math.max(1,Math.round(n*.1));
    if(setup+test+submit>=n)return null;
    return {setup,implement:n-setup-test-submit,test,submit};
  }
  return Object.freeze({empty,validate,budget,steps});
});
