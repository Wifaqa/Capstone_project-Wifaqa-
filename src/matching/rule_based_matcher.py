

def rule_based_match(resume: dict, jd: dict) -> dict:
    print("RAW skills:", resume.get("skills"))
    print("NORMALIZED skills:", resume.get("deterministic_normalized_skills"))


    resume_skills = set(resume.get("deterministic_normalized_skills", []))


    jd_required = set(jd.get("required", {}).get("skills", []))
    jd_preferred = set(jd.get("preferred", {}).get("skills", []))

    matched_required = [
    jd_skill for jd_skill in jd_required
    if any(jd_skill in rs or rs in jd_skill for rs in resume_skills)
    ]


    missing_required = [
    s for s in jd_required
    if s not in matched_required
    ]


    matched_preferred = [
    jd_skill for jd_skill in jd_preferred
    if any(jd_skill in rs or rs in jd_skill for rs in resume_skills)
    ]


    missing_preferred = [
    s for s in jd_preferred
    if s not in matched_preferred
    ]

    resume_exp = resume.get("years_of_experience")
    min_exp = jd.get("required", {}).get("min_years_exp")

    experience_match = (
        resume_exp is not None and
        min_exp is not None and
        resume_exp >= min_exp
    )

    return {
        "required_skills": {
            "matched": matched_required,
            "missing": missing_required
        },
        "preferred_skills": {
            "matched": matched_preferred,
            "missing": missing_preferred
        },
        "experience": {
            "resume_years": resume_exp,
            "required_years": min_exp,
            "match": experience_match
        }
    }