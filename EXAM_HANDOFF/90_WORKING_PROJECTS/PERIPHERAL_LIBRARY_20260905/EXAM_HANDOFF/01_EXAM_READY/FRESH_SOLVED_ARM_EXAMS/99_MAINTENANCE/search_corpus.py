"""Deterministic offline corpus; originals and answer code are read only."""
from __future__ import annotations
import hashlib, html, json, re
from html.parser import HTMLParser
from urllib.parse import urlsplit
from search_metadata import FIELDS, date_aliases, enrich, unique

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip+=1
        if tag in ('p','pre','li','h1','h2','h3','td','br','summary'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style') and self.skip: self.skip-=1
    def handle_data(self, value):
        if not self.skip: self.parts.append(value)

def plain(value):
    parser=Text(); parser.feed(value)
    return re.sub(r'\s+', ' ', ' '.join(parser.parts)).strip()

def digest(value):
    return hashlib.sha256(re.sub(r'\s+', ' ', value).strip().encode()).hexdigest()[:20]

def build(context, items):
    root,portal=context['ROOT'],context['PORTAL']; search=portal/'search.html'; rel=context['rel']
    sources=enrich(context,items)
    canonical={urlsplit(i['route']).path:i for i in items}
    by_route={i['route']:i for i in items}
    output=[]; seen={}; inventory={}
    report=dict(indexedFiles=0,pdfPages=0,duplicates=0,unindexed=[],attachments=[],unmappedMaterial=[],
                excludedRoots=['90_WORKING_PROJECTS','backups','build artifacts','caches'])
    def add(record):
        text=record.get('text','').strip()
        if not text: return
        for field in ('aliases','topics','components','languages','relatedIds','scopeRoutes'): record.setdefault(field,[])
        record.setdefault('examHistory','Extra practice'); record.setdefault('track','General reference')
        record.setdefault('materialType','Source reference')
        record['id']='text-'+digest(record['route']+record.get('examId','')+record.get('question',''))
        record['summary']=text[:230]; record['alternateSources']=[]
        fingerprint=digest(text)
        if fingerprint not in seen:
            seen[fingerprint]=record; output.append(record); return
        original=seen[fingerprint]
        if not any(v['id']==record['id'] for v in [original]+original['alternateSources']):
            original['alternateSources'].append({k:v for k,v in record.items() if k not in {'text','code','alternateSources'}})
        report['duplicates']+=1
    for item in items:
        item.setdefault('sourceClass','Maintained'); item.setdefault('text','')
        item.setdefault('heading',item['title']); item.setdefault('alternateSources',[])
    for path in sorted(portal.rglob('*.html')):
        relative=path.relative_to(root).as_posix()
        if path.name in {'search.html','search-coverage.html'} or (path.name=='index.html' and path.parent.name!='asm'):
            inventory[relative]=dict(status='excluded',reason='Navigation or generated search report'); continue
        raw=path.read_text(encoding='utf-8')
        if 'data-compatibility-page' in raw:
            inventory[relative]=dict(status='excluded',reason='Compatibility link to canonical section'); continue
        body=raw.split('<div class="page-body">',1)[-1].split('</main>',1)[0]
        body=re.sub(r'<section data-exam-search-metadata.*?</section>', '', body, flags=re.S)
        meta=canonical.get(rel(path,search),{})
        title=meta.get('title') or plain(re.search(r'<h1[^>]*>(.*?)</h1>',raw,re.S)[1])
        # Single-page references need one complete entry record, not only the first code block.
        for article in re.findall(r'<article\b[^>]*data-asm-entry[^>]*>.*?</article>', body, re.S):
            anchor=re.search(r'<h3[^>]*id="([^"]+)"',article)
            if not anchor: continue
            target=rel(path,search,anchor[1]); entry=by_route.get(target,{})
            record={k:entry[k] for k in FIELDS if k in entry}
            record.update(title=entry.get('title',anchor[1]),heading=entry.get('title',anchor[1]),text=plain(article),code='',
                          route=target,sourcePath=relative,sourceClass='Maintained',kind='ASM Reference',
                          languages=['Assembly'],materialType='Assembly reference',parentId=entry.get('id',''),scopeRoutes=[target,rel(path,search)])
            add(record)
        body=re.sub(r'<article\b[^>]*data-asm-entry[^>]*>.*?</article>', '', body, flags=re.S)
        boundaries=[(0,'',title)]
        for a in re.finditer(r'<(?:h2|h3|div)\b[^>]*\bid="([^"]+)"[^>]*>',body):
            if a[0].startswith('<div') and not a[1].startswith('listing-'): continue
            heading='Code listing '+a[1].split('-')[1] if a[1].startswith('listing-') else plain(body[a.end():].split('</h',1)[0])
            boundaries.append((a.start(),a[1],heading))
        for i,(start,anchor,heading) in enumerate(boundaries):
            fragment=body[start:boundaries[i+1][0] if i+1<len(boundaries) else len(body)]
            text=plain(fragment)
            if len(text)<30: continue
            code='\n\n'.join(html.unescape(re.sub('<[^>]+>','',p)).strip() for p in re.findall(r'<pre\b[^>]*>(.*?)</pre>',fragment,re.S))
            warning=bool(re.search(r'common wrong|common mistakes|source status|related |handbook|why the important',heading,re.I))
            record={k:meta[k] for k in FIELDS if k in meta}
            record.update(title=title,heading=heading,text=text,code=code,route=rel(path,search,anchor),sourcePath=relative,
                          sourceClass='Maintained',kind=meta.get('kind','Guides'),parentId=meta.get('id',''),
                          contentRole='Supporting guidance' if warning else 'Solution' if code else 'Explanation')
            if code and str(meta.get('id','')).startswith('exam-'):
                record.update(sourceClass='Historical',materialType='Historical solution')
            add(record)
        inventory[relative]=dict(status='indexed',reason='Page sections')
    cache_path=context['MAINTENANCE']/'SEARCH_DOCUMENT_CACHE.json'
    cache=json.loads(cache_path.read_text(encoding='utf-8')) if cache_path.exists() else {}; new_cache={}
    from pypdf import PdfReader
    text_types={'.pdf','.md','.txt','.c','.h','.s','.html','.htm','.csv'}
    attachment_types={'.zip','.7z','.rar','.m4a','.mp3','.wav','.mp4','.png','.jpg','.jpeg','.gif','.bmp','.svg','.webp','.tga','.ico','.ppt','.pptx','.doc','.docx'}
    skip_parts={'objects','listings','.git','_python_packages','99_maintenance','assets'}
    for folder in ('01_EXAM_READY','02_ORIGINAL_MATERIALS','03_ADDITIONAL_STUDY_MATERIAL'):
        for path in sorted((root/folder).rglob('*')):
            if not path.is_file() or path.is_relative_to(portal): continue
            relative=path.relative_to(root).as_posix(); parts={p.lower() for p in path.relative_to(root).parts[:-1]}
            if parts&skip_parts or any(p.startswith('.') or 'backup' in p or p=='__pycache__' or p.startswith('cmsis') for p in parts):
                inventory[relative]=dict(status='excluded',reason='Maintenance, dependency, backup, cache, or build output'); continue
            suffix=path.suffix.lower()
            if suffix not in text_types|attachment_types:
                inventory[relative]=dict(status='excluded',reason='Project configuration, binary, or unsupported format'); continue
            classification='Original' if folder=='02_ORIGINAL_MATERIALS' else 'Maintained' if folder=='01_EXAM_READY' or '/01 - Learn/' in relative else 'Historical'
            mappings=sources.get(relative,[]); exam_source=relative.startswith('02_ORIGINAL_MATERIALS/Exams/')
            track='Architecture / theory' if '/Architectures/' in relative or 'mips' in path.name.lower() else 'ARM programming' if '/ARM/' in relative or mappings else 'General reference'
            base=dict(title=path.stem,heading=path.name,sourcePath=relative,sourceClass=classification,
                      kind='Past Exams' if exam_source else 'Original material' if suffix=='.pdf' else 'Source references',track=track,aliases=[path.name,path.stem],topics=[path.parent.name],
                      materialType='Original paper' if exam_source and suffix=='.pdf' else 'Source reference',
                      solutionStatus='No maintained solution mapping' if exam_source and not mappings else '')
            found=re.search(r'(20\d{2})[-_]?([01]\d)[-_]?([0-3]\d)',path.stem)
            if found:
                try:
                    value='-'.join(found.groups()); aliases=date_aliases(value)
                    base.update(date=value,year=value[:4]); base['aliases']+=aliases
                except ValueError: pass
            if exam_source and not mappings: report['unmappedMaterial'].append({'path':relative})
            if not mappings: mappings=[{}]
            data=path.read_bytes(); file_hash=hashlib.sha256(data).hexdigest()
            inventory[relative]=dict(status='indexed',reason='Full text',hash=file_hash)
            def emit(value,heading=None,page=None,code='',attachment=False):
                for mapping in mappings:
                    record={**base,**mapping,'heading':heading or path.name,'text':value,'code':code,
                            'route':rel(path,search)+(f'#page={page}' if page else '')}
                    record['aliases']=unique(base['aliases']+mapping.get('aliases',[]))
                    if attachment: record.update(materialType='Attachment (name only)',contentRole='Filename only')
                    add(record)
            if suffix in attachment_types:
                reason='Filename and description only; contents are not indexed'
                inventory[relative].update(status='metadata-only',reason=reason)
                report['attachments'].append({'path':relative,'reason':reason})
                emit(path.name+' · '+path.parent.name+' · '+reason,attachment=True)
            elif suffix=='.pdf':
                cached=cache.get(relative)
                if cached and cached.get('hash')==file_hash: pages,errors=cached['pages'],cached.get('errors',[])
                else:
                    pages=[]; errors=[]
                    try:
                        for index,page in enumerate(PdfReader(path).pages):
                            try: pages.append(page.extract_text() or '')
                            except Exception as exc: pages.append(''); errors.append(f'page {index+1}: {type(exc).__name__}')
                    except Exception as exc: errors.append(type(exc).__name__)
                new_cache[relative]={'hash':file_hash,'pages':pages,'errors':errors}
                if errors: report['unindexed'].append({'path':relative,'reason':'; '.join(errors)})
                for index,value in enumerate(pages):
                    value=re.sub(r'\s+',' ',value).strip()
                    if not value:
                        report['unindexed'].append({'path':relative,'page':index+1,'reason':'No extractable text; open the original page'})
                        emit(path.name+' · Page has no extractable text','Page '+str(index+1),index+1,attachment=True)
                    else: emit(value,'Page '+str(index+1),index+1); report['pdfPages']+=1
                if not pages:
                    inventory[relative].update(status='metadata-only',reason='PDF extraction failed'); emit(path.name+' · PDF extraction failed',attachment=True)
            else:
                value=data.decode('utf-8-sig',errors='replace')
                if suffix in {'.html','.htm'}: value=plain(value)
                code=value.strip() if suffix in {'.c','.h','.s'} else ''
                if code: base['languages']=['Assembly' if suffix=='.s' else 'C']
                if not value.strip():
                    inventory[relative].update(status='metadata-only',reason='Empty file'); emit(path.name+' · Empty file',attachment=True)
                else: emit(value,code=code)
    for name in ('README.md', 'START_HERE.html'):
        path=root/name
        if not path.exists(): continue
        if name.endswith('.html'):
            inventory[name]=dict(status='excluded',reason='Home navigation'); continue
        value=path.read_text(encoding='utf-8')
        add(dict(title='Package instructions',heading=name,text=value,code='',route=rel(path,search),sourcePath=name,sourceClass='Maintained',kind='Guides',materialType='Guide'))
        inventory[name]=dict(status='indexed',reason='Full text',hash=hashlib.sha256(path.read_bytes()).hexdigest())
    # These navigation/report pages are written after corpus collection on a full build.
    for name in ('search.html','search-coverage.html'):
        inventory[(portal/name).relative_to(root).as_posix()]=dict(status='excluded',reason='Navigation or generated search report')
    report['inventory']=[{'path':p,**v} for p,v in sorted(inventory.items())]
    report['indexedFiles']=sum(v['status']!='excluded' for v in inventory.values())
    report['sectionRecords']=len(output); report['catalogRecords']=len(items)
    report['reviewedExams']=sum(i['id'].startswith('exam-') for i in items)
    report['reviewedQuestions']=sum(i['id'].startswith('question-') for i in items)
    context['write'](cache_path,json.dumps(new_cache,ensure_ascii=False))
    context['write'](context['MAINTENANCE']/'SEARCH_COVERAGE.json',json.dumps(report,indent=2,ensure_ascii=False))
    items.extend(output)
    return report
