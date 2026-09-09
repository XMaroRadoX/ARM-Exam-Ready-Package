"""Regenerate reviewed exam content only. Run in staging before publishing."""
from pathlib import Path
import csv, io, json, re
import BUILD_STUDENT_PORTAL as b
from portal_presentation import install
from workstation_extensions import install as extensions
from asm_reference import install as asm_install
from question_review import read_reviews

def main():
    reviews=read_reviews()
    reviewed=b.COURSE/'REVIEWED_EXAM_INDEX.csv'
    exams=b.read_csv(reviewed)
    for row in exams:
        papers={r['paper'] for r in reviews.values() if r['examId']==row['exam_id']}
        assert len(papers)==1,(row['exam_id'],papers)
        row['source_pdf']=papers.pop()
    questions=b.read_csv(b.GUIDES/'QUESTION_INDEX.csv')
    for row in questions:
        r=reviews[row['question_id']]
        row['requirement_summary']=r['summary'];row['argument_mapping']=r['contract']
    solutions=b.read_csv(b.GUIDES/'CURRENT_TEMPLATE_SOLUTION_INDEX.csv')
    context=vars(b);install(context);extensions(context);asm_install(context)
    data_path=b.ASSETS/'portal-data.js'
    data=json.loads(re.fullmatch(r'\s*window\.ARM_PORTAL_DATA=(.*);\s*',data_path.read_text(encoding='utf-8-sig'),re.S)[1])
    def links(kind,folder):
        return {x['title']:b.PORTAL/x['route'] for x in data['items'] if x['kind']==kind and x.get('route','').startswith(folder+'/') and not x['id'].startswith('text-')}
    captured={};original_source=b.source_code
    b.write=lambda p,text:captured.__setitem__(Path(p),text)
    b.source_code=lambda p:captured.get(p,original_source(p))
    original_details=b.details_code
    def details(label,code,raw,destination,language,expanded=False):
        panel=original_details(label,code,raw,destination,language,expanded)
        if raw in captured and not raw.exists():
            panel=panel.replace('<div class="code-actions"></div>','<div class="code-actions">'+b.href(raw,destination,'Open raw '+language+' file','raw-link')+'</div>')
        return panel
    b.details_code=details
    items=[]
    b.build_exams(exams,questions,solutions,links('Solution Patterns','patterns'),links('Algorithms','algorithms'),links('Peripheral Combos','combos'),items)
    assert len([x for x in items if x['id'].startswith('question-')])==48
    replacements={x['id']:x for x in items}
    for item in data['items']:
        if item['id'] in replacements:
            fresh=replacements[item['id']]
            item.update({k:v for k,v in fresh.items() if k!='relatedIds'})
    captured[data_path]='window.ARM_PORTAL_DATA='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n'
    for path,rows in [(reviewed,exams),(b.GUIDES/'QUESTION_INDEX.csv',questions)]:
        output=io.StringIO(newline='');writer=csv.DictWriter(output,fieldnames=list(rows[0]),quoting=csv.QUOTE_ALL);writer.writeheader();writer.writerows(rows);captured[path]=output.getvalue()
    for p,text in captured.items():
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text,encoding='utf-8',newline='\n')
    print(json.dumps({'questions':48,'papers':len(exams),'generatedFiles':len(captured)}))

if __name__=='__main__':main()
