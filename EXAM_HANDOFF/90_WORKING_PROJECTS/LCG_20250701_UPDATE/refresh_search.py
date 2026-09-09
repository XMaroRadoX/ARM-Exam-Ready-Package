from pathlib import Path
import sys,json,hashlib
root=Path.cwd();maint=root/"01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE"
sys.path.insert(0,str(maint))
import BUILD_STUDENT_PORTAL as b
from portal_presentation import install
from workstation_extensions import install as ext
from asm_reference import install as asm
from REFRESH_SEARCH import refresh
from scenario_library import historical_specs
stage=root/"90_WORKING_PROJECTS/LCG_20250701_UPDATE"
changed=[]
def write(path,text):
 path=Path(path)
 assert path.is_relative_to(root),path
 if path == b.ASSETS/"portal_logic.js":return
 old=path.read_bytes() if path.exists() else None
 if old is not None and old.decode("utf-8-sig").replace("\r\n","\n")==text.replace("\r\n","\n"):return
 backup=stage/"before"/path.relative_to(root)
 if old is not None and not backup.exists():
  backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(old)
 path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_name(path.name+".lcg-tmp");tmp.write_text(text,encoding="utf-8",newline="\n");tmp.replace(path)
 changed.append(path.relative_to(root).as_posix())
b.write=write;c=vars(b);install(c);ext(c);asm(c)
p=b.ASSETS/"portal-data.js"
data=json.loads(p.read_text(encoding="utf-8").removeprefix("window.ARM_PORTAL_DATA=").rstrip(";\n"))
key="paper-e2025-07-01-a1";spec=historical_specs(c)[key]
for item in data["items"]:
 if item["id"]==key:
  item["summary"]=spec["purpose"];item["aliases"]=spec["questions"];item["components"]=spec["features"]
items=[i for i in data["items"] if not i["id"].startswith("text-")]
refresh(c,items)
(stage/"search-published.json").write_text(json.dumps(changed,indent=2)+"\n")
print("Changed search/publication files:",len(changed))

