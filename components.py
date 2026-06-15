def hero_html() -> str:
    return """
    <div class="hero">
        <h1>📄 Resume ATS Analyzer</h1>
        <p>Upload your resume and paste the job description to get your ATS score,
           missing skills, and tailored improvement tips.</p>
    </div>"""


def score_ring_html(score: int, color: str, grade: str, grade_color: str) -> str:
    return f"""
    <div class="score-ring">
        <div class="score-number" style="color:{color}">{score}</div>
        <div class="score-label">ATS Score</div>
        <div class="grade-badge"
             style="background:rgba(108,99,255,0.15);color:{grade_color}">{grade}</div>
    </div>"""


def mini_card_html(value, label: str, color: str) -> str:
    return f"""
    <div class="mini-card">
        <div class="mini-val" style="color:{color}">{value}</div>
        <div class="mini-lbl">{label}</div>
    </div>"""


def insight_card_html(icon: str, title: str, body: str) -> str:
    return f"""
    <div class="mini-card" style="text-align:left;padding:20px">
        <div style="font-size:1.4rem;margin-bottom:8px">{icon}</div>
        <div style="font-size:0.75rem;color:#8b90a7;text-transform:uppercase;
                    letter-spacing:1px;margin-bottom:8px">{title}</div>
        <div style="font-size:0.9rem;color:#c8ccd8;line-height:1.5">{body}</div>
    </div>"""


def skill_tags_html(skills: list, tag_class: str, prefix: str = "") -> str:
    if not skills:
        return ""
    return "".join(f'<span class="tag {tag_class}">{prefix}{s}</span>' for s in skills)


def card_html(title: str, body_html: str, title_color: str = "var(--accent)") -> str:
    return f"""
    <div class="card">
        <div class="card-title" style="color:{title_color}">{title}</div>
        {body_html}
    </div>"""