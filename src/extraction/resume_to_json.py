import json
import re
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# OpenRouter client
client = OpenAI(
    # api_key="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",
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "deepseek/deepseek-chat"

INPUT_TEXT_DIR = Path("data/resumes/extracted_text/demo_cleaned_txt")
OUTPUT_JSON_DIR = Path("data/resumes/structured_json")
OUTPUT_JSON_DIR.mkdir(parents=True, exist_ok=True)

def safe_json_parse(text: str) -> dict:
    """
    Cleans and safely parses JSON returned by LLM.
    Removes ```json fences if present.
    """
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON",
            "raw_output": text
        }

# def safe_json_parse(text: str) -> dict:
#     # Remove markdown fences
#     cleaned = re.sub(r"```json|```", "", text).strip()

#     # Extract JSON object only
#     match = re.search(r"\{.*\}", cleaned, re.DOTALL)
#     if not match:
#         return {
#             "error": "No JSON found",
#             "raw_output": text
#         }

#     json_text = match.group()

#     try:
#         return json.loads(json_text)
#     except json.JSONDecodeError as e:
#         return {
#             "error": "Invalid JSON",
#             "reason": str(e),
#             "raw_output": json_text
#         }

# =========================
# Prompt Builder
# =========================
def build_prompt(text: str) -> str:
    return """
Extract the following resume into STRICT JSON ONLY.
Do NOT include explanations or markdown.

Schema:
{
  "full_name": "string | null",

  "contact_info": {
    "email": "string | null",
    "phone": "string | null",
    "linkedin": "string | null",
    "location": "string | null"
  },

  "summary": "string | null",

  "years_of_experience": "number | null",

  "experiences": [
    {
      "title": "string | null",
      "company": "string | null",
      "location": "string | null",
      "start_date": "string | null",
      "end_date": "string | null",
      "bullets": ["string"]
    }
  ],

  "education": [
    {
      "degree": "string | null",
      "university": "string | null",
      "start_date": "string | null",
      "end_date": "string | null",
      "gpa": "string | null"
    }
  ],

  "certifications": [
    {
      "title": "string | null",
      "provider": "string | null",
      "start_date": "string | null",
      "end_date": "string | null"
    }
  ],

  "projects": [
    {
      "title": "string | null",
      "description": "string | null",
      "bullets": ["string"],
      "tools": ["string"]
    }
  ],

  "other_sections": ["string"],

  "skills": ["string"]
}

Resume:
\"\"\"
""" + text + """
\"\"\"
"""

# =========================
# LLM Extraction
# =========================
def extract_json_from_text(text: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You extract structured resume data as strict JSON."},
            {"role": "user", "content": build_prompt(text)}
        ],
        temperature=0,
        max_tokens=1500,
    )

    content = response.choices[0].message.content
    return safe_json_parse(content)

# =========================
# Process All TXT Files
# =========================
def process_all_txt(session_dir: Path):
    INPUT_TEXT_DIR = session_dir / "resumes" / "extracted_text_cleaned"
    OUTPUT_JSON_DIR = session_dir / "resumes" / "structured_json"
    OUTPUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
    txt_files = list(INPUT_TEXT_DIR.glob("*.txt"))

    if not txt_files:
        print("No .txt files found.")
        return

    for txt_file in txt_files:
        out_file = OUTPUT_JSON_DIR / f"{txt_file.stem}.json"
        if out_file.exists():
            print(f"Skipping (exists): {out_file.name}")
            continue

        print(f"Processing {txt_file.name}")

        text = txt_file.read_text(encoding="utf-8")
        resume_json = extract_json_from_text(text)

        out_path = OUTPUT_JSON_DIR / f"{txt_file.stem}.json"
        out_path.write_text(
            json.dumps(resume_json, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        print(f"Saved {out_path.name}")

    print("All resumes processed!")

# =========================
# Run
# =========================
