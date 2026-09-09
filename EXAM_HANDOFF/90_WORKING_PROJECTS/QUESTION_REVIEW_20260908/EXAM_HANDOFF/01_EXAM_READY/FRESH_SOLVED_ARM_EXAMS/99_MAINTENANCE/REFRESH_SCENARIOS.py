"""Refresh scenario projects/pages after a scenario-source change."""
import json,hashlib
import BUILD_STUDENT_PORTAL as b
from portal_presentation import install
from workstation_extensions import install as courses
from asm_reference import install as asm
from scenario_library import practice_specs,historical_specs,render_scenario,build_index
from lcd_scenario import spec as lcd

def main():
    c=vars(b);install(c);courses(c);asm(c)
    specs={**practice_specs(),**historical_specs(c),'paper-lcd-maze':lcd(c)}
    path=b.MAINTENANCE/'SCENARIO_MANIFEST.json'
    old={r['id']:r for r in json.loads(path.read_text())}
    records=[]
    for key,s in specs.items():
        # Page descriptions may change independently of source files; render
        # explicitly requested entries or missing entries in this incremental run.
        import sys
        if key not in old or '--all' in sys.argv or ('--historical' in sys.argv and s.get('paper')) or key in sys.argv:
            record=render_scenario(c,key,s)
        else:record=old[key]
        records.append(record)
    path.write_text(json.dumps(records,indent=2)+'\n')
    destinations=json.loads((b.MAINTENANCE/'SECTION_DESTINATIONS.json').read_text())
    build_index(c,records,destinations)
    data_path=b.ASSETS/'portal-data.js'
    data=json.loads(data_path.read_text(encoding='utf-8').removeprefix('window.ARM_PORTAL_DATA=').rstrip(';\n'))
    data['items']=[i for i in data['items'] if not i['id'].startswith(('mix-','task-','paper-','text-'))]
    for r in records:
        s=specs[r['id']]
        data['items'].append(dict(id=r['id'],kind='Solution Patterns',title=s['title'],summary=s['purpose'],route=r['route'],languages=['Both'] if s.get('paper') else ['C'],components=s['features'],topics=[s['group']],aliases=s['questions'],examHistory=s['history'],relatedIds=[]))
    data_path.write_text('window.ARM_PORTAL_DATA='+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
    coverage=b.PORTAL/'patterns/coverage.html';text=coverage.read_text(encoding='utf-8')
    if 'data-lcd-extension' not in text:
        text=text.replace('</main>','<section class="section-block" data-lcd-extension><h2>Additional supplied board question</h2><p><a href="paper-lcd-maze.html">2024-07-09 Q5: LCD maze and joystick movement</a>. This extension uses the supplied display driver and has its own complete project.</p></section></main>')
        coverage.write_text(text,encoding='utf-8')
    print('Scenario entries:',len(records))
if __name__=='__main__':main()
