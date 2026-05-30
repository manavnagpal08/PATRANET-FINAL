import os
import fitz  # PyMuPDF
from core.ocr_engine import extract_text_from_image
from core.table_extractor import extract_tables_from_pdf
from core.image_extractor import extract_images_from_pdf
from core.spelling_corrector import auto_correct_spelling

def process_document(file_path, storage_dirs):
    """
    Orchestrates the IDP pipeline:
    1. Page rendering (if PDF) or straight OCR (if Image)
    2. Embedded image extraction
    3. OCR Text extraction
    4. Table extraction
    5. Spelling auto-correction
    6. Returns structured document dictionary
    """
    doc_name = os.path.basename(file_path)
    file_ext = doc_name.split('.')[-1].lower()
    
    pages_text = []
    total_conf = 0.0
    page_count = 0
    extracted_images = []
    tables = []
    page_images = []
    
    # 1. Process Embedded Images & Tables if PDF
    if file_ext == 'pdf':
        try:
            # Extract images from PDF
            extracted_images = extract_images_from_pdf(file_path, storage_dirs['images'])
            
            # Extract tables
            tables = extract_tables_from_pdf(file_path)
            
            # Open PDF to render pages for OCR and visualization
            doc = fitz.open(file_path)
            page_count = len(doc)
            
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                
                # Render page image for visualizer preview
                pix = page.get_pixmap(dpi=150)
                page_img_name = f"{os.path.splitext(doc_name)[0]}_p{page_num + 1}.png"
                page_img_path = os.path.join(storage_dirs['images'], page_img_name)
                pix.save(page_img_path)
                page_images.append(page_img_path)
                
                # Try direct digital text extraction first
                digital_text = page.get_text().strip()
                if digital_text:
                    pages_text.append(digital_text)
                    total_conf += 1.0
                else:
                    # Perform OCR using the preprocessed page image to minimize errors
                    from core.image_preprocessor import preprocess_image_for_ocr
                    preprocessed_img_path = preprocess_image_for_ocr(page_img_path)
                    ocr_result = extract_text_from_image(preprocessed_img_path)
                    pages_text.append(ocr_result.get('text', ''))
                    total_conf += ocr_result.get('confidence', 0.0)
                    
        except Exception as e:
            print(f"Error processing PDF {doc_name}: {e}")
            
    # Process straight Image
    elif file_ext in ['png', 'jpg', 'jpeg']:
        page_count = 1
        page_images.append(file_path)
        from core.image_preprocessor import preprocess_image_for_ocr
        preprocessed_img_path = preprocess_image_for_ocr(file_path)
        ocr_result = extract_text_from_image(preprocessed_img_path)
        pages_text.append(ocr_result.get('text', ''))
        total_conf = ocr_result.get('confidence', 0.0)
        
    # Compile structure
    avg_confidence = total_conf / page_count if page_count > 0 else 0.0
    full_text = "\n\n--- PAGE BREAK ---\n\n".join(pages_text)
    
    # Auto-correct spelling mistakes automatically in the background
    full_text = auto_correct_spelling(full_text)
    
    return {
        "document_name": doc_name,
        "text": full_text,
        "tables": tables,
        "images": extracted_images,
        "page_images": page_images,
        "metadata": {
            "pages": page_count,
            "confidence": round(avg_confidence, 4)
        }
    }
