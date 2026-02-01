import json
from pathlib import Path
from src.extraction.job_description_to_json import extract_jd_to_json

def process_job_description(jd_text: str, session_dir: Path) -> Path:
    """
    Extract JD → save txt + json inside session folder
    """

    # 1) save raw text
    jd_txt = session_dir / "job_description.txt"
    jd_txt.write_text(jd_text.strip(), encoding="utf-8")

    # 2) extract structured JSON
    jd_json = extract_jd_to_json(jd_text)

    # 3) save JSON
    jd_json_path = session_dir / "job_description.json"
    jd_json_path.write_text(
        json.dumps(jd_json, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return jd_json_path