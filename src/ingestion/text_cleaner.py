from pathlib import Path
import re


def clean_text(text: str) -> str:
    """
    Cleans raw extracted resume text.
    """
    # Normalize line endings
    text = text.replace("\r", "\n")

    # Remove multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove non-ASCII characters (optional but helps messy PDFs)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Trim whitespace
    return text.strip()


def clean_all_texts(
    input_dir: str = "../../data/resumes/extracted_text/demo",
    output_dir: str = "../../data/resumes/extracted_text/demo_cleaned_txt",
    overwrite: bool = False,
) -> None:
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    txt_files = sorted(input_path.glob("*.txt"))
    if not txt_files:
        print(f"No text files found in {input_path}")
        return

    print(f"Cleaning {len(txt_files)} text file(s)...")

    for txt_file in txt_files:
        out_file = output_path / txt_file.name

        if out_file.exists() and not overwrite:
            print(f"Skipping (exists): {out_file.name}")
            continue

        raw_text = txt_file.read_text(encoding="utf-8", errors="ignore")
        cleaned = clean_text(raw_text)

        out_file.write_text(cleaned, encoding="utf-8")

        print(f"Cleaned: {txt_file.name}")

    print("Cleaning complete.")


