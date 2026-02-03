# import json
# import os
# from openai import OpenAI

# # client = OpenAI(
# #     api_key="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",
# #     base_url="https://openrouter.ai/api/v1"
# # )

# # MODEL = "deepseek/deepseek-chat"

# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# MODEL = "gpt-4o-mini"  

# def extract_jd_to_json(jd_text: str) -> dict:
#     prompt = f"""
# You are an HR analyst.

# Extract structured information from the following job description.

# Rules:
# 1. Identify REQUIRED skills.
# 2. Identify PREFERRED (nice-to-have) skills if mentioned.
# 3. Extract minimum years of experience if stated.
# 4. Normalize skills to lowercase.
# 5. Output ONLY valid JSON.

# Schema:
# {{
#   "job_title": "string",
#   "seniority_level": "junior|mid|senior|lead|null",
#   "required": {{
#     "skills": ["string"],
#     "tools": ["string"],
#     "domain_knowledge": ["string"],
#     "min_years_exp": "number or null",
#     "education_level": "string or null",
#     "degree_fields": ["string"],
#     "languages": ["string"]
#   }},
#   "preferred": {{
#     "skills": ["string"],
#     "tools": ["string"],
#     "certifications": ["string"],
#     "industry_exp": ["string"]
#   }},
#   "responsibilities": ["string"],
#   "keywords": ["string"]
# }}

# Job Description:
# \"\"\"
# {jd_text}
# \"\"\"
# """

#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You extract job requirements as structured JSON."},
#             {"role": "user", "content": prompt},
#         ],
#         temperature=0,
#         max_tokens=400,
#     )

#     content = response.choices[0].message.content.strip()

#     # ✅ CLEAN CODE FENCES
#     content = content.replace("```json", "").replace("```", "").strip()

#     try:
#         return json.loads(content)
#     except Exception as e:
#         raise ValueError(
#             f"Failed to parse JD JSON.\nRaw response:\n{content}"
#         ) from e


import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def _strip_code_fences(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    # remove triple backticks fences
    text = text.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
    return text


def extract_jd_to_json(jd_text: str) -> dict:
    prompt = f"""
You are an HR analyst.

Extract structured information from the following job description.

Rules:
1. Identify REQUIRED skills.
2. Identify PREFERRED (nice-to-have) skills if mentioned.
3. Extract minimum years of experience if stated.
4. Normalize skills to lowercase.
5. Output ONLY valid JSON.

Schema:
{{
  "job_title": "string",
  "seniority_level": "junior|mid|senior|lead|null",
  "required": {{
    "skills": ["string"],
    "tools": ["string"],
    "domain_knowledge": ["string"],
    "min_years_exp": "number or null",
    "education_level": "string or null",
    "degree_fields": ["string"],
    "languages": ["string"]
  }},
  "preferred": {{
    "skills": ["string"],
    "tools": ["string"],
    "certifications": ["string"],
    "industry_exp": ["string"]
  }},
  "responsibilities": ["string"],
  "keywords": ["string"]
}}

Job Description:
\"\"\"
{jd_text}
\"\"\"
"""

    # ✅ أهم تعديل: أجبر الموديل يرجّع JSON
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You extract job requirements as structured JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=700,
        response_format={"type": "json_object"},  # ✅ هذا يخلي الرد JSON فقط
    )

    content = (response.choices[0].message.content or "").strip()
    content = _strip_code_fences(content)

    # ✅ اطبع raw content في logs عشان لو خرب نعرف السبب
    print("====== JD RAW MODEL OUTPUT START ======")
    print(content)
    print("====== JD RAW MODEL OUTPUT END ======")

    # ✅ Parse
    try:
        data = json.loads(content)
    except Exception as e:
        raise ValueError(
            "Failed to parse JD JSON. Check logs for raw output."
        ) from e

    # ✅ Validation بسيطة (اختياري لكن مفيد)
    if "required" not in data or "preferred" not in data:
        raise ValueError("JD JSON missing required/preferred keys. Check logs.")

    return data