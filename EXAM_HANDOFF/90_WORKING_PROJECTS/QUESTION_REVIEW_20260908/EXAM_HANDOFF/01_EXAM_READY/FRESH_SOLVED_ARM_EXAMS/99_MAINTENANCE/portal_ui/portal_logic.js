/* One offline engine for global and scoped searches. */
(function(host,factory){const logic=factory();if(typeof module==='object'&&module.exports)module.exports=logic;else host.ARM_PORTAL_LOGIC=logic;})(typeof window==='object'?window:this,function(){
  'use strict';
  const norm=v=>String(v||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').trim();
  const equivalent=v=>norm(v).replace(/\binterrupt handlers?\b|\binterrupt service routines?\b|\birq\b/g,'isr').replace(/\b(?:fifth|5th|stack) arguments?\b/g,'stackarg').replace(/\bdebouncing\b/g,'debounce').replace(/\bquestion\s+(\d+)\b/g,'q$1').replace(/\barm\s+(\d)\b/g,'arm$1').replace(/\b(20\d{2})[-/]([01]\d)[-/]([0-3]\d)\b/g,'$1$2$3');
  const words=v=>equivalent(v).split(/\s+/).filter(Boolean);
  const names=v=>String(v||'').replace(/([a-z])([A-Z])/g,'$1 $2').replace(/_/g,' ');
  function languageMatches(value,requested){let a=(Array.isArray(value)?value:[value]).flatMap(v=>norm(v).split(/[,|]/)).map(v=>v.trim());if(a.includes('both')||a.includes('c and assembly'))a=['c','assembly'];return !requested||(norm(requested)==='both'?a.includes('c')&&a.includes('assembly'):a.includes(norm(requested)));}
  function componentMatches(value,requested){const w=norm(requested),a=(Array.isArray(value)?value:[value]).map(norm);if(!w)return true;if(w==='timer')return a.some(v=>/^timer(?:[0-3]|\b)/.test(v)||v==='multi-timer');if(w==='buttons')return a.some(v=>/^(buttons?|eint)(?:\b|[0-2])/.test(v));return a.some(v=>v===w||v.startsWith(w+' '));}
  function fields(item,body=equivalent(item.text||item.summary)){const title=equivalent(item.title),heading=equivalent(item.heading),aliases=equivalent([...(item.aliases||[]),names(item.title),...(item.functions||[]).map(names),item.examId,item.date,item.question].join(' ')),topics=equivalent([...(item.topics||[]),...(item.components||[]),...(item.architecture||[])].join(' ')),functions=(item.functions||[]).map(equivalent);return {title,heading,aliases,topics,body,functions,hay:[title,heading,aliases,topics,body].join(' ')};}
  function rank(item,f,query,matched=false,q=equivalent(query),tokens=words(query),bodyMatches=null){if(!q)return 1;if(!matched&&!tokens.every(w=>f.hay.includes(w)))return 0;let bodyMatch;if(bodyMatches){if(!bodyMatches.has(f.body))bodyMatches.set(f.body,f.body.includes(q));bodyMatch=bodyMatches.get(f.body);}else bodyMatch=f.body.includes(q);let n=f.title===q?10000:f.title.startsWith(q)?1500:f.title.includes(q)?900:0;
    if(f.functions.includes(q))n+=String(item.id).startsWith('question-')?9000:String(item.id).startsWith('exam-')?7000:bodyMatch?7500:0;if(item.examId&&q===equivalent(item.date))n+=String(item.id).startsWith('exam-')?14000:String(item.id).startsWith('question-')?11000:3000;if(f.heading===q)n+=1200;else if(f.heading.includes(q))n+=550;if(f.aliases.includes(q))n+=450;if(f.topics.includes(q))n+=600;if(bodyMatch)n+=100;
    tokens.forEach(w=>{if(f.title.includes(w))n+=45;if(f.heading.includes(w))n+=30;if(f.aliases.includes(w))n+=25;if(f.topics.includes(w))n+=180;});
    if(item.question&&tokens.includes(norm(item.question)))n+=200;
    if(item.contentRole==='Supporting guidance')n=Math.min(n,25);if(item.contentRole==='Filename only')n=Math.min(n,80);
    return n+({Maintained:15,Original:5,Historical:0}[item.sourceClass]||0)+1;
  }
  function score(item,query){return rank(item,fields(item),query);}
  function matchesFilters(item,filters){return Object.entries(filters||{}).every(([key,value])=>{if(!value)return true;if(key==='languages')return languageMatches(item.languages,value);if(key==='components')return componentMatches(item.components,value);return Array.isArray(item[key])?item[key].some(v=>norm(v)===norm(value)):norm(item[key])===norm(value);});}
  function distanceOne(a,b){let i=0,j=0,e=0;while(i<a.length&&j<b.length){if(a[i]===b[j]){i++;j++;continue;}if(++e>1)return false;if(a.length>=b.length)i++;if(b.length>=a.length)j++;}return e+(a.length-i)+(b.length-j)===1;}
  function prepare(input){
    const fieldCache=new WeakMap(),bodies=new Map();
    function cachedFields(item){let f=fieldCache.get(item);if(!f){const text=item.text||item.summary||'';if(!bodies.has(text))bodies.set(text,equivalent(text));f=fields(item,bodies.get(text));fieldCache.set(item,f);}return f;}
    // Duplicate sources inherit content only. Their own tags, class, and routes remain searchable.
    let items, prepared, vocabulary;
    const index=new Map();
    function prepareSources(){
    if(prepared)return;
    items=input.flatMap(i=>[i,...(i.alternateSources||[]).filter(a=>a.id).map(a=>({...a,text:i.text,code:i.code,documentRoute:!/[#]|\.(?:pdf|html?)(?:$|[?#])/i.test(i.route)&&!/[#]|\.(?:pdf|html?)(?:$|[?#])/i.test(a.route)?i.route:a.route,alternateSources:[{title:i.title,route:i.route,sourceClass:i.sourceClass}]}))]);
    prepared=items.map(cachedFields);
    prepared.forEach((f,i)=>{for(const word of new Set(f.hay.match(/[a-z0-9_]+/g)||[])){if(!index.has(word))index.set(word,[]);index.get(word).push(i);}});
    vocabulary=[...index.keys()];
    }
    function search(query,filters={}){prepareSources();const q=equivalent(query),tokens=words(query);let candidates=null;
      for(const token of tokens){
        const set=new Set(),fragment=(token.match(/[a-z0-9_]+/g)||[]).sort((a,b)=>b.length-a.length)[0];
        if(fragment){for(const word of vocabulary)if(word.includes(fragment))for(const i of index.get(word))set.add(i);if(fragment!==token)for(const i of set)if(!prepared[i].hay.includes(token))set.delete(i);}
        else prepared.forEach((f,i)=>{if(f.hay.includes(token))set.add(i);});
        candidates=candidates===null?set:new Set([...candidates].filter(i=>set.has(i)));if(!candidates.size)break;
      }
      const bodyMatches=new Map();
      const indices=candidates===null?items.map((_,i)=>i):[...candidates];
      return indices.filter(i=>(tokens.length||filters.sourceClass||filters.materialType||filters.track||!String(items[i].id).startsWith('text-'))&&matchesFilters(items[i],filters)).map(i=>({item:items[i],rank:rank(items[i],prepared[i],query,true,q,tokens,bodyMatches)})).filter(x=>x.rank>0).sort((a,b)=>b.rank-a.rank||a.item.title.localeCompare(b.item.title)||a.item.route.localeCompare(b.item.route));
    }
    function scoped(query,filters={}){const map=new Map();for(const result of search(query,filters)){for(const route of new Set([result.item.route,result.item.route.split('#')[0],...(result.item.scopeRoutes||[])])){if(!map.has(route))map.set(route,[]);map.get(route).push(result);}}return map;}
    function suggestions(query){prepareSources();const q=norm(query);if(!/^[a-z_][a-z0-9_]{3,60}$/.test(q))return [];return vocabulary.filter(v=>v!==q&&Math.abs(v.length-q.length)<=1&&distanceOne(q,v)).slice(0,5);}
    const catalog=new Map(input.filter(i=>!String(i.id).startsWith('text-')&&i.sourceClass==='Maintained'&&!['Source references','Original material'].includes(i.kind)).map(i=>[i.id,i]));
    function study(query,filters={}){
      const pages=new Map();
      const question=words(query).find(w=>/^q\d+$/.test(w));
      const direct=[...catalog.values()].filter(item=>matchesFilters(item,filters)&&(!question||norm(item.question)===question)).map(item=>({item,rank:rank(item,cachedFields(item),query),match:item})).filter(result=>result.rank>0);
      const candidates=direct.length?direct:search(query,filters);
      for(const result of candidates){
        if(['Supporting guidance','Filename only'].includes(result.item.contentRole))continue;
        const parent=catalog.get(result.item.parentId)||catalog.get(result.item.id);
        if(!parent||(question&&norm(parent.question)!==question))continue;
        const directRank=matchesFilters(parent,filters)?rank(parent,cachedFields(parent),query):0;
        // Page metadata leads; a passing mention in its content cannot displace it.
        const candidate={item:{...parent,route:directRank?parent.route:result.item.route},rank:directRank||Math.min(result.rank,400),match:directRank?parent:result.item};
        if(!pages.has(parent.id)||candidate.rank>pages.get(parent.id).rank)pages.set(parent.id,candidate);
      }
      const matches=[...pages.values()].sort((a,b)=>b.rank-a.rank||a.item.title.localeCompare(b.item.title));
      const questions=new Set(matches.filter(r=>r.item.question).map(r=>r.item.examId));
      const byTitle=new Map(),output=[];
      for(const result of matches){
        const item=result.item;
        // Date searches keep their paper overview; topic searches lead to the question.
        if(item.materialType==='Exam overview'&&questions.has(item.examId)&&!filters.materialType&&result.rank<10000)continue;
        const title=['Algorithms','Solution Patterns'].includes(item.kind)?norm(item.title):item.id;
        if(byTitle.has(title))byTitle.get(title).related.push(item);
        else{result.related=[];byTitle.set(title,result);output.push(result);}
      }
      return output;
    }
    return {search,study,scoped,suggestions};
  }
  function excerpt(item,query){const text=String(item.text||item.summary||'').replace(/\s+/g,' ');let at=-1;for(const token of norm(query).split(/\s+/).filter(Boolean)){at=norm(text).indexOf(token);if(at>=0)break;}const start=Math.max(0,at-70),end=Math.min(text.length,start+250);return (start?'…':'')+text.slice(start,end)+(end<text.length?'…':'');}
  return Object.freeze({norm,words,languageMatches,componentMatches,score,prepare,excerpt,distanceOne,matchesFilters});
});
