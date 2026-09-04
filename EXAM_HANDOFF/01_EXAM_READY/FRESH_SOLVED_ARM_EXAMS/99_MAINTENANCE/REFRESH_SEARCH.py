"""Refresh search only; never regenerate lessons, projects, or answer files."""
import json
import BUILD_STUDENT_PORTAL as builder
from portal_presentation import install
from search_corpus import build
from search_metadata import finish

def main():
    context = vars(builder)
    install(context)
    render_search = builder.build_search
    from workstation_extensions import install as install_extensions
    install_extensions(context)
    # Install page/navigation hooks without invoking their content builders.
    if (builder.MAINTENANCE / 'asm_reference.py').exists():
        from asm_reference import install as install_asm
        install_asm(context)
    raw = (builder.ASSETS / 'portal-data.js').read_text(encoding='utf-8-sig')
    items = json.loads(raw.removeprefix('window.ARM_PORTAL_DATA=').rstrip(';\n'))['items']
    items = [i for i in items if not i['id'].startswith('text-')]
    names = ['portal_logic.js', 'portal.js']
    if (builder.MAINTENANCE / 'portal_ui/asm_reference.js').exists(): names.append('asm_reference.js')
    for name in names:
        builder.write(builder.ASSETS / name, (builder.MAINTENANCE / 'portal_ui' / name).read_text(encoding='utf-8-sig'))
    report = build(context, items)
    render_search(items)
    finish(context, items, report)
    print(json.dumps({key: report[key] for key in ('indexedFiles', 'pdfPages', 'catalogRecords', 'sectionRecords', 'duplicates', 'reviewedExams', 'reviewedQuestions')}, indent=2))

if __name__ == '__main__':
    main()
