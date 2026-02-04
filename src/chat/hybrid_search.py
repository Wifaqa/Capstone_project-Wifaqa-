

import re
import chromadb
from pathlib import Path
from rank_bm25 import BM25Okapi


# -----------------------------
# Helpers
# -----------------------------
def _tokenize(text: str) -> list[str]:
    if not text:
        return []
   
    return re.findall(r"[a-z0-9]+", text.lower())


def _get_collection(session_dir: Path):
    chroma_client = chromadb.PersistentClient(path=str(session_dir / "index"))
    return chroma_client.get_or_create_collection(name="resumes")


def _get_all_docs(collection, batch_size: int = 1000):
    """
    Chroma collection.get() قد يحتاج pagination.
    نجيب كل docs + metas + ids
    """
    all_docs = []
    all_metas = []
    all_ids = []

    offset = 0
    while True:
        batch = collection.get(
            include=["documents", "metadatas"],
            limit=batch_size,
            offset=offset
        )
        docs = batch.get("documents") or []
        metas = batch.get("metadatas") or []
        ids = batch.get("ids") or []

        if not docs:
            break

        all_docs.extend(docs)
        all_metas.extend(metas)
        all_ids.extend(ids)

        offset += len(docs)

    return all_docs, all_metas, all_ids


# -----------------------------
# 1) BM25 search
# -----------------------------
def bm25_search(question: str, session_dir: Path, top_k: int = 5):
    collection = _get_collection(session_dir)
    docs, metas, ids = _get_all_docs(collection)

    if not docs:
        return []

    tokenized_corpus = [_tokenize(d or "") for d in docs]
    bm25 = BM25Okapi(tokenized_corpus)

    q_tokens = _tokenize(question)
    scores = bm25.get_scores(q_tokens)

    ranked = sorted(range(len(docs)), key=lambda i: scores[i], reverse=True)[:top_k]

    results = []
    for i in ranked:
        results.append({
            "doc": docs[i],
            "meta": metas[i] or {},
            "id": ids[i],
            "score": float(scores[i])
        })
    return results


# -----------------------------
# 2) Vector search (Chroma built-in)
# -----------------------------
def vector_search(question: str, session_dir: Path, top_k: int = 5):
    collection = _get_collection(session_dir)

    res = collection.query(
        query_texts=[question],          
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    distances = (res.get("distances") or [[]])[0]

    results = []
    for d, m, dist in zip(docs, metas, distances):
     
        results.append({
            "doc": d,
            "meta": m or {},
            "id": None,
            "score": float(-dist) 
        })

    return results


# -----------------------------
# 3) RRF merge
# -----------------------------
def rrf_merge(bm25_results: list[dict], vector_results: list[dict], k: int = 60, top_k: int = 5):
    """
    Reciprocal Rank Fusion:
    score = sum(1 / (k + rank))
    """
    fused = {}

    def _key(r: dict):
      
        cid = (r.get("meta") or {}).get("candidate_id", "unknown")
        doc = r.get("doc", "")
        return f"{cid}::{doc}"

    for rank, r in enumerate(bm25_results, start=1):
        key = _key(r)
        fused.setdefault(key, {"doc": r["doc"], "meta": r.get("meta") or {}, "score": 0.0})
        fused[key]["score"] += 1.0 / (k + rank)

    for rank, r in enumerate(vector_results, start=1):
        key = _key(r)
        fused.setdefault(key, {"doc": r["doc"], "meta": r.get("meta") or {}, "score": 0.0})
        fused[key]["score"] += 1.0 / (k + rank)

    ranked = sorted(fused.values(), key=lambda x: x["score"], reverse=True)[:top_k]
    return ranked


# -----------------------------
# 4) Hybrid Search
# -----------------------------
def hybrid_search(question: str, session_dir: Path, top_k: int = 5):
    bm25 = bm25_search(question, session_dir, top_k=top_k)
    vec = vector_search(question, session_dir, top_k=top_k)

    fused = rrf_merge(bm25, vec, k=60, top_k=top_k)

   
    return [(x["doc"], x["meta"]) for x in fused]