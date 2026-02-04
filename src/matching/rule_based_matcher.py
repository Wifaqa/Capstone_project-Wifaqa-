


def rule_based_match(resume: dict, jd: dict) -> dict:

    # =====================
    # Skills (STABLE + SIMPLE)
    # =====================
    resume_skills = set(resume.get("deterministic_normalized_skills", []))

    jd_required = jd.get("required", {}).get("skills", [])
    jd_preferred = jd.get("preferred", {}).get("skills", [])

    matched_required = [
        s for s in jd_required
        if any(s.lower() in rs or rs in s.lower() for rs in resume_skills)
    ]

    missing_required = [
        s for s in jd_required if s not in matched_required
    ]

    matched_preferred = [
        s for s in jd_preferred
        if any(s.lower() in rs or rs in s.lower() for rs in resume_skills)
    ]

    missing_preferred = [
        s for s in jd_preferred if s not in matched_preferred
    ]

    # =====================
    # Experience
    # =====================
    resume_exp = resume.get("years_of_experience")
    min_exp = jd.get("required", {}).get("min_years_exp")

    experience_match = (
        resume_exp is not None and
        min_exp is not None and
        resume_exp >= min_exp
    )

    # =====================
    # Education (SOFT MATCH)
    # =====================
    # Education (ROBUST)
    jd_level = (jd.get("required", {}).get("education_level") or "").lower()
    jd_fields = [f.lower() for f in jd.get("required", {}).get("degree_fields", [])]

    resume_degrees = [
        edu.get("degree", "").lower()
        for edu in resume.get("education", [])
        if edu.get("degree")
    ]

    education_level_match = False
    if "bachelor" in jd_level:
        education_level_match = any("bachelor" in deg for deg in resume_degrees)
    elif "master" in jd_level:
        education_level_match = any("master" in deg for deg in resume_degrees)
    elif "phd" in jd_level or "doctorate" in jd_level:
        education_level_match = any(
            "phd" in deg or "doctorate" in deg
            for deg in resume_degrees
        )

    education_field_match = any(
        field in deg
        for field in jd_fields
        for deg in resume_degrees
    )

    # =====================
    # Domain Knowledge (KEYWORD BASED – SAFE)
    # =====================

    jd_domains = jd.get("required", {}).get("domain_knowledge", [])

    resume_text = " ".join(
        s for s in [
            resume.get("summary") or "",
            " ".join(resume.get("deterministic_normalized_skills", [])),
            " ".join(
                bullet
                for exp in resume.get("experiences", [])
                for bullet in (exp.get("bullets") or [])
                if bullet
            ),
            " ".join(
                bullet
                for proj in resume.get("projects", [])
                for bullet in (proj.get("bullets") or [])
                if bullet
            )
        ]
        if s
    ).lower()

    domain_matched = [d for d in jd_domains if d.lower() in resume_text]
    domain_missing = [d for d in jd_domains if d not in domain_matched]

    # =====================
    # Final Result
    # =====================
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
        },
        "education": {
            "level_match": education_level_match,
            "field_match": education_field_match
        },
        "domain_knowledge": {
            "matched": domain_matched,
            "missing": domain_missing
        }
    }