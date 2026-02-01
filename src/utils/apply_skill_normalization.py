import json
from pathlib import Path
from src.utils.skill_normalizer import normalize_skills_llm
from src.utils.skills_deterministic import normalize_skill


def process_all_json(session_dir: Path):
    
    input_json_dir = session_dir / "resumes" / "structured_json"
    output_json_dir = session_dir / "resumes" / "structured_json_normalized_skills"
    output_json_dir.mkdir(parents=True, exist_ok=True)
    for json_file in input_json_dir.glob('*.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        skills = data.get('skills', [])
        data['skills'] = skills

        

        normalized_skills = normalize_skills_llm(skills)
        data['normalized_skills'] = normalized_skills

        deterministic_skills = normalize_skill(normalized_skills)
        data['deterministic_normalized_skills'] = deterministic_skills

        print(f"Normalized skills for {json_file.name}")
        
        output_file = output_json_dir / json_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


