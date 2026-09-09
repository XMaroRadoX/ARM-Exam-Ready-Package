from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re,zipfile
root=Path.cwd();base=root/"01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS"
portal=base/"01_GUIDES_AND_INDEXES/PORTAL"
source=root/"03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source"
raw=base/"03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/exam-solutions"
class Page(HTMLParser):
 def __init__(s):super().__init__(convert_charrefs=True);s.links=[];s.ids=set();s.pre=False;s.blocks=[];s.current=[]
 def handle_starttag(s,tag,attrs):
  a=dict(attrs)
  if "id" in a:s.ids.add(a["id"])
  for key in ("href","src"):
   if key in a:s.links.append(a[key])
  if tag=="pre":s.pre=True;s.current=[]
 def handle_endtag(s,tag):
  if tag=="pre":s.pre=False;s.blocks.append("".join(s.current).strip())
 def handle_data(s,data):
  if s.pre:s.current.append(data)
issues=[];links=0;files=0
for q in ("Q1","Q2","Q3"):
 name="2025-07-01-arm1-"+q.lower()
 path=portal/"exams"/(name+".html")
 text=path.read_text(encoding="utf-8");page=Page();page.feed(text)
 for f in (source/q).iterdir():
  if f.suffix not in (".s",".c",".md"):continue
  assert f.read_text(encoding="utf-8")== (raw/name/f.name).read_text(encoding="utf-8"),f
  if f.suffix in (".s",".c"):
   assert f.read_text(encoding="utf-8").strip() in page.blocks,("Missing complete code block",f)
  files+=1
 assert "No code reference is available" not in text
 if q=="Q1":assert "Reset_Handler" in text and "STRB" in text
 if q=="Q2":assert "3000" in text and "TIMER0_IRQHandler" in text
 if q=="Q3":assert "Why use RIT?" in text and "33 seconds" in text and "10 ms" in text
 for url in page.links:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  p=(path.parent/unquote(u.path)).resolve() if u.path else path
  links+=1
  if not p.exists():issues.append([path.name,url])
  elif u.fragment and p.suffix==".html":
   pp=Page();pp.feed(p.read_text(encoding="utf-8"))
   if unquote(u.fragment) not in pp.ids:issues.append([path.name,url,"fragment"])
assert not issues,issues
project=base/"03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects/paper-e2025-07-01-a1"
assert (project/"Source/sample.c").read_text()==(source/"Q3/main.c").read_text()
assert (project/"Source/ASM_funct.s").read_text()==(source/"Q3/assembly.s").read_text()
with zipfile.ZipFile(project/"paper-e2025-07-01-a1.zip") as z:
 assert z.read("Source/sample.c").decode().replace("\r\n","\n")== (source/"Q3/main.c").read_text()
 assert z.read("Source/ASM_funct.s").decode().replace("\r\n","\n")== (source/"Q3/assembly.s").read_text()
mapping=json.loads((raw/"manifest.json").read_text(encoding="utf-8"))
selected=[q for q in mapping["questions"] if q["examId"]=="E2025-07-01-A1"]
assert [len(q["requiredFiles"]) for q in selected]==[1,3,4]
report=dict(status="PASS",complete_files=files,local_links_checked=links,complete_code_blocks=True,native_project_and_zip_match=True,question_required_files=[1,3,4],browser_preview="Unavailable: browser policy blocks local file URLs",physical_board="NOT_TESTED")
(base/"99_MAINTENANCE/LCG_20250701_PUBLICATION.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))


