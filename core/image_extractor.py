import os
import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extracts all embedded images from the pages of a PDF file.
    Saves them to the output_dir and returns a list of dictionaries with image details.
    """
    os.makedirs(output_dir, exist_ok=True)
    extracted_images = []
    
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_name = f"extracted_p{page_num + 1}_img{img_index + 1}.{image_ext}"
                image_path = os.path.join(output_dir, image_name)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                extracted_images.append({
                    "name": image_name,
                    "path": image_path,
                    "page": page_num + 1,
                    "format": image_ext,
                    "size": len(image_bytes)
                })
    except Exception as e:
        print(f"Error extracting images from PDF: {e}")
        
    return extracted_images
