import os
import streamlit as st

# Set Streamlit page configurations
st.set_page_config(
    page_title="PATRANET | Intelligent Document Processing",
    page_icon="📄",
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
        padding-top: 2rem;
    }
    
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }
    
    /* Elegant Card Design */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
    }
    
    /* Top Bar Styling */
    .top-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2);
    }
    
    .top-banner h1 {
        color: white !important;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .top-banner p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
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
            <p>AI-Powered Intelligent Document Processing & Data Extraction Suite</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("### Welcome to PATRANET IDP Platform")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            """
            This platform enables automated document data extraction leveraging next-gen OCR, PDF layout structural intelligence, and table mapping. 
            
            #### Main Capabilities:
            * **Scanned & Digital PDF OCR**: Extracted with high precision using PaddleOCR.
            * **Structured Table Extraction**: Detect and maintain tabular alignment.
            * **Embedded Asset Siphoning**: Auto-extract diagrams/images nested in source files.
            * **Multi-Format Export**: Compile document fields into Excel spreadsheets, CSVs, or JSON arrays.
            """
        )
        
        st.info("👈 Navigate using the sidebar menu to upload documents, view extracted outputs, or query past document history.")
        
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">App Mode</div>
                <div class="metric-value" style="font-size: 1.5rem; color: #2563eb;">Enterprise Sandbox</div>
                <p style="margin-top: 0.5rem; font-size: 0.85rem; color: #64748b;">
                    Running with Local DB and Mock fallback features to ensure zero-delay hackathon evaluations.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
