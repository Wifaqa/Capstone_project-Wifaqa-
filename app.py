
import streamlit as st
import json
from pathlib import Path
import subprocess
from pathlib import Path
from src.pipline.save_job_description import process_job_description
# from src.matching.run_matching import run_matching
from src.pipline.run_matching import run_matching
from src.chat.chat_engine import chat_answer
from src.pipline.pdf_to_json import run_pdf_to_json_pipeline
from src.indexing.build_index import build_resume_index

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="AI Recruiter",
    layout="wide"
)

st.title("🤖 AI Recruiter")



# -----------------------
# Sessions 
# -----------------------
SESSIONS_ROOT = Path("data/sessions")
SESSIONS_ROOT.mkdir(parents=True, exist_ok=True)

sessions = [p.name for p in SESSIONS_ROOT.iterdir() if p.is_dir()]

if "session_name" not in st.session_state:
    st.session_state.session_name = sessions[0] if sessions else ""

st.sidebar.header("Session")

# اختيار Session موجودة
selected_session = st.sidebar.selectbox(
    "Choose existing session",
    options=[""] + sessions,
    index=([""] + sessions).index(st.session_state.session_name)
    if st.session_state.session_name in sessions else 0
)

# إنشاء Session جديدة
new_session = st.sidebar.text_input("Or create new session")

if st.sidebar.button("Use Session"):
    if new_session.strip():
        st.session_state.session_name = new_session.strip()
    elif selected_session:
        st.session_state.session_name = selected_session

# لو ما فيه Session
if not st.session_state.session_name:
    st.warning("Please select or create a session")
    st.stop()

SESSION_DIR = SESSIONS_ROOT / st.session_state.session_name
SESSION_DIR.mkdir(parents=True, exist_ok=True)

st.success(f"Active Session: {st.session_state.session_name}")

# =====================================================
# Job Description Input
# =====================================================
st.header("📄 Job Description")

jd_text = st.text_area(
    "Paste Job Description here",
    height=200
)

if st.button("💾 Save Job Description"):
    if jd_text.strip():
        process_job_description(jd_text, SESSION_DIR)
        st.success("Job Description saved ✅")
    else:
        st.warning("Please enter a job description")

# =====================================================
# Upload Resumes
# =====================================================
st.header("📤 Upload CVs")

uploaded_files = st.file_uploader(
    "Upload PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)
if st.button("⬆️ Save PDFs"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF")
    else:
        raw_dir = SESSION_DIR / "resumes" / "raw_pdfs"
        raw_dir.mkdir(parents=True, exist_ok=True)

        for f in uploaded_files:
            (raw_dir / f.name).write_bytes(f.getbuffer())

        st.success(f"{len(uploaded_files)} PDFs saved ✅")


# =====================================================
# Run Pipeline
# =====================================================
st.header("🛠 Pipeline")

if st.button("Run PDF → JSON Pipeline"):
    with st.spinner("Running pipeline..."):
        run_pdf_to_json_pipeline(SESSION_DIR)
        build_resume_index(SESSION_DIR)
    st.success("Pipeline + Index built ✅")


# =====================================================
# Matching Results (Dashboard)
# =====================================================
st.header("🏆 Matching Results")

top_k = st.slider("Top K Candidates", 5, 20, 10)

if st.button("🚀 Run Matching"):
    with st.spinner("Running matching..."):
        output_path = run_matching(SESSION_DIR, top_k=top_k)

    st.success("Matching completed ✅")

    results = json.loads(output_path.read_text(encoding="utf-8"))

    st.subheader("📊 Ranked Candidates")

    for idx, r in enumerate(results, start=1):
        with st.container():
            st.markdown(
                f"## {idx}. {r['candidate_name']} — **{r['fit_score']}%**"
            )

            st.markdown("### 🔍 Score Breakdown")
            st.json(r["score_breakdown"])

            st.markdown("### 🧠 Explanation (Why this score?)")
            st.write(r["explanation"])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Matched Required Skills")
                st.write(r["matched_required_skills"] or "—")

                st.markdown("### ⭐ Matched Preferred Skills")
                st.write(r["matched_preferred_skills"] or "—")

            with col2:
                st.markdown("### ❌ Missing Required Skills")
                st.write(r["missing_required_skills"] or "—")

                st.markdown("### ⏳ Experience Match")
                st.write("Yes ✅" if r["experience_match"] else "No ❌")

            st.divider()

# =====================================================
# Recruiter Chat
# =====================================================
st.header("💬 Recruiter Chat")

question = st.text_input("Ask a question about candidates")

if st.button("Ask"):
    if question.strip():
        with st.spinner("Thinking..."):
            answer = chat_answer(question, SESSION_DIR)
        st.write(answer)
    else:
        st.warning("Please enter a question")