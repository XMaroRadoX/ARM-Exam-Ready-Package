"""Offline presentation layer. Canonical builders retain ownership of content."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


def navigation(context, source, active=''):
    esc, rel = context['esc'], context['rel']
    return ''.join(
        f'<a href="{rel(target, source)}"' + (' aria-current="page"' if label == active else '') +
        f'><span class="nav-number" aria-hidden="true" data-number="{index:02d}"></span>{esc(label)}</a>'
        for index, (label, target) in enumerate(context['NAV'])
    )


def refresh_navigation(context):
    """Refresh navigation on retained pages without replacing their study content."""
    for path in [context['HOME'], *sorted(context['PORTAL'].rglob('*.html'))]:
        text = path.read_text(encoding='utf-8')
        active = next((label for label, target in context['NAV']
                       if path == target or (label != 'Home' and path.parent == target.parent)), '')
        updated = re.sub(r'(<nav\b[^>]*aria-label="Primary navigation"[^>]*>).*?(</nav>)',
                         lambda m: m[1] + navigation(context, path, active) + m[2], text, flags=re.S)
        if updated != text:
            context['write'](path, updated)


def install(context: dict) -> None:
    """Install presentation hooks before the canonical build starts."""
    if context.get('_presentation_installed'):
        return
    context['_presentation_installed'] = True
    root, portal, home = (context[key] for key in ('ROOT', 'PORTAL', 'HOME'))
    assets = portal / 'assets'
    ui = Path(__file__).parent / 'portal_ui'
    esc, rel, write = (context[key] for key in ('esc', 'rel', 'write'))
    original_search = context['build_search']

    def build_assets():
        for filename in ('portal.css', 'portal.js', 'theme.js', 'portal_logic.js'):
            write(assets / filename, (ui / filename).read_text(encoding='utf-8'))

    def decorate(body, source):
        def complete_languages(match):
            options = match[2]
            if '<option>Assembly</option>' not in options:
                options += '<option>Assembly</option>'
            return match[1] + options + '</select>'
        body = re.sub(r'(<select[^>]*data-filter="language"[^>]*>)(.*?)</select>', complete_languages, body, flags=re.S)
        # Add anchors to canonical section headings without changing their content.
        used = set(re.findall(r'\bid="([^"]+)"', body))
        headings = []

        def heading(match):
            attrs, label = match.groups()
            existing = re.search(r'\bid="([^"]+)"', attrs)
            name = html.unescape(re.sub('<[^>]+>', '', label)).strip()
            anchor = existing.group(1) if existing else 'section-' + context['slug'](name)
            if not existing:
                candidate, index = anchor, 2
                while anchor in used:
                    anchor = f'{candidate}-{index}'
                    index += 1
                used.add(anchor)
                attrs += f' id="{anchor}"'
            headings.append((anchor, name))
            return f'<h2{attrs}>{label}</h2>'

        # Listing cards are not document sections.
        is_listing = source.name == 'index.html' and source.parent.name != 'api'
        if not is_listing:
            body = re.sub(r'<h2([^>]*)>(.*?)</h2>', heading, body, flags=re.S)
        body = re.sub(r'(<aside\b[^>]*class="api-sidebar"[^>]*>)',
                      r'\1<h2 class="sr-only">Browse API functions</h2>', body)
        body = re.sub(r'<details([^>]*\bclass="code-panel"[^>]*)>',
                      lambda m: '<details' + m[1] + ('' if re.search(r'\bopen\b', m[1]) else ' open') + '>', body)
        count = 0
        first_code = None

        def code_frame(match):
            nonlocal count, first_code
            count += 1
            anchor = f'listing-{count}'
            while anchor in used:
                anchor += '-code'
            used.add(anchor)
            if first_code is None:
                first_code = anchor
            language = re.search(r'language-([\w-]+)', match[0])
            label = language[1].upper() if language else 'CODE'
            pre = match[0]
            if 'tabindex=' not in pre.split('>', 1)[0]:
                pre = pre.replace('<pre', '<pre tabindex="0"', 1)
            return (f'<div class="code-frame" id="{anchor}"><div class="code-toolbar">'
                    f'<span>{esc(label)}</span><button type="button" class="copy-code js-only" '
                    f'aria-label="Copy {esc(label)} listing {count}">Copy code</button></div>'
                    f'{pre}<p class="copy-status" role="status" aria-live="polite"></p></div>')

        body = re.sub(r'<pre\b[^>]*>.*?</pre>', code_frame, body, flags=re.S)
        # A known incomplete starter should not look ready to paste.
        for snippet in re.findall(r'<pre\b[^>]*>(.*?)</pre>', body, re.S):
            plain = html.unescape(re.sub('<[^>]+>', '', snippet))
            if '__WFI()' in plain and '#include "exam_api.h"' in plain and '#include "LPC17xx.h"' not in plain:
                body = ('<aside class="source-notice"><strong>Before using this starter</strong>'
                        '<p>The example below uses <code>__WFI()</code>. Include '
                        '<code>LPC17xx.h</code> as well as <code>exam_api.h</code>, as in the starting project.</p></aside>') + body
                break
        toc = ''
        if headings and source != home:
            toc = '<nav class="page-contents" aria-label="On this page"><span>On this page</span>' + ''.join(
                f'<a href="#{esc(anchor)}">{esc(label)}</a>' for anchor, label in headings
            ) + '</nav>'
        return body, toc, first_code

    def page(source, title, description, body, crumbs, section='', extra_head=''):
        source = Path(source)
        body, toc, first_code = decorate(body, source)
        active = section or ('Home' if source == home else '')
        nav = navigation(context, source, active)
        breadcrumb = '<nav class="breadcrumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(
            f'<a href="{rel(target, source)}">{esc(label)}</a>' if index < len(crumbs) - 1
            else f'<span aria-current="page">{esc(label)}</span>'
            for index, (label, target) in enumerate(crumbs)
        ) + '</nav>'
        if source == home:
            breadcrumb = ''
        title_text = title if title == 'ARM Exam Workstation' else title + ' · ARM Exam Workstation'
        heading = '' if source == home else (
            f'<header class="page-heading"><p class="eyebrow">{esc(section or "Find your next step")}</p>'
            f'<h1>{esc(title)}</h1><p>{esc(description)}</p>' +
            (f'<a class="text-action" href="#{first_code}">Jump to code <span aria-hidden="true">↓</span></a>' if first_code else '') + '</header>'
        )
        listing_class = ' is-listing' if source.name == 'index.html' and section != 'API' else ''
        return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="{esc(description)}">
  <title>{esc(title_text)}</title>
  <script src="{rel(assets / 'theme.js', source)}"></script>
  <link rel="stylesheet" href="{rel(assets / 'portal.css', source)}">
  {extra_head}
</head>
<body data-section="{esc(active)}" class="workstation{listing_class}">
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <a class="brand" href="{rel(home, source)}"><span class="brand-mark" aria-hidden="true">ARM</span><span>Exam <br>Workstation</span></a>
    <p class="rail-label">YOUR STUDY DESK</p>
    <nav class="primary-nav" aria-label="Primary navigation">{nav}</nav>
    <div class="rail-bottom"><a href="{rel(portal / 'guides' / 'start-a-working-project.html', source)}">Start a practice project <span aria-hidden="true">↗</span></a><p>ARM · C · LPC1768<br>Available offline</p></div>
  </header>
  <div class="workspace-bar"><span class="workspace-label">STUDY / REFERENCE</span>
    <a class="search-shortcut" data-search-shortcut href="{rel(portal / 'search.html', source)}">Search the package <kbd aria-hidden="true">/</kbd></a>
    <button class="theme-toggle js-only" type="button" aria-label="Switch color theme">Theme</button>
  </div>
  <main id="main-content" tabindex="-1">{breadcrumb}{heading}{toc}<div class="page-body">{body}</div></main>
  <footer><span>ARM Exam Workstation</span><a href="{rel(home, source)}">Back to home</a><span>Local study material · Keep the folder together</span></footer>
  <script src="{rel(assets / 'portal_logic.js', source)}" defer></script>
  <script src="{rel(assets / 'portal.js', source)}" defer></script>
</body>
</html>'''

    def build_home():
        def link(folder, name):
            return rel(portal / folder / name, home)
        routes = [
            ('01', 'Start with the essentials', 'Understand the package and the steps from a question to a working answer.', 'start-from-zero'),
            ('02', 'Learn C and ARM assembly', 'Work through registers, arrays, branches, the stack, and function calls.', 'learn-assembly'),
            ('03', 'Connect the peripherals', 'Study buttons, timers, LEDs, ADC, DAC, and interrupt ownership.', 'use-peripherals'),
            ('04', 'Solve a past exam', 'Read the paper, follow the method, and study the complete C and assembly answer.', 'solve-a-past-exam'),
        ]
        route_cards = ''.join(
            f'<a class="study-route" href="{link("guides", key + ".html")}"><span class="route-number">{number}</span>'
            f'<div><h3>{title}</h3><p>{summary}</p></div><span class="route-arrow" aria-hidden="true">↗</span></a>'
            for number, title, summary, key in routes
        )
        destinations = ''.join(
            f'<a class="reference-tile" href="{link(key, "index.html")}"><strong>{title}</strong><span>{summary}</span><span aria-hidden="true">→</span></a>'
            for key, (title, summary) in context['SECTION_META'].items()
        )
        body = f'''<section class="home-intro"><p class="eyebrow">YOUR ARM STUDY WORKSPACE</p>
          <h1>ARM study workspace</h1>
          <p>Follow a study route, work through a past paper, or find the exact function you need.</p>
          <form class="search-form" action="{link('', 'search.html')}" method="get"><label class="sr-only" for="home-search">Search exams, code, functions, and peripherals</label><input id="home-search" name="q" type="search" placeholder="A question, algorithm, or API function…"><button type="submit">Search</button></form>
          <div class="search-examples"><span>Try</span><a href="{link('', 'search.html')}?q=fifth+argument">fifth argument</a><a href="{link('', 'search.html')}?q=ADC">ADC</a><a href="{link('', 'search.html')}?q=Mastermind">Mastermind</a></div>
        </section>
        <section class="study-section"><div class="section-heading"><div><p class="eyebrow">LEARN BY DOING</p><h2>Choose where to begin</h2></div><a href="{link('guides', 'index.html')}">All study guides →</a></div><div class="study-routes">{route_cards}</div>
          <p class="route-footnote">Working on C first? <a href="{link('guides', 'learn-c.html')}">Open the C learning guide</a>.</p></section>
        <section class="reference-section"><div class="section-heading"><div><p class="eyebrow">KEEP IT CLOSE</p><h2>Your reference library</h2></div></div><div class="reference-grid">{destinations}</div></section>
        <aside class="practice-banner"><div><strong>A fresh project for every attempt</strong><p>Copy the starting template into <code>90_WORKING_PROJECTS</code>, then work in your copy.</p></div><a class="button" href="{link('guides', 'start-a-working-project.html')}">Prepare a practice project →</a></aside>'''
        write(home, page(home, 'ARM Exam Workstation', 'Study ARM assembly, C, and LPC1768 peripherals with complete code and past exams.', body, [('Home', home)]))

    def build_search(items):
        original_search(items)
        path = portal / 'search.html'
        text = path.read_text(encoding='utf-8')
        # Only counts are announced, rather than the complete search result tree.
        text = text.replace('<div data-search-results aria-live="polite"></div>',
                            '<p data-search-count role="status" aria-live="polite"></p><div data-search-results></div>')
        fallback = '<noscript><section class="notice"><h2>Browse without search</h2><p>Search needs JavaScript. All study pages and code remain available through these sections.</p><ul>' + ''.join(
            f'<li><a href="{rel(portal / key / "index.html", path)}">{esc(title)}</a></li>'
            for key, (title, _) in context['SECTION_META'].items()
        ) + '</ul></section></noscript>'
        text = text.replace('<div class="page-body">', '<div class="page-body">' + fallback, 1)
        text = text.replace('Search all six sections from one place.', 'Find exams, methods, API functions, algorithms, and study guides.')
        write(path, text)

    context.update(page=page, build_assets=build_assets, build_home=build_home, build_search=build_search, render_search_page=build_search)
