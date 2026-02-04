
# import streamlit as st
# import json
# from pathlib import Path
# import subprocess
# from pathlib import Path
# from src.pipline.save_job_description import process_job_description
# # from src.matching.run_matching import run_matching
# from src.pipline.run_matching import run_matching
# from src.chat.chat_engine import chat_answer
# from src.pipline.pdf_to_json import run_pdf_to_json_pipeline
# from src.indexing.build_index import build_resume_index

# # -----------------------
# # Page Config
# # -----------------------
# st.set_page_config(
#     page_title="AI Recruiter",
#     layout="wide"
# )

# st.title("🤖 AI Recruiter")



# # -----------------------
# # Sessions 
# # -----------------------
# SESSIONS_ROOT = Path("data/sessions")
# SESSIONS_ROOT.mkdir(parents=True, exist_ok=True)

# sessions = [p.name for p in SESSIONS_ROOT.iterdir() if p.is_dir()]

# if "session_name" not in st.session_state:
#     st.session_state.session_name = sessions[0] if sessions else ""

# st.sidebar.header("Session")

# # اختيار Session موجودة
# selected_session = st.sidebar.selectbox(
#     "Choose existing session",
#     options=[""] + sessions,
#     index=([""] + sessions).index(st.session_state.session_name)
#     if st.session_state.session_name in sessions else 0
# )

# # إنشاء Session جديدة
# new_session = st.sidebar.text_input("Or create new session")

# if st.sidebar.button("Use Session"):
#     if new_session.strip():
#         st.session_state.session_name = new_session.strip()
#     elif selected_session:
#         st.session_state.session_name = selected_session

# # لو ما فيه Session
# if not st.session_state.session_name:
#     st.warning("Please select or create a session")
#     st.stop()

# SESSION_DIR = SESSIONS_ROOT / st.session_state.session_name
# SESSION_DIR.mkdir(parents=True, exist_ok=True)

# st.success(f"Active Session: {st.session_state.session_name}")

# # =====================================================
# # Job Description Input
# # =====================================================
# st.header("📄 Job Description")

# jd_text = st.text_area(
#     "Paste Job Description here",
#     height=200
# )

# if st.button("💾 Save Job Description"):
#     if jd_text.strip():
#         process_job_description(jd_text, SESSION_DIR)
#         st.success("Job Description saved ✅")
#     else:
#         st.warning("Please enter a job description")

# # =====================================================
# # Upload Resumes
# # =====================================================
# st.header("📤 Upload CVs")

# uploaded_files = st.file_uploader(
#     "Upload PDF resumes",
#     type=["pdf"],
#     accept_multiple_files=True
# )
# if st.button("⬆️ Save PDFs"):
#     if not uploaded_files:
#         st.warning("Please upload at least one PDF")
#     else:
#         raw_dir = SESSION_DIR / "resumes" / "raw_pdfs"
#         raw_dir.mkdir(parents=True, exist_ok=True)

#         for f in uploaded_files:
#             (raw_dir / f.name).write_bytes(f.getbuffer())

#         st.success(f"{len(uploaded_files)} PDFs saved ✅")


# # =====================================================
# # Run Pipeline
# # =====================================================
# st.header("🛠 Pipeline")

# if st.button("Run PDF → JSON Pipeline"):
#     with st.spinner("Running pipeline..."):
#         run_pdf_to_json_pipeline(SESSION_DIR)
#         build_resume_index(SESSION_DIR)
#     st.success("Pipeline + Index built ✅")


# # =====================================================
# # Matching Results (Dashboard)
# # =====================================================
# st.header("🏆 Matching Results")

# top_k = st.slider("Top K Candidates", 5, 20, 10)

# if st.button("🚀 Run Matching"):
#     with st.spinner("Running matching..."):
#         output_path = run_matching(SESSION_DIR, top_k=top_k)

#     st.success("Matching completed ✅")

#     results = json.loads(output_path.read_text(encoding="utf-8"))

#     st.subheader("📊 Ranked Candidates")

#     for idx, r in enumerate(results, start=1):

#         with st.container():
#             rules = r.get("rules", {})
#             # -------------------------
#             # Header
#             # -------------------------
#             st.markdown(
#                 f"## {idx}. {r['candidate_name']} — **{r['final_score']}%**"
#             )

#             # -------------------------
#             # Score Breakdown
#             # -------------------------
#             st.markdown("### 🔍 Score Breakdown")

#             st.json({
#                 "rule_based_score": r.get("rules_score"),
#                 "llm_score": r.get("llm_score"),
#                 "final_score": r.get("final_score")
#             })

#             # -------------------------
#             # Explanation
#             # -------------------------
#             # st.markdown("### 🧠 Explanation (Why this score?)")

#             # if "llm" in r and isinstance(r["llm"], dict):
#             #     st.write(r["llm"].get("reasoning", "No explanation provided by LLM."))
#             # else:
#             #     st.write("No explanation available.")
#             st.markdown("### 🧠 Explanation (Why this score?)")

#         llm = r.get("llm", {})

#         if not llm:
#             st.write("No explanation available.")
#         else:
#             # 1) One-line executive summary
#             summary = llm.get("one_sentence_summary", "").strip()
#             if summary:
#                 st.markdown(f"**Summary:** {summary}")

#             # 2) Rubric breakdown (VERY IMPORTANT)
#             rubric = llm.get("rubric", {})
#             if rubric:
#                 st.markdown("**Score Breakdown (LLM):**")
#                 st.json(rubric)

#             # 3) Strengths
#             strengths = llm.get("strengths", [])
#             if strengths:
#                 st.markdown("**Key Strengths:**")
#                 for s in strengths:
#                     st.markdown(f"- {s}")

#             # 4) Concerns
#             concerns = llm.get("concerns", [])
#             if concerns:
#                 st.markdown("**Main Concerns:**")
#                 for c in concerns:
#                     st.markdown(f"- {c}")

#             col1, col2 = st.columns(2)

#             # -------------------------
#             # Left column
#             # -------------------------
#             with col1:
#                 st.markdown("### ✅ Matched Required Skills")
                
#                 st.write(
#                     rules.get("required_skills", {}).get("matched", []) or "—"
#                 )

#                 st.markdown("### ⭐ Matched Preferred Skills")
#                 st.write(
#                     rules.get("preferred_skills", {}).get("matched", []) or "—"
#                 )

#             # -------------------------
#             # Right column
#             # -------------------------
#             with col2:
#                 st.markdown("### ❌ Missing Required Skills")
#                 st.write(
#                     rules.get("required_skills", {}).get("missing", []) or "—"
#                 )

#                 st.markdown("### ⏳ Experience Match")
#                 st.write(
#                     "Yes ✅" if rules.get("experience", {}).get("match") else "No ❌"
#                 )

#             # -------------------------
#             # Education
#             # -------------------------
#             st.markdown("### 🎓 Education Match")
            
#             edu = rules.get("education", {})
#             if edu:
#                 st.write(
#                     "Yes ✅"
#                     if (edu.get("level_match") or edu.get("field_match"))
#                     else "No ❌"
#                 )
#             else:
#                 st.write("—")

#             # -------------------------
#             # Domain Knowledge
#             # -------------------------
#             st.markdown("### 🧠 Domain Knowledge")

#             rules = r.get("rules", {})
#             domain = rules.get("domain_knowledge", None)

#             if domain is None:
#                 st.write("—")
#             else:
#                 matched = domain.get("matched", [])
#                 missing = domain.get("missing", [])

#                 # لو الـ JD ما حدد دومين
#                 if not matched and not missing:
#                     st.write("Not specified in JD (domain_knowledge empty).")
#                 else:
#                     st.markdown("**Matched:**")
#                     st.write(matched or "—")

#                     st.markdown("**Missing:**")
#                     st.write(missing or "—")

#             st.divider()

# # =====================================================
# # Recruiter Chat
# # =====================================================
# st.header("💬 Recruiter Chat")

# question = st.text_input("Ask a question about candidates")

# if st.button("Ask"):
#     if question.strip():
#         with st.spinner("Thinking..."):
#             answer = chat_answer(question, SESSION_DIR)
#         st.write(answer)
#     else:
#         st.warning("Please enter a question")


import streamlit as st
import json
from pathlib import Path

from src.pipline.save_job_description import process_job_description
from src.pipline.run_matching import run_matching
from src.chat.chat_engine import chat_answer
from src.pipline.pdf_to_json import run_pdf_to_json_pipeline
from src.indexing.build_index import build_resume_index
from styles import load_css, render_top_header, render_main_page_header, image_to_base64






# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Wifaqa AI Recruiter",
    layout="wide",
    initial_sidebar_state="expanded" 
)


# =====================================================
# Session State Init
# =====================================================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "page" not in st.session_state:
    st.session_state.page = "sessions"

if "session_name" not in st.session_state:
    st.session_state.session_name = ""

if "active_step" not in st.session_state:
    st.session_state.active_step = "Job Description"

if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
# =====================================================
# CSS & STYLING
# =====================================================


load_css()
# =====================================================




# =====================================================
# PAGE 1: SESSIONS (Landing)
# =====================================================
if st.session_state.page == "sessions":
    # Theme Toggle Top Right
    col_top = st.columns([10, 1])
    with col_top[1]:
        if st.button("🌗", key="session_theme_toggle", help="Toggle Theme"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()
        

    # Render Waves
    st.markdown("""
    <div class="ocean">
      <div class="wave"></div>
      <div class="wave"></div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    col_center = st.columns([1, 2, 1])
    with col_center[1]:        
     if Path("w_logo.png").exists():
        logo_base64 = image_to_base64("w_logo.png")
        st.markdown(f"""
        <div class="landing-logo">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
        """, unsafe_allow_html=True)


        
        st.markdown("<h2>Welcome to Wifaqa</h2>", unsafe_allow_html=True)
        st.markdown("<p style='opacity:0.8; font-size:0.95rem;'>AI-Powered Recruitment Assistant</p>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

        SESSIONS_ROOT = Path("data/sessions")
        SESSIONS_ROOT.mkdir(parents=True, exist_ok=True)
        sessions = [p.name for p in SESSIONS_ROOT.iterdir() if p.is_dir()]

        selected_session = st.selectbox("Resume Session", [""] + sessions, placeholder="Select existing...")
        st.markdown("<div style='margin: 10px 0; font-size:0.8rem; opacity:0.6;'>— OR —</div>", unsafe_allow_html=True)
        new_session = st.text_input("New Session Name", placeholder="e.g. Senior_Dev_Hiring")

        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        
        if st.button("Start Session"):
            session_to_start = ""
            if new_session.strip():
                session_to_start = new_session.strip()
            elif selected_session:
                session_to_start = selected_session
            
            if session_to_start:
                st.session_state.session_name = session_to_start
                (SESSIONS_ROOT / st.session_state.session_name).mkdir(parents=True, exist_ok=True)
                st.session_state.page = "main"
                st.rerun()
            else:
                st.warning("Please select or create a session.")

        st.markdown('</div>', unsafe_allow_html=True) 
    st.stop()


# =====================================================
# PAGE 2: MAIN DASHBOARD
# =====================================================
SESSION_DIR = Path("data/sessions") / st.session_state.session_name
SESSION_DIR.mkdir(parents=True, exist_ok=True)


# -----------------
# 1. LAYOUT SETUP
# -----------------
render_main_page_header()

# ====== STEPS NAVIGATION ======
st.markdown('<div class="steps-wrapper">', unsafe_allow_html=True)

# 1. Background Layer (Ghost Container)
st.markdown("""
<div class="steps-background-card">
    <div class="steps-line"></div>
</div>
""", unsafe_allow_html=True)

# 2. Interactive Buttons Layer
step_cols = st.columns(4)

steps_options = ["Job Description", "Upload Resumes", "Analysis Pipeline", "Matching Results"]
steps_subs = ["Define Constraints", "Bulk Processing", "AI Extraction", "Rank Candidates"]
icons = ["📝", "📂", "⚙️", "🎯"]
for i, col in enumerate(step_cols):
    with col:
        is_active = st.session_state.active_step == steps_options[i]

        st.markdown('<div class="step-item">', unsafe_allow_html=True)

        if st.button(
            icons[i],
            key=f"step_btn_{i}",
            type="primary" if is_active else "secondary",
        ):
            st.session_state.active_step = steps_options[i]
            st.rerun()

        st.markdown(f"""
            <div class="step-label">{steps_options[i]}</div>
            <div class="step-sub">{steps_subs[i]}</div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)




# -----------------
# 2. MAIN CONTENT + CHAT (CONDITIONAL SPLIT VIEW)
# -----------------
if st.session_state.show_chat:
    c_content, c_chat = st.columns([0.65, 0.35], gap="large")
    
    # === RENDER CHAT ===
    with c_chat:
        st.markdown("###  AI Assistant")
        # Chat Container
        chat_container = st.container(height=500, border=True)
        
        # Initialize history if needed
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        with chat_container:
            for role, msg in st.session_state.chat_history:
                 with st.chat_message(role):
                    st.write(msg)
                    
        # Chat Input (Inline)
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Ask a question...", placeholder="Type here...")
            c_sub_1, c_sub_2 = st.columns([1, 4]) 
            submit_chat = st.form_submit_button("Send ", use_container_width=True)
            
        if submit_chat and user_input:
            st.session_state.chat_history.append(("user", user_input))
            with chat_container:
                 with st.chat_message("user"):
                    st.write(user_input)
                    
            with st.spinner("Analyzing..."):
                try:
                    answer = chat_answer(user_input, SESSION_DIR)
                except Exception as e:
                    answer = f"Error: {e}"
            
            st.session_state.chat_history.append(("assistant", answer))
            st.rerun() 

else:
    # Full Width
    c_content = st.container()
 

                

# -----------------
# 2. MAIN CONTENT
# -----------------
# ====== CONTENT DYNAMIC DISPLAY ======
with c_content:

        if st.session_state.active_step == "Job Description":
            st.markdown('<div class="step-header">STEP 1: JOB DESCRIPTION</div>', unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("**Define Constraint & Requirements**")
                jd_text = st.text_area("JD Content", height=300, placeholder="Paste Job Description here...", label_visibility="collapsed")
            
                c_act1, c_act2 = st.columns([1, 4])
                with c_act1:
                    if st.button("Save Description", use_container_width=True):
                        if jd_text.strip():
                            process_job_description(jd_text, SESSION_DIR)
                            st.success("Saved!")
                        else:
                            st.error("Empty text.")
        
        elif st.session_state.active_step == "Upload Resumes":
            st.markdown('<div class="step-header">STEP 2: UPLOAD RESUMES</div>', unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("**Bulk Upload PDFs**")
                uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
            
                if st.button("Process & Save Files", use_container_width=True):
                    if uploaded_files:
                        raw_dir = SESSION_DIR / "resumes" / "raw_pdfs"
                        raw_dir.mkdir(parents=True, exist_ok=True)
                        count = 0
                        for f in uploaded_files:
                            (raw_dir / f.name).write_bytes(f.getbuffer())
                            count += 1
                        st.success(f"Saved {count} resumes.")
                    else:
                        st.warning("No files selected.")

        elif st.session_state.active_step == "Analysis Pipeline":
            st.markdown('<div class="step-header">STEP 3: ANALYSIS PIPELINE</div>', unsafe_allow_html=True)
            with st.container(border=True):
                st.info("Run this pipeline to extract specific data from resumes (Uses LLMs).")
            
                if st.button("Run Extraction Pipeline", type="primary", use_container_width=True):
                    with st.spinner("Analyzing documents... this may take time."):
                        run_pdf_to_json_pipeline(SESSION_DIR)
                        build_resume_index(SESSION_DIR)
                    st.success("Analysis Pipeline Completed!")

        elif st.session_state.active_step == "Matching Results":
            st.markdown('<div class="step-header">STEP 4: MATCHING RESULTS</div>', unsafe_allow_html=True)
            with st.container(border=True):
                c_k, c_btn = st.columns([1, 1])
                with c_k:
                    top_k = st.slider("Top Candidates", 3, 50, 10)
                with c_btn:
                    st.write("") # spacer
                    run_match_btn = st.button("Calculate Matches", type="primary", use_container_width=True)

                if run_match_btn:
                    with st.spinner("Matching..."):
                        output_path = run_matching(SESSION_DIR, top_k=top_k)

                    if output_path and output_path.exists():
                        results = json.loads(output_path.read_text(encoding="utf-8"))
                        st.markdown(f"**Found {len(results)} matches**")
                    
                        for rank, r in enumerate(results, start=1):
                            final_score = r.get('final_score', 0)
                            score_color = "#2ecc71" if final_score > 75 else "#f1c40f" if final_score > 50 else "#e74c3c"
                        
                            st.markdown(f"""
                            <div class="result-card">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <h3 style="margin:0;">#{rank} {r.get('candidate_name', 'Unknown')}</h3>
                                    <h2 style="margin:0; color:{score_color} !important;">{final_score}%</h2>
                                </div>
                                <hr style="opacity:0.2; margin:10px 0;">
                                <div style="display:flex; gap:20px; font-size:0.9rem;">
                                    <span><b>Rules:</b> {r.get('rules_score', 0)}%</span>
                                    <span><b>Semantic:</b> {r.get('llm_score', 0)}%</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                            with st.expander(f"Details: {r.get('candidate_name')}"):
                                st.json(r)
                    else:
                        st.info("No matching results found. Please run analysis first.")