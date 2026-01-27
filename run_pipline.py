from src.ingestion.text_cleaner import clean_all_texts
from src.ingestion.pdf_loader import extract_all_pdfs
from src.extraction.resume_to_json import process_all_txt
from src.utils.apply_skill_normalization import process_all_json



def main():
    # Step 1: Extract text from PDFs
    extract_all_pdfs(
        input_dir="data/resumes/raw_pdfs",
        output_dir="data/resumes/extracted_text/demo",
        overwrite=False,
    )

    # Step 2: Clean extracted text files
    clean_all_texts(
        input_dir="data/resumes/extracted_text/demo",
        output_dir="data/resumes/extracted_text/demo_cleaned_txt",
        overwrite=False,
    )

    # Step 3: Extract structured JSON from cleaned text
    process_all_txt()

    # Step 4: Apply skill normalization to structured JSON
    process_all_json()


if __name__ == "__main__":
    main()