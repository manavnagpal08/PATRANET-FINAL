import os
import streamlit as st
from firebase.storage_service import upload_file
from firebase.firestore_service import add_document, save_result
from core.pdf_processor import process_document
from core.export_engine import generate_exports

# Import styling helper
from core.style_config import CUSTOM_CSS_LOGGED_IN
st.markdown(CUSTOM_CSS_LOGGED_IN, unsafe_allow_html=True)

# Define storage directories locally to prevent app.py circular import errors
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STORAGE_DIRS = {
    "uploads": os.path.join(BASE_DIR, "storage", "uploads"),
    "outputs": os.path.join(BASE_DIR, "storage", "outputs"),
    "images": os.path.join(BASE_DIR, "storage", "images")
}

st.title("Document Upload Center")

# Authentication Check
if "user" not in st.session_state or st.session_state["user"] is None:
    st.markdown("<style>[data-testid='stSidebar'] {display: none !important;}</style>", unsafe_allow_html=True)
    st.warning("Authentication required. Please sign in via the Firebase Authentication widget in the main application portal.")
    st.stop()

st.write("Ingest PDF documents, invoices, receipts, or images to trigger the parsing pipeline.")

# Multiple files uploader
uploaded_files = st.file_uploader(
    "Select PDF or Image Files", 
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} files staged for processing.")
    
    # Process files button
    if st.button("Run Ingestion Pipeline", use_container_width=True):
        progress_bar = st.progress(0)
        
        for idx, file in enumerate(uploaded_files):
            st.write(f"Analyzing File: {file.name}")
            
            # Step 1: Save local copy
            local_input_path = os.path.join(STORAGE_DIRS["uploads"], file.name)
            with open(local_input_path, "wb") as f:
                f.write(file.getbuffer())
                
            # Step 2: Upload to Storage (real or mock fallback)
            remote_path = f"uploads/{file.name}"
            storage_url = upload_file(local_input_path, remote_path)
            
            # Step 3: Run pipeline
            extracted_data = process_document(local_input_path, STORAGE_DIRS)
            
            # Step 4: Generate exports (JSON, CSV, Excel)
            export_paths = generate_exports(extracted_data, STORAGE_DIRS["outputs"])
            
            # Upload outputs to Firebase Storage as well
            for fmt, path in export_paths.items():
                upload_file(path, f"exports/{os.path.basename(path)}")
                
            # Step 5: Save documents database metadata
            doc_record = {
                "document_name": file.name,
                "storage_url": storage_url,
                "pages": extracted_data["metadata"]["pages"],
                "confidence": extracted_data["metadata"]["confidence"],
                "user_id": st.session_state["user"]["uid"],
            }
            doc_id = add_document(doc_record)
            
            # Step 6: Save extraction result
            result_record = {
                "document_id": doc_id,
                "document_name": file.name,
                "text": extracted_data["text"],
                "tables": extracted_data["tables"],
                "images": extracted_data["images"],
                "metadata": extracted_data["metadata"],
                "export_paths": export_paths
            }
            save_result(result_record)
            
            # Save selection to session state to display in Results page
            st.session_state["selected_doc"] = doc_id
            st.session_state["current_pipeline_result"] = result_record
            
            progress_val = int((idx + 1) / len(uploaded_files) * 100)
            progress_bar.progress(progress_val)
            
        st.success("Document ingestion and parsing complete.")
        st.info("Results are now ready for review under the Results section.")
