def score_color(score: int) -> str:
    if score >= 80:
        return "#00d4aa"
    if score >= 60:
        return "#6c63ff"
    if score >= 40:
        return "#ffb347"
    return "#ff6b6b"


def score_grade(score: int):
    if score >= 85:
        return ("Excellent", "#00d4aa")
    if score >= 70:
        return ("Good", "#6c63ff")
    if score >= 55:
        return ("Average", "#ffb347")
    if score >= 40:
        return ("Needs Work", "#ff8c42")
    return ("Poor", "#ff6b6b")


def progress_bar_html(pct: int, color: str) -> str:
    return f"""
    <div class="prog-bar-wrap">
        <div class="prog-bar-fill" style="width:{pct}%;background:{color}"></div>
    </div>"""