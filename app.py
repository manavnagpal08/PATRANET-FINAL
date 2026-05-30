import os
import streamlit as st
from core.style_config import CUSTOM_CSS_LOGGED_IN, CUSTOM_CSS_LOGGED_OUT

# Set Streamlit page configurations
st.set_page_config(
    page_title="PATRANET | Document Processing Suite",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define storage folders paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIRS = {
    "uploads": os.path.join(BASE_DIR, "storage", "uploads"),
    "outputs": os.path.join(BASE_DIR, "storage", "outputs"),
    "images": os.path.join(BASE_DIR, "storage", "images")
}

# Ensure folders exist
for folder in STORAGE_DIRS.values():
    os.makedirs(folder, exist_ok=True)

# Initialize Session States
if "user" not in st.session_state:
    st.session_state["user"] = None
if "selected_doc" not in st.session_state:
    st.session_state["selected_doc"] = None
if "current_pipeline_result" not in st.session_state:
    st.session_state["current_pipeline_result"] = None

# Authentication Routing
if st.session_state["user"] is None:
    st.markdown(CUSTOM_CSS_LOGGED_OUT, unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="login-container">
            <div class="login-title">PATRANET</div>
            <div class="login-subtitle">Enterprise Document Processing Platform</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email_input = st.text_input("Username / Email", "admin@patranet.ai", key="login_email")
        pass_input = st.text_input("Password", "••••••••", type="password", key="login_pass")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Sign In", use_container_width=True):
                st.session_state["user"] = {"email": email_input, "uid": "firebase_mock_uid_19283"}
                st.rerun()
        with btn_col2:
            if st.button("Register", use_container_width=True):
                st.session_state["user"] = {"email": email_input, "uid": "firebase_mock_uid_19283"}
                st.rerun()
                
else:
    # Logged In Layout
    st.markdown(CUSTOM_CSS_LOGGED_IN, unsafe_allow_html=True)
    
    # Setup Sidebar profile
    st.sidebar.markdown("<h2 style='text-align: center; color: #0f172a;'>PATRANET</h2>", unsafe_allow_html=True)
    st.sidebar.write("---")
    st.sidebar.markdown(
        f"""
        <div class="user-profile-card">
            <div class="user-name">{st.session_state["user"]["email"]}</div>
            <div class="user-role">Access: Administrator</div>
            <div class="user-role">Directory: Active Session</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.sidebar.button("Sign Out", use_container_width=True):
        st.session_state["user"] = None
        st.session_state["selected_doc"] = None
        st.session_state["current_pipeline_result"] = None
        st.rerun()
        
    st.sidebar.write("---")
    st.sidebar.info("Operational session active. Stored records are processed locally.")
    
    # Main Dashboard Page
    st.markdown(
        """
        <div class="top-banner">
            <h1>PATRANET</h1>
            <p>Document Processing & Structured Data Extraction Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("### Production Environment Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            """
            This console manages the automated ingestion, optical character recognition (OCR), table boundary analysis, and structural metadata extraction of business documents.
            
            #### Core Functions
            * **OCR Text Extraction**: Converts scanned documents and image files into searchable, plain text data streams.
            * **Table Boundaries Mapping**: Identifies and extracts row-and-column grids directly into structured schemas.
            * **Asset Separation**: Detects and isolates embedded graphics, photos, or diagrams from PDF inputs.
            * **Export Engine**: Generates download links for Excel sheets, CSV records, and standard JSON formats.
            """
        )
        
        st.info("Select a module from the sidebar navigation menu to ingest files, review extraction outputs, or view processed document histories.")
        
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Execution Environment</div>
                <div class="metric-value" style="font-size: 1.35rem; color: #2563eb;">Enterprise Sandbox</div>
                <p style="margin-top: 0.5rem; font-size: 0.8rem; color: #475569; line-height: 1.4;">
                    Configured for high-speed offline parsing with local data storage services active.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Main execution flow runs top-to-bottom in Streamlit
