GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

:root {
    --bg:      #0f1117;
    --card:    #21263a;
    --accent:  #6c63ff;
    --accent2: #00d4aa;
    --warn:    #ff6b6b;
    --text:    #e8eaf0;
    --muted:   #8b90a7;
    --border:  #2d3250;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
}
.stApp { background: var(--bg); }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

.hero {
    background: linear-gradient(135deg, #1a1d27 0%, #21263a 50%, #1a1d27 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 48px 40px;
    margin-bottom: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6c63ff, #00d4aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}
.hero p { color: var(--muted); font-size: 1.05rem; margin: 0; }

.score-ring {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px 24px;
    text-align: center;
}
.score-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 5rem;
    font-weight: 700;
    line-height: 1;
}
.score-label {
    color: var(--muted);
    font-size: 0.9rem;
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.grade-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 0.95rem;
    margin-top: 14px;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
}
.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 16px;
}

.tag-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { padding: 5px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 500; }
.tag-found   { background: rgba(0,212,170,0.15);  color: #00d4aa; border: 1px solid rgba(0,212,170,0.3); }
.tag-missing { background: rgba(255,107,107,0.12); color: #ff6b6b; border: 1px solid rgba(255,107,107,0.3); }
.tag-neutral { background: rgba(108,99,255,0.12);  color: #9d97ff; border: 1px solid rgba(108,99,255,0.3); }

.prog-bar-wrap {
    background: var(--border);
    border-radius: 8px;
    height: 8px;
    width: 100%;
    margin: 6px 0 16px;
}
.prog-bar-fill { height: 8px; border-radius: 8px; }

.sug-item {
    background: rgba(108,99,255,0.07);
    border-left: 3px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 0.93rem;
    line-height: 1.6;
    color: var(--text);
}
.sug-warn {
    background: rgba(255,107,107,0.07);
    border-left: 3px solid #ff6b6b;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 0.93rem;
    line-height: 1.6;
    color: var(--text);
}

.mini-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
}
.mini-val { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; }
.mini-lbl { color: var(--muted); font-size: 0.8rem; margin-top: 4px; }

.sec-hd {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    margin: 28px 0 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

.stFileUploader > div {
    background: var(--card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 14px !important;
}
.stTextArea textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-size: 0.9rem !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #00d4aa) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 0 !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100% !important;
}
#MainMenu, footer, header { visibility: hidden; }
</style>
"""