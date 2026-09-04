/* Native page content remains visible if JavaScript or storage is unavailable. */
(() => {
  const root=document.querySelector('[data-scenario-browser]');if(!root)return;
  const boxes=[...root.querySelectorAll('[data-required-peripheral]')];
  const query=root.querySelector('[data-scenario-query]');
  const group=root.querySelector('[data-scenario-group]');
  const cards=[...root.querySelectorAll('[data-scenario-card]')];
  const url=new URL(location.href);
  boxes.forEach(b=>{b.checked=url.searchParams.getAll('peripheral').includes(b.value);});
  query.value=url.searchParams.get('q')||'';group.value=url.searchParams.get('collection')||'';
  function update(save=true){
    const required=boxes.filter(b=>b.checked).map(b=>b.value);
    const words=query.value.toLowerCase().trim().split(/\s+/).filter(Boolean);let count=0;
    cards.forEach(card=>{
      const features=card.dataset.features.split('|');
      const shown=required.every(p=>features.includes(p))&&(!group.value||card.dataset.group===group.value)&&words.every(w=>card.textContent.toLowerCase().includes(w));
      card.hidden=!shown;if(shown)count++;
    });
    root.querySelectorAll('[data-scenario-section]').forEach(section=>{section.hidden=![...section.querySelectorAll('[data-scenario-card]')].some(c=>!c.hidden);});
    root.querySelector('[data-scenario-count]').textContent=`${count} complete scenarios match. Required peripherals must all be present.`;
    if(save){try{const u=new URL(location.href);u.search='';required.forEach(p=>u.searchParams.append('peripheral',p));if(query.value)u.searchParams.set('q',query.value);if(group.value)u.searchParams.set('collection',group.value);history.replaceState(null,'',u);}catch{}}
  }
  root.addEventListener('input',()=>update());root.addEventListener('change',()=>update());update(false);
})();
