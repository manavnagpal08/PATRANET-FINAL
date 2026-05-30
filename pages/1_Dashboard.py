import streamlit as st
import pandas as pd
from firebase.firestore_service import get_documents, get_result

# Import styling helper
from app import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("📊 Operational Dashboard")
st.write("Real-time telemetry and statistics on processed documents.")

# Fetch all docs
docs = get_documents()

# Compute aggregates
total_docs = len(docs)
total_tables = 0
total_images = 0

for doc in docs:
    res = get_result(doc.get('id'))
    if res:
        total_tables += len(res.get('tables', []))
        total_images += len(res.get('images', []))

# Metric card template HTML
def metric_card(label, value):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

# Layout metrics side-by-side
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(metric_card("Total Documents", total_docs), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Tables Extracted", total_tables), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Images Siphoned", total_images), unsafe_allow_html=True)
with col4:
    st.markdown(metric_card("OCR System Health", "100%"), unsafe_allow_html=True)

st.write("---")

# Recent documents table
st.subheader("🗓️ Recent Activity Logs")
if docs:
    table_data = []
    for doc in docs:
        table_data.append({
            "Document ID": doc.get('id')[:8] + "...",
            "Name": doc.get('document_name'),
            "Page Count": doc.get('pages', 1),
            "OCR Confidence": f"{float(doc.get('confidence', 0.0))*100:.2f}%",
            "Processed At": doc.get('created_at', '')[:19]
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No documents processed yet. Head over to the Document Upload section to begin!")
