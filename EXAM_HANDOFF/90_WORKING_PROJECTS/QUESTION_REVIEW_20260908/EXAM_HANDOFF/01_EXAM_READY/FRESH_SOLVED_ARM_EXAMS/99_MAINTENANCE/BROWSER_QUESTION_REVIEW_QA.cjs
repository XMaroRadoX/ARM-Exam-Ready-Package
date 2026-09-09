/* Exercise the reviewed guide directly through file URLs, without a web server. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/marwa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../../..'),portal=path.join(root,'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL');
const reviews=JSON.parse(fs.readFileSync(path.join(__dirname,'QUESTION_REVIEWS.json'),'utf8'));
const out=path.join(__dirname,'.question-ui-qa');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const errors=[],external=[];let checks=0;
 try {
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(!/^(file|data|blob):/.test(r.url()))external.push(r.url());});
  const check=(value,message)=>{assert(value,message);checks++;};
  for(const [qid,r] of Object.entries(reviews)){
   await page.goto(pathToFileURL(path.join(portal,'exams',qid.toLowerCase().replaceAll('_','-')+'.html')).href);
   for(const title of ['Exact contract','Solution reasoning','Worked trace','Code explanation','Relevant mistakes','Validation evidence for this answer'])check(await page.getByRole('heading',{name:title,exact:true}).count()===1,qid+' '+title);
   check(await page.locator('a[href*=".pdf#page="]').count()>0,qid+' original PDF link');
   check(await page.locator('pre code').count()>=1,qid+' complete code');
   check(await page.locator('a.raw-link').count()>=1,qid+' download');
   if(qid==='2025-01-29_ARM1-Q1')await page.screenshot({path:path.join(out,'affine-desktop.png')});
  }
  await page.goto(pathToFileURL(path.join(portal,'exams','2024-09-16-q1.html')).href);
  check(await page.getByRole('heading',{name:'Known correctness limitation',exact:true}).count()===1,'Kruskal warning visible');
  await page.screenshot({path:path.join(out,'kruskal-limitation.png')});
  await page.setViewportSize({width:390,height:844});
  await page.goto(pathToFileURL(path.join(portal,'exams','2025-01-29-arm1-q2.html')).href);
  check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile page fits viewport');
  await page.screenshot({path:path.join(out,'affine-mobile.png')});
  await page.setViewportSize({width:1440,height:1000});
  await page.goto(pathToFileURL(path.join(portal,'search.html')).href+'?q=bitwiseAffineTransformation');
  await page.locator('.search-result').first().waitFor();
  check((await page.locator('.search-result h3 a').first().getAttribute('href')).includes('2025-01-29-arm1-q1.html'),'Affine search points to reviewed Q1');
  await page.locator('.search-result h3 a').first().click();
  await page.getByRole('heading',{name:'Exact contract',exact:true}).waitFor();
  check(await page.getByText('R0=A, R1=b, R2=c',{exact:false}).count()>0,'Search navigation reaches corrected register contract');
  const raw=page.locator('a.raw-link').first(),link=await raw.getAttribute('href');
  const target=new URL(link,page.url());
  check(target.protocol==='file:','Download stays local');
  check(fs.readFileSync(require('node:url').fileURLToPath(target),'utf8').includes('bitwiseAffineTransformation'),'Download is complete assembly');
  await page.goto(pathToFileURL(path.join(portal,'exams','index.html')).href);
  await page.locator('[data-filter="text"]').fill('digitSum');
  await page.waitForFunction(()=>document.querySelector('[data-results-note]').textContent.startsWith('1 of'));
  check(await page.locator('[data-filter-item]:visible').count()===1,'Exam scope selects one paper');
  check((await page.locator('[data-filter-item]:visible [data-scope-match] a').getAttribute('href')).includes('2023-09-18-q1.html'),'Exam scope links the matching question');
  await page.locator('[data-filter="text"]').press('Tab');
  await page.waitForFunction(()=>location.search.includes('f-text=digitSum'));
  await page.locator('[data-filter="year"]').selectOption('2026');
  check(await page.locator('[data-filter-item]:visible').count()===0,'Exam filters combine');
  await page.goBack();await page.waitForFunction(()=>document.querySelector('[data-filter="year"]').value===''&&document.querySelector('[data-results-note]').textContent.startsWith('1 of'));
  check(await page.locator('[data-filter-item]:visible').count()===1,'Back restores exam filter state');
  await page.setViewportSize({width:390,height:844});
  await page.goto(pathToFileURL(path.join(portal,'search.html')).href+'?q=digitSum');
  await page.locator('.search-result').first().waitFor();
  check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile search fits viewport');
  await page.goto(pathToFileURL(path.join(portal,'search.html')).href+'?q=unmatched_question_identifier_91823');
  await page.locator('.empty-state').waitFor();check(await page.locator('.empty-state').count()===1,'Empty search state');
  check(errors.length===0,'No page JavaScript errors: '+errors.join(';'));
  check(external.length===0,'No external network requests: '+external.join(';'));
  fs.writeFileSync(path.join(__dirname,'QUESTION_PORTAL_RESULTS.json'),JSON.stringify({status:'PASS',questionPages:48,checks,fileUrls:true,externalRequests:external.length,javaScriptErrors:errors.length,viewports:[1440,390]},null,2)+'\n');
  console.log(JSON.stringify({status:'PASS',questions:48,checks,externalRequests:external.length}));
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
