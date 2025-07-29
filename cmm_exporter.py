import pandas as pd
from fpdf import FPDF
import os
from config import Config
from drawing_standards import DrawingStandards

class CMMExporter:
    def __init__(self, balloons, standard='ASME_Y14.5'):
        self.balloons = balloons
        self.standard = DrawingStandards(standard)
    
    def to_excel(self):
        """Export balloon data to Excel format"""
        data = []
        for balloon in self.balloons:
            dim = balloon.dimension
            data.append({
                'Balloon ID': balloon.id,
                'Dimension': dim['text'],
                'Value': dim['value'],
                'Tolerance': dim.get('tolerance', ''),
                'Page': dim['page'] + 1
            })
        
        df = pd.DataFrame(data)
        excel_path = os.path.join(Config.OUTPUT_FOLDER, 'balloon_report.xlsx')
        df.to_excel(excel_path, index=False)
        return excel_path
    
    def to_csv(self):
        """Export balloon data to CSV format"""
        data = []
        for balloon in self.balloons:
            dim = balloon.dimension
            data.append({
                'Balloon ID': balloon.id,
                'Dimension': dim['text'],
                'Value': dim['value'],
                'Tolerance': dim.get('tolerance', ''),
                'Page': dim['page'] + 1
            })
        
        df = pd.DataFrame(data)
        csv_path = os.path.join(Config.OUTPUT_FOLDER, 'balloon_report.csv')
        df.to_csv(csv_path, index=False)
        return csv_path
    
    def to_pdf_report(self, original_pdf_path):
        """Generate PDF report with ballooned drawings"""
        pdf = FPDF()
        
        # Add cover page
        pdf.add_page()
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(0, 40, "Ballooned Drawing Report", 0, 1, 'C')
        pdf.ln(20)
        
        # Add balloon table
        pdf.set_font("Arial", size=12)
        col_widths = [20, 30, 50, 30, 20]
        headers = ['ID', 'Value', 'Tolerance', 'Page', 'Notes']
        
        # Table header
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
        pdf.ln()
        
        # Table rows
        for balloon in self.balloons:
            dim = balloon.dimension
            pdf.cell(col_widths[0], 10, str(balloon.id), 1, 0, 'C')
            pdf.cell(col_widths[1], 10, str(dim['value']), 1, 0, 'C')
            pdf.cell(col_widths[2], 10, str(dim.get('tolerance', '')), 1, 0, 'C')
            pdf.cell(col_widths[3], 10, str(dim['page'] + 1), 1, 0, 'C')
            pdf.cell(col_widths[4], 10, '', 1, 1, 'C')
        
        # Save PDF
        pdf_path = os.path.join(Config.OUTPUT_FOLDER, 'balloon_report.pdf')
        pdf.output(pdf_path)
        return pdf_path
