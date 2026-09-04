"""Regenerate legacy teaching pages and apply canonical section destinations."""
import json
import BUILD_STUDENT_PORTAL as b
from portal_presentation import install
from workstation_extensions import install as courses
from asm_reference import install as asm
from pattern_runnable import install as runnable
from scenario_library import classify,rebase,build_index
def main():
    c=vars(b);install(c);courses(c);asm(c);runnable(c);c['reuse_pattern_projects']=True
    path=b.ASSETS/'portal-data.js'
    data=json.loads(path.read_text(encoding='utf-8').removeprefix('window.ARM_PORTAL_DATA=').rstrip(';\n'))
    items=[i for i in data['items'] if not i['id'].startswith(('text-','pattern-','workflow-')) and i['kind']!='Algorithms' and i['id']!='complete-pattern-projects']
    exams=b.read_csv(b.COURSE/'REVIEWED_EXAM_INDEX.csv');rows=b.read_csv(b.COURSE/'CANONICAL_PATTERN_INDEX.csv');solutions=b.read_csv(b.GUIDES/'CURRENT_TEMPLATE_SOLUTION_INDEX.csv')
    b.build_algorithms(exams,items);b.build_patterns(rows,exams,solutions,items)
    moves,destinations=classify(c,items)
    for p in b.PORTAL.rglob('*.html'):
        text=p.read_text(encoding='utf-8');new=rebase(text,p,p,moves)
        if text!=new:b.write(p,new)
    records=json.loads((b.MAINTENANCE/'SCENARIO_MANIFEST.json').read_text());build_index(c,records,destinations)
    data['items']=items;path.write_text('window.ARM_PORTAL_DATA='+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
    print('Canonical section pages regenerated')
if __name__=='__main__':main()
