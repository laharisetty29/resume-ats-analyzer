<img width="1366" height="613" alt="ats-checker" src="https://github.com/user-attachments/assets/fe530297-1e09-4d38-80a2-025d320c7c84" /># 📄 Resume ATS Analyzer

An AI-powered web app that analyzes your resume against a job description and gives you an ATS compatibility score, missing skills, and tailored improvement tips — instantly.

---

## 🚀 Live Demo

👉 [Try it here](https://resume-ats-analyzer-vclgbvwcvmpwfqugnxmzju.streamlit.app/)

---

## ✨ Features

- ✅ ATS Score (0–100) with grade badge
- 🔑 Keyword match, format, and experience sub-scores
- 💚 Skills found vs ❌ missing — color-coded tags
- 📊 Visual score breakdown with progress bars
- 💡 Strengths and ⚠️ weaknesses analysis
- 🛠️ 5–7 specific, actionable improvement suggestions
- 🎯 Job title match, experience gap, and education fit insights
- 📌 Recommended resume sections to add or improve
- 📄 Supports PDF, DOCX, and TXT resume uploads

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| AI Model | LLaMA 3.3 70B via Groq API |
| Resume Parsing | PyPDF2, python-docx |
| Styling | Custom CSS (dark theme) |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure

```bash
resume_ats_analyzer/

├── app.py            # Main entry point

├── analyzer.py       # Groq AI analysis logic

├── extractor.py      # PDF / DOCX / TXT text extraction

├── layout.py         # Streamlit result rendering

├── components.py     # Reusable HTML components

├── styles.py         # All CSS styles

├── helpers.py        # Score colors, grades, progress bars

├── requirements.txt  # Dependencies

└── .env              # API key (local only, not in GitHub)

```

---

## ⚙️ Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/resume-ats-analyzer.git
cd resume-ats-analyzer
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key_here
```
> 🔑 Get your **free** Groq API key at [console.groq.com](https://console.groq.com) — no credit card needed.

### 5. Run the app
```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file as `app.py`
5. Go to **Advanced Settings → Secrets** and add:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
6. Click **Deploy** ✅

---

## 🔑 Get Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google or email (no card needed)
3. Click **API Keys** → **Create API Key**
4. Copy and paste into your `.env` file or Streamlit secrets

---

## 📄 License

MIT License — free to use, modify, and distribute.


