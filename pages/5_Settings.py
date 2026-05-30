import os
import shutil
import streamlit as st
from firebase.firebase_config import is_mock, SERVICE_ACCOUNT_PATH

# Import styling helper
from app import CUSTOM_CSS, STORAGE_DIRS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("⚙️ System Settings")
st.write("Configure and inspect PATRANET IDP service modules.")

st.subheader("🌐 Firebase Integration Connection")
if not is_mock:
    st.success("🟢 Connected to real Firebase cloud project (Authentication, Firestore, and Storage).")
else:
    st.info("ℹ️ Running in Local Sandbox fallback mode. Service account key file was not found.")
    st.markdown(
        f"""
        To connect to a live Firebase project:
        1. Place your Google Service Account credential JSON at: `{SERVICE_ACCOUNT_PATH}`
        2. Set up your Storage buckets and DB collection permissions.
        3. Refresh the application.
        """
    )

st.subheader("📁 Local Storage Directory Details")
st.code(
    f"""
Uploads Directory: {STORAGE_DIRS['uploads']}
Outputs Directory: {STORAGE_DIRS['outputs']}
Images Directory:  {STORAGE_DIRS['images']}
    """
)

# Utility actions
st.subheader("🧹 System Utilities")
if st.button("Purge Processed Document Cache", type="primary"):
    # Delete uploaded files, generated images, and local JSON database files
    count_deleted = 0
    for key, folder in STORAGE_DIRS.items():
        if os.path.exists(folder):
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        count_deleted += 1
                except Exception as e:
                    st.error(f"Error removing {file}: {e}")
                    
    # Delete local mock database JSONs
    for mock_file in ["mock_documents.json", "mock_results.json"]:
        p = os.path.join(STORAGE_DIRS["uploads"], "..", mock_file)
        p = os.path.abspath(p)
        if os.path.exists(p):
            os.remove(p)
            count_deleted += 1
            
    # Reset session states
    st.session_state["selected_doc"] = None
    st.session_state["current_pipeline_result"] = None
    
    st.success(f"Purged {count_deleted} objects. System reset complete.")
