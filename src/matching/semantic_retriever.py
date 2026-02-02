import json
from pathlib import Path
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
EMBEDDING_MODEL = "text-embedding-3-small"


def retrieve_evidence(
    session_dir: Path,
    query: str,
    candidate_id: str,
    top_k: int = 3
) -> dict:
    """
    Retrieve semantic evidence (sentences) from a candidate CV
    """

    index_dir = session_dir / "index"

    # chroma_client = chromadb.Client(
    #     chromadb.config.Settings(
    #         persist_directory=str(index_dir)
    #     )
    # )
    chroma_client = chromadb.PersistentClient(
        path=str(index_dir)
    )

    collection = chroma_client.get_collection(name="resumes")

    # Embed the query (job description or skill query)
    query_embedding = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    ).data[0].embedding

    # Search only inside this candidate
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"candidate_id": candidate_id}
    )

    documents = results.get("documents", [[]])[0]

    return {
        "candidate_id": candidate_id,
        "evidence": documents
    }