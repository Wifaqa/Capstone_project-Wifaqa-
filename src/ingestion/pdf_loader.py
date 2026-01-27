from __future__ import annotations

from pathlib import Path
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extracts raw text from a PDF using PyMuPDF.
    Returns a single string (all pages combined).
    """
    doc = fitz.open(pdf_path)
    pages_text = []

    for page in doc:
        
        pages_text.append(page.get_text("text"))
        
    doc.close()
    return "\n".join(pages_text)


def extract_all_pdfs(
    input_dir: str = "../../data/resumes/raw_pdfs",
    output_dir: str = "../../data/resumes/extracted_text/demo",
    overwrite: bool = False,
) -> None:
    """
    Reads all PDFs from input_dir and writes .txt files to output_dir.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(input_path.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in: {input_path}")
        return

    print(f"Found {len(pdf_files)} PDF(s). Extracting text...")

    for pdf in pdf_files:
        txt_name = pdf.stem + ".txt"
        txt_path = output_path / txt_name

        if txt_path.exists() and not overwrite:
            print(f"Skipping (exists): {txt_path.name}")
            continue

        try:
            raw_text = extract_text_from_pdf(pdf)

           
            txt_path.write_text(raw_text, encoding="utf-8")

            print(f"Done: {pdf.name} -> {txt_path.name}")

        except Exception as e:
            print(f"Failed on {pdf.name}: {e}")

    print("Done All PDFs.")


