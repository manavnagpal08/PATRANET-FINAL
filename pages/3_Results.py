import os
import json
import streamlit as st
import pandas as pd
from firebase.firestore_service import get_result

# Import styling helper
from app import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("Extraction Results Viewer")

# Fetch document ID to show
doc_id = st.session_state.get("selected_doc")
result_data = st.session_state.get("current_pipeline_result")

# If page loaded and we don't have current session result, fetch from DB
if doc_id and not result_data:
    result_data = get_result(doc_id)

if not result_data:
    st.warning("No active document loaded. Please upload a file or select a record from the History page.")
else:
    doc_name = result_data.get("document_name", "Document")
    meta = result_data.get("metadata", {})
    
    st.write(f"Record: **{doc_name}**")
    
    # Overview Banner
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("OCR Confidence Score", f"{float(meta.get('confidence', 0.0))*100:.1f}%")
    with col2:
        st.metric("Document Pages", meta.get("pages", 1))
    with col3:
        st.metric("Tables Extracted", len(result_data.get("tables", [])))
        
    st.write("---")
    
    # Download actions
    st.write("### Data Export Formats")
    exp_cols = st.columns(3)
    
    # Read files locally or fallbacks to serve Streamlit download button bytes
    export_paths = result_data.get("export_paths", {})
    
    for idx, (fmt, path) in enumerate(export_paths.items()):
        if os.path.exists(path):
            with open(path, "rb") as f:
                file_bytes = f.read()
            btn_label = f"Download {fmt.upper()}"
            mime_types = {
                "json": "application/json",
                "csv": "text/csv",
                "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
            exp_cols[idx % 3].download_button(
                label=btn_label,
                data=file_bytes,
                file_name=os.path.basename(path),
                mime=mime_types.get(fmt, "application/octet-stream"),
                use_container_width=True
            )
            
    st.write("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Extracted Text", "Tables", "Images", "Structured JSON"])
    
    # Tab 1: Extracted Text
    with tab1:
        st.subheader("Raw Text Output")
        text_content = result_data.get("text", "")
        if text_content:
            st.text_area("Plaintext Content Stream", text_content, height=400)
        else:
            st.info("No textual elements were detected in this document.")
            
    # Tab 2: Tables
    with tab2:
        st.subheader("Extracted Table Schemas")
        tables = result_data.get("tables", [])
        if tables:
            for idx, table in enumerate(tables):
                st.write(f"**Table {idx+1} (Page {table.get('page')})**")
                table_data = table.get("data", [])
                if len(table_data) > 0:
                    headers = table_data[0]
                    rows = table_data[1:]
                    df = pd.DataFrame(rows, columns=headers)
                    st.dataframe(df, use_container_width=True)
                    st.write("")
        else:
            st.info("No structured tables were parsed from the document.")
            
    # Tab 3: Images
    with tab3:
        st.subheader("Isolated PDF Asset Objects")
        images = result_data.get("images", [])
        if images:
            img_cols = st.columns(3)
            for idx, img in enumerate(images):
                img_path = img.get("path")
                if os.path.exists(img_path):
                    with img_cols[idx % 3]:
                        st.image(img_path, caption=img.get("name"), use_column_width=True)
                        with open(img_path, "rb") as f:
                            img_bytes = f.read()
                        st.download_button(
                            label=f"Download Asset",
                            data=img_bytes,
                            file_name=img.get("name"),
                            mime=f"image/{img.get('format', 'png')}",
                            key=f"dl_img_{idx}"
                        )
        else:
            st.info("No embedded image files were siphoned from the PDF document.")
            
    # Tab 4: JSON
    with tab4:
        st.subheader("JSON Output Object")
        # Structure payload to match target schema
        json_output = {
            "document_name": result_data.get("document_name", ""),
            "text": result_data.get("text", ""),
            "tables": result_data.get("tables", []),
            "images": result_data.get("images", []),
            "metadata": result_data.get("metadata", {})
        }
        st.code(json.dumps(json_output, indent=4), language="json")
