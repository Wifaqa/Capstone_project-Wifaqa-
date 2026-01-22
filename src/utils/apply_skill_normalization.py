import json
from pathlib import Path
from src.utils.skill_normalizer import normalize_skill



input_json_dir = Path('data/resumes/structured_json')
output_json_dir = Path('data/resumes/structured_json_normalized_skills')
output_json_dir.mkdir(parents=True, exist_ok=True)


def process_all_json():
    print("📂 Looking in:", input_json_dir.resolve())
    print("📄 Files found:", list(input_json_dir.glob("*.json")))
    for json_file in input_json_dir.glob('*.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        skills = data.get('skills', [])
        # normalized_skills = set()
        # for skill in skills:
        #     normalized = normalize_skill(skill)
        #     if normalized:
        #         normalized_skills.update(normalized)
        data['skills'] = skills
        data['normalized_skills'] = normalize_skill(skills)

        output_file = output_json_dir / json_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    process_all_json()