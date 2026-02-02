import json
from pathlib import Path

from src.matching.rule_based_matcher import rule_based_match
from src.matching.fit_score import calculate_fit_score
from src.matching.explain_matching import explain_score
from src.matching.semantic_retriever import retrieve_evidence


def run_matching(session_dir: Path, top_k: int = 10) -> Path:
    
    """
    Run rule-based matching + fit score + explanation
    Saves ranking_results.json inside session/outputs
    """

    resumes_dir = session_dir / "resumes" / "structured_json_normalized_skills"
    jd_path = session_dir / "job_description.json"
    output_dir = session_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    resume_files = list(resumes_dir.glob("*.json"))

    print("DEBUG: resumes_dir =", resumes_dir)
    print("DEBUG: total resumes found =", len(resume_files))
    print("DEBUG: resume files =")
    for f in resume_files:
        print(" -", f.name)

    # Load Job Description JSON
    jd = json.loads(jd_path.read_text(encoding="utf-8"))

    results = []

    for resume_file in resumes_dir.glob("*.json"):
        resume = json.loads(resume_file.read_text(encoding="utf-8"))

        candidate_name = resume.get("full_name") or resume_file.stem

        # 1) Rule-based matching
        match_result = rule_based_match(resume, jd)

        # 2) Fit score
        score_result = calculate_fit_score(match_result, jd)

        # 3) Semantic evidence from CV
        try:
            evidence = retrieve_evidence(
                session_dir=session_dir,
                query=" ".join(jd["required"].get("skills", [])),
                candidate_id=resume_file.stem,
                top_k=3
            )
        except Exception:
            evidence = {"candidate_id": resume_file.stem, "evidence": []}

        # 4) Explanation (LLM)
        explanation = explain_score(
            resume=resume,
            jd=jd,
            match_result=match_result,
            score_result=score_result
        )

        print("DEBUG: processing", resume_file.name)
        print("DEBUG: evidence =", evidence)

        # 5) Collect result
        # 5) Collect result
        results.append({
            "candidate_id": resume_file.stem,
            "candidate_name": candidate_name,

            "fit_score": score_result["fit_score"],
            "score_breakdown": score_result["score_breakdown"],

            # Skills
            "matched_required_skills": match_result["required_skills"]["matched"],
            "missing_required_skills": match_result["required_skills"]["missing"],
            "matched_preferred_skills": match_result["preferred_skills"]["matched"],

            # Experience
            "experience_match": match_result["experience"]["match"],

            # 🆕 Education
            "education_match": {
                "level_match": match_result["education"]["level_match"],
                "field_match": match_result["education"]["field_match"],
            },

            # 🆕 Domain knowledge
            "domain_knowledge": {
                "matched": match_result["domain_knowledge"]["matched"],
                "missing": match_result["domain_knowledge"]["missing"]
            },

            # Explanation + Evidence
            "explanation": explanation,
            "evidence": evidence.get("evidence", [])
        })

    # Sort by score
    results = sorted(results, key=lambda x: x["fit_score"], reverse=True)
    results = results[:top_k]

    output_path = output_dir / "ranking_results.json"
    output_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print("DEBUG FINAL RESULTS")
    for r in results:
        print(r["candidate_name"], r["fit_score"], len(r.get("evidence", [])))

    return output_path