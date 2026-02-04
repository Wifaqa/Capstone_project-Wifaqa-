

import json
import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()


def build_resume_index(session_dir: Path):
    resumes_dir = session_dir / "resumes" / "structured_json_normalized_skills"
    index_dir = session_dir / "index"
    index_dir.mkdir(parents=True, exist_ok=True)

    print("Resumes dir:", resumes_dir)
    files = list(resumes_dir.glob("*.json"))
    print("Found resumes:", files)

    if not files:
        print("No resume JSON files found. Stop.")
        return

    
    chroma_client = chromadb.PersistentClient(path=str(index_dir))

    
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"  
    )

    
    try:
        chroma_client.delete_collection("resumes")
        print("Old collection deleted")
    except Exception:
        pass

    collection = chroma_client.get_or_create_collection(
        name="resumes",
        embedding_function=embedding_function
    )

    total_docs = 0

    for resume_file in files:
        resume = json.loads(resume_file.read_text(encoding="utf-8"))
        candidate_id = resume_file.stem
        candidate_name = resume.get("full_name") or candidate_id

        documents = []

        # 1️⃣ Summary
        if resume.get("summary"):
            documents.append(resume["summary"])

        # 2️⃣ Skills
        skills = resume.get("deterministic_normalized_skills", [])
        if skills:
            documents.append("Skills: " + ", ".join(skills))

        # 3️⃣ Experiences
        for exp in resume.get("experiences", []):
            title = exp.get("title")
            company = exp.get("company")
            if title or company:
                documents.append(f"{title or ''} at {company or ''}".strip())

            for bullet in exp.get("bullets", []):
                if bullet:
                    documents.append(bullet)

        # 4️⃣ Projects
        for proj in resume.get("projects", []):
            for bullet in proj.get("bullets", []):
                if bullet:
                    documents.append(bullet)

        # 5️⃣ Add to Chroma
        for i, text in enumerate(documents):
            collection.add(
                documents=[text],
                ids=[f"{candidate_id}_{i}"],
                metadatas=[{
                    "candidate_id": candidate_id,
                    "candidate_name": candidate_name
                }]
            )

        total_docs += len(documents)

    print("✅ Total documents indexed:", total_docs)
    print("✅ Collection count:", collection.count())