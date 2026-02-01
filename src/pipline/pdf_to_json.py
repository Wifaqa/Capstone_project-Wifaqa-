from pathlib import Path
from src.ingestion.text_cleaner import clean_all_texts
from src.ingestion.pdf_loader import extract_all_pdfs
from src.extraction.resume_to_json import process_all_txt
from src.utils.apply_skill_normalization import process_all_json


def run_pdf_to_json_pipeline(session_dir: Path):
    raw_pdfs = session_dir / "resumes" / "raw_pdfs"
    extracted = session_dir / "resumes" / "extracted_text"
    cleaned = session_dir / "resumes" / "extracted_text_cleaned"
    structured = session_dir / "resumes" / "structured_json"

    extract_all_pdfs(
        input_dir=raw_pdfs,
        output_dir=extracted,
        overwrite=False,
    )

    clean_all_texts(
        input_dir=extracted,
        output_dir=cleaned,
        overwrite=False,
    )

    process_all_txt(session_dir)

    process_all_json(session_dir)