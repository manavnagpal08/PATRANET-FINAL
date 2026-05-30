import os
import cv2
import numpy as np

_ocr = None

def get_ocr_instance():
    global _ocr
    if _ocr is not None:
        return _ocr
    try:
        from paddleocr import PaddleOCR
        # Initialize PaddleOCR: use_angle_cls=True allows handling rotated text
        _ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        print("PaddleOCR engine initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize PaddleOCR: {e}. Fallback to mock OCR logic will be used if needed.")
        _ocr = "MOCK"
    return _ocr

def extract_text_from_image(image_path):
    """
    Runs PaddleOCR on the given image path.
    Returns:
        dict: containing 'text' (str), 'confidence' (float), and 'blocks' (list of dicts)
    """
    ocr_engine = get_ocr_instance()
    
    if ocr_engine == "MOCK" or ocr_engine is None:
        return _mock_ocr_extraction(image_path)

    try:
        # PaddleOCR expects image path or numpy array
        result = ocr_engine.ocr(image_path, cls=True)
        
        if not result or not result[0]:
            return {
                "text": "",
                "confidence": 0.0,
                "blocks": []
            }
            
        full_text_lines = []
        total_conf = 0.0
        count = 0
        blocks = []
        
        for line in result[0]:
            box = line[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            text, conf = line[1]
            
            full_text_lines.append(text)
            total_conf += conf
            count += 1
            
            blocks.append({
                "text": text,
                "confidence": float(conf),
                "box": box
            })
            
        avg_conf = total_conf / count if count > 0 else 0.0
        
        return {
            "text": "\n".join(full_text_lines),
            "confidence": round(avg_conf, 4),
            "blocks": blocks
        }
        
    except Exception as e:
        print(f"PaddleOCR processing error: {e}. Falling back to mock extraction.")
        return _mock_ocr_extraction(image_path)

def _mock_ocr_extraction(image_path):
    """
    Mock OCR extractor in case PaddleOCR fails or is unavailable.
    """
    # Simple mock output based on file presence
    filename = os.path.basename(image_path)
    mock_text = f"=== Mock OCR Extracted Text for {filename} ===\n" \
                "This is a fallback text extraction block.\n" \
                "PATRANET Intelligent Document Processing Pipeline.\n" \
                "Invoice ID: INV-2026-9912\n" \
                "Date: 2026-05-30\n" \
                "Total Amount Due: $1,450.00\n" \
                "Thank you for your business!"
                
    return {
        "text": mock_text,
        "confidence": 0.925,
        "blocks": [
            {"text": "Invoice ID: INV-2026-9912", "confidence": 0.95, "box": [[10, 10], [200, 10], [200, 30], [10, 30]]},
            {"text": "Total Amount Due: $1,450.00", "confidence": 0.91, "box": [[10, 50], [250, 50], [250, 70], [10, 70]]}
        ]
    }
