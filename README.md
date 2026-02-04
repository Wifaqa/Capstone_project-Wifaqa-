# Wifaqa – AI Recruiter


## Features

- Resume PDF parsing
- Structured JSON extraction
- Job description analysis
- Candidate–job matching
- Hybrid search (BM25 + Vector Search + RRF)
- Rule-based fit score
- LLM-based evaluation with explanation
- Final weighted score
- Chat-based recruiter interaction

## Tech Stack

- Python 3.12
- OpenAI (GPT-4o-mini)
- ChromaDB
- Sentence Transformers
- Rank-BM25
- Streamlit

## To run this code:

1. Install dependencies:

- uv sync

2. Run Streamlit:

- uv run streamlit run app.py

## Environment Variables

Create a `.env` file and add:

- OPENAI_API_KEY=your_api_key_here

## Notes

- Rule-based score weight: 40%
- LLM-based score weight: 60%
- Designed as a graduation capstone project
- Deployed using Streamlit Cloud




## URL:
https://capstoneproject-wifaapp-git-2ulm9dqqkc4quyprbszncs.streamlit.app
