from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
import json
from pypdf import PdfReader

root = Path('90_WORKING_PROJECTS/20230704_Sociable_Complete')
report = json.loads((root/'validation/results.json').read_text())
assert len(report['native_builds']) == 4
assert len(report['sociable_cases']) == 23
doc = PdfReader(root/'Detailed_Solution.pdf')
assert len(doc.pages) == 14
text = '\n'.join(p.extract_text() for p in doc.pages)
assert all(s in text for s in ['Appendix A', 'Appendix D', '4938136', 'TIMER1_IRQHandler', 'UDIV'])
for project in root.glob('*/sample.uvprojx'):
    for entry in ET.parse(project).findall('.//Files/File/FilePath'):
        assert (project.parent/entry.text.replace('\\','/')).is_file(), entry.text
md = (root/'Detailed_Solution.md').read_text()
for relative in ['Q1_Assembly/Source/ASM_funct.s','Q1_Assembly/Source/sample.c',
                 'Q2_Timer_LEDs/Source/sample.c','Q2_Timer_LEDs/Source/timer/IRQ_timer.c']:
    assert (root/relative).read_text() in md, relative
archive = root.parent/'20230704_Sociable_Complete.zip'
files = [p for p in root.rglob('*') if p.is_file() and p.suffix not in ['.o','.pyc']
         and '__pycache__' not in p.parts and 'Listings' not in p.parts]
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, p.relative_to(root.parent).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert sum(n.endswith('.uvprojx') for n in z.namelist()) == 2
print('Verified:', len(files), 'archive files, 2 complete project file lists, 14 PDF pages')
print('ZIP bytes:', archive.stat().st_size)
print(archive.resolve())
