const {chromium}=require('C:/Users/marwa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');const path=require('node:path'),fs=require('node:fs'),assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const portal=path.resolve(__dirname,'../01_GUIDES_AND_INDEXES/PORTAL'),out=path.join(__dirname,'.scenario-qa');fs.mkdirSync(out,{recursive:true});
 let checks=0;const check=(ok,message)=>{assert(ok,message);checks++;};
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(portal,'patterns/index.html')).href);
  const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'SCENARIO_MANIFEST.json')));
  check(await page.locator('[data-scenario-card]').count()===manifest.length,'All projects discoverable');
  for(const f of ['Buttons','ADC','DAC'])await page.locator(`[data-required-peripheral][value="${f}"]`).check();
  const visible=page.locator('[data-scenario-card]:visible');check(await visible.count()>0,'Multi-peripheral matches');
  for(const tag of await visible.evaluateAll(nodes=>nodes.map(n=>n.dataset.features.split('|'))))check(['Buttons','ADC','DAC'].every(x=>tag.includes(x)),'AND filter');
  await page.reload();check(await page.locator('[data-required-peripheral]:checked').count()===3,'Filter URL restored');
  await page.screenshot({path:path.join(out,'combinations-desktop.png')});
  await page.locator('[data-scenario-query]').fill('no-such-scenario-xyz');check(await page.locator('[data-scenario-card]:visible').count()===0,'Empty search result');
  for(const name of ['patterns/task-reaction-rit.html','patterns/mix-led-buttons-joystick-timer-rit-systick-adc-dac.html','patterns/paper-lcd-maze.html','algorithms/selection-sort.html','patterns/signed-and-unsigned-array-sorting.html']){
   await page.goto(pathToFileURL(path.join(portal,name)).href);check(await page.locator('h1').count()===1,'One heading '+name);
   check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Desktop width '+name);
   const ids=await page.locator('[id]').evaluateAll(nodes=>nodes.map(n=>n.id));check(new Set(ids).size===ids.length,'Unique anchors '+name);
   if(name.includes('signed-and-unsigned')){check(await page.locator('[data-compatibility-page]').count()===1,'Bookmark compatibility');}
   else {check(await page.locator('.copy-code').count()>0,'Copy code available');await page.locator('.copy-code').first().click();}
   await page.setViewportSize({width:390,height:844});check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Narrow width '+name);
   if(name.includes('reaction'))await page.screenshot({path:path.join(out,'reaction-narrow.png')});
   await page.setViewportSize({width:1440,height:1000});
  }
  check(!errors.length,'No browser exceptions');
  const context=await browser.newContext({javaScriptEnabled:false});const offline=await context.newPage();
  await offline.goto(pathToFileURL(path.join(portal,'patterns/index.html')).href);check(await offline.locator('[data-scenario-card]:visible').count()===manifest.length,'All scenarios without scripts');await context.close();
  fs.writeFileSync(path.join(__dirname,'SCENARIO_BROWSER_RESULTS.json'),JSON.stringify({status:'PASS',checks,desktop:true,narrow:true,noJavaScript:true},null,2));console.log(checks,'browser checks passed');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
