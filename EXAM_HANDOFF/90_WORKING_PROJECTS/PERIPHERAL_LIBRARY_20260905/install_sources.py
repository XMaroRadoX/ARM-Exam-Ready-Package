from pathlib import Path
import shutil
work=Path(__file__).resolve().parent
stage=work/'EXAM_HANDOFF'
maint=stage/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE'
for name in ('scenario_library.py','scenario_engine.c'):
    shutil.copy2(work/name,maint/name)
shutil.copy2(work/'scenarios.js',maint/'portal_ui/scenarios.js')
path=maint/'workstation_extensions.py';text=path.read_text(encoding='utf-8')
text=text.replace('course_pages(items);exam_pages(items)','course_pages(items);exam_pages(items)\n        if "scenario_finalize" in c:c["scenario_finalize"](items)')
path.write_text(text,encoding='utf-8')
path=maint/'BUILD_STUDENT_PORTAL.py';text=path.read_text(encoding='utf-8')
text=text.replace('    install_runnable(globals())\n    main()','    install_runnable(globals())\n    from scenario_library import install as install_scenarios\n    install_scenarios(globals())\n    main()')
path.write_text(text,encoding='utf-8')
# Compatibility pages should not be indexed as duplicate primary lessons.
path=maint/'search_corpus.py';text=path.read_text(encoding='utf-8')
text=text.replace("        raw=path.read_text(encoding='utf-8')", "        raw=path.read_text(encoding='utf-8')\n        if 'data-compatibility-page' in raw:\n            inventory[relative]=dict(status='excluded',reason='Compatibility link to canonical section'); continue")
path.write_text(text,encoding='utf-8')
print('Installed authoritative extension in staging')
