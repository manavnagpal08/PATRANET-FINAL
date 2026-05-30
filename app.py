import os
import streamlit as st

# Set Streamlit page configurations
st.set_page_config(
    page_title="PATRANET | Intelligent Document Processing",
    page_icon=None, # Clean, no emojis
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI / Light Theme
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
        padding-top: 1.5rem;
    }
    
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Elegant Card Design */
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        border-color: #cbd5e1;
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
    }
    
    /* Top Bar Styling */
    .top-banner {
        background: #0f172a;
        color: white;
        padding: 1.75rem 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        border-left: 4px solid #2563eb;
    }
    
    .top-banner h1 {
        color: white !important;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .top-banner p {
        margin: 0.25rem 0 0 0;
        font-size: 0.95rem;
        color: #94a3b8;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Define storage folders paths relative to work dir
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
    st.session_state["user"] = {"email": "hackathon_demo@patranet.ai", "uid": "demo_user"}
if "selected_doc" not in st.session_state:
    st.session_state["selected_doc"] = None
if "current_pipeline_result" not in st.session_state:
    st.session_state["current_pipeline_result"] = None

def main():
    st.markdown(
        """
        <div class="top-banner">
            <h1>PATRANET</h1>
            <p>Intelligent Document Processing & Structured Data Extraction</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("### Enterprise Extraction Suite")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            """
            PATRANET orchestrates optical character recognition (OCR), table boundary analysis, and embedded asset parsing to transform raw documents into normalized, queryable business intelligence.
            
            #### Operational Features
            * **Scanned & Native PDF Parsing**: Advanced character mapping and text line matching.
            * **Tabular Layout Preservation**: Accurate extraction of data coordinates and table schemas.
            * **Embedded Resource Siphoning**: Automatic detection and isolation of nested media and image elements.
            * **Standard Exports**: Direct file generation for Excel, CSV, and structured JSON formats.
            """
        )
        
        st.info("Use the sidebar navigation panel to access the upload center, check extraction outputs, or search historical records.")
        
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">System Deployment</div>
                <div class="metric-value" style="font-size: 1.35rem; color: #2563eb;">Enterprise Sandbox</div>
                <p style="margin-top: 0.5rem; font-size: 0.8rem; color: #475569; line-height: 1.4;">
                    Running in hybrid local database mode to ensure rapid, offline hackathon evaluation.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
