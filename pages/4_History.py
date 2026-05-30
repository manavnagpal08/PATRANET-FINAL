import os
import streamlit as st
from firebase.firestore_service import get_documents, get_result

# Import styling helper
from app import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("📂 Document History")
st.write("Browse, search, and manage previously analyzed documents.")

# Search query
search_query = st.text_input("🔍 Search documents by name", "")

# Load all documents from DB
docs = get_documents()

# Filter by search
if search_query:
    docs = [d for d in docs if search_query.lower() in d.get("document_name", "").lower()]

if not docs:
    st.info("No documents found matching the search criteria.")
else:
    for idx, doc in enumerate(docs):
        doc_id = doc.get("id")
        doc_name = doc.get("document_name")
        pages = doc.get("pages", 1)
        conf = float(doc.get("confidence", 0.0)) * 100
        created = doc.get("created_at", "")[:19].replace("T", " ")
        
        with st.container():
            # Card styling
            st.markdown(f"""
            <div style="background-color: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;">
                <h4 style="margin: 0 0 0.5rem 0; color: #1e3a8a;">{doc_name}</h4>
                <div style="display: flex; gap: 20px; font-size: 0.85rem; color: #64748b;">
                    <span>📄 Pages: <strong>{pages}</strong></span>
                    <span>🎯 Confidence: <strong>{conf:.2f}%</strong></span>
                    <span>🕒 Date: <strong>{created}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("👁️ View Results", key=f"view_{doc_id}_{idx}"):
                    st.session_state["selected_doc"] = doc_id
                    st.session_state["current_pipeline_result"] = None  # Reset so it re-fetches
                    st.success(f"Selected: {doc_name}. Go to 'Results' page!")
                    
            with col2:
                # Fetch results record to get the exports paths
                res_data = get_result(doc_id)
                if res_data:
                    export_paths = res_data.get("export_paths", {})
                    dl_cols = st.columns(3)
                    for e_idx, (fmt, path) in enumerate(export_paths.items()):
                        if os.path.exists(path):
                            with open(path, "rb") as f:
                                file_bytes = f.read()
                            dl_cols[e_idx].download_button(
                                label=f"Download {fmt.upper()}",
                                data=file_bytes,
                                file_name=os.path.basename(path),
                                mime="application/octet-stream",
                                key=f"dl_{doc_id}_{fmt}_{idx}"
                            )
            st.write("")
