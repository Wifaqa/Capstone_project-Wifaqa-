# def calculate_fit_score(match_result: dict, jd: dict) -> dict:
#     total_score = 0
#     breakdown = {}

#     # ---------- Required skills (30%) ----------
#     required_skills = jd["required"].get("skills", [])
#     matched_required = match_result["required_skills"]["matched"]

#     if required_skills:
#         score_required = (30 / len(required_skills)) * len(matched_required)
#     else:
#         score_required = 30

#     breakdown["required_skills"] = round(score_required, 2)
#     total_score += score_required


#     # ---------- Preferred skills (10%) ----------
#     preferred_skills = jd["preferred"].get("skills", [])
#     matched_preferred = match_result["preferred_skills"]["matched"]

#     if preferred_skills:
#         score_preferred = (10 / len(preferred_skills)) * len(matched_preferred)
#     else:
#         score_preferred = 0

#     breakdown["preferred_skills"] = round(score_preferred, 2)
#     total_score += score_preferred


#     # ---------- Domain knowledge (20%) ----------
#     domain_required = set(jd["required"].get("domain_knowledge", []))
#     matched_domains = set(match_result["domain_knowledge"]["matched"])

#     if domain_required:
#         score_domain = (20 / len(domain_required)) * len(matched_domains)
#     else:
#         score_domain = 20

#     breakdown["domain_knowledge"] = round(score_domain, 2)
#     total_score += score_domain


#     # ---------- Education (20%) ----------
#     education_match = (
#         match_result["education"]["level_match"] or
#         match_result["education"]["field_match"]
#     )

#     score_education = 20 if education_match else 0
#     breakdown["education"] = score_education
#     total_score += score_education


#     # ---------- Experience (20%) ----------
#     experience_match = match_result["experience"]["match"]
#     score_exp = 20 if experience_match else 0

#     breakdown["experience"] = score_exp
#     total_score += score_exp


#     return {
#         "fit_score": round(total_score, 2),
#         "score_breakdown": breakdown
#     }



def calculate_fit_score(match_result: dict, jd: dict) -> dict:
    total_score = 0
    breakdown = {}

    # ---------- Required skills (30%) ----------
    required_skills = jd["required"].get("skills", [])
    matched_required = match_result["required_skills"]["matched"]

    if required_skills:
        score_required = (30 / len(required_skills)) * len(matched_required)
    else:
        score_required = 30

    breakdown["required_skills"] = round(score_required, 2)
    total_score += score_required

    # ---------- Preferred skills (10%) ----------
    preferred_skills = jd["preferred"].get("skills", [])
    matched_preferred = match_result["preferred_skills"]["matched"]

    if preferred_skills:
        score_preferred = (10 / len(preferred_skills)) * len(matched_preferred)
    else:
        score_preferred = 0

    breakdown["preferred_skills"] = round(score_preferred, 2)
    total_score += score_preferred

    # ---------- Domain knowledge (15%) ----------
    domain_required = jd["required"].get("domain_knowledge", [])
    matched_domains = match_result["domain_knowledge"]["matched"]

    if domain_required:
        score_domain = (15 / len(domain_required)) * len(matched_domains)
    else:
        score_domain = 15

    breakdown["domain_knowledge"] = round(score_domain, 2)
    total_score += score_domain

    # ---------- Education (15%) ----------
    education_match = (
        match_result["education"]["level_match"] or
        match_result["education"]["field_match"]
    )

    score_education = 15 if education_match else 0
    breakdown["education"] = score_education
    total_score += score_education

    # ---------- Experience (30%) ----------
    score_exp = 30 if match_result["experience"]["match"] else 0
    breakdown["experience"] = score_exp
    total_score += score_exp

    return {
        "fit_score": round(total_score, 2),
        "score_breakdown": breakdown
    }