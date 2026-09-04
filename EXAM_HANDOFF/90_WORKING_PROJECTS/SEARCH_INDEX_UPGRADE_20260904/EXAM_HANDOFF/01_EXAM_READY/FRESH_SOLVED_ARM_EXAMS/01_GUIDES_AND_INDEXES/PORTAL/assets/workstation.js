/* Courses and an offline exam checklist. Nothing is sent to a server. */
(()=>{
  'use strict';
  const api=window.ARM_WORKSTATION_STATE;
  if(!api)return;
  const key='arm-workstation-progress-v1';
  let state=api.empty(),storageOK=true;
  try{const raw=localStorage.getItem(key);if(raw)state=api.validate(JSON.parse(raw));}catch(_){storageOK=false;}
  const status=message=>document.querySelectorAll('[data-storage-status]').forEach(el=>{el.textContent=message;});
  function persist(){
    try{localStorage.setItem(key,JSON.stringify(state));storageOK=true;}
    catch(_){storageOK=false;}
    status(storageOK?'Progress saved in this browser. Export it before moving the folder or changing computers.':'Browser storage is unavailable. This page still works; export progress before leaving.');
  }
  function progress(){
    document.querySelectorAll('[data-lesson-complete]').forEach(box=>{box.checked=state.completed.includes(box.dataset.lessonComplete);});
    document.querySelectorAll('[data-completion-mark]').forEach(el=>{el.textContent=state.completed.includes(el.dataset.completionMark)?' · Completed':'';});
    const entries=[...document.querySelectorAll('[data-course-entry]')];
    document.querySelectorAll('[data-course-progress]').forEach(el=>{el.textContent=entries.filter(x=>state.completed.includes(x.dataset.courseEntry)).length+' of '+entries.length+' lesson checkpoints completed';});
  }
  const guide=document.querySelector('[data-exam-guide]');
  function showExam(focus=false){
    if(!guide)return;
    if(focus)guide.querySelector('[data-exam-sitting]').open=state.exam.step===0;
    const steps=[...guide.querySelectorAll('[data-exam-step]')];
    steps.forEach((el,i)=>{el.hidden=!state.exam.full&&i!==state.exam.step;});
    guide.querySelectorAll('[data-go-step]').forEach(el=>{
      if(Number(el.dataset.goStep)===state.exam.step)el.setAttribute('aria-current','step');else el.removeAttribute('aria-current');
    });
    guide.querySelectorAll('[data-exam-check]').forEach(el=>{el.checked=state.exam.checks.includes(el.dataset.examCheck);});
    guide.querySelector('[data-exam-all]').textContent=state.exam.full?'Show one step at a time':'Show full checklist';
    guide.querySelector('[data-exam-status]').textContent='Step '+(state.exam.step+1)+' of '+steps.length+' · '+state.exam.checks.length+' checklist items checked. You may skip or revisit any step.';
    guide.querySelectorAll('[data-exam-prev]').forEach(el=>{el.disabled=state.exam.step===0&&!state.exam.full;});
    guide.querySelectorAll('[data-exam-next]').forEach(el=>{el.disabled=state.exam.step===steps.length-1&&!state.exam.full;});
    const b=api.budget(state.exam.fields.duration);
    guide.querySelector('[data-time-budget]').textContent=b?'Suggested budget only: '+b.setup+' min read/setup · '+b.implement+' min implementation · '+b.test+' min testing · '+b.submit+' min final submission. Adjust to the actual paper.':'Optional budgets are suggestions, not course rules. Enter a valid duration if useful.';
    const order=state.exam.fields.order;
    guide.querySelector('[data-order-guidance]').textContent=order==='board'?'Your choice: board first. Prove one input/output action with the exact-interface stub, then replace it and retest real values.':order==='assembly'?'Your choice: assembly first. Prove a small real case and ABI preservation, then connect the board.':'Choose an order after reading both questions; both routes still require real integration and testing.';
    if(focus)steps[state.exam.step].querySelector('h2').focus();
  }
  function restore(){
    progress();
    if(guide)guide.querySelector('[data-exam-sitting]').open=state.exam.step===0;
    if(guide)guide.querySelectorAll('[data-exam-field]').forEach(el=>{el.value=state.exam.fields[el.dataset.examField]||'';});
    showExam();
    status(storageOK?'Progress stays in this browser; export it before moving the package.':'Storage could not be read. Use export/import to carry this session.');
  }
  document.querySelectorAll('[data-lesson-complete]').forEach(el=>el.addEventListener('change',()=>{
    state.completed=state.completed.filter(v=>v!==el.dataset.lessonComplete);
    if(el.checked)state.completed.push(el.dataset.lessonComplete);
    persist();progress();
  }));
  function move(step){
    state.exam.step=Math.max(0,Math.min(api.steps.length-1,step));
    state.exam.full=false;persist();showExam(true);
    try{history.pushState(null,'','#step-'+api.steps[state.exam.step]);}catch(_){}
  }
  if(guide){
    guide.querySelectorAll('[data-go-step]').forEach(el=>el.addEventListener('click',event=>{event.preventDefault();move(Number(el.dataset.goStep));}));
    guide.querySelectorAll('[data-exam-prev]').forEach(el=>el.addEventListener('click',()=>move(Number(el.closest('[data-exam-step]').dataset.examStep)-1)));
    guide.querySelectorAll('[data-exam-next]').forEach(el=>el.addEventListener('click',()=>move(Number(el.closest('[data-exam-step]').dataset.examStep)+1)));
    guide.querySelector('[data-exam-all]').addEventListener('click',()=>{state.exam.full=!state.exam.full;persist();showExam();});
    guide.querySelectorAll('[data-exam-field]').forEach(el=>el.addEventListener('input',()=>{
      if(el.dataset.examField==='duration'&&el.value!==''&&!el.checkValidity())return;
      state.exam.fields[el.dataset.examField]=el.value;persist();showExam();
    }));
    guide.querySelectorAll('[data-exam-check]').forEach(el=>el.addEventListener('change',()=>{
      state.exam.checks=state.exam.checks.filter(v=>v!==el.dataset.examCheck);
      if(el.checked)state.exam.checks.push(el.dataset.examCheck);
      persist();showExam();
    }));
    guide.querySelector('[data-exam-reset]').addEventListener('click',()=>{
      if(!window.confirm('Reset this exam session and notes? Course progress will be kept. Export first if you need a copy.'))return;
      state.exam=api.empty().exam;persist();restore();
      try{history.replaceState(null,'',location.pathname+location.search);}catch(_){}
    });
    const hash=()=>{
      const index=api.steps.indexOf(location.hash.replace('#step-',''));
      if(index>=0){state.exam.step=index;state.exam.full=false;showExam();}
    };
    window.addEventListener('popstate',hash);window.addEventListener('hashchange',hash);hash();
  }
  document.querySelectorAll('[data-progress-export]').forEach(el=>el.addEventListener('click',()=>{
    try{
      const blob=new Blob([JSON.stringify(api.validate(state),null,2)],{type:'application/json'});
      const url=URL.createObjectURL(blob),a=document.createElement('a');
      a.href=url;a.download='arm-study-exam-progress.json';document.body.append(a);a.click();a.remove();
      setTimeout(()=>URL.revokeObjectURL(url),1000);
      status('Progress export requested. Keep that file for another browser, computer, or moved folder.');
    }catch(_){status('Export could not start in this browser. Keep this page open and record essential notes manually.');}
  }));
  document.querySelectorAll('[data-progress-import]').forEach(el=>el.addEventListener('change',async()=>{
    try{
      const file=el.files&&el.files[0];if(!file)return;
      if(file.size>100000)throw Error('The progress file is too large.');
      const next=api.validate(JSON.parse(await file.text()));
      if(!window.confirm('Replace saved course progress and exam notes with this imported progress?'))return;
      state=next;persist();restore();
    }catch(error){status('Import rejected: '+error.message+' Existing progress was kept.');}
    finally{el.value='';}
  }));
  restore();
})();
