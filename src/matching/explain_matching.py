# # src/matching/explain_score.py

# from openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv()
# import os
# def explain_score(resume: dict, jd: dict, match_result: dict, score_result: dict) -> str:
#     """
#     يشرح السكور فقط (ما يحسبه).
#     يرجع نص explanation.
#     """

#     # 1) جهّز بيانات بسيطة للـ prompt
#     name = resume.get("full_name", "Candidate")
#     job_title = jd.get("job_title", "Job")
#     fit_score = score_result.get("fit_score", 0)

#     matched_required = match_result.get("required_skills", {}).get("matched", [])
#     missing_required = match_result.get("required_skills", {}).get("missing", [])
#     matched_preferred = match_result.get("preferred_skills", {}).get("matched", [])
#     exp_match = match_result.get("experience", {}).get("match", False)

#     resume_exp = resume.get("years_of_experience")
#     jd_min_exp = jd.get("required", {}).get("min_years_exp")

#     # 2) اكتب prompt بسيط جدًا
#     prompt = f"""
# Explain why this candidate got this fit score.

# Candidate name: {name}
# Job title: {job_title}

# Fit score: {fit_score}

# Matched required skills: {matched_required}
# Missing required skills: {missing_required}
# Matched preferred skills: {matched_preferred}

# Candidate years of experience: {resume_exp}
# Minimum years required: {jd_min_exp}
# Experience match: {exp_match}

# Rules:
# - Do NOT change the score.
# - Do NOT invent skills.
# - Output short bullets only.
# """

#     # 3) نكلم الـ LLM
#     client = OpenAI(
#         api_key=os.getenv("OPENAI_API_KEY"),
#         base_url=os.getenv("OPENAI_BASE_URL")
#     )

#     response = client.chat.completions.create(
#         model="deepseek/deepseek-chat",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0,
#         max_tokens=250
#     )

#     # 4) نرجع النص
#     return response.choices[0].message.content.strip()




# src/matching/explain_score.py

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def explain_score(resume: dict, jd: dict, match_result: dict, score_result: dict) -> str:
    """
    Explains the fit score using existing matching results.
    Does NOT calculate or modify the score.
    """

    # ------------------
    # Basic info
    # ------------------
    name = resume.get("full_name", "Candidate")
    job_title = jd.get("job_title", "Job")
    fit_score = score_result.get("fit_score", 0)

    # ------------------
    # Skills
    # ------------------
    matched_required = match_result["required_skills"]["matched"]
    missing_required = match_result["required_skills"]["missing"]
    matched_preferred = match_result["preferred_skills"]["matched"]

    # ------------------
    # Experience
    # ------------------
    resume_exp = match_result["experience"]["resume_years"]
    required_exp = match_result["experience"]["required_years"]
    experience_match = match_result["experience"]["match"]

    # ------------------
    # Education
    # ------------------
    education = match_result.get("education", {})
    education_level_match = education.get("level_match", False)
    education_field_match = education.get("field_match", False)

    # ------------------
    # Domain knowledge
    # ------------------
    domain = match_result.get("domain_knowledge", {})
    matched_domains = domain.get("matched", [])
    missing_domains = domain.get("missing", [])

    # ------------------
    # Prompt
    # ------------------
    prompt = f"""
Explain why this candidate received this fit score.

Candidate name: {name}
Job title: {job_title}
Final fit score: {fit_score}

Required skills matched: {matched_required}
Required skills missing: {missing_required}
Preferred skills matched: {matched_preferred}

Domain knowledge matched: {matched_domains}
Domain knowledge missing: {missing_domains}

Education level match: {education_level_match}
Education field match: {education_field_match}

Candidate years of experience: {resume_exp}
Minimum required experience: {required_exp}
Experience match: {experience_match}

Rules:
- Do NOT change the score.
- Do NOT invent qualifications.
- Use short bullet points only.
- Base explanation strictly on the data above.
"""

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "system", "content": "You explain recruitment fit scores objectively."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()