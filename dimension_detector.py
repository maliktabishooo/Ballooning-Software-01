import cv2
import pytesseract
import re
import numpy as np
from drawing_standards import DrawingStandards

class DimensionDetector:
    def __init__(self, standard='ASME_Y14.5'):
        self.standard = DrawingStandards(standard)
        self.dimension_pattern = self.standard.get_dimension_regex()
        
    def detect_lines(self, img):
        """Detect dimension lines using Hough Line Transform"""
        # Detect edges
        edges = cv2.Canny(img, 50, 150, apertureSize=3)
        
        # Detect lines
        lines = cv2.HoughLinesP(
            edges, 1, np.pi/180, Config.LINE_DETECTION_THRESHOLD,
            minLineLength=50, maxLineGap=10
        )
        
        return lines
    
    def detect_dimensions(self, img, page_num):
        """Detect dimensions using OCR and line detection"""
        # Run OCR to get text data
        ocr_data = pytesseract.image_to_data(
            img, output_type=pytesseract.Output.DICT, config='--psm 6'
        )
        
        dimensions = []
        line_segments = self.detect_lines(img) if img is not None else []
        
        # Process OCR results
        for i in range(len(ocr_data['text'])):
            text = ocr_data['text'][i].strip()
            conf = int(ocr_data['conf'][i])
            
            # Skip low confidence or empty text
            if conf < Config.MIN_DIMENSION_CONFIDENCE or not text:
                continue
                
            # Check if text matches dimension pattern
            if match := self.dimension_pattern.match(text):
                x, y, w, h = (
                    ocr_data['left'][i], 
                    ocr_data['top'][i], 
                    ocr_data['width'][i], 
                    ocr_data['height'][i]
                )
                
                # Find associated dimension lines
                associated_lines = self.find_associated_lines(
                    (x, y, w, h), line_segments
                )
                
                dimensions.append({
                    'text': text,
                    'value': match.group(1),
                    'tolerance': match.group(2) if match.lastindex >= 2 else None,
                    'coords': (x, y, w, h),
                    'lines': associated_lines,
                    'page': page_num
                })
        
        return dimensions
    
    def find_associated_lines(self, text_bbox, lines):
        """Find dimension lines associated with text"""
        if lines is None:
            return []
            
        tx, ty, tw, th = text_bbox
        text_center = (tx + tw//2, ty + th//2)
        associated = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            line_center = ((x1+x2)//2, (y1+y2)//2)
            
            # Calculate distance from text center to line center
            distance = np.sqrt((text_center[0]-line_center[0])**2 + 
                              (text_center[1]-line_center[1])**2)
            
            # If close enough, consider associated
            if distance < 200:  # 200 pixels threshold
                associated.append((x1, y1, x2, y2))
        
        return associated
