import os
import fitz  # PyMuPDF
from core.ocr_engine import extract_text_from_image
from core.table_extractor import extract_tables_from_pdf
from core.image_extractor import extract_images_from_pdf

def process_document(file_path, storage_dirs):
    """
    Orchestrates the IDP pipeline:
    1. Page rendering (if PDF) or straight OCR (if Image)
    2. Embedded image extraction
    3. OCR Text extraction
    4. Table extraction
    5. Returns structured document dictionary
    """
    doc_name = os.path.basename(file_path)
    file_ext = doc_name.split('.')[-1].lower()
    
    pages_text = []
    total_conf = 0.0
    page_count = 0
    extracted_images = []
    tables = []
    
    # 1. Process Embedded Images & Tables if PDF
    if file_ext == 'pdf':
        try:
            # Extract images from PDF
            extracted_images = extract_images_from_pdf(file_path, storage_dirs['images'])
            
            # Extract tables
            tables = extract_tables_from_pdf(file_path)
            
            # Open PDF to render pages for OCR
            doc = fitz.open(file_path)
            page_count = len(doc)
            
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                
                # Try direct digital text extraction first
                digital_text = page.get_text().strip()
                if digital_text:
                    pages_text.append(digital_text)
                    total_conf += 1.0
                else:
                    # Fall back to OCR rendering for scanned pages
                    pix = page.get_pixmap(dpi=150)
                    temp_image_path = os.path.join(storage_dirs['uploads'], f"temp_page_{page_num + 1}.png")
                    pix.save(temp_image_path)
                    
                    ocr_result = extract_text_from_image(temp_image_path)
                    pages_text.append(ocr_result.get('text', ''))
                    total_conf += ocr_result.get('confidence', 0.0)
                    
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)
                    
        except Exception as e:
            print(f"Error processing PDF {doc_name}: {e}")
            
    # Process straight Image
    elif file_ext in ['png', 'jpg', 'jpeg']:
        page_count = 1
        ocr_result = extract_text_from_image(file_path)
        pages_text.append(ocr_result.get('text', ''))
        total_conf = ocr_result.get('confidence', 0.0)
        
    # Compile structure
    avg_confidence = total_conf / page_count if page_count > 0 else 0.0
    full_text = "\n\n--- PAGE BREAK ---\n\n".join(pages_text)
    
    return {
        "document_name": doc_name,
        "text": full_text,
        "tables": tables,
        "images": extracted_images,
        "metadata": {
            "pages": page_count,
            "confidence": round(avg_confidence, 4)
        }
    }
