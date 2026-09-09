/* Run with Node; Playwright is optional via NODE_PATH for offline browser checks. */
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const {performance}=require('node:perf_hooks');
const portal=path.resolve(__dirname,'../01_GUIDES_AND_INDEXES/PORTAL');
const logic=require('./portal_ui/portal_logic.js');
const data=JSON.parse(fs.readFileSync(path.join(portal,'assets/portal-data.js'),'utf8').replace(/^window.ARM_PORTAL_DATA=/,'').replace(/;\s*$/,''));
const start=performance.now(),engine=logic.prepare(data.items);
console.log('Engine preparation:',Math.round(performance.now()-start),'ms');
assert(engine.study('timer').length>0);
assert(engine.study('digitSum').some(r=>r.item.question));
assert.equal(engine.search('zzzznotfound').length,0);
for(const query of ['timer','LED','20230918','digitSum','stack argument','LPC_TIM0->MR0']){
  const expected=data.items.filter(i=>logic.matchesFilters(i,{sourceClass:'Maintained'})&&logic.score(i,query)>0).map(i=>i.id).sort();
  const actual=engine.search(query,{sourceClass:'Maintained'}).filter(r=>data.items.includes(r.item)).map(r=>r.item.id).sort();
  assert.deepEqual(actual,expected,query);
}
if(process.argv.includes('--browser'))(async()=>{
  const browser=await require('playwright').chromium.launch({headless:true,channel:process.env.ARM_TEST_BROWSER || "chrome"});
  try{
    const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
    for(const route of ['search.html','exams/index.html','api/index.html','asm/index.html','algorithms/index.html','algorithms/basic-exam-algorithms.html']){
      await page.goto(pathToFileURL(path.join(portal,route)).href);
      assert.equal(await page.evaluate(()=>!!window.ARM_PORTAL_DATA),false,route+' loaded corpus before a query');
      console.log(route,await page.evaluate(()=>Math.round(performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd)),'ms to ready');
    }
    await page.locator('a[href="checked-array-sum.html"]').click();
    await page.waitForURL('**/algorithms/checked-array-sum.html');
    assert(await page.locator('pre code').count()>0,'Restored algorithm must display its code');
    await page.goto(pathToFileURL(path.join(portal,'search.html')).href);
    await page.locator('[name=q]').fill('timer');
    await page.locator('[name=q]').press('Enter');
    await page.locator('[name=q]').fill('');
    await page.locator('[name=q]').press('Enter');
    await page.waitForFunction(()=>!!window.ARM_PORTAL_DATA,{},{timeout:60000});
    assert.equal(await page.locator('.search-result').count(),0,'Cleared query must not render stale results');
    await page.locator('[name=q]').fill('timer');
    await page.waitForFunction(()=>document.querySelectorAll('.search-result').length>0,{},{timeout:60000});
    assert.equal(await page.locator('.search-result').count(),10);
    await page.getByRole('button',{name:'Show more results',exact:true}).click();
    await page.waitForFunction(()=>document.querySelectorAll('.search-result').length===20);
    await page.locator('[name=q]').fill('zzzznotfound');
    await page.waitForFunction(()=>document.querySelector('[data-search-count]').textContent.startsWith('0 study'),{},{timeout:60000});
    await page.locator('[name=q]').fill('digitSum');
    await page.waitForFunction(()=>document.querySelector('.search-result')?.textContent.includes('digit'),{},{timeout:60000});
    await page.getByRole('button',{name:'Search all source material',exact:true}).click();
    await page.waitForFunction(()=>document.querySelector('[data-search-count]').textContent.includes('source result'));
    for(const [route,selector] of [['exams/index.html','input[data-filter]'],['api/index.html','[data-api-nav-search]'],['asm/index.html','#asm-filter']]){
      await page.goto(pathToFileURL(path.join(portal,route)).href);
      await page.locator(selector).first().fill('timer');
      await page.waitForFunction(()=>!!window.ARM_PORTAL_DATA,{},{timeout:60000});
      await page.waitForFunction(()=>![...document.querySelectorAll('[role=status],#asm-count')].some(e=>e.textContent==='Searching…'),{},{timeout:60000});
    }
    await page.goto(pathToFileURL(path.join(portal,'search.html')).href+'?q=digitSum');
    await page.waitForFunction(()=>document.querySelectorAll('.search-result').length>0,{},{timeout:60000});
    assert.deepEqual(errors,[]);console.log('PASS: offline startup, search, pagination, no matches, source scope and section filters');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
else console.log('PASS: search matches direct scoring, including punctuation');

