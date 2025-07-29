import re

class DrawingStandards:
    def __init__(self, standard='ASME_Y14.5'):
        self.standard = standard
        self.patterns = {
            'ASME_Y14.5': r'^(\d+\.?\d*)\s*([±\+\-]\s*\d+\.?\d*)?$',
            'ISO_1101': r'^(\d+\.?\d*)\s*(\+\d+\.?\d*\s*\/\s*\-\d+\.?\d*)?$',
            'DIN_406': r'^(\d+\.?\d*)\s*(\(\+\d+\.?\d*\s*\/\s*\-\d+\.?\d*\))?$',
            'JIS_B_0021': r'^(\d+\.?\d*)\s*([\+\-]\d+\.?\d*)?$'
        }
    
    def get_dimension_regex(self):
        """Get regex pattern for the current standard"""
        pattern = self.patterns.get(self.standard, self.patterns['ASME_Y14.5'])
        return re.compile(pattern)
    
    def get_tolerance_format(self):
        """Get tolerance formatting rules for the standard"""
        formats = {
            'ASME_Y14.5': "{value} {tolerance}",
            'ISO_1101': "{value} {tolerance}",
            'DIN_406': "{value} {tolerance}",
            'JIS_B_0021': "{value}{tolerance}"
        }
        return formats.get(self.standard, formats['ASME_Y14.5'])
