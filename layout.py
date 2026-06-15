import streamlit as st
from helpers import score_color, score_grade, progress_bar_html
from components import (
    score_ring_html,
    mini_card_html,
    insight_card_html,
    skill_tags_html,
    card_html,
)


def render_results(result: dict) -> None:
    st.markdown('<hr style="border:none;border-top:1px solid #2d3250;margin:24px 0">',
                unsafe_allow_html=True)

    ats = result.get("ats_score", 0)
    kw  = result.get("keyword_match_score", 0)
    fmt = result.get("format_score", 0)
    exp = result.get("experience_match_score", 0)
    missing_count = len(result.get("skills_missing", []))
    grade, grade_color = score_grade(ats)

    # ── Score Row ──────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns([1.4, 1, 1, 1, 1], gap="medium")
    with c1:
        st.markdown(score_ring_html(ats, score_color(ats), grade, grade_color),
                    unsafe_allow_html=True)
    for col, label, val in zip(
        [c2, c3, c4],
        ["Keyword Match", "Format Score", "Experience Match"],
        [kw, fmt, exp],
    ):
        with col:
            st.markdown(mini_card_html(val, label, score_color(val)),
                        unsafe_allow_html=True)
    with c5:
        st.markdown(mini_card_html(missing_count, "Missing Skills", "#ff6b6b"),
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary ────────────────────────────────────────────────────────
    summary = result.get("summary", "")
    if summary:
        body = f'<p style="color:#c8ccd8;line-height:1.7;margin:0">{summary}</p>'
        st.markdown(card_html("🧠 AI Summary", body), unsafe_allow_html=True)

    # ── Skills Found / Missing ─────────────────────────────────────────
    s1, s2 = st.columns(2, gap="medium")
    with s1:
        found = result.get("skills_found", [])
        tags = skill_tags_html(found, "tag-found", "✓ ")
        body = f'<div class="tag-grid">{tags}</div>' if tags else '<span style="color:#8b90a7">None detected</span>'
        st.markdown(card_html(f"✅ Skills Found ({len(found)})", body),
                    unsafe_allow_html=True)
    with s2:
        missing = result.get("skills_missing", [])
        tags = skill_tags_html(missing, "tag-missing", "✗ ")
        body = f'<div class="tag-grid">{tags}</div>' if tags else '<span style="color:#00d4aa">None missing!</span>'
        st.markdown(card_html(f"❌ Missing Skills ({len(missing)})", body),
                    unsafe_allow_html=True)

    # ── Keywords ───────────────────────────────────────────────────────
    k1, k2 = st.columns(2, gap="medium")
    with k1:
        kws = result.get("keywords_found", [])
        tags = skill_tags_html(kws, "tag-neutral")
        body = f'<div class="tag-grid">{tags}</div>' if tags else "—"
        st.markdown(card_html("🔑 ATS Keywords Found", body), unsafe_allow_html=True)
    with k2:
        kmiss = result.get("keywords_missing", [])
        tags = skill_tags_html(kmiss, "tag-missing")
        body = f'<div class="tag-grid">{tags}</div>' if tags else '<span style="color:#00d4aa">All covered!</span>'
        st.markdown(card_html("🔍 Keywords to Add", body), unsafe_allow_html=True)

    # ── Score Breakdown ────────────────────────────────────────────────
    st.markdown('<div class="sec-hd">📊 Score Breakdown</div>', unsafe_allow_html=True)
    for label, val in [
        ("ATS Overall Score", ats),
        ("Keyword Match", kw),
        ("Format & Structure", fmt),
        ("Experience Match", exp),
    ]:
        color = score_color(val)
        st.markdown(
            f'<div style="margin-bottom:4px;display:flex;justify-content:space-between">'
            f'<span style="font-size:0.9rem;color:#c8ccd8">{label}</span>'
            f'<span style="font-size:0.9rem;font-weight:600;color:{color}">{val}/100</span>'
            f'</div>{progress_bar_html(val, color)}',
            unsafe_allow_html=True,
        )

    # ── Strengths & Weaknesses ─────────────────────────────────────────
    sw1, sw2 = st.columns(2, gap="medium")
    with sw1:
        items = "".join(
            f'<div class="sug-item">💪 {s}</div>'
            for s in result.get("strengths", [])
        )
        body = items or '<p style="color:#8b90a7">No strengths detected</p>'
        st.markdown(card_html("💡 Strengths", body), unsafe_allow_html=True)
    with sw2:
        items = "".join(
            f'<div class="sug-warn">⚠️ {w}</div>'
            for w in result.get("weaknesses", [])
        )
        body = items or '<p style="color:#8b90a7">No weaknesses found</p>'
        st.markdown(card_html("⚠️ Weaknesses", body, title_color="#ff6b6b"),
                    unsafe_allow_html=True)

    # ── Suggestions ────────────────────────────────────────────────────
    st.markdown('<div class="sec-hd">🛠️ Improvement Suggestions</div>',
                unsafe_allow_html=True)
    for i, sug in enumerate(result.get("suggestions", []), 1):
        st.markdown(
            f'<div class="sug-item">'
            f'<span style="color:#6c63ff;font-weight:700;margin-right:10px">#{i}</span>{sug}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Deeper Insights ────────────────────────────────────────────────
    st.markdown('<div class="sec-hd">🔎 Deeper Insights</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3, gap="medium")
    for col, icon, title, key in [
        (d1, "🎯", "Job Title Match",  "job_title_match"),
        (d2, "📅", "Experience Gap",   "experience_gap"),
        (d3, "🎓", "Education Match",  "education_match"),
    ]:
        with col:
            st.markdown(
                insight_card_html(icon, title, result.get(key, "Not analyzed")),
                unsafe_allow_html=True,
            )

    # ── Recommended Sections ───────────────────────────────────────────
    recs = result.get("recommended_sections", [])
    if recs:
        tags = skill_tags_html(recs, "tag-neutral", "+ ")
        body = f'<div class="tag-grid">{tags}</div>'
        st.markdown("<br>" + card_html("📌 Recommended Sections to Add/Improve", body),
                    unsafe_allow_html=True)