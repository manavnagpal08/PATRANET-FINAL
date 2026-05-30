import os
import json
import pandas as pd

def generate_exports(extracted_data, output_dir):
    """
    Generates real output files (JSON, CSV, XLSX) in the output_dir.
    Returns:
        dict: Paths to the generated files.
    """
    os.makedirs(output_dir, exist_ok=True)
    doc_name = extracted_data.get("document_name", "document")
    base_name = os.path.splitext(doc_name)[0]
    
    export_paths = {}
    
    # 1. Generate JSON
    json_path = os.path.join(output_dir, f"{base_name}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=4, default=str)
    export_paths["json"] = json_path
    
    # 2. Generate Excel (XLSX)
    xlsx_path = os.path.join(output_dir, f"{base_name}.xlsx")
    tables = extracted_data.get("tables", [])
    
    try:
        with pd.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
            # Additional sheets for extracted tables first
            tables_written = False
            if tables:
                for idx, table in enumerate(tables):
                    table_data = table.get("data", [])
                    if len(table_data) > 0:
                        # Extract headers
                        headers = table_data[0]
                        rows = table_data[1:]
                        df = pd.DataFrame(rows, columns=headers)
                        sheet_name = f"Table P{table['page']}_T{table['index']}"[:30] # Excel limit 31 chars
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        tables_written = True
            
            # Sheet: Metadata & Text Overview (written last so tables appear first)
            meta_df = pd.DataFrame([
                {"Metric": "Document Name", "Value": doc_name},
                {"Metric": "Pages", "Value": extracted_data["metadata"]["pages"]},
                {"Metric": "Confidence Score", "Value": extracted_data["metadata"]["confidence"]},
                {"Metric": "Text Characters", "Value": len(extracted_data["text"])}
            ])
            meta_df.to_excel(writer, sheet_name="Overview", index=False)
            
            if not tables_written:
                # Dummy sheet if no tables
                pd.DataFrame([{"Message": "No tables detected."}]).to_excel(writer, sheet_name="Tables", index=False)
        export_paths["xlsx"] = xlsx_path
    except Exception as e:
        print(f"Failed to generate Excel: {e}")
        
    # 3. Generate CSV (of the first table if available, else text summary)
    csv_path = os.path.join(output_dir, f"{base_name}.csv")
    try:
        if tables and len(tables[0].get("data", [])) > 0:
            first_table = tables[0]["data"]
            headers = first_table[0]
            rows = first_table[1:]
            df = pd.DataFrame(rows, columns=headers)
            df.to_csv(csv_path, index=False)
        else:
            meta_df.to_csv(csv_path, index=False)
        export_paths["csv"] = csv_path
    except Exception as e:
        print(f"Failed to generate CSV: {e}")
        
    return export_paths
