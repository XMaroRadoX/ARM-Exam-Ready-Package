/* Offline controls. No network services or external runtime dependencies. */
(() => {
  'use strict';
  const {norm, words, languageMatches, componentMatches, score} = window.ARM_PORTAL_LOGIC;
  let sharedEngine;
  function getEngine() {
    if (!window.ARM_PORTAL_DATA || !window.ARM_PORTAL_LOGIC.prepare) return null;
    return sharedEngine || (sharedEngine = window.ARM_PORTAL_LOGIC.prepare(window.ARM_PORTAL_DATA.items));
  }
  function searchUrl() { return new URL(document.querySelector('[data-search-shortcut]').href, location.href); }
  function absoluteRoute(route) { return new URL(route, searchUrl()).href; }
  function wholePackageLink(container) {
    const p = document.createElement('p'), link = document.createElement('a');
    link.textContent = 'Search whole package'; p.append(link); container.append(p);
    return query => { const url = searchUrl(); url.search = ''; if (query.trim()) url.searchParams.set('q', query.trim()); link.href = url.href; };
  }
  function setUrl(values, keys, push = true) {
    const url = new URL(location.href);
    keys.forEach(key => { url.searchParams.delete(key); });
    Object.entries(values).forEach(([key, value]) => { if (value) url.searchParams.set(key, value); });
    if (url.href !== location.href) {
      try { history[push ? 'pushState' : 'replaceState'](null, '', url.href); }
      catch (_) { /* Some file viewers restrict History. Filtering still works. */ }
    }
  }
  function button(label, handler, className = 'subtle-button') {
    const el = document.createElement('button');
    el.type = 'button'; el.className = className; el.textContent = label;
    el.addEventListener('click', handler);
    return el;
  }
  function initTheme() {
    const el = document.querySelector('.theme-toggle');
    if (!el) return;
    const query = matchMedia('(prefers-color-scheme: dark)');
    const current = () => document.documentElement.dataset.theme || (query.matches ? 'dark' : 'light');
    const update = () => {
      el.textContent = current() === 'dark' ? 'Light theme' : 'Dark theme';
      el.setAttribute('aria-label', `Switch to ${current() === 'dark' ? 'light' : 'dark'} theme`);
    };
    el.addEventListener('click', () => {
      const next = current() === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem('arm-workstation-theme', next); } catch (_) { /* Keep session choice. */ }
      update();
    });
    query.addEventListener('change', update); update();
  }
  function initCode() {
    document.querySelectorAll('.copy-code').forEach(el => {
      el.addEventListener('click', async () => {
        const frame = el.closest('.code-frame'), pre = frame.querySelector('pre'), code = pre.querySelector('code') || pre;
        const status = frame.querySelector('.copy-status');
        try {
          if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
          await navigator.clipboard.writeText(code.textContent);
          status.textContent = 'Code copied.';
        } catch (_) {
          pre.focus();
          const selection = window.getSelection(), range = document.createRange();
          range.selectNodeContents(code); selection.removeAllRanges(); selection.addRange(range);
          status.textContent = 'Code selected. Press Ctrl+C (or Command+C) to copy.';
        }
      });
    });
  }
  function initLists() {
    document.querySelectorAll('[data-filter-scope]').forEach(scope => {
      const controls = [...scope.querySelectorAll('[data-filter]')], cards = [...scope.querySelectorAll('[data-filter-item]')];
      const note = scope.querySelector('[data-results-note]') || scope.appendChild(document.createElement('p'));
      note.setAttribute('role', 'status'); note.setAttribute('aria-live', 'polite');
      const engine = getEngine(), updateLink = engine ? wholePackageLink(scope) : () => {};
      const active = document.createElement('p'); active.className = 'active-filters';
      const empty = document.createElement('p'); empty.className = 'empty-state'; empty.textContent = 'No matching items. Clear a filter or try fewer words.'; empty.hidden = true;
      const keys = controls.map(c => 'f-' + c.dataset.filter);
      const restore = () => { const params = new URLSearchParams(location.search); controls.forEach(c => { c.value = params.get('f-' + c.dataset.filter) || ''; }); };
      const apply = () => {
        const query = controls.filter(c => c.tagName === 'INPUT').map(c => c.value).join(' ').trim();
        const filters = {};
        for (const control of controls.filter(c => c.tagName === 'SELECT')) {
          const key = ({language:'languages', component:'components', history:'examHistory', year:'year', variant:'variant'})[control.dataset.filter];
          if (key && control.value) filters[key] = control.value;
        }
        const matches = engine && query ? engine.scoped(query, filters) : null;
        let shown = 0;
        cards.forEach(card => {
          const route = card.dataset.searchRoute;
          const found = matches && route ? matches.get(route) || [] : null;
          const ok = controls.every(control => {
            const key = control.dataset.filter, wanted = norm(control.value);
            if (!wanted) return true;
            if (control.tagName === 'INPUT' && found) return found.length > 0;
            const value = card.dataset[key] || card.textContent;
            if (/language/i.test(key)) return languageMatches(value, wanted);
            if (/component/i.test(key)) return componentMatches(value.split(/[,|]/), wanted);
            return control.tagName === 'INPUT' ? words(wanted).every(w => norm(value).includes(w)) : norm(value).split(/\s*[,|]\s*/).includes(wanted) || norm(value).includes(wanted);
          });
          card.hidden = !ok; if (ok) shown++;
          let hint = card.querySelector('[data-scope-match]');
          if (!hint && engine) { hint = document.createElement('p'); hint.dataset.scopeMatch = ''; hint.className = 'scoped-match'; (card.querySelector('.card-body') || card).append(hint); }
          if (hint) {
            hint.replaceChildren(); hint.hidden = !(ok && query && found && found.length);
            if (!hint.hidden) { const result = found[0].item, a = document.createElement('a'); a.href = absoluteRoute(result.route); a.textContent = 'Match: ' + (result.question ? result.question + ' · ' : '') + (result.heading || result.title); hint.append(a); }
          }
        });
        note.textContent = `${shown} of ${cards.length} items`;
        active.textContent = controls.filter(c => c.value).map(c => c.tagName === 'SELECT' ? c.options[c.selectedIndex].text : c.value).join(' · ');
        active.hidden = !active.textContent; empty.hidden = shown !== 0; updateLink(query);
      };
      const save = () => { setUrl(Object.fromEntries(controls.map(c => ['f-' + c.dataset.filter, c.value])), keys); apply(); };
      const clear = button('Clear filters', () => { controls.forEach(c => { c.value = ''; }); save(); });
      const toolbar = scope.querySelector('.filter-bar') || scope;
      toolbar.append(clear); note.after(active); scope.append(empty);
      let timer;
      controls.forEach(c => { c.addEventListener(c.tagName === 'INPUT' ? 'input' : 'change', c.tagName === 'INPUT' ? () => { clearTimeout(timer); timer=setTimeout(apply,60); } : save); if (c.tagName === 'INPUT') c.addEventListener('change', save); });
      window.addEventListener('popstate', () => { clearTimeout(timer); restore(); apply(); }); restore(); apply();
    });
  }
  function initSearch() {
    const root=document.querySelector('[data-global-search]');
    if(!root)return;
    const form=root.querySelector('form'),input=root.querySelector('[name=q]'),results=root.querySelector('[data-search-results]');
    const count=root.querySelector('[data-search-count]'),controls=[...root.querySelectorAll('[data-search-filter]')];
    if(!window.ARM_PORTAL_DATA||!Array.isArray(window.ARM_PORTAL_DATA.items)){
      count.textContent='The search index could not be loaded. Browse the sections in the navigation.';return;
    }
    const engine=getEngine();
    const keys=['q',...controls.map(c=>c.dataset.searchFilter)];
    const active=document.createElement('p');active.className='active-filters';count.after(active);
    let limit=50,timer;
    const more=button('Show more results',()=>{limit+=50;render();});more.classList.add('load-more');results.after(more);
    function restore(){
      const params=new URLSearchParams(location.search);input.value=params.get('q')||'';
      controls.forEach(c=>{c.value=params.get(c.dataset.searchFilter)||'';});
    }
    function save(){setUrl(Object.fromEntries([['q',input.value.trim()],...controls.map(c=>[c.dataset.searchFilter,c.value])]),keys);}
    function highlight(el,text,query){
      const tokens=norm(query).split(/\s+/).filter(t=>t.length>1);
      const lowered=norm(text);
      let cursor=0;
      while(cursor<text.length){
        let at=-1,length=0;
        for(const token of tokens){
          const pos=lowered.indexOf(token,cursor);
          if(pos>=0&&(at<0||pos<at)){at=pos;length=token.length;}
        }
        if(at<0){el.append(document.createTextNode(text.slice(cursor)));break;}
        el.append(document.createTextNode(text.slice(cursor,at)));
        const mark=document.createElement('mark');mark.textContent=text.slice(at,at+length);el.append(mark);cursor=at+length;
      }
    }
    function row(result){
      const item=result.item,article=document.createElement('article');article.className='search-result';
      const h=document.createElement('h3'),a=document.createElement('a');a.href=item.route;
      a.textContent=item.title+(item.heading&&item.heading!==item.title?' — '+item.heading:'');h.append(a);
      const excerpt=document.createElement('p');highlight(excerpt,window.ARM_PORTAL_LOGIC.excerpt(item,input.value),input.value);
      const meta=document.createElement('p');meta.className='result-meta';
      meta.textContent=[item.sourceClass||'Maintained',item.materialType,item.date,item.variant,item.question,...(item.languages||[]),...(item.components||[]).slice(0,3),item.track,item.metadataScope,item.solutionStatus].filter(Boolean).join(' · ');
      article.append(h,excerpt,meta);
      if (item.paperRoute || (item.solutionRoutes || []).length) {
        const links = document.createElement('p'); links.className = 'result-links';
        for (const [label, route] of [...(item.paperRoute ? [['Original paper', item.paperRoute]] : []), ...(item.solutionRoutes || []).map(route => [(route.match(/-q(\d+)\//i) ? 'Q' + route.match(/-q(\d+)\//i)[1] + ' · ' : '') + (/\.s$/i.test(route) ? 'Assembly answer' : 'C answer'), route])]) {
          if (links.childNodes.length) links.append(document.createTextNode(' · '));
          const a=document.createElement('a');a.href=route;a.textContent=label;links.append(a);
        }
        article.append(links);
      }
      const others=[...(result.sections||[]),...(item.alternateSources||[])];
      if(others.length){
        const details=document.createElement('details'),summary=document.createElement('summary');
        summary.textContent='Other matched sections or source copies ('+others.length+')';details.append(summary);
        const list=document.createElement('ul');
        for(const other of others.slice(0,20)){
          const li=document.createElement('li'),link=document.createElement('a');link.href=other.route;
          link.textContent=(other.sourceClass?other.sourceClass+' · ':'')+(other.heading||other.title);li.append(link);list.append(li);
        }
        details.append(list);article.append(details);
      }
      return article;
    }
    function render(){
      const started=performance.now(),filters=Object.fromEntries(controls.map(c=>[c.dataset.searchFilter,c.value]));
      const raw=engine.search(input.value,filters),byPage=new Map();
      for(const result of raw){
        const item=result.item;
        const route=/\.pdf(?:#|$)/i.test(item.route)?item.route:item.route.split('#')[0];
        if(!byPage.has(route))byPage.set(route,{...result,sections:[]});
        else if(item.route!==byPage.get(route).item.route)byPage.get(route).sections.push(item);
      }
      const matches=[...byPage.values()];
      results.replaceChildren();
      count.textContent=matches.length+' result'+(matches.length===1?'':'s')+(matches.length>limit?' · showing '+limit:'');
      active.textContent=[input.value.trim(),...controls.filter(c=>c.value).map(c=>c.options[c.selectedIndex].text)].filter(Boolean).join(' · ');
      active.hidden=!active.textContent;more.hidden=matches.length<=limit;
      if(!matches.length){
        const empty=document.createElement('p');empty.className='empty-state';empty.textContent='No matches. Try fewer words or clear the filters.';results.append(empty);
        const suggestions=engine.suggestions(input.value);
        if(suggestions.length){
          const p=document.createElement('p');p.textContent='Did you mean: ';
          suggestions.forEach(word=>p.append(button(word,()=>{input.value=word;save();render();})));results.append(p);
        }
      }else{
        const bestCount=input.value.trim()?Math.min(3,matches.length):0;
        if(bestCount){
          const best=document.createElement('section');best.className='best-matches';
          const heading=document.createElement('h2');heading.textContent='Best matches';best.append(heading);
          matches.slice(0,bestCount).forEach(r=>best.append(row(r)));results.append(best);
        }
        const groups=new Map();
        matches.slice(bestCount,limit).forEach(result=>{
          const kind=result.item.kind;if(!groups.has(kind))groups.set(kind,[]);groups.get(kind).push(result);
        });
        for(const [kind,group] of groups){
          const section=document.createElement('section');section.className='search-group';
          const heading=document.createElement('h2');heading.textContent=kind;section.append(heading);
          group.forEach(r=>section.append(row(r)));results.append(section);
        }
      }
      root.dataset.lastSearchMs=(performance.now()-started).toFixed(1);
    }
    form.addEventListener('submit',event=>{event.preventDefault();clearTimeout(timer);limit=50;save();render();});
    input.addEventListener('input',()=>{clearTimeout(timer);limit=50;timer=setTimeout(render,60);});
    controls.forEach(c=>c.addEventListener('change',()=>{clearTimeout(timer);limit=50;save();render();}));
    root.querySelector('.filter-bar').append(button('Clear all',()=>{clearTimeout(timer);input.value='';controls.forEach(c=>{c.value='';});limit=50;save();render();input.focus();}));
    window.addEventListener('popstate',()=>{clearTimeout(timer);limit=50;restore();render();});
    restore();render();
  }
  function initApi() {
    document.querySelectorAll('[data-api-nav-search]').forEach(input => {
      const sidebar = input.closest('.api-sidebar'), entries = [...sidebar.querySelectorAll('[data-api-entry]')], groups = [...sidebar.querySelectorAll('[data-api-group]')];
      const count = sidebar.querySelector('[data-api-nav-count]'); count.setAttribute('role', 'status'); count.setAttribute('aria-live', 'polite');
      const engine = getEngine(), updateLink = engine ? wholePackageLink(sidebar) : () => {};
      const restore = () => { input.value = new URLSearchParams(location.search).get('api-q') || ''; };
      const apply = () => {
        const query = words(input.value), matches = engine && input.value.trim() ? engine.scoped(input.value,{kind:'API'}) : null;
        const urls = matches ? new Set([...matches.keys()].map(absoluteRoute)) : null;
        let shown = 0;
        entries.forEach(entry => { const a=entry.querySelector('a'); entry.hidden = urls ? !urls.has(new URL(a.href,location.href).href) : !query.every(word => norm(entry.textContent).includes(word)); if (!entry.hidden) shown++; });
        groups.forEach(group => { group.hidden = ![...group.querySelectorAll('[data-api-entry]')].some(entry => !entry.hidden); });
        count.textContent = `${shown} of ${entries.length} functions${shown ? '' : ' · try fewer words'}`; updateLink(input.value);
      };
      let timer; input.addEventListener('input', () => { clearTimeout(timer); timer=setTimeout(apply,60); });
      input.addEventListener('change', () => { setUrl({'api-q':input.value},['api-q']); apply(); });
      window.addEventListener('popstate', () => { clearTimeout(timer); restore(); apply(); }); restore(); apply();
    });
  }
  document.addEventListener('keydown', event => {
    if (event.key !== '/' || event.ctrlKey || event.metaKey || event.altKey || event.target.closest('input, textarea, select, [contenteditable=true]')) return;
    event.preventDefault();
    const input = document.querySelector('#home-search, [data-global-search] [name=q]');
    if (input) input.focus(); else document.querySelector('[data-search-shortcut]').click();
  });
  const init = () => {
    initTheme(); initCode(); initLists(); initSearch(); initApi();
    const nav = document.querySelector('.primary-nav'), current = nav && nav.querySelector('[aria-current=page]');
    if (current && nav.scrollWidth > nav.clientWidth) current.scrollIntoView({block:'nearest',inline:'center'});
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
