import re
import json
import os
from groq import Groq

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


def _clean_json(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\n?```\s*$", "", raw)
    start = raw.find("{")
    end   = raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start : end + 1]
    return raw.strip()


def _parse_result(raw_text: str) -> dict:
    clean = _clean_json(raw_text)
    try:
        result = json.loads(clean)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from AI.\n\nError: {e}\n\nRaw:\n{raw_text[:600]}")

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

    for score_key in ["ats_score", "keyword_match_score", "format_score", "experience_match_score"]:
        try:
            result[score_key] = max(0, min(100, int(result[score_key])))
        except (TypeError, ValueError):
            result[score_key] = 0

    return result


def analyze_resume(resume_text: str, jd_text: str) -> dict:
    """
    Analyze resume using Groq API (free, fast, no rate limits).
    Get free key at: console.groq.com
    Add to .env:  GROQ_API_KEY=your_key_here
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty. Make sure your PDF is not a scanned image.")
    if not jd_text or not jd_text.strip():
        raise ValueError("Job description is empty.")

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in .env file.\n"
            "1. Go to console.groq.com\n"
            "2. Sign up free (no card needed)\n"
            "3. Click 'API Keys' → 'Create API Key'\n"
            "4. Add to .env:  GROQ_API_KEY=your_key_here\n"
            "5. Restart the app"
        )

    client = Groq(api_key=api_key)

    prompt = PROMPT_TEMPLATE.format(
        resume_text=resume_text[:4000],
        jd_text=jd_text[:2000],
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # Free, powerful model on Groq
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS analyzer. Always respond with valid JSON only. No markdown, no explanation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=2048,
            response_format={"type": "json_object"},  # Forces pure JSON output
        )

        raw_text = response.choices[0].message.content
        return _parse_result(raw_text)

    except Exception as e:
        error_msg = str(e).lower()
        if "api_key" in error_msg or "invalid" in error_msg or "401" in error_msg:
            raise ValueError("Invalid Groq API key. Check GROQ_API_KEY in your .env file.")
        elif "quota" in error_msg or "rate" in error_msg or "429" in error_msg:
            raise ValueError("Groq rate limit hit. Wait 30 seconds and try again.")
        else:
            raise ValueError(f"Groq API error: {e}")