import re
from typing import List


CATEGORY_PREFIXES = [
    "programming",
    "programming languages",
    "framework",
    "frameworks",
    "tools",
    "platforms",
    "web development",
    "soft skills",
    "languages",
]

def normalize_skill(skills: List[str]) -> List[str]:
    normalized = []
    
    for skill in skills:
        text = skill.strip().lower()
        # Split skills by common delimiters
        text = re.sub(rf"^[^:]+: \s*","", text)

        parts = re.split(r",| and | & |\|", text)
        for p in parts:
            p_clean = p.strip()
            if p_clean:
                normalized.append(p_clean)
    
    return list(normalized)