"""Audit rendered navigation, inline source fidelity, and offline presentation."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[3]
PORTAL = ROOT / '01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.headings, self.pre = [], [], [], []
        self.in_pre = False
        self.closed_code = 0
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        for name in ('href', 'src', 'action'):
            if attrs.get(name): self.links.append(attrs[name])
        if re.fullmatch('h[1-6]', tag): self.headings.append(int(tag[1]))
        if tag == 'pre': self.in_pre = True; self.pre.append('')
        if tag == 'details' and 'code-panel' in attrs.get('class', '').split() and 'open' not in attrs:
            self.closed_code += 1

    def handle_endtag(self, tag):
        if tag == 'pre': self.in_pre = False

    def handle_data(self, data):
        if self.in_pre: self.pre[-1] += data


def audit():
    paths = [ROOT / 'START_HERE.html', *sorted(PORTAL.rglob('*.html'))]
    pages = {p: Page(p.read_text(encoding='utf-8')) for p in paths}
    issues, links, copies, inline = [], 0, 0, 0
    notices = []
    for path, page in pages.items():
        label = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding='utf-8')
        if page.headings.count(1) != 1: issues.append(f'{label}: expected one main heading')
        if any(b > a + 1 for a, b in zip(page.headings, page.headings[1:])):
            issues.append(f'{label}: heading levels skip a level')
        if len(page.ids) != len(set(page.ids)): issues.append(f'{label}: duplicate anchors')
        if page.closed_code: issues.append(f'{label}: code hidden by default')
        if 'portal_logic.js' not in text or 'theme.js' not in text: issues.append(f'{label}: missing presentation asset')
        if 'aria-label="Primary navigation"' not in text: issues.append(f'{label}: missing main navigation')
        if 'class="source-notice"' in text: notices.append(label)
        inline += len(page.pre)
        if page.pre and 'Jump to code' not in text: issues.append(f'{label}: missing code shortcut')
        if any('tabindex="0"' not in opening for opening in re.findall(r'<pre\b[^>]*>', text)):
            issues.append(f'{label}: code cannot receive keyboard focus')
        copies += len(re.findall(r'class="copy-code\b', text))
        if len(page.pre) != len(re.findall(r'class="copy-code\b', text)):
            issues.append(f'{label}: not every listing has a copy control')
        for link in page.links:
            links += 1
            url = urlsplit(link)
            if url.scheme or url.netloc or url.path.startswith(('/', '\\')):
                issues.append(f'{label}: non-local reference {link}')
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_relative_to(ROOT.resolve()): issues.append(f'{label}: escaped package {link}'); continue
            if not target.exists(): issues.append(f'{label}: missing target {link}'); continue
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                issues.append(f'{label}: missing anchor {link}')
        # Download links in canonical code panels must match the displayed source.
        for panel in re.findall(r'<details\b[^>]*class="code-panel"[^>]*>(.*?)</details>', text, re.S):
            raw = re.search(r'class="raw-link" href="([^"]+)"', panel)
            if raw is None: continue
            raw_path = (path.parent / unquote(raw[1])).resolve()
            parsed = Page(panel)
            if raw_path.is_file() and parsed.pre:
                expected = raw_path.read_text(encoding='utf-8-sig').strip()
                if parsed.pre[0].strip() != expected:
                    issues.append(f'{label}: displayed code differs from its raw file')
    home = (ROOT / 'START_HERE.html').read_text(encoding='utf-8')
    if '.uvprojx' in home: issues.append('Home bypasses the practice-copy instructions')
    search = (PORTAL / 'search.html').read_text(encoding='utf-8')
    if '<noscript>' not in search: issues.append('Search lacks a no-JavaScript browsing fallback')
    if 'data-search-results aria-live' in search: issues.append('Entire results tree is a live region')
    css = (PORTAL / 'assets/portal.css').read_text(encoding='utf-8')
    contrasts = {}
    def luminance(hex_color):
        value = hex_color.lstrip('#')
        if len(value) == 3: value = ''.join(c * 2 for c in value)
        rgb = [int(value[i:i+2], 16) / 255 for i in (0, 2, 4)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
        return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))
    for theme, selector in [('light', r':root\s*\{([^}]+)'), ('dark', r':root\[data-theme=dark\]\s*\{([^}]+)')]:
        block = re.search(selector, css).group(1)
        tokens = dict(re.findall(r'--([\w-]+):\s*(#[0-9a-f]+)', block))
        for front, back in [('ink','paper'),('muted','paper'),('muted','wash'),('accent','paper'),('accent','accent-soft'),('code-ink','code'),('warning-ink','warning')]:
            values = sorted([luminance(tokens[front]), luminance(tokens[back])])
            ratio = (values[1] + .05) / (values[0] + .05)
            key = f'{theme}:{front}/{back}'
            contrasts[key] = round(ratio, 2)
            if ratio < 4.5: issues.append(f'Text contrast below 4.5:1: {key} ({ratio:.2f})')
    if '@media print' not in css or 'details::details-content' not in css: issues.append('Missing expanded-code print rules')
    if 'prefers-reduced-motion' not in css: issues.append('Missing reduced-motion rules')
    sizes = sorted(path.stat().st_size for path in paths)
    assets = {path.name:path.stat().st_size for path in (PORTAL / 'assets').iterdir() if path.is_file()}
    return {'pages':len(pages), 'links':links, 'inline_listings':inline, 'copy_controls':copies,
            'page_bytes':{'median':sizes[len(sizes)//2], 'maximum':max(sizes)},
            'asset_bytes':assets,
            'theme_text_contrast':contrasts,
            'source_notice_pages':notices, 'issues':issues}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', type=Path, help='Optional evidence output path')
    args = parser.parse_args()
    result = audit()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if result['issues'] else 0)
