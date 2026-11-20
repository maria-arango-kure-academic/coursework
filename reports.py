"""Printable classroom records. No grades or unobserved outcomes are inferred."""
from io import BytesIO
from outcomes import MODEL
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ASSETS=Path(__file__).resolve().parent/'assets'
FONT,BOLD,TITLE,HEADING='VFI simulation-Regular','VFI simulation-Bold','VFI simulation-Title','VFI simulation-Heading'
for name,filename in [(FONT,'PangeaText-Regular.ttf'),(BOLD,'PangeaText-Bold.ttf'),(TITLE,'ZTTalk-Black.ttf'),(HEADING,'ZTTalk-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(ASSETS/filename)))
INK=colors.HexColor('#3a3b3a')
PALE=colors.HexColor('#f7faf2')
STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle('ReportTitle', fontName=TITLE, fontSize=25, leading=29, spaceAfter=12, textColor=INK))
STYLES.add(ParagraphStyle('ReportHeading', fontName=HEADING, fontSize=16, leading=20, spaceBefore=16, spaceAfter=8, keepWithNext=True, textColor=INK))
STYLES.add(ParagraphStyle('ReportBody', fontName=FONT, fontSize=11, leading=17, spaceAfter=8, textColor=INK, splitLongWords=True))
STYLES.add(ParagraphStyle('ReportSmall', parent=STYLES['ReportBody'], fontSize=10, leading=15, spaceAfter=5))
STYLES.add(ParagraphStyle('ReportCell', parent=STYLES['ReportBody'], fontSize=10, leading=15, spaceAfter=0))


def paragraph(text, style='ReportBody'):
    # Escape all participant text before adding the line breaks used for notes.
    return Paragraph(escape(str(text)).replace('\n', '<br/>'), STYLES[style])


def table(rows, widths):
    result = Table([[paragraph(cell, 'ReportCell') for cell in row] for row in rows], colWidths=widths, repeatRows=1, hAlign='LEFT')
    result.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PALE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), .6, colors.HexColor('#aeaead')),
        ('LINEBELOW', (0, 1), (-1, -1), .25, colors.HexColor('#dcdfd8')),
    ]))
    return result


def build(story, title):
    output = BytesIO()
    document = SimpleDocTemplate(output, pagesize=A4, leftMargin=46, rightMargin=46, topMargin=42, bottomMargin=43,
                                 title=title, author='VFI simulation')
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT, 9)
        canvas.setFillColor(colors.HexColor('#3a3b3a'))
        canvas.drawString(46, 23, 'VFI simulation | ' + title[:70])
        canvas.drawRightString(A4[0]-46, 23, str(doc.page))
        canvas.restoreState()
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    return output.getvalue()


def decision_source(reason):
    return {'decision':'Company decision', 'executive_override':'CEO override',
            'deadline':'Default applied when time expired', 'facilitator_skip':'Year skipped by the teacher'}.get(reason, reason)


def stage_label(key):
    year, phase = key.split(':', 1)
    label = {'decision':'Decision discussion', 'event':'Company update', 'checkpoint':'Checkpoint', 'report':'Final reflection'}.get(phase, phase)
    return f'Year {year} - {label}'


def case_document(doc):
    if not doc:return []
    lines=[paragraph(doc['title'], 'ReportHeading'),paragraph(doc['sender'], 'ReportSmall')]
    lines += [paragraph(text) for text in doc['body']]
    lines += [paragraph(text) for text in doc.get('follow_up',[])]
    if doc.get('callback'):lines.append(paragraph(doc['callback']))
    if doc.get('rows'):lines.append(table(doc['rows'],[200,303]))
    lines.append(paragraph('Fictional VFI simulation case material; audio transcript included where available.', 'ReportSmall'))
    return lines


def company_pdf(companies, session_title, content, personal=None, participants=None):
    story = []
    if not companies:
        story = [paragraph('Company decisions and outcomes', 'ReportTitle'), paragraph(session_title), paragraph('No companies have joined yet.')]
    for index, company in enumerate(companies):
        if index: story.append(PageBreak())
        status = 'Complete' if company['complete'] else f'In progress at Year {company["year"]}'
        story += [paragraph(company['name'], 'ReportTitle'), paragraph('Company decisions and outcomes', 'ReportHeading'),
                  paragraph(f'{session_title} | {company["country"]} | {status}', 'ReportSmall')]
        if not company['decisions']:
            story.append(paragraph('No company decisions have been recorded yet.'))
        for year, decision in sorted(company['decisions'].items(), key=lambda item: int(item[0])):
            y = int(year)
            year_content = content['years'][y]
            option = next(o for o in year_content['options'] if o['id'] == decision['option'])
            story += [paragraph(f'Year {year} - {year_content["theme"]}', 'ReportHeading'),
                      paragraph(option['title']), paragraph(MODEL['rules'][str(y)][decision['option']]['consequence'] if decision['reason'] not in ('deadline','facilitator_skip') else 'The team agreed no new action this year. The company continued its existing service, prices, contracts and duties.'),
                      paragraph(decision_source(decision['reason']), 'ReportSmall')]
            events = [h for h in company['history'] if h['type'] == 'event' and h['year'] == y]
            if company.get('current_event') and company['current_event']['year'] == y:
                events.append(company['current_event'])
            # A facilitator skip must not print the same update twice.
            seen = set()
            for event in events:
                marker = (event.get('title'), event.get('update'))
                if marker in seen: continue
                seen.add(marker)
                story += case_document(company.get('story',{}).get('records',{}).get(str(y)))
                story += [paragraph(event['title'], 'ReportHeading'), paragraph(event.get('update') or content['events'][y]['story'])]
        story += case_document(company.get('story',{}).get('records',{}).get('10'))
        story += [paragraph(f'Company position at Year {company["year"]}', 'ReportHeading'), paragraph(company['context'])]
        if company['interventions']:
            story.append(paragraph('Recorded role actions', 'ReportHeading'))
            for action in company['interventions']:
                story.append(paragraph(f'Year {action["year"]} - {content["roles"][action["role"]][0]}: {action["reason"]}'))
        performance=company.get('performance')
        if performance:
            position=performance['state']
            story += [paragraph('Simulated company performance', 'ReportHeading'),
                paragraph(f"Market presence {position['growth']:.0f} (relative business size, start 100); trust {position['trust']:.0f}/100; original rollout venues {position['contracts']}; new partnerships {position['new_partners']}; compulsory redundancies in the rollout team {position['redundancies']}."),
                paragraph(f"Cash EUR {position['cash']:,.0f}k; debt EUR {position['debt']:,.0f}k. Financially operational: {'yes' if performance['viable'] else 'no'}." )]
            for name,met in performance['commitments'].items():
                story.append(paragraph(f"{name}: {('target met' if met else 'target not met') if performance['final'] else ('target currently met' if met else 'target remains open')}. {performance['targets'][name]}"))
        story.append(paragraph('These figures come from the fictional simulation. Company performance and private mission success do not determine grades.', 'ReportSmall'))
    if personal:
        story += [PageBreak(), paragraph(personal['name'], 'ReportTitle'), paragraph(personal['role'], 'ReportHeading'),
                  paragraph('Your reflections', 'ReportHeading')]
        if personal.get('mission'):
            story.append(paragraph(personal['mission']))
            story.append(paragraph(personal.get('mission_outcome','Your mission is evaluated after Year 10.')))
            story += case_document(personal.get('closing_message'))
        notes = [(key,note) for key,note in personal['notes'].items() if note['text'].strip()]
        if not notes: story.append(paragraph('No reflections have been saved.'))
        for key, note in sorted(notes, key=lambda item: (int(item[0].split(':')[0]), item[1]['saved'])):
            story += [paragraph(stage_label(key), 'ReportHeading'), paragraph(note['text'])]
    if participants is not None:
        story += [PageBreak()] + participation_story(participants, session_title)
    return build(story, session_title)


def participation_story(rows, session_title):
    story = [paragraph('Participation record', 'ReportTitle'), paragraph(session_title),
             paragraph('Recorded reflections and role actions are evidence saved in the exercise. They do not measure everything said in the discussion or determine a grade.', 'ReportSmall')]
    if not rows: story.append(paragraph('No students have joined yet.'))
    else:
        summary = [['Name', 'Company', 'Role', 'Saved work']]
        summary += [[r['name'], r['company'], r['role'],
                     f'{r["reflections_saved"]} reflection'+('' if r['reflections_saved']==1 else 's')+'\n'+
                     f'{len(r["actions"])} role action'+('' if len(r['actions'])==1 else 's')] for r in rows]
        story.append(table(summary, [112, 115, 155, 121]))
        story.append(PageBreak())
        for i, row in enumerate(rows):
            if i: story.append(Spacer(1, 12))
            student = [paragraph(row['name'], 'ReportHeading'), paragraph(f'{row["company"]} | {row["role"]}')]
            for action in row['actions']:
                student.append(paragraph(action))
            if not row['actions']: student.append(paragraph('No role action recorded.', 'ReportSmall'))
            for note in row['reflections']:
                student += [paragraph(stage_label(note['stage']), 'ReportHeading'), paragraph(note['text'])]
            if not row['reflections']: student.append(paragraph('No reflections saved.', 'ReportSmall'))
            story.extend(student)
    return story


def participation_pdf(rows, session_title):
    return build(participation_story(rows, session_title), 'Participation record')
