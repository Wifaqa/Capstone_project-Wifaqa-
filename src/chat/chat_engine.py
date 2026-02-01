import chromadb
from openai import OpenAI
from pathlib import Path

client = OpenAI()

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

def get_resume_collection(session_dir: Path):
    chroma_client = chromadb.Client(
        chromadb.config.Settings(
            persist_directory=str(session_dir / "index")
        )
    )

    return chroma_client.get_collection("resumes")

def semantic_search(question: str, session_dir: Path, top_k: int = 5):
    collection = get_resume_collection(session_dir)

    query_embedding = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    return list(zip(docs, metas))



def chat_answer(question: str, session_dir: Path) -> str:
    evidence = semantic_search(question, session_dir)

    if not evidence:
        return "No evidence found in the resumes."

    evidence_lines = []
    for text, meta in evidence:
        candidate_name = meta.get("candidate_name") or meta.get("candidate_id", "Unknown")
        candidate_id = meta.get("candidate_id", "Unknown")

        evidence_lines.append(
            f"- Candidate: {candidate_name} ({candidate_id}): {text}"
        )

    evidence_text = "\n".join(evidence_lines)

    prompt = f"""
You are an AI recruitment assistant.

Answer the question using ONLY the evidence below.
DO NOT invent candidate names or IDs.
If unsure, say you don't have enough evidence.

Evidence:
{evidence_text}

Question:
{question}


Answer in clear, professional language.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You answer recruiter questions using evidence."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()

