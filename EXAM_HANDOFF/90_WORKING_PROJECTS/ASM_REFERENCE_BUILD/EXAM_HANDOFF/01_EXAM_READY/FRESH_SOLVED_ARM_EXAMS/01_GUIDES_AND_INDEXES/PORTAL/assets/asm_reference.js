(() => {
  'use strict';
  const input=document.querySelector('#asm-filter');
  if(!input) return;
  const category=document.querySelector('#asm-category');
  const entries=[...document.querySelectorAll('[data-asm-entry]')];
  const groups=[...document.querySelectorAll('[data-asm-group]')];
  const count=document.querySelector('#asm-count');
  function filter(){
    const terms=input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    // Keep filtered results close to the controls on narrow screens.
    document.querySelector('.asm-index').hidden=terms.length>0 || !!category.value;
    for(const e of entries) e.hidden=!!((category.value && e.dataset.category!==category.value) || !terms.every(t=>e.dataset.search.includes(t)));
    for(const g of groups) g.hidden=![...g.querySelectorAll('[data-asm-entry]')].some(e=>!e.hidden);
    const n=entries.filter(e=>!e.hidden).length;
    count.textContent=n ? `${n} of ${entries.length} entries shown` : 'No matches. Try a mnemonic, a shorter phrase, or clear the category.';
  }
  function clear(){input.value='';category.value='';filter();}
  function reveal(){
    let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch{return;}
    if(target && target.closest('[data-asm-entry], [data-asm-group]')){clear();target.scrollIntoView();}
  }
  input.addEventListener('input',filter);category.addEventListener('change',filter);
  document.querySelector('#asm-clear').addEventListener('click',()=>{clear();input.focus();});
  document.querySelector('#asm-print').addEventListener('click',()=>window.print());
  window.addEventListener('hashchange',reveal);
  // Clicking the current anchor again still reveals an entry hidden by a filter.
  document.querySelectorAll('.asm-index a,.asm-categories a').forEach(a=>a.addEventListener('click',()=>clear()));
  filter();reveal();
})();
