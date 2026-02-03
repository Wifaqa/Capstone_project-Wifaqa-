def resume_profile_text(resume: dict) -> str:
    parts = []

    if resume.get("summary"):
        parts.append(resume["summary"])

    for exp in resume.get("experiences", []):
        for b in exp.get("bullets", []):
            if b:
                parts.append(b)

    for proj in resume.get("projects", []):
        for b in proj.get("bullets", []):
            if b:
                parts.append(b)

    for skill in resume.get("skills", []):
        parts.append(skill)

    return "\n".join(parts)