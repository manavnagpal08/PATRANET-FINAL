import cv2
import numpy as np

def preprocess_image_for_ocr(image_path):
    """
    Applies OpenCV preprocessing techniques to improve OCR character recognition accuracy.
    Includes binarization, noise reduction, and contrast enhancement.
    """
    try:
        # Load image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return image_path
            
        # 1. Resize image if too small to increase DPI readability
        height, width = img.shape[:2]
        if width < 1500:
            scale_factor = 2
            img = cv2.resize(img, (width * scale_factor, height * scale_factor), interpolation=cv2.INTER_CUBIC)
            
        # 2. Apply Adaptive Thresholding (Otsu's Binarization) to convert to sharp black & white
        # This removes shadows and gradients behind the handwriting
        img = cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # 3. Denoising using morphological opening to clean stray spots
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        
        # Overwrite or save processed image
        processed_path = image_path.replace(".png", "_preprocessed.png").replace(".jpg", "_preprocessed.jpg").replace(".jpeg", "_preprocessed.jpeg")
        cv2.imwrite(processed_path, img)
        return processed_path
        
    except Exception as e:
        print(f"OpenCV Preprocessing failed: {e}. Using raw image path.")
        return image_path
