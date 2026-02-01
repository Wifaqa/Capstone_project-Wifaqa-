from typing import List, Dict

def resume_json_to_chunks(resume: Dict) -> List[str]:
    '''
    For Embedding generation: convert resume JSON to list of text chunks
    
    '''
    chunks = []

    # summary
    if resume.get("summary"):
        chunks.append(resume["summary"])

    # experience bullets
    for exp in resume.get("experiences", []):
        for b in exp.get("bullets", []):
            chunks.append(b)

    # project descriptions + bullets
    for proj in resume.get("projects", []):
        if proj.get("description"):
            chunks.append(proj["description"])
        for b in proj.get("bullets", []):
            chunks.append(b)

    return chunks