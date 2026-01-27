import json
from pathlib import Path
from src.utils.skill_normalizer import normalize_skills_llm
from src.utils.skills_deterministic import normalize_skill



input_json_dir = Path('data/resumes/structured_json')
output_json_dir = Path('data/resumes/structured_json_normalized_skills')
output_json_dir.mkdir(parents=True, exist_ok=True)


def process_all_json():
    for json_file in input_json_dir.glob('*.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        skills = data.get('skills', [])
        data['skills'] = skills

        deterministic_skills = normalize_skill(skills)
        data['deterministic_normalized_skills'] = deterministic_skills

        normalized_skills = normalize_skills_llm(deterministic_skills)
        data['normalized_skills'] = normalized_skills

        print(f"Normalized skills for {json_file.name}")
        
        output_file = output_json_dir / json_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


