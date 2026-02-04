

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-4o-mini"  


REASON_SYSTEM = """
You are an expert recruiter.
Score candidate fit for the job using a strict rubric and return ONLY JSON.

Rubric (total 100):
Skills match (0-40): must-have + nice-to-have coverage and specificity.
Experience relevance (0-25): relevant roles, responsibilities, domain similarity.
Projects impact (0-20): relevance, complexity, measurable outcomes.
Tools/stack fit (0-10): stack overlap beyond basic skills.
Education/certifications (0-5): relevant degree/certs.

Rules:
Be discriminative: if two candidates are similar, scores must still reflect small differences.
Penalize missing MUST requirements heavily.
If missing 3+ core must-have technical requirements, fit_score MUST be <= 50.
Do not invent info. Use only provided text.

Return JSON with:
{
 "fit_score": number,
 "rubric": {
   "skills": number,
   "experience": number,
   "projects": number,
   "tools": number,
   "education": number
 },
 "matched_skills": [string],
 "missing_skills": [string],
 "strengths": [string],
 "concerns": [string],
 "one_sentence_summary": string
}
"""


def llm_compare(job_req: dict, resume_text: str) -> dict:
    print("DEBUG: LLM CALLED")

    user_prompt = f"""
Job requirements:
{json.dumps(job_req, indent=2)}

Candidate profile:
{resume_text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": REASON_SYSTEM},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        result = json.loads(content)

        return {
            "fit_score": float(result.get("fit_score", 0)),
            "rubric": result.get("rubric", {}),
            "matched_skills": result.get("matched_skills", []),
            "missing_skills": result.get("missing_skills", []),
            "strengths": result.get("strengths", []),
            "concerns": result.get("concerns", []),
            "summary": result.get("one_sentence_summary", "")
        }

    except Exception as e:
        print("❌ LLM ERROR:", e)
        return {
            "fit_score": 0,
            "rubric": {},
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "concerns": ["LLM response could not be parsed"],
            "summary": ""
        }