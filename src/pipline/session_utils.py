
from pathlib import Path

SESSIONS_ROOT = Path("data/sessions")

def list_sessions() -> list[str]:
    SESSIONS_ROOT.mkdir(parents=True, exist_ok=True)
    return sorted([p.name for p in SESSIONS_ROOT.iterdir() if p.is_dir()])

def ensure_session_folders(session_name: str) -> Path:
    session_dir = SESSIONS_ROOT / session_name

    (session_dir / "resumes" / "raw_pdfs").mkdir(parents=True, exist_ok=True)
    (session_dir / "resumes" / "extracted_text").mkdir(parents=True, exist_ok=True)
    (session_dir / "resumes" / "extracted_text_cleaned").mkdir(parents=True, exist_ok=True)
    (session_dir / "resumes" / "structured_json").mkdir(parents=True, exist_ok=True)

    (session_dir / "index").mkdir(parents=True, exist_ok=True)
    (session_dir / "outputs").mkdir(parents=True, exist_ok=True)

    return session_dir