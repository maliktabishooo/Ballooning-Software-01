import fitz  # PyMuPDF
import cv2
import numpy as np
import os
from config import Config

class PDFProcessor:
    def __init__(self):
        Config.init_folders()
    
    def pdf_to_images(self, pdf_path):
        """Convert PDF to high-resolution images"""
        images = []
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            zoom = Config.DPI / 72  # 72 is default DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, 3)
            images.append(img)
        
        return images
    
    def preprocess_image(self, img):
        """Enhance image for better OCR and line detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Noise reduction
        kernel = np.ones((2, 2), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        return processed
    
    def save_temp_image(self, img, page_num):
        """Save temporary image for debugging"""
        temp_path = os.path.join(Config.TEMP_FOLDER, f"page_{page_num+1}.png")
        cv2.imwrite(temp_path, img)
        return temp_path
