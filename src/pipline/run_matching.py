




import json
from pathlib import Path
from collections import defaultdict

from src.matching.rule_based_matcher import rule_based_match
from src.matching.fit_score import calculate_fit_score
from src.chat.hybrid_search import hybrid_search
from src.matching.llm_matcher import llm_compare


# -------------------------
# Helpers
# -------------------------
def load_resume_json(session_dir: Path, resume_id: str) -> dict:
    path = session_dir / "resumes" / "structured_json_normalized_skills" / f"{resume_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def resume_profile_text(resume: dict) -> str:
    parts = []

    if resume.get("summary"):
        parts.append(resume["summary"])

    parts.extend(resume.get("deterministic_normalized_skills", []))

    for exp in resume.get("experiences", []):
        parts.extend(exp.get("bullets", []) or [])

    for proj in resume.get("projects", []):
        parts.extend(proj.get("bullets", []) or [])

    return "\n".join(p for p in parts if isinstance(p, str))


# -------------------------
# Main Pipeline
# -------------------------
def run_matching(session_dir: Path, top_k: int = 5) -> Path:
    """
    Hybrid Search + Rule-based Score (0.4) + LLM Score (0.6)
    """

    jd_path = session_dir / "job_description.json"
    output_dir = session_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    jd = json.loads(jd_path.read_text(encoding="utf-8"))

    # ==========================
    # 1️⃣ Hybrid Search
    # ==========================
    query = " ".join(jd.get("required", {}).get("skills", []))
    hybrid_results = hybrid_search(query, session_dir, top_k=30)

    
    candidate_map = {}

    for doc, meta in hybrid_results:
        resume_id = (meta or {}).get("candidate_id")
        if not resume_id:
            continue

        # لا تعالج نفس المرشح مرتين
        if resume_id in candidate_map:
            continue

        resume = load_resume_json(session_dir, resume_id)

        # ==========================
        # 2️⃣ Rule-based score
        # ==========================
        match_result = rule_based_match(resume, jd)
        rule_score = calculate_fit_score(match_result, jd)["fit_score"]

        # ==========================
        # 3️⃣ LLM score
        # ==========================
        profile_text = resume_profile_text(resume)

        try:
            llm_result = llm_compare(jd, profile_text)
            llm_score = float(llm_result.get("fit_score", 0))
        except Exception:
            llm_result = {}
            llm_score = 0.0

        # ==========================
        # 4️⃣ Final weighted score
        # ==========================
        final_score = round(0.4 * rule_score + 0.6 * llm_score, 2)

        candidate_map[resume_id] = {
            "candidate_id": resume_id,
            "candidate_name": resume.get("full_name", resume_id),

            # scores
            "final_score": final_score,
            "rules_score": rule_score,
            "llm_score": llm_score,

            # detailed results (USED BY UI)
            "rules": match_result,
            "llm": llm_result,

            # optional evidence
            "evidence": doc,
        }

    # ==========================
    # 5️⃣ Sort & Top-K
    # ==========================
    results = list(candidate_map.values())
    results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    results = results[:top_k]

    output_path = output_dir / "ranking_results.json"
    output_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return output_path