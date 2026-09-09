from pathlib import Path
p=Path('90_WORKING_PROJECTS/QUESTION_REVIEW_20260908/EXAM_HANDOFF/01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/BUILD_STUDENT_PORTAL.py')
s=p.read_text(encoding='utf-8-sig')
start=s.index('def build_exams(');body=s.index('\n',start)+1
s=s[:body]+"    from question_review import read_reviews, render as render_question_review, assembly_dependency\n    reviews = read_reviews()\n"+s[body:]
s=s.replace('            question_raw_dir = GENERATED_SOURCES', '            review = reviews[q["question_id"]]\n            dependency = assembly_dependency(review)\n            question_raw_dir = GENERATED_SOURCES',1)
s=s.replace('question_raw_dir / "assembly.s" if needs_asm else None','question_raw_dir / "assembly.s" if needs_asm or dependency else None',1)
s=s.replace('write(question_asm_path, source_code(specific if specific and specific.exists() else asm_path))','write(question_asm_path, source_code(dependency or (specific if specific and specific.exists() else asm_path)))',1)
s=s.replace('            if needs_asm:\n                code_sections +=', '            if question_asm_path:\n                code_sections +=',1)
a=s.index('            method_steps = [',start);z=s.index('            write(question_destination, page(',a)
s=s[:a]+'''            relevant_algorithms = [href(path, question_destination, f"Study {label}") for label, path in algorithm_links.items() if any(slug(tag) in slug(label) or slug(label) in slug(tag) for tag in question_algorithms)][:6]
            paper = ROOT / review['paper']
            paper_links = '<p>' + ' · '.join('<a class="button" href="' + esc(rel(paper, question_destination)) + '#page=' + str(n) + '">Original paper — page ' + str(n) + '</a>' for n in review['pages']) + '</p>'
            related = ('<ul>'+''.join(f'<li>{x}</li>' for x in relevant_algorithms)+'</ul>') if relevant_algorithms else '<p>Use the Algorithms and Solution Patterns sections for related methods.</p>'
            notes_link = '<p>' + href(question_raw_dir / 'README.md', question_destination, 'Existing detailed walkthrough and placement table') + '</p>' if question_notes and question_notes.exists() else ''
            question_body = render_question_review(review, code_sections, paper_links, related, notes_link)
''' +s[z:]
old='"compileStatus": "See this paper\\\'s revision review; no native Keil result claimed" if question_notes and question_notes.exists() else "Previously checked with the supplied platform; API symbols re-audited by the canonical verifier", "behaviorStatus": "Deterministic algorithms are source-testable; hardware flow is statically checked without a board claim"'
assert old in s
s=s.replace(old,'"compileStatus": review["verification"]["nativeBuild"]["status"] + ": " + review["verification"]["nativeBuild"]["detail"], "behaviorStatus": review["reviewStatus"] + "; physical board UNVERIFIED", "reviewedOn": review["reviewedOn"], "limitations": review["limitations"]',1)
# All actual dependencies are downloadable, even if only C is newly requested in Q2.
s=s.replace('"Both" if needs_c and needs_asm else "C" if needs_c else "Assembly"','"Both" if needs_c and question_asm_path else "C" if needs_c else "Assembly"',1)
p.write_text(s,encoding='utf-8',newline='\n')
print('Installed strict question review renderer in existing builder.')
