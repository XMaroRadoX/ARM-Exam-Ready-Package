from pathlib import Path
import shutil
work=Path(__file__).resolve().parent;maint=work/'EXAM_HANDOFF/01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE'
for name in ('lcd_scenario.py','VERIFY_SCENARIOS.py'):
    shutil.copy2(work/name,maint/name)
path=maint/'pattern_runnable.py';text=path.read_text(encoding='utf-8')
text=text.replace("    if spec.get('reference') is not None:files['Source/reference.c']=spec['reference']", "    if spec.get('reference') is not None:files['Source/reference.c']=spec['reference']\n    files.update(spec.get('extra_files',{}))")
text=text.replace("        text=clean(code,key);(project/name).write_text(text,encoding='utf-8')", "        text=clean(code,key);(project/name).parent.mkdir(parents=True,exist_ok=True);(project/name).write_text(text,encoding='utf-8')")
marker="    readme=['# '+key"
extra='''    if spec.get('extra_files'):
        path=project/'sample.uvprojx';tree=ET.parse(path)
        for groups in tree.findall('.//Target/Groups'):
            group=ET.SubElement(groups,'Group');ET.SubElement(group,'GroupName').text='Supplied display driver'
            files_node=ET.SubElement(group,'Files')
            for filename in spec['extra_files']:
                if not filename.endswith('.c'):continue
                f=ET.SubElement(files_node,'File')
                for tag,value in [('FileName',Path(filename).name),('FileType','1'),('FilePath','./'+filename)]:ET.SubElement(f,tag).text=value
        tree.write(path,encoding='utf-8',xml_declaration=True)
'''
text=text.replace(marker,extra+marker);path.write_text(text,encoding='utf-8')
path=maint/'scenario_library.py';text=path.read_text(encoding='utf-8')
text=text.replace("    specs={**practice_specs(),**historical_specs(c)}", "    from lcd_scenario import spec as lcd_spec\n    specs={**practice_specs(),**historical_specs(c),'paper-lcd-maze':lcd_spec(c)}")
text=text.replace("    files=write_project(key,spec,c['clean_algorithm_code'])", "    try:\n        files=write_project(key,spec,c['clean_algorithm_code'],reuse=True)\n    except (ValueError,FileNotFoundError):\n        files=write_project(key,spec,c['clean_algorithm_code'])")
text=text.replace("source=spec['source'])", "source=spec['source'],externalQuestion=spec.get('externalQuestion'))")
text=text.replace("        if r['questions']:body+=", "        if r['questions'] or r.get('externalQuestion'):body+=")
text=text.replace("', '.join(r['questions'])+' — '+r['title']", "', '.join(r['questions'] or [r['externalQuestion']])+' — '+r['title']")
path.write_text(text,encoding='utf-8')
# Source-agreement checks follow the canonical destination after migration.
path=maint/'VERIFY_PATTERN_COVERAGE.py';text=path.read_text(encoding='utf-8')
text=text.replace("  page=b.PORTAL/'patterns'/(b.slug(row['title'])+'.html')", "  destinations=json.loads((HERE/'SECTION_DESTINATIONS.json').read_text())\n  page=b.PORTAL/destinations[row['title']]['route']")
path.write_text(text,encoding='utf-8')
# Native scenario gate uses the same native compiler/project method and hashes.
text=(maint/'VERIFY_PATTERN_PROJECTS.py').read_text(encoding='utf-8')
text=text.replace("coverage=json.loads((HERE/'PATTERN_COVERAGE.json').read_text())", "coverage=[{'projects':json.loads((HERE/'SCENARIO_MANIFEST.json').read_text())}]")
text=text.replace("HERE/('PATTERN_BOARD_NATIVE_BUILDS.json' if args.board_only else 'PATTERN_NATIVE_BUILDS.json')", "HERE/'SCENARIO_NATIVE_BUILDS.json'")
text=text.replace("    if not args.board_only:\n", "    if False:\n")
text=text.replace("'pattern-native-logs'", "'scenario-native-logs'")
(maint/'VERIFY_SCENARIO_PROJECTS.py').write_text(text,encoding='utf-8')
print('Installed LCD extension and scenario checks')
