

import json
import os
from openai import OpenAI
import re



from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-4o-mini"  


def safe_json_parse(text: str) -> list[str]:
    cleaned = re.sub(r"```json|```", "", text).strip()
    return json.loads(cleaned)

def normalize_skills_llm(skills: list[str]) -> list[str]:

    prompt = f"""
You are an expert HR skill extraction and normalization system.

Your task:
Extract ATOMIC, individual skills from the list below.

Rules:
1. Split combined skills into individual skills.
   - Handle separators like: ",", "and", "&", "|"
2. Remove category labels such as:
   - "Programming Languages:"
   - "Frameworks:"
   - "Tools:"
   - "Web Development:"
3. Do NOT keep full sentences or descriptions.
4. Normalize skill names:
   - lowercase
   - normalize common tools (e.g., "VS Code" → "vs code")
5. Do NOT invent or infer skills.
6. Keep both technical and soft skills if explicitly present.
7. Remove duplicates.
8. Each output item must be a single skill only.
9. Output ONLY a valid JSON array of strings. No explanations.

Input skills:
{skills}

Example:
Input:
["Programming Languages: Java and Python."]


Output:
["java", "python"]
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You normalize skill lists."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=300,
    )

    content = response.choices[0].message.content.strip()

    # Safety parse
    try:
        return safe_json_parse(content)
    except Exception:
        return [s.lower() for s in skills]