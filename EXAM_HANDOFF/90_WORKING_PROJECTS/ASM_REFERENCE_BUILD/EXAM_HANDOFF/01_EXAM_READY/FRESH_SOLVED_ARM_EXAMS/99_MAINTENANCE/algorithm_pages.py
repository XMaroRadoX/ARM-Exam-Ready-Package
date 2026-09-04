"""Algorithm teaching-page rendering, independent of the portal theme."""
import html,re,subprocess
from pathlib import Path
from functools import lru_cache
def esc(s):return html.escape(str(s))
@lru_cache(maxsize=512)
def readable_c(code):
    binary=Path('C:/Program Files/LLVM/bin/clang-format.exe')
    if not binary.exists():return code
    p=subprocess.run([str(binary),'-style={BasedOnStyle: LLVM, IndentWidth: 2, ColumnLimit: 88}'],
                     input=code,text=True,capture_output=True,check=True)
    return p.stdout
def argument_rows(prototype):
    rows=[]
    for m in re.finditer(r'([A-Za-z_]\w*)\s*\(([^()]*)\)',prototype):
        fn,params=m.groups()
        if fn in ('struct','if'):continue
        word=0
        for param in params.split(','):
            param=param.strip()
            if param in ('','void'):continue
            width=2 if '*' not in param and re.search(r'\b(?:u?int64_t|long long)\b',param) else 1
            if width==2 and word%2:word+=1
            if word<4 and word+width>4:word=4
            location=(':'.join('R'+str(i) for i in range(word,word+width)) if word<4
                      else '[entry SP'+('+'+str((word-4)*4) if word>4 else '')+']'+(' and next word' if width==2 else ''))
            rows.append((fn,param,location));word+=width
    return rows
def body(data,c_code,asm_code,fixture,c_path,asm_path,test_path,dest,details,href):
    prototype=str(data.get('prototype',''))
    abi=argument_rows(prototype)
    abi_table='<table><thead><tr><th>Function</th><th>Argument</th><th>Entry location</th></tr></thead><tbody>'+''.join(
        f'<tr><td><code>{esc(fn)}</code></td><td><code>{esc(param)}</code></td><td><code>{esc(loc)}</code></td></tr>' for fn,param,loc in abi)+'</tbody></table>'
    steps=[re.sub(r'^\d+[.)]\s*','',s.strip()) for s in str(data.get('procedure') or data.get('method','')).splitlines() if s.strip()]
    method='<ol>'+''.join('<li>'+esc(x)+'</li>' for x in steps)+'</ol>'
    focus=data.get('focus_entry','')
    focus_html=('<p><strong>Routine for this variation:</strong> <code>'+esc(focus)+'</code>. The downloadable file also includes its related helpers and variants.</p>') if focus else ''
    family=esc(data['family']);history=esc(data.get('history','Possible variation'))
    source_note=('This page shares its source implementation with related variants; it is not an additional independent implementation.' if data.get('shared_source') else '')
    test_html=details('Show exact expected-output tests',fixture,test_path,dest,'C')
    return f'''<section class="section-block"><dl class="fact-grid"><div class="fact"><dt>Family</dt><dd>{family}</dd></div><div class="fact"><dt>Exam history</dt><dd>{history}</dd></div><div class="fact"><dt>Complexity</dt><dd>{esc(data.get('complexity','See loop bounds below.'))}</dd></div></dl>{focus_html}<p>{esc(source_note)}</p></section>
<section class="section-block"><h2>Problem and contract</h2><p>{esc(data.get('contract',''))}</p><h3>C interface</h3><pre><code>{esc(prototype)}</code></pre><h3>Register map</h3>{abi_table}<p>Stack locations above are measured at function entry. Add the bytes pushed or reserved by the prologue before loading a later argument. A word result returns in R0; a 64-bit integer returns low word in R0 and high word in R1. Modified R4–R11 registers must be restored, and SP must retain eight-byte alignment at a call.</p></section>
<section class="section-block"><h2>How to solve it</h2>{method}<h3>Worked trace</h3><p>{esc(data.get('trace',''))}</p></section>
<section class="section-block"><h2>Complete ARM assembly</h2>{details('Show complete ARM implementation',asm_code,asm_path,dest,'Assembly',True)}<h2>Matching C</h2>{details('Show readable C reference',c_code,c_path,dest,'C')}</section>
<section class="section-block"><h2>Expected results and boundary tests</h2><p>The test fixture below contains concrete inputs and expected outputs. It is separate from the algorithm implementation. Use the same cases when stepping through the assembly.</p>{test_html}<h3>Adapting it in an exam</h3><ul><li>Keep the declared element width and signed comparisons together when changing the input type.</li><li>Distinguish a returned value, an index, a count and a status flag before changing the calling C code.</li><li>Check the stated storage, overlap, arithmetic and recursion limits before using a larger example.</li><li>For a nested BL call, preserve live arguments and the return address as shown in the implementation.</li></ul></section>'''
