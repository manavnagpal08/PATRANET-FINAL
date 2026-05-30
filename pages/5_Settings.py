import os
import streamlit as st
from firebase.firebase_config import is_mock

# Import styling helper
from app import CUSTOM_CSS, STORAGE_DIRS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("System Settings")

# Authentication Check
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("Authentication required. Please sign in via the Firebase Authentication widget in the sidebar.")
    st.stop()

st.write("Configure and inspect PATRANET IDP service modules.")

st.subheader("Firebase Connection Status")
if not is_mock:
    st.success("Connected to Firebase cloud services (Authentication, Firestore, Storage).")
else:
    st.info("System operating in Local Sandbox mode. Offline databases and local filesystems active.")

st.subheader("Active Filesystem Paths")
st.code(
    f"""
Uploads Directory: {STORAGE_DIRS['uploads']}
Outputs Directory: {STORAGE_DIRS['outputs']}
Images Directory:  {STORAGE_DIRS['images']}
    """
)

# Utility actions
st.subheader("Data Cache Utilities")
if st.button("Reset Stored Cache Database", type="primary"):
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
    
    st.success(f"Successfully removed {count_deleted} database objects. System memory cleared.")
