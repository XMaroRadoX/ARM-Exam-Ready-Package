from pathlib import Path
from html import escape
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
import pypdfium2 as pdfium
from PIL import Image, ImageOps, ImageDraw

root = Path.cwd()
out = root/'90_WORKING_PROJECTS/20230704_Sociable_Complete'
path = out/'Detailed_Solution.md'
text = path.read_text(encoding='utf-8')
if '## Appendix A' not in text:
    for title, source, lang in [
        ('Appendix A - Complete assembly (both questions)', 'Q1_Assembly/Source/ASM_funct.s', 'asm'),
        ('Appendix B - Question 1 test driver', 'Q1_Assembly/Source/sample.c', 'c'),
        ('Appendix C - Question 2 main program', 'Q2_Timer_LEDs/Source/sample.c', 'c'),
        ('Appendix D - Question 2 complete timer handlers', 'Q2_Timer_LEDs/Source/timer/IRQ_timer.c', 'c')]:
        text += '\n## '+title+'\n\nFile: `'+source+'`\n\n```'+lang+'\n'+(out/source).read_text()+'```\n'
    path.write_text(text, encoding='utf-8')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text', fontName='Helvetica', fontSize=10.1, leading=14.7, spaceAfter=8))
styles.add(ParagraphStyle(name='Section', fontName='Helvetica-Bold', fontSize=15, leading=19,
                         textColor=colors.HexColor('#163b55'), spaceBefore=17, spaceAfter=9, keepWithNext=True))
styles.add(ParagraphStyle(name='Subsection', fontName='Helvetica-Bold', fontSize=11.6, leading=15,
                         textColor=colors.HexColor('#21566c'), spaceBefore=10, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name='Cell', fontName='Helvetica', fontSize=8.2, leading=11.1))
styles.add(ParagraphStyle(name='Mono', fontName='Courier', fontSize=7.65, leading=10.1,
                         backColor=colors.HexColor('#f2f5f7'), borderPadding=7, spaceBefore=6, spaceAfter=10))
styles.add(ParagraphStyle(name='BulletText', parent=styles['Text'], leftIndent=13, firstLineIndent=-10))

def markup(s):
    s = escape(s)
    s = re.sub(r'`([^`]+)`', r'<font name="Courier" size="9">\1</font>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s

story = [Spacer(1, 52), Paragraph('ARM EXAM SOLUTIONS', styles['Heading2']),
         Paragraph('4 July 2023', styles['Title']), Spacer(1, 18),
         Paragraph('Aliquot sums, sociable numbers,<br/>Timer 1 and LED output', styles['Section']),
         Spacer(1, 15), Paragraph('Complete worked answers to Questions 1 and 2', styles['Text']),
         Paragraph('LPC1768 / Cortex-M3 | Keil ARMASM and C', styles['Text']), Spacer(1, 27),
         Paragraph('<b>Included:</b> step-by-step reasoning, register and stack explanations, all expected sequences, timer calculations, LED mapping, project instructions, and the full source code.', styles['Text']),
         Spacer(1, 20), Paragraph('<b>Verified:</b> four native compile/link builds; native instruction execution against mathematical references; boundary and compiled interrupt-handler checks. Physical board timing has not been tested.', styles['Text']),
         Spacer(1, 35), Paragraph('Open Q1_Assembly/sample.uvprojx for Question 1.<br/>Open Q2_Timer_LEDs/sample.uvprojx for the complete application.', styles['Text']),
         PageBreak()]
lines = text.splitlines()
i = 1
while i < len(lines):
    line = lines[i]
    if not line.strip():
        i += 1
        continue
    if line.startswith('```'):
        code = []
        i += 1
        while i < len(lines) and not lines[i].startswith('```'):
            code.append(lines[i])
            i += 1
        if code and 'AREA' in code[0] and '; uint32_t aliquotSum(uint32_t n)' in code:
            split = code.index('; uint32_t aliquotSum(uint32_t n)')
            story.append(Preformatted('\n'.join(code[:split]), styles['Mono']))
            story.append(PageBreak())
            story.append(Paragraph('Appendix A (continued) - Aliquot-sum helper', styles['Section']))
            story.append(Preformatted('\n'.join(code[split:]), styles['Mono']))
        else:
            story.append(Preformatted('\n'.join(code), styles['Mono']))
        i += 1
    elif line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            row = [c.strip() for c in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r'[: -]+', c) for c in row):
                rows.append([Paragraph(markup(c), styles['Cell']) for c in row])
            i += 1
        table = Table(rows, repeatRows=1, hAlign='LEFT', colWidths=[487/len(rows[0])]*len(rows[0]))
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce8ef')),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f4f7f9')]),
            ('VALIGN',(0,0),(-1,-1),'TOP'), ('LEFTPADDING',(0,0),(-1,-1),7),
            ('RIGHTPADDING',(0,0),(-1,-1),7), ('TOPPADDING',(0,0),(-1,-1),7),
            ('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LINEBELOW',(0,0),(-1,0),0.6,colors.HexColor('#91a9b8'))]))
        story += [table, Spacer(1, 11)]
    elif line.startswith('## '):
        if 'Appendix' in line:
            story.append(PageBreak())
        story.append(Paragraph(markup(line[3:]), styles['Section']))
        i += 1
    elif line.startswith('### '):
        story.append(Paragraph(markup(line[4:]), styles['Subsection']))
        i += 1
    elif line.startswith('- ') or re.match(r'^\d+\. ', line):
        label = '- ' if line.startswith('- ') else ''
        story.append(Paragraph(markup(line), styles['BulletText']))
        i += 1
    else:
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '|', '```', '- ')):
            paragraph.append(lines[i])
            i += 1
        story.append(Paragraph(markup(' '.join(paragraph)), styles['Text']))

def frame(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#486174'))
    if doc.page > 1:
        canvas.drawString(54, A4[1]-32, '4 JULY 2023 | WORKED ARM EXAM SOLUTIONS')
    canvas.drawString(54, 28, 'LPC1768 / Cortex-M3')
    canvas.drawRightString(A4[0]-54, 28, str(doc.page))
    canvas.restoreState()

pdf = out/'Detailed_Solution.pdf'
doc = SimpleDocTemplate(str(pdf), pagesize=A4, leftMargin=54, rightMargin=54,
                        topMargin=51, bottomMargin=48, title='ARM exam 4 July 2023 - Complete worked solutions', author='')
doc.build(story, onFirstPage=frame, onLaterPages=frame)
render = root/'tmp/pdfs/20230704/rendered'
render.mkdir(exist_ok=True)
document = pdfium.PdfDocument(pdf)
thumbs=[]
for index, page in enumerate(document):
    picture = page.render(scale=1.4).to_pil()
    picture.save(render/f'page-{index+1:02}.png')
    picture.thumbnail((298, 422))
    thumb = Image.new('RGB', (318, 451), 'white')
    thumb.paste(picture, (10, 6))
    ImageDraw.Draw(thumb).text((10, 431), f'Page {index+1}', fill='black')
    thumbs.append(thumb)
for start in range(0,len(thumbs),6):
    batch=thumbs[start:start+6]
    sheet=Image.new('RGB',(318*3,451*2),'#c8d0d6')
    for j, thumb in enumerate(batch):
        sheet.paste(thumb, ((j%3)*318, (j//3)*451))
    sheet.save(render/f'contact-{start//6+1}.png')
print('PDF pages:',len(document))
print(pdf)
