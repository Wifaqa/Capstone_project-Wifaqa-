import json
import os
from openai import OpenAI

# client = OpenAI(
#     api_key="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",
#     base_url="https://openrouter.ai/api/v1"
# )

# MODEL = "deepseek/deepseek-chat"

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-4o-mini"  # سريع + ممتاز للتقييم

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

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You extract job requirements as structured JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=400,
    )

    content = response.choices[0].message.content.strip()

    # ✅ CLEAN CODE FENCES
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(content)
    except Exception as e:
        raise ValueError(
            f"Failed to parse JD JSON.\nRaw response:\n{content}"
        ) from e