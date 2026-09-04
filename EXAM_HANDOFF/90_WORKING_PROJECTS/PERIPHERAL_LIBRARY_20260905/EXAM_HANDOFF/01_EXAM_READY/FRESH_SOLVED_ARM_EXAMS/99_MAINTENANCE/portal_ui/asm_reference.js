(() => {
  'use strict';
  const input=document.querySelector('#asm-filter');
  if(!input) return;
  const category=document.querySelector('#asm-category');
  const entries=[...document.querySelectorAll('[data-asm-entry]')];
  const groups=[...document.querySelectorAll('[data-asm-group]')];
  const count=document.querySelector('#asm-count');
  const engine=window.ARM_PORTAL_DATA&&window.ARM_PORTAL_LOGIC ? window.ARM_PORTAL_LOGIC.prepare(window.ARM_PORTAL_DATA.items) : null;
  const searchUrl=new URL(document.querySelector('[data-search-shortcut]').href,location.href);
  const link=document.createElement('a');link.textContent='Search whole package';
  const linkRow=document.createElement('p');linkRow.append(link);count.after(linkRow);
  function save(){
    const url=new URL(location.href);url.searchParams.delete('asm-q');url.searchParams.delete('asm-category');
    if(input.value.trim())url.searchParams.set('asm-q',input.value.trim());if(category.value)url.searchParams.set('asm-category',category.value);
    try{if(url.href!==location.href)history.pushState(null,'',url.href);}catch(_){}
  }
  function restore(){const params=new URLSearchParams(location.search);input.value=params.get('asm-q')||'';category.value=params.get('asm-category')||'';}

  function filter(){
    const terms=input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    const matches=engine&&terms.length ? engine.scoped(input.value,{kind:'ASM Reference',topics:category.value}) : null;
    const whole=new URL(searchUrl);if(input.value.trim())whole.searchParams.set('q',input.value.trim());link.href=whole.href;
    // Keep filtered results close to the controls on narrow screens.
    document.querySelector('.asm-index').hidden=terms.length>0 || !!category.value;
    for(const e of entries) e.hidden=!!((category.value && e.dataset.category!==category.value) || !(matches ? matches.has('asm/index.html#'+e.querySelector('h3[id]').id) : terms.every(t=>e.dataset.search.includes(t))));
    for(const g of groups) g.hidden=![...g.querySelectorAll('[data-asm-entry]')].some(e=>!e.hidden);
    const n=entries.filter(e=>!e.hidden).length;
    count.textContent=n ? `${n} of ${entries.length} entries shown` : 'No matches. Try a mnemonic, a shorter phrase, or clear the category.';
  }
  function clear(){input.value='';category.value='';filter();}
  function reveal(){
    let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch{return;}
    if(target && target.closest('[data-asm-entry], [data-asm-group]')){clear();target.scrollIntoView();}
  }
  input.addEventListener('input',filter);input.addEventListener('change',()=>{save();filter();});category.addEventListener('change',()=>{save();filter();});window.addEventListener('popstate',()=>{restore();filter();});
  document.querySelector('#asm-clear').addEventListener('click',()=>{clear();save();input.focus();});
  document.querySelector('#asm-print').addEventListener('click',()=>window.print());
  window.addEventListener('hashchange',reveal);
  // Clicking the current anchor again still reveals an entry hidden by a filter.
  document.querySelectorAll('.asm-index a,.asm-categories a').forEach(a=>a.addEventListener('click',()=>clear()));
  restore();filter();reveal();
})();
