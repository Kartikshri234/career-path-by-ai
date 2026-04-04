from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ..models import ScreeningSession


def download_report(request, token):
    session = get_object_or_404(ScreeningSession, share_token=token)
    results = session.results.order_by('rank')

    try:
        import fitz as _fitz

        doc = _fitz.open()
        m = 50
        pw, ph = 595, 842

        c_brand = (0.318, 0.42, 0.925)
        c_emerald = (0.204, 0.831, 0.6)
        c_amber = (0.98, 0.749, 0.141)
        c_rose = (0.984, 0.443, 0.522)
        c_cyan = (0.133, 0.827, 0.933)
        c_dark = (0.059, 0.078, 0.118)
        c_mid = (0.58, 0.639, 0.722)
        c_light = (0.945, 0.961, 0.988)
        c_white = (1, 1, 1)

        def new_page():
            p = doc.new_page(width=pw, height=ph)
            p.draw_rect(_fitz.Rect(0, 0, pw, ph), color=None, fill=c_dark)
            return p

        def sc(tier):
            return {'A': c_emerald, 'B': c_cyan, 'C': c_amber, 'D': c_rose}.get(tier, c_mid)

        # Cover page.
        page = new_page()
        page.draw_rect(_fitz.Rect(0, 0, pw, 120), color=None, fill=(0.07, 0.09, 0.22))
        page.draw_line(_fitz.Point(0, 120), _fitz.Point(pw, 120), color=c_brand, width=2)
        page.insert_text((m, 52), 'CareerCompass', fontsize=22, color=c_white, fontname='helv')
        page.insert_text((m, 80), 'Resume Screening Report', fontsize=13, color=c_mid, fontname='helv')

        y = 148
        jd_preview = (session.job_description[:200] + '...') if len(session.job_description) > 200 else session.job_description
        page.insert_text((m, y), 'Job Description (preview):', fontsize=9, color=c_mid, fontname='helv')
        y += 18
        words, line, lines = jd_preview.split(), [], []
        for w in words:
            line.append(w)
            if len(' '.join(line)) > 85:
                lines.append(' '.join(line[:-1]))
                line = [w]
        if line:
            lines.append(' '.join(line))
        for l in lines[:6]:
            page.insert_text((m, y), l, fontsize=9, color=c_light, fontname='helv')
            y += 14

        y += 12
        for label, val in [
            ('Resumes Screened', str(session.resume_count)),
            ('Screening Date', session.created_at.strftime('%d %b %Y, %I:%M %p')),
            ('Top Score', f'{results.first().score:.1f}%' if results.exists() else '-'),
        ]:
            page.insert_text((m, y), f'{label}:', fontsize=9, color=c_mid, fontname='helv')
            page.insert_text((220, y), val, fontsize=9, color=c_white, fontname='helv')
            y += 18

        y += 20
        page.draw_line(_fitz.Point(m, y), _fitz.Point(pw - m, y), color=c_brand, width=0.5)
        y += 14
        page.insert_text((m, y), 'Ranked Results', fontsize=13, color=c_white, fontname='helv')
        y += 22

        cols = [m, 80, 240, 330, 420, 480]
        for i, h in enumerate(['#', 'Filename', 'Match', 'Grade', 'ATS', 'Keywords']):
            page.insert_text((cols[i], y), h, fontsize=8, color=c_mid, fontname='helv')
        y += 4
        page.draw_line(_fitz.Point(m, y + 4), _fitz.Point(pw - m, y + 4), color=(0.2, 0.23, 0.38), width=0.5)
        y += 14

        for r in results:
            if y > ph - 80:
                page = new_page()
                y = 80
            color = sc(r.strength_tier)
            total_kw = len(r.matched_keywords) + len(r.missing_keywords)
            for i, val in enumerate([
                str(r.rank),
                r.filename[:28],
                f'{r.score:.1f}%',
                r.strength_tier,
                f'{r.ats_score}%',
                f'{len(r.matched_keywords)}/{total_kw}',
            ]):
                page.insert_text((cols[i], y), val, fontsize=8, color=(color if i in (2, 3) else c_light), fontname='helv')
            y += 16

        # Per-resume detail pages.
        for r in results:
            page = new_page()
            page.draw_rect(_fitz.Rect(0, 0, pw, 90), color=None, fill=(0.07, 0.09, 0.22))
            color = sc(r.strength_tier)
            page.draw_line(_fitz.Point(0, 90), _fitz.Point(pw, 90), color=color, width=2)
            page.insert_text((m, 34), f'#{r.rank}  {r.filename}', fontsize=14, color=c_white, fontname='helv')
            page.insert_text((m, 58), f'{r.strength_emoji}  {r.strength_label}', fontsize=10, color=color, fontname='helv')
            page.insert_text((pw - 110, 38), f'{r.score:.1f}%', fontsize=22, color=color, fontname='helv')
            page.insert_text((pw - 110, 62), 'Similarity', fontsize=8, color=c_mid, fontname='helv')

            y = 116

            def section(title):
                nonlocal y
                page.insert_text((m, y), title, fontsize=9, color=c_mid, fontname='helv')
                y += 4
                page.draw_line(_fitz.Point(m, y + 4), _fitz.Point(pw - m, y + 4), color=(0.2, 0.23, 0.38), width=0.4)
                y += 16

            section('Score Breakdown')
            for label, val, clr in [
                ('Similarity', r.score, c_brand),
                ('ATS Score', r.ats_score, c_emerald),
                ('Keyword Coverage', r.kw_score, c_cyan),
                ('Skill Match', r.skill_score, c_amber),
            ]:
                page.insert_text((m, y), label + ':', fontsize=8, color=c_mid, fontname='helv')
                page.insert_text((200, y), f'{val:.0f}%', fontsize=8, color=c_white, fontname='helv')
                fill_w = max(4, int(340 * min(val, 100) / 100))
                page.draw_rect(_fitz.Rect(m, y + 4, m + 340, y + 10), color=None, fill=(0.2, 0.23, 0.38))
                page.draw_rect(_fitz.Rect(m, y + 4, m + fill_w, y + 10), color=None, fill=clr)
                y += 22

            y += 6
            section('Matched Skills')
            page.insert_text((m, y), '  '.join(r.matched_skills[:12]) or 'None', fontsize=8, color=c_emerald, fontname='helv')
            y += 18
            section('Missing Skills')
            page.insert_text((m, y), '  '.join(r.missing_skills[:12]) or 'None', fontsize=8, color=c_rose, fontname='helv')
            y += 18

            page.draw_line(_fitz.Point(m, ph - 40), _fitz.Point(pw - m, ph - 40), color=(0.2, 0.23, 0.38), width=0.4)
            page.insert_text((m, ph - 24), 'Generated by CareerCompass - AI-Powered Career Guidance', fontsize=7, color=c_mid, fontname='helv')

        pdf_bytes = doc.tobytes()
        resp = HttpResponse(pdf_bytes, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="screening_report_{session.share_token}.pdf"'
        return resp

    except Exception as e:
        return HttpResponse(f'PDF generation failed: {e}', status=500)
