/* Offline reference acceptance checks in a disposable browser context. */
const {chromium}=require('C:/Users/marwa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'../../..'),portal=path.join(root,'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL');
const out=path.join(__dirname,'.asm-reference-qa');fs.mkdirSync(out,{recursive:true});
const url=p=>pathToFileURL(path.join(portal,p)).href;
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage();
  const errors=[],external=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(!/^(file|data|blob):/.test(r.url()))external.push(r.url());});
  let checks=0;function check(v,m){assert(v,m);checks++;}
  await page.goto(pathToFileURL(path.join(root,'START_HERE.html')).href);
  const nav=await page.locator('.primary-nav a').allTextContents();check(nav.findIndex(s=>s==='ASM Reference')===nav.findIndex(s=>s==='API')+1,'Sidebar beside API');
  await page.locator('.reference-tile').filter({hasText:'ASM Reference'}).click();
  check(await page.locator('h1').count()===1,'One title');
  const all=await page.locator('[data-asm-entry]').count();check(all>70,'Complete reference');
  await page.screenshot({path:path.join(out,'reference-desktop.png')});
  await page.locator('#asm-filter').fill('fifth argument');check(await page.locator('#fifth-argument').isVisible(),'Plain language filter');
  await page.locator('#asm-filter').fill('unsigned less than');check(await page.locator('#blo').isVisible(),'Unsigned comparison phrase');
  await page.locator('#asm-filter').fill('BICLS');check(await page.locator('#and').isVisible(),'Observed conditional mnemonic');
  await page.locator('#asm-filter').fill('not-a-real-instruction');check(await page.locator('[data-asm-entry]:visible').count()===0,'No results');
  await page.evaluate(()=>{location.hash='ldr';});await page.locator('#ldr').waitFor();check(await page.locator('#ldr').isVisible(),'Anchor clears filter');
  await page.locator('#asm-category').selectOption('Arithmetic');check(await page.locator('[data-asm-entry]:visible').count()>5,'Category filter');
  await page.locator('#asm-filter').fill('carry');
  await page.emulateMedia({media:'print'});check(await page.locator('[data-asm-entry]:visible').count()===all,'Print restores all entries');
  check(!(await page.locator('#asm-filter').isVisible()),'Print hides controls');
  await page.screenshot({path:path.join(out,'reference-print.png')});await page.emulateMedia({media:'screen'});
  await page.locator('#asm-clear').click();await page.locator('#asm-filter').fill('LDRB');
  await page.screenshot({path:path.join(out,'reference-loads.png')});
  await page.setViewportSize({width:390,height:844});check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Narrow layout');
  await page.screenshot({path:path.join(out,'reference-mobile.png')});
  await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>document.documentElement.dataset.theme='dark');
  await page.screenshot({path:path.join(out,'reference-dark.png')});
  await page.goto(url('search.html')+'?q='+encodeURIComponent('fifth argument'));
  await page.locator('[data-search-results] a[href*="asm/index.html#fifth-argument"]').first().waitFor();check(true,'Global search finds stack argument entry');
  await page.goto(url('search.html')+'?q=UDIV');await page.locator('[data-search-results] a[href*="asm/index.html#udiv"]').first().waitFor();check(true,'Global mnemonic search');
  await page.goto(url('in-exam/index.html'));await page.getByRole('link',{name:'Open ASM Reference',exact:true}).click();check(page.url().includes('/asm/index.html'),'Exam shortcut');
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:1200,height:900}}),plain=await nojs.newPage();
  await plain.goto(url('asm/index.html'));check(await plain.locator('[data-asm-entry]:visible').count()===all,'No-JavaScript content');check(!(await plain.locator('#asm-filter').isVisible()),'No-JavaScript controls hidden');
  await plain.locator('.asm-index a').filter({hasText:/^PUSH$/}).click();check(await plain.locator('#push').isVisible(),'No-JavaScript anchor');
  check(errors.length===0,'No browser errors');check(external.length===0,'No external network requests');
  const report={checks,entries:all,browserErrors:errors,externalRequests:external,status:'PASS'};fs.writeFileSync(path.join(__dirname,'ASM_REFERENCE_BROWSER_RESULTS.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
