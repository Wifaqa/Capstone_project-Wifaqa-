# from typing import List
# import re
# Skill_map = {
#     "python": ["python", "python3", "py"],
#     "java": ["java", "jdk", "jre"],
#     "javascript": ["javascript", "js"],
#     "c++": ["c++", "cpp"],
#     "c#": ["c#", "csharp"],
#     "ruby": ["ruby", "rb"],
#     "php": ["php"],
#     "html": ["html", "html5"],
#     "css": ["css", "css3"],
#     "sql": ["sql", "mysql", "postgresql", "sqlite"],
#     "aws": ["aws", "amazon web services"],
#     "docker": ["docker", "containerization"],
#     "kubernetes": ["kubernetes", "k8s"],
#     "react": ["react", "reactjs"],
#     "angular": ["angular", "angularjs"],
#     "vue.js": ["vue.js", "vuejs", "vue"],
#     "node.js": ["node.js", "nodejs", "node"],
#     "django": ["django", "django framework"],
#     "flask": ["flask", "flask framework"],
#     "spring": ["spring", "spring framework"],
#     "laravel": ["laravel", "laravel framework"],
#     "tensorflow": ["tensorflow", "tf"],
#     "pytorch": ["pytorch", "torch"],
#     "machine_learning": ["machine learning", "ml"],
#     "data analysis": ["data analysis", "data analytics"],
#     "git": ["git", "github", "gitlab"],
#     "linux": ["linux", "unix"],
#     "deep_learning": ["deep learning", "dl"],
#     "nlp": ["nlp", "natural language processing"],
#     "computer_vision": ["computer vision", "cv"],
#     "gcp": ["gcp", "google cloud", "google cloud platform"],
#     "azure": ["azure", "microsoft azure"],
#     "mongodb": ["mongodb", "mongo"],
#     "redis": ["redis"],
#     "excel": ["excel", "microsoft excel"],
#     "powerbi": ["power bi", "powerbi"],
#     "tableau": ["tableau"],
# }

# def normalize_skill(skills: List[str]) -> List[str]:
#     normalized = []
    
#     for skill in skills:
#         skill_lower = skill.strip().lower()
#         replaced = False

#         for standard_skill, variants in Skill_map.items():
            
#             for v in variants:
#                 pattern = r'\b' + re.escape(v) + r'\b'
#                 if re.search(pattern, skill_lower):
#                     normalized.append(standard_skill)
#                     replaced = True
#                     break
#         if not replaced:
#             normalized.append(skill_lower)
#     return list(normalized)


import json
import os
from openai import OpenAI
import re

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