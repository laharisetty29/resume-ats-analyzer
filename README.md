# Resume ATS Analyzer

AI-powered Resume ATS Analyzer built with Streamlit. This app analyzes a resume against a job description and gives an ATS score, missing skills, matched skills, and improvement suggestions.

## Live Demo

🔗 Streamlit App: https://resume-ats-analyzer-vclgbvwcvmpwfqugnxmzju.streamlit.app/

## Features

- Upload resume in PDF, DOCX, or TXT format
- Paste job description
- Generate ATS compatibility score
- Identify matched and missing skills
- Get resume improvement suggestions
- Simple Streamlit web interface
- AI-powered analysis using Groq LLaMA model

## Tech Stack

- Python
- Streamlit
- Groq API
- LLaMA 3.3 70B
- PyPDF2
- python-docx
- dotenv

## Project Structure

```text
resume-ats-analyzer/
│
├── app.py
├── analyzer.py
├── extractor.py
├── layout.py
├── components.py
├── helpers.py
├── styles.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation
```bash
git clone https://github.com/laharisetty29/resume-ats-analyzer.git
cd resume-ats-analyzer
pip install -r requirements.txt
```

## Add API Key

### Create a .env file:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Run Locally
```bash
streamlit run app.py
```

## How It Works
- User uploads a resume
- User pastes the job description
- The app extracts resume text
- AI compares resume with job requirements
- App displays ATS score, matched skills, missing skills, and suggestions


## Author

** Lahari Gadamsetty **

GitHub: https://github.com/laharisetty29
LinkedIn: https://www.linkedin.com/in/laharigadamsetty


## License

This project is for learning and portfolio purposes.
