"""Offline full-text corpus builder. Original files are read, never modified."""
from __future__ import annotations
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ("script","style"): self.skip+=1
        if tag in ("p","pre","li","h1","h2","h3","td","br","summary"): self.parts.append("\n")
    def handle_endtag(self,tag):
        if tag in ("script","style") and self.skip: self.skip-=1
    def handle_data(self,value):
        if not self.skip: self.parts.append(value)

def plain(value):
    p=Text(); p.feed(value)
    return re.sub(r"\s+"," "," ".join(p.parts)).strip()

def digest(value):
    return hashlib.sha256(re.sub(r"\s+"," ",value).strip().encode()).hexdigest()[:20]

def build(context, items):
    root,portal=context["ROOT"],context["PORTAL"]
    search=portal/"search.html"
    rel=context["rel"]
    canonical={}
    for item in items:
        route=urlsplit(item["route"]).path
        canonical.setdefault(route,item)
    output=[]
    seen={}
    report={"indexedFiles":0,"pdfPages":0,"duplicates":0,"unindexed":[],"excludedRoots":["90_WORKING_PROJECTS","build artifacts","caches","binary files"]}
    def add(record):
        text=record.get("text","").strip()
        if not text:return
        # Exact code/text duplicates point to one maintained result, with other sources retained.
        fingerprint=digest(record.get("code") or text)
        alternate={"title":record["title"],"route":record["route"],"sourceClass":record["sourceClass"]}
        if fingerprint in seen:
            original=seen[fingerprint]
            priority={"Maintained":2,"Original":1,"Historical":0}
            if priority[record["sourceClass"]]>priority[original["sourceClass"]]:
                previous={"title":original["title"],"route":original["route"],"sourceClass":original["sourceClass"]}
                alternates=list(original["alternateSources"])
                original.update(record)
                original["id"]="text-"+digest(record["route"]+record["title"])
                original["summary"]=text[:230]
                original["alternateSources"]=alternates+[previous]
                report["duplicates"]+=1
                return
            if record["route"]!=original["route"] and alternate not in original["alternateSources"]:
                original["alternateSources"].append(alternate)
            report["duplicates"]+=1
            return
        record.setdefault("alternateSources",[])
        record.setdefault("relatedIds",[])
        record.setdefault("aliases",[])
        record.setdefault("topics",[])
        record.setdefault("components",[])
        record.setdefault("languages",[])
        record.setdefault("examHistory","Extra practice")
        record["id"]="text-"+digest(record["route"]+record["title"])
        record["summary"]=text[:230]
        seen[fingerprint]=record; output.append(record)

    # Keep existing catalog entries and enrich them; preserve their IDs and URL routes.
    for item in items:
        item.setdefault("sourceClass","Maintained")
        item.setdefault("text","")
        item.setdefault("heading",item["title"])
        item.setdefault("alternateSources",[])

    for path in sorted(portal.rglob("*.html")):
        if path.name=="search.html":continue
        raw=path.read_text(encoding="utf-8")
        body=raw.split('<div class="page-body">',1)[-1].split("</main>",1)[0]
        route=rel(path,search)
        meta=canonical.get(route,{})
        title=meta.get("title") or plain(re.search(r"<h1[^>]*>(.*?)</h1>",raw,re.S)[1])
        # The generated shell gives stable anchors to headings and code frames.
        anchors=list(re.finditer(r'<(?:h2|h3|div)\b[^>]*\bid="([^"]+)"[^>]*>',body))
        boundaries=[(0,"",title)]
        for a in anchors:
            if a[0].startswith("<div") and not a[1].startswith("listing-"):continue
            heading="Code listing "+a[1].split("-")[1] if a[1].startswith("listing-") else plain(body[a.end():].split("</h",1)[0])
            boundaries.append((a.start(),a[1],heading))
        for i,(start,anchor,heading) in enumerate(boundaries):
            end=boundaries[i+1][0] if i+1<len(boundaries) else len(body)
            fragment=body[start:end]
            text=plain(fragment)
            if len(text)<30:continue
            pre=re.search(r"<pre\b[^>]*>(.*?)</pre>",fragment,re.S)
            code=html.unescape(re.sub("<[^>]+>","",pre[1])).strip() if pre else ""
            if code: text=code
            add(dict(title=title,heading=heading,text=text,code=code,
                     route=rel(path,search,anchor),sourcePath=path.relative_to(root).as_posix(),
                     sourceClass="Maintained",kind=meta.get("kind","Guides"),
                     languages=meta.get("languages",[]),components=meta.get("components",[]),
                     topics=meta.get("topics",[]),aliases=meta.get("aliases",[]),
                     examHistory=meta.get("examHistory","Extra practice"),
                     parentId=meta.get("id","")))
        report["indexedFiles"]+=1

    cache_path=context["MAINTENANCE"]/"SEARCH_DOCUMENT_CACHE.json"
    cache=json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    new_cache={}
    from pypdf import PdfReader
    allowed={".pdf",".md",".txt",".c",".h",".s",".html",".htm"}
    skip_parts={"__pycache__","Objects","Listings",".git","_python_packages"}
    for folder in ("02_ORIGINAL_MATERIALS","03_ADDITIONAL_STUDY_MATERIAL"):
        for path in sorted((root/folder).rglob("*")):
            if not path.is_file() or any(p in skip_parts for p in path.parts):continue
            suffix=path.suffix.lower()
            if suffix not in allowed:continue
            relative=path.relative_to(root).as_posix()
            original=folder=="02_ORIGINAL_MATERIALS"
            classification="Original" if original else "Historical"
            if folder=="03_ADDITIONAL_STUDY_MATERIAL" and "01 - Learn/" in relative:
                classification="Maintained"
            data=path.read_bytes()
            file_hash=hashlib.sha256(data).hexdigest()
            if suffix==".pdf":
                cached=cache.get(relative)
                if cached and cached.get("hash")==file_hash:
                    pages=cached["pages"]; errors=cached.get("errors",[])
                else:
                    pages=[];errors=[]
                    try:
                        reader=PdfReader(path)
                        for index,page in enumerate(reader.pages):
                            try:
                                pages.append(page.extract_text() or "")
                            except Exception as exc:
                                pages.append("");errors.append(f"page {index+1}: {type(exc).__name__}")
                    except Exception as exc:errors.append(type(exc).__name__)
                new_cache[relative]={"hash":file_hash,"pages":pages,"errors":errors}
                if errors:report["unindexed"].append({"path":relative,"reason":"; ".join(errors)})
                for index,value in enumerate(pages):
                    value=re.sub(r"\s+"," ",value).strip()
                    if not value:
                        report["unindexed"].append({"path":relative,"page":index+1,"reason":"No extractable text; original page remains available"})
                        continue
                    add(dict(title=path.stem,heading=f"Page {index+1}",text=value,code="",
                             route=rel(path,search)+f"#page={index+1}",sourcePath=relative,
                             sourceClass=classification,kind="Original material",topics=[path.parent.name]))
                    report["pdfPages"]+=1
            else:
                value=data.decode("utf-8-sig",errors="replace")
                if suffix in (".html",".htm"):value=plain(value)
                # Raw code is indexed as a complete file, not a guessed executable fragment.
                code=value.strip() if suffix in (".c",".h",".s") else ""
                add(dict(title=path.stem,heading=path.name,text=value,code=code,
                         route=rel(path,search),sourcePath=relative,sourceClass=classification,
                         kind="Source references",languages=["Assembly" if suffix==".s" else "C"] if code else [],
                         topics=[path.parent.name]))
            report["indexedFiles"]+=1
    # Index current template declarations and instructions, but never build output.
    template=context["STARTING_TEMPLATE"]
    for path in sorted(template.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md",".h",".c",".s"}:continue
        if any(part in {"Objects","Listings","CMSIS_core"} for part in path.parts):continue
        value=path.read_text(encoding="utf-8-sig",errors="replace")
        add(dict(title=path.name,heading="Current starting template",text=value,code=value if path.suffix.lower() in {".h",".c",".s"} else "",
                 route=rel(path,search),sourcePath=path.relative_to(root).as_posix(),sourceClass="Maintained",
                 kind="Source references",languages=["Assembly" if path.suffix.lower()==".s" else "C"]))
    context["write"](cache_path,json.dumps(new_cache,ensure_ascii=False))
    report["sectionRecords"]=len(output);report["catalogRecords"]=len(items)
    context["write"](context["MAINTENANCE"]/"SEARCH_COVERAGE.json",json.dumps(report,indent=2,ensure_ascii=False))
    # Titles/metadata remain the original catalog. Full text uses section records.
    items.extend(output)
    return report
