import re
import json
import os
import time

# ─────────────────────────────────────────────────────────────────────────────
# Load secret from Streamlit Cloud or local .env
# ─────────────────────────────────────────────────────────────────────────────
try:
    import streamlit as st
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass  # Running locally — will read from .env instead

# ─────────────────────────────────────────────────────────────────────────────
# PROMPT TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """
You are an expert ATS (Applicant Tracking System) and career coach AI.
Carefully analyze the resume against the job description provided.

Return ONLY a valid JSON object with this exact structure.
No markdown, no explanation, no code fences, no extra text — raw JSON only.

{{
  "ats_score": <integer 0-100, overall ATS compatibility score>,
  "keyword_match_score": <integer 0-100, how many JD keywords appear in resume>,
  "format_score": <integer 0-100, resume structure and formatting quality>,
  "experience_match_score": <integer 0-100, experience level alignment>,
  "skills_found": [<list of strings: skills from JD that are present in resume>],
  "skills_missing": [<list of strings: important skills from JD absent in resume>],
  "keywords_found": [<list of strings: ATS-relevant keywords present in resume>],
  "keywords_missing": [<list of strings: important ATS keywords missing from resume>],
  "strengths": [<list of 3-5 strings: resume strengths relevant to this job>],
  "weaknesses": [<list of 3-5 strings: resume weaknesses for this specific job>],
  "suggestions": [<list of 5-7 strings: specific actionable improvements to make>],
  "summary": "<string: 2-3 sentence overall assessment of resume fit for this role>",
  "job_title_match": "<string: how well the resume title and experience match the role>",
  "experience_gap": "<string: analysis of years/level of experience vs what JD requires>",
  "education_match": "<string: how well education aligns with job requirements>",
  "recommended_sections": [<list of strings: resume sections to add or significantly improve>]
}}

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{jd_text}
"""


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — Strip markdown fences
# ─────────────────────────────────────────────────────────────────────────────
def _clean_json(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\n?```\s*$", "", raw)
    start = raw.find("{")
    end   = raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start : end + 1]
    return raw.strip()


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — Parse and validate JSON result
# ─────────────────────────────────────────────────────────────────────────────
def _parse_result(raw_text: str) -> dict:
    clean = _clean_json(raw_text)

    try:
        result = json.loads(clean)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"AI returned invalid JSON.\n\nError: {e}\n\nRaw output:\n{raw_text[:600]}"
        )

    # Fill missing keys with safe defaults
    defaults = {
        "ats_score":              0,
        "keyword_match_score":    0,
        "format_score":           0,
        "experience_match_score": 0,
        "skills_found":           [],
        "skills_missing":         [],
        "keywords_found":         [],
        "keywords_missing":       [],
        "strengths":              [],
        "weaknesses":             [],
        "suggestions":            [],
        "summary":                "Analysis complete.",
        "job_title_match":        "Not analyzed.",
        "experience_gap":         "Not analyzed.",
        "education_match":        "Not analyzed.",
        "recommended_sections":   [],
    }
    for key, default in defaults.items():
        if key not in result:
            result[key] = default

    # Clamp scores 0–100
    for score_key in ["ats_score", "keyword_match_score", "format_score", "experience_match_score"]:
        try:
            result[score_key] = max(0, min(100, int(result[score_key])))
        except (TypeError, ValueError):
            result[score_key] = 0

    return result


# ─────────────────────────────────────────────────────────────────────────────
# MAIN FUNCTION — called from app.py
# ─────────────────────────────────────────────────────────────────────────────
def analyze_resume(resume_text: str, jd_text: str) -> dict:
    """
    Analyze resume vs job description using Groq API (free, fast).
    Get your free key at: console.groq.com
    Local:  add GROQ_API_KEY=your_key to .env
    Cloud:  add GROQ_API_KEY in Streamlit secrets dashboard
    """

    # ── Input validation ──────────────────────────────────────────────────────
    if not resume_text or not resume_text.strip():
        raise ValueError(
            "Resume text is empty. "
            "Could not extract text from the uploaded file. "
            "Make sure your PDF is not a scanned image."
        )
    if not jd_text or not jd_text.strip():
        raise ValueError(
            "Job description is empty. Please paste the full job description."
        )

    # ── Check package ─────────────────────────────────────────────────────────
    try:
        from groq import Groq
    except ImportError:
        raise ImportError(
            "groq package is not installed.\n"
            "Run:  pip install groq"
        )

    # ── Check API key ─────────────────────────────────────────────────────────
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found.\n\n"
            "Local setup:\n"
            "  1. Go to console.groq.com\n"
            "  2. Sign up free (no card needed)\n"
            "  3. Click 'API Keys' → 'Create API Key'\n"
            "  4. Add to .env:  GROQ_API_KEY=your_key_here\n"
            "  5. Restart the app\n\n"
            "Streamlit Cloud:\n"
            "  Add GROQ_API_KEY in App Settings → Secrets"
        )

    # ── Build prompt ──────────────────────────────────────────────────────────
    prompt = PROMPT_TEMPLATE.format(
        resume_text=resume_text[:4000],
        jd_text=jd_text[:2000],
    )

    # ── Call Groq API with retry ──────────────────────────────────────────────
    client = Groq(api_key=api_key)
    raw_text    = None
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert ATS analyzer. "
                            "Always respond with valid JSON only. "
                            "No markdown, no explanation, no code fences."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.2,
                max_tokens=2048,
                response_format={"type": "json_object"},
            )

            raw_text = response.choices[0].message.content
            break  # success — exit retry loop

        except Exception as e:
            error_msg = str(e).lower()

            if "api_key" in error_msg or "invalid" in error_msg or "401" in error_msg:
                raise ValueError(
                    "Invalid Groq API key. "
                    "Check your GROQ_API_KEY in .env or Streamlit secrets."
                )

            elif "quota" in error_msg or "rate" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    wait = 30 * (attempt + 1)   # 30s first, 60s second
                    try:
                        import streamlit as st
                        st.warning(
                            f"⏳ Rate limit hit — retrying in {wait}s "
                            f"(attempt {attempt + 1}/{max_retries})..."
                        )
                    except Exception:
                        pass
                    time.sleep(wait)
                    continue
                else:
                    raise ValueError(
                        "Groq API rate limit exceeded after 3 attempts. "
                        "Please wait 1 minute and try again."
                    )

            else:
                raise ValueError(f"Groq API error: {e}")

    if raw_text is None:
        raise ValueError("No response received from Groq after retries.")

    # ── Parse and return ──────────────────────────────────────────────────────
    return _parse_result(raw_text)