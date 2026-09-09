"""Verify all published answers, explanations, paper links and evidence bindings."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json, re
from question_review import ROOT, GUIDES, read_reviews, current_sources

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.codes=[];self.links=[];self.code=None;self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='code' and attrs.get('class','').startswith('language-'):self.code=''
        if tag=='a' and attrs.get('href'):self.links.append(attrs['href'])
    def handle_data(self,text):
        if self.code is not None:self.code+=text
    def handle_endtag(self,tag):
        if tag=='code' and self.code is not None:self.codes.append(self.code);self.code=None

def main():
    reviews=read_reviews();portal=GUIDES/'PORTAL'
    raw=GUIDES.parent/'03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/exam-solutions'
    manifest=json.loads((raw/'manifest.json').read_text(encoding='utf-8'))
    assert len(reviews)==48 and {q['questionId'] for q in manifest['questions']}==set(reviews)
    paper_set=set();download_count=0
    headings=['Exact contract','Solution reasoning','Worked trace','Code explanation','Relevant mistakes','Validation evidence for this answer','Review findings and corrections']
    for qid,r in reviews.items():
        stem=qid.lower().replace('_','-');page=portal/'exams'/f'{stem}.html';text=page.read_text(encoding='utf-8');parsed=Page(text)
        assert all(h in text for h in headings),qid
        assert 'Initialization establishes one owner for every peripheral' not in text,qid
        assert 'Previously checked with the supplied platform' not in text,qid
        assert r['verification']['nativeBuild']['status']=='PASS',qid
        assert r['verification']['instructionExecution']['status']=='PASS',qid
        assert r['verification']['physicalBoard']['status']=='UNVERIFIED',qid
        expected=[]
        for source in current_sources(r):
            target=raw/stem/source.name
            a=source.read_text(encoding='utf-8').replace('\r\n','\n');b=target.read_text(encoding='utf-8').replace('\r\n','\n')
            assert a==b,(qid,'download differs',source)
            assert b in parsed.codes,(qid,'display differs',source)
            assert any((page.parent/unquote(urlsplit(link).path)).resolve()==target.resolve() for link in parsed.links),(qid,'download link absent',target)
            expected.append(target.relative_to(ROOT).as_posix());download_count+=1
        record=next(x for x in manifest['questions'] if x['questionId']==qid)
        assert set(record['requiredFiles'])==set(expected),(qid,'manifest files differ')
        original=(ROOT/r['paper']).resolve();paper_set.add(original)
        assert original.is_file(),qid
        assert any((page.parent/unquote(urlsplit(link).path)).resolve()==original and urlsplit(link).fragment==f'page={r["pages"][0]}' for link in parsed.links),(qid,'original paper link')
        for link in parsed.links:
            parts=urlsplit(link)
            if not parts.scheme and parts.path:assert (page.parent/unquote(parts.path)).exists(),(qid,link)
        if 'unresolved' in r['reviewStatus'].lower():assert 'Known correctness limitation' in text,qid
    assert len(paper_set)==23,len(paper_set)
    print(json.dumps({'questions':len(reviews),'originalPapers':len(paper_set),'completeDownloadsAndCodeBlocks':download_count,'status':'PASS'}))

if __name__=='__main__':main()
