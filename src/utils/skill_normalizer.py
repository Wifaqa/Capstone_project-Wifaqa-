from typing import List
import re
Skill_map = {
    "python": ["python", "python3", "py"],
    "java": ["java", "jdk", "jre"],
    "javascript": ["javascript", "js"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "csharp"],
    "ruby": ["ruby", "rb"],
    "php": ["php"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "react": ["react", "reactjs"],
    "angular": ["angular", "angularjs"],
    "vue.js": ["vue.js", "vuejs", "vue"],
    "node.js": ["node.js", "nodejs", "node"],
    "django": ["django", "django framework"],
    "flask": ["flask", "flask framework"],
    "spring": ["spring", "spring framework"],
    "laravel": ["laravel", "laravel framework"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "machine_learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "git": ["git", "github", "gitlab"],
    "linux": ["linux", "unix"],
    "deep_learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "computer_vision": ["computer vision", "cv"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "azure": ["azure", "microsoft azure"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"],
    "excel": ["excel", "microsoft excel"],
    "powerbi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
}

def normalize_skill(skills: List[str]) -> List[str]:
    normalized = []
    
    for skill in skills:
        skill_lower = skill.strip().lower()
        replaced = False

        for standard_skill, variants in Skill_map.items():
            
            for v in variants:
                pattern = r'\b' + re.escape(v) + r'\b'
                if re.search(pattern, skill_lower):
                    normalized.append(standard_skill)
                    replaced = True
                    break
        if not replaced:
            normalized.append(skill_lower)
    return list(normalized)


