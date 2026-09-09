"""Check partial-refresh preservation without changing the published package."""
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import BUILD_STUDENT_PORTAL as builder
import REFRESH_SEARCH
from portal_presentation import refresh_navigation


def main():
    with tempfile.TemporaryDirectory(prefix='arm-portal-refresh-') as folder:
        root = Path(folder)
        portal = root / 'portal'
        portal.mkdir()
        home = root / 'index.html'
        lesson = portal / 'lesson.html'
        content = '<nav aria-label="Primary navigation"><a href="old.html">Old navigation</a></nav><main>Keep this lesson and its code.</main>'
        for path in [home, lesson]:
            path.write_text(content, encoding='utf-8', newline='\n')
        context = dict(HOME=home, PORTAL=portal, NAV=[('Home', home), ('ASM Reference', lesson)],
                       esc=builder.esc, rel=builder.rel, write=builder.write)
        refresh_navigation(context)
        first = lesson.read_text(encoding='utf-8')
        assert 'ASM Reference' in first and '<main>Keep this lesson and its code.</main>' in first
        refresh_navigation(context)
        assert lesson.read_text(encoding='utf-8') == first, 'Navigation refresh must be idempotent'
        records = [dict(id='pattern-example', kind='Algorithms'),
                   dict(id='algorithm-old', kind='Algorithms'), dict(id='text-old', kind='Algorithms')]
        (root / 'portal-data.js').write_text('window.ARM_PORTAL_DATA=' + json.dumps({'items': records}) + ';', encoding='utf-8', newline='\n')
        captured = []
        with patch.object(builder, 'ASSETS', root), \
             patch.object(builder, 'build_algorithms', lambda exams, items: items.append(dict(id='algorithm-new', kind='Algorithms'))), \
             patch.object(builder, 'connect_related', lambda *args: None), \
             patch.object(REFRESH_SEARCH, 'refresh', lambda context, items: captured.extend(items)), \
             patch.object(sys, 'argv', ['BUILD_STUDENT_PORTAL.py', '--algorithms-only']), \
             contextlib.redirect_stdout(io.StringIO()):
            builder.main()
        assert {item['id'] for item in captured} == {'pattern-example', 'algorithm-new'}
    print('PASS: partial algorithm refresh preserves related patterns and refreshes search; navigation preserves lesson content and is idempotent.')


if __name__ == '__main__':
    main()
