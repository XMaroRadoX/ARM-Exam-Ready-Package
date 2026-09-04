/* Shared offline search engine: precomputed fields, no network dependencies. */
(function(host,factory){
  const logic=factory();
  if(typeof module==='object'&&module.exports)module.exports=logic;else host.ARM_PORTAL_LOGIC=logic;
})(typeof window==='object'?window:this,function(){
  'use strict';
  const norm=v=>String(v||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').trim();
  const equivalent=v=>norm(v).replace(/\binterrupt handlers?\b|\binterrupt service routines?\b|\birq\b/g,'isr')
    .replace(/\b(?:fifth|5th|stack) arguments?\b/g,'stackarg').replace(/\bdebouncing\b/g,'debounce');
  const words=v=>equivalent(v).split(/\s+/).filter(Boolean);
  function languageMatches(value,requested){
    let available=(Array.isArray(value)?value:[value]).flatMap(v=>norm(v).split(/[,|]/)).map(v=>v.trim());
    if(available.includes('both')||available.includes('c and assembly'))available=['c','assembly'];
    return !requested||(norm(requested)==='both'?available.includes('c')&&available.includes('assembly'):available.includes(norm(requested)));
  }
  function componentMatches(value,requested){
    const wanted=norm(requested),entries=(Array.isArray(value)?value:[value]).map(norm);
    if(!wanted)return true;
    if(wanted==='timer')return entries.some(v=>/^timer(?:[0-3]|\b)/.test(v)||v==='multi-timer');
    if(wanted==='buttons')return entries.some(v=>/^(buttons?|eint)(?:\b|[0-2])/.test(v));
    return entries.some(v=>v===wanted||v.startsWith(wanted+' '));
  }
  function fields(item){
    const title=equivalent(item.title),heading=equivalent(item.heading),aliases=equivalent((item.aliases||[]).join(' '));
    const topics=equivalent([...(item.topics||[]),...(item.components||[])].join(' ')),body=equivalent(item.text||item.summary);
    return {title,heading,aliases,topics,body,hay:[title,heading,aliases,topics,body].join(' ')};
  }
  function rank(item,f,query){
    const q=equivalent(query),tokens=words(query);
    if(!q)return 1;
    if(!tokens.every(w=>f.hay.includes(w)))return 0;
    let n=f.title===q?10000:f.title.startsWith(q)?1500:f.title.includes(q)?900:0;
    if(f.heading===q)n+=1200;else if(f.heading.includes(q))n+=550;
    if(f.aliases.includes(q))n+=450;
    if(f.topics.includes(q))n+=240;
    if(f.body.includes(q))n+=100;
    tokens.forEach(w=>{if(f.title.includes(w))n+=45;if(f.heading.includes(w))n+=30;if(f.aliases.includes(w))n+=25;});
    return n+({Maintained:15,Original:5,Historical:0}[item.sourceClass]||0)+1;
  }
  function score(item,query){return rank(item,fields(item),query);}
  function matchesFilters(item,filters){
    return Object.entries(filters||{}).every(([key,value])=>{
      if(!value)return true;
      if(key==='languages')return languageMatches(item.languages,value);
      if(key==='components')return componentMatches(item.components,value);
      return Array.isArray(item[key])?item[key].some(v=>norm(v)===norm(value)):norm(item[key])===norm(value);
    });
  }
  function distanceOne(a,b){
    let i=0,j=0,edits=0;
    while(i<a.length&&j<b.length){
      if(a[i]===b[j]){i++;j++;continue;}
      if(++edits>1)return false;
      if(a.length>=b.length)i++;
      if(b.length>=a.length)j++;
    }
    return edits+(a.length-i)+(b.length-j)===1;
  }
  function prepare(items){
    const prepared=items.map(fields),index=new Map();
    prepared.forEach((f,i)=>{
      for(const word of new Set(f.hay.match(/[a-z0-9_]+/g)||[])){
        if(!index.has(word))index.set(word,[]);index.get(word).push(i);
      }
    });
    const vocabulary=[...index.keys()];
    function search(query,filters={}){
      const tokens=words(query);let candidates=null;
      for(const token of tokens){
        const set=new Set();
        for(const word of vocabulary)if(word.includes(token))for(const i of index.get(word))set.add(i);
        if(!/^[a-z0-9_]+$/.test(token))prepared.forEach((f,i)=>{if(f.hay.includes(token))set.add(i);});
        candidates=candidates===null?set:new Set([...candidates].filter(i=>set.has(i)));
        if(!candidates.size)break;
      }
      const indexes=candidates===null?items.map((_,i)=>i):[...candidates];
      return indexes.filter(i=>(tokens.length||!String(items[i].id).startsWith('text-'))&&matchesFilters(items[i],filters))
        .map(i=>({item:items[i],rank:rank(items[i],prepared[i],query)})).filter(x=>x.rank>0)
        .sort((a,b)=>b.rank-a.rank||a.item.title.localeCompare(b.item.title)||a.item.route.localeCompare(b.item.route));
    }
    function suggestions(query){
      const q=norm(query);
      if(!/^[a-z_][a-z0-9_]{3,60}$/.test(q))return [];
      return vocabulary.filter(v=>v!==q&&Math.abs(v.length-q.length)<=1&&distanceOne(q,v)).slice(0,5);
    }
    return {search,suggestions};
  }
  function excerpt(item,query){
    const text=String(item.text||item.summary||'').replace(/\s+/g,' ');
    let at=-1;
    for(const token of norm(query).split(/\s+/).filter(Boolean)){at=norm(text).indexOf(token);if(at>=0)break;}
    const start=Math.max(0,at-70),end=Math.min(text.length,start+250);
    return (start?'…':'')+text.slice(start,end)+(end<text.length?'…':'');
  }
  return Object.freeze({norm,words,languageMatches,componentMatches,score,prepare,excerpt,distanceOne});
});
