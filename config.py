# Configuration settings
import os

class Config:
    # Path settings
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'outputs'
    TEMP_FOLDER = 'temp'
    
    # Processing parameters
    DPI = 300  # PDF conversion DPI
    MIN_DIMENSION_CONFIDENCE = 80  # OCR confidence threshold
    BALLOON_RADIUS = 20  # Balloon circle radius
    BALLOON_PADDING = 40  # Padding around balloons
    LINE_DETECTION_THRESHOLD = 100  # For dimension line detection
    
    # Supported standards
    SUPPORTED_STANDARDS = ['ASME_Y14.5', 'ISO_1101', 'DIN_406', 'JIS_B_0021']
    
    @staticmethod
    def init_folders():
        """Create necessary directories"""
        for folder in [Config.UPLOAD_FOLDER, Config.OUTPUT_FOLDER, Config.TEMP_FOLDER]:
            os.makedirs(folder, exist_ok=True)
