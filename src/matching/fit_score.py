

def calculate_fit_score(match_result: dict, jd: dict) -> dict:
    total_score = 0
    breakdown = {}

    required_skills = jd["required"].get("skills", [])
    preferred_skills = jd["preferred"].get("skills", [])

    # Required skills (60%)
    matched_required = match_result["required_skills"]["matched"]
    if required_skills:
        per_skill = 60 / len(required_skills)
        score_required = per_skill * len(matched_required)
    else:
        score_required = 60

    breakdown["required_skills"] = round(score_required, 2)
    total_score += score_required

    # Preferred skills (20%)
    matched_preferred = match_result["preferred_skills"]["matched"]
    if preferred_skills:
        per_skill = 20 / len(preferred_skills)
        score_preferred = per_skill * len(matched_preferred)
    else:
        score_preferred = 0

    breakdown["preferred_skills"] = round(score_preferred, 2)
    total_score += score_preferred

    # Experience (20%)
    experience_match = match_result["experience"]["match"]
    score_exp = 20 if experience_match else 0
    breakdown["experience"] = score_exp
    total_score += score_exp

    return {
        "fit_score": round(total_score, 2),
        "score_breakdown": breakdown
    }