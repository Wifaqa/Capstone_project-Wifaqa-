import streamlit as st
import base64
from pathlib import Path

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =====================================================
# CSS & STYLING
# =====================================================
def load_css():
    
    # Defining shared colors based on theme
    if st.session_state.theme == "light":
        # Richer Light Mode: Stronger top-left glow + subtle bottom-right warmth
        bg_color = """
        radial-gradient(circle at 0% 0%, rgba(159, 87, 198, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 100% 100%, rgba(180, 100, 255, 0.1) 0%, transparent 50%),
        #faf7fc
        """

        text_color = "#4a2c5e" 
        brand_color = "#9f57c6"
        glass_bg = "rgba(255, 255, 255, 0.75)"
        glass_border = "rgba(255, 255, 255, 0.5)"
        card_shadow = "0 8px 32px 0 rgba(31, 38, 135, 0.15)"
        sidebar_bg = "#f4eff9"
    else:
        # Richer Dark Mode: Deep Purple top-left + Deep Blue/Black bottom-right (Premium Aurora)
        bg_color = """
            radial-gradient(circle at 20% 0%, rgba(94, 27, 137, 0.4) 0%, transparent 70%),
            radial-gradient(circle at 80% 100%, rgba(30, 10, 60, 0.5) 0%, transparent 70%),
            linear-gradient(180deg, #0b0b0d 0%, #1a1a1f 100%)
        """
        text_color = "#e0c3fc"
        brand_color = "#9f57c6"
        glass_bg = "rgba(18, 18, 22, 0.65)"
        glass_border = "rgba(159, 87, 198, 0.3)"
        card_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.5)"
        sidebar_bg = "#0e0e11"

    # SVG Wave encoded color (Use lighter version for transparency overlap)
    svg_color = brand_color.replace('#', '%23')

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* GLOBAL RESET */
    html, body, .stApp {{
        background: {bg_color} !important;
        background-attachment: fixed !important; 
        background-size: cover !important;
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: {text_color} !important;
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid rgba(159,87,198,0.1);
    }}

    /* REMOVE DEFAULT PADDING/MARGINS FOR CLEAN LOOK */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 5rem;
    }}
    
    /* GLASS CARD (For Sessions Page & Results) */
    .glass-card {{
        background: {glass_bg};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid {glass_border};
        box-shadow: {card_shadow};
        padding: 40px;
        text-align: center;
        max-width: 500px;
        margin: auto;
    }}
    
    /* STYLED CONTAINER (Native Streamlit Containers) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {glass_bg};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {glass_border};
        border-radius: 24px;
        padding: 20px;
        box-shadow: {card_shadow};
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: {brand_color}; 
        box-shadow: 0 0 20px {brand_color}50;
    }}

    .step-header {{
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 20px;
        color: {brand_color} !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* ===== SEAMLESS SINE WAVES ===== */
    .ocean {{
        height: 90%;
        width: 100%;
        position: fixed;
        bottom: 0;
        left: 0;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }}
    
    .wave {{
        position: absolute;
        bottom: -25;
        /* Using a pure Sine Wave for seamless looping "no straight lines" */
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 1200 120' xmlns='http://www.w3.org/2000/svg' preserveAspectRatio='none'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='{svg_color}'/%3E%3Cpath d='M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z' opacity='.5' fill='{svg_color}'/%3E%3C/svg%3E");
        background-size: 200% 100%; /* Important for looping */
        background-repeat: repeat-x;
        width: 200%;
        height: 40%; /* Adjust height of wave relative to screen */
    }}
    
    /* Modify wave appearance to look "filled" from bottom */
    .ocean::after {{
        /* Fill bottom solid */
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 20%; /* Base height fill */
        background: linear-gradient(to bottom, transparent, {brand_color});
        opacity: 0.1;
    }}
    
    /* WAVE 1: Moves RIGHT to LEFT */
    .wave:nth-of-type(1) {{
        bottom: -5%;
        opacity: 0.7;
        animation: wave-animation 20s linear infinite;
        z-index: 1;
    }}
    
    /* WAVE 2: Moves LEFT to RIGHT (Opposing) */
    .wave:nth-of-type(2) {{
        bottom: -10%;
        opacity: 0.5;
        animation: wave-animation-reverse 25s linear infinite;
        z-index: 2;
        filter: hue-rotate(30deg);
    }}

    @keyframes wave-animation {{
        0% {{ transform: translateX(0) scaleY(-1); }}
        100% {{ transform: translateX(-50%) scaleY(-1); }} /* Move exactly half width (since width is 200%) */
    }}

    @keyframes wave-animation-reverse {{
        0% {{ transform: translateX(-50%) scaleY(-1) scaleX(-1); }}
        100% {{ transform: translateX(0) scaleY(-1) scaleX(-1); }}
    }}

    
    /* BUTTON STYLING - UNIFORM FOR ALL */
    div.stButton > button {{
        background: linear-gradient(135deg, #9f57c6 0%, #7d44a6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        font-family: 'Lato', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(159, 87, 198, 0.25);
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important; /* Added to ensure text is centered */
        margin: 0 auto !important;
        width: auto !important;
    }}
    
    /* Ensure internal text/icon (often in a p tag) is centered */
    div.stButton > button p {{
        text-align: center !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }}

    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(159, 87, 198, 0.4);
        background: linear-gradient(135deg, #b06fd6 0%, #8e4bbd 100%) !important;
    }}
    div.stButton > button:active {{
        transform: translateY(1px);
        box-shadow: 0 2px 10px rgba(159, 87, 198, 0.2);
    }}

    /* INPUTS & SELECTBOXES */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(159, 87, 198, 0.2) !important;
        color: {text_color} !important;
    }}

    
    /* FILE UPLOADER */
    section[data-testid="stFileUploader"] {{
         background-color: rgba(255, 255, 255, 0.05) !important;
         border: 1px dashed {brand_color} !important;
         border-radius: 10px;
         padding: 20px;
    }}

    /* RESULT CARD */
    .result-card {{
        background: {glass_bg};
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid {brand_color};
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}
    /* ===== LANDING LOGO WITH GLOW ===== */
    .landing-logo {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;
    }}

    .landing-logo img {{
        width: 460px;
        max-width: 90%;
        filter:
            drop-shadow(0 0 25px rgba(159, 87, 198, 0.45))
            drop-shadow(0 0 60px rgba(159, 87, 198, 0.25));
        transition: transform 0.4s ease, filter 0.4s ease;
    }}

    .landing-logo img:hover {{
        transform: scale(1.04);
        filter:
            drop-shadow(0 0 35px rgba(159, 87, 198, 0.6))
            drop-shadow(0 0 90px rgba(159, 87, 198, 0.35));
    }}
    /* ===== FIXED THEME TOGGLE BUTTON ===== */
    .theme-toggle {{
        position: fixed;
        top: 18px;
        right: 24px;
        z-index: 9999;
    }}


    /* ===== HIDE STREAMLIT TOP WHITE BAR ===== */

    /* Hide Streamlit header / toolbar */
    header[data-testid="stHeader"] {{
        display: none;
    }}

    /* Hide deploy / menu toolbar */
    div[data-testid="stToolbar"] {{
        display: none;
    }}

    /* STEP NAVIGATION CSS */
    
    /* 1. Only target buttons in the first horizontal block (Navigation) to avoid affecting other buttons */
    /* We assume the nav is the first stHorizontalBlock, or we discriminate by avoiding border-wrappers */
    
    /* Variable to control which buttons get styled */
    /* We use a very specific selector: Buttons inside columns, but NOT inside a bordered container */
    

    /* Better Selector: Buttons that are DIRECT children of the main column layout flow (Steps) */
    /* vs Buttons inside the "Action Cards" (which are inside stVerticalBlockBorderWrapper) */
    

    /* Streamlit doesn't render keys to DOM. */
    
    /* We will use the :has() selector for buttons containing just Emoji */
    /* This works in most modern agents. If not, we fall back to layout-based. */
    
    /* Layout-Based: The Steps are in a container with a custom class 'steps-background' injected before it? No. */
    
    /* We'll rely on the text content or hierarchy */

    /* We will rely on the exact button labels "📝", "📂", "⚙️", "🎯" */
    
    /* ---------------------------------------------------------------- */
    /* CIRCULAR STEPS BUTTONS */
    /* ---------------------------------------------------------------- */
    
    /* We can target the `aria-label` or text content in newer CSS, but standard CSS cannot. */
    /* We will apply this style to ALL buttons, then UN-APPLY it for buttons with text? No. */
    
    /* And we only target Secondary buttons in the top columns. */
    
    /* ACTION BUTTONS (Inside border wrapper) - RESTORE NORMAL RECTANGLE */
    div[data-testid="stVerticalBlockBorderWrapper"] button {{
        border-radius: 8px !important;
        width: 100% !important;
        height: auto !important;
        padding: 0.5rem 1rem !important;
        background: linear-gradient(135deg, #9f57c6 0%, #7d44a6 100%) !important;
        box-shadow: 0 4px 15px rgba(159, 87, 198, 0.25) !important;
        font-size: 1rem !important;
        aspect-ratio: auto !important; /* Cancel 1:1 ratio if implied */
    }}

    /* STEPS BACKGROUND CONTAINER (Ghost) */
    .steps-wrapper {{
        position: relative;
        margin: 40px 0;   /* فقط مسافة عمودية */
    }}

    .steps-background-card {{
        position: absolute;
        top: 28px;
        left: 0;
        width: 100%;
        height: 130px;
        background: rgba(159, 87, 198, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        z-index: 0;
    }}
    .steps-line {{
        position: absolute;
        top: 55px; /* Center of button approx */
        left: 12%; 
        width: 76%;
        height: 3px;
        background: rgba(159, 87, 198, 0.2);
        z-index: 0;
    }}
    
    /* LABEL TEXT Styling */
    .step-label {{
        text-align: center;
        margin-top: 4px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {text_color};
    }}
    .step-sub {{
        margin-top: 2px;
        text-align: center;
        line-height: 1.2;
        font-size: 0.7rem;
        opacity: 0.6;
        color: {text_color};
    }}


    /* Prevent any top margin bleed */
    .stApp {{
        margin-top: 0 !important;
    }}

    /* ===== STEP ITEM ALIGNMENT FIX ===== */
    .step-item {{
    position: relative;
    z-index: 1; /* فوق الخلفية */
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    justify-content: flex-start;

    }}


        /* ensure the icon button is centered */
    .step-item .stButton > button {{
        width: 56px !important;
    height: 56px !important;
    border-radius: 50% !important;
    padding: 0 !important;
    font-size: 1.3rem !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    margin-bottom: 4px !important;
    }}
    
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# HELPER: HEADER
# =====================================================
def render_top_header(show_change_session: bool, show_title: bool):
    col_logo, col_title, col_actions = st.columns([2, 5, 3])

    with col_logo:
        if Path("w_logo.png").exists():
            st.image("w_logo.png", width=300)
        else:
            st.write("Wifaqa")

    with col_title:
        if show_title:
            st.markdown(
                "<h3 style='margin: 20px 0 0 0; font-weight:700;'>Wifaqa AI Recruiter</h3>",
                unsafe_allow_html=True
            )

    with col_actions:
        # Buttons aligned to the right: Exit (Left) | Theme (Right)
        # Using columns to position them
        c_fill, c_exit, c_theme = st.columns([2, 2, 1]) 
        
        with c_exit:
            if show_change_session:
                if st.button("Exit ", key="exit_session", help="Return to Sessions"):
                    st.session_state.page = "sessions"
                    st.rerun()
        
        with c_theme:
            if st.button("🌗", key=f"theme_toggle_{st.session_state.page}", help="Toggle Theme"):
                st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
                st.rerun()

        # Chat Toggle Button (only on main page, or we can pass a flag)
        # We'll handle this in the main page call, but for visual consistency:
        # Actually, adding it to the Actions is best. Let's make columns [2, 2, 2, 1]
        
    
def render_main_page_header():
    # ===== ROW 1: LOGO + ACTIONS =====
    col_logo, col_spacer, col_actions = st.columns([2, 6, 2])

    with col_logo:
        if Path("w_logo.png").exists():
            st.image("w_logo.png", width=280)
        else:
            st.write("Wifaqa")

    with col_actions:
        c_exit, c_theme = st.columns([1, 1])

        with c_exit:
            if st.button("Exit", use_container_width=True):
                st.session_state.page = "sessions"
                st.rerun()

        with c_theme:
            if st.button("🌗", use_container_width=True):
                st.session_state.theme = (
                    "dark" if st.session_state.theme == "light" else "light"
                )
                st.rerun()

    # مسافة بسيطة
    st.write("")

    # ===== ROW 2: SESSION NAME + CHAT BUTTON =====
    c_session, c_chat = st.columns([0.75, 0.25])

    with c_session:
        st.markdown(
            f"#### Session: *{st.session_state.session_name}*",
            unsafe_allow_html=True
        )

    with c_chat:
        chat_label = "Close Chat ❌" if st.session_state.show_chat else "Chat 💬"
        chat_type = "primary" if st.session_state.show_chat else "secondary"

        if st.button(chat_label, type=chat_type, use_container_width=True):
            st.session_state.show_chat = not st.session_state.show_chat
            st.rerun()