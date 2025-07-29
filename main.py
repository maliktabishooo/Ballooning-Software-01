import streamlit as st
import os
import tempfile
from pdf_processor import PDFProcessor
from dimension_detector import DimensionDetector
from balloon_engine import BalloonEngine
from cmm_exporter import CMMExporter
from drawing_standards import DrawingStandards
from config import Config
import cv2

# Initialize configuration
Config.init_folders()

# Set page config
st.set_page_config(
    page_title="Advanced Drawing Ballooning",
    layout="wide",
    page_icon="🎈"
)

def main():
    st.title("🎈 Advanced Engineering Drawing Ballooning Software")
    st.markdown("""
    **Upload engineering drawings (PDF) to automatically detect dimensions 
    and add balloons for CMM inspection preparation.**
    """)
    
    # Create sidebar
    with st.sidebar:
        st.header("Configuration")
        drawing_standard = st.selectbox(
            "Drawing Standard",
            DrawingStandards.SUPPORTED_STANDARDS,
            index=0
        )
        show_debug = st.checkbox("Show Debug Information", value=False)
        st.divider()
        st.info("""
        This software automates dimension ballooning for:
        - CMM inspection preparation
        - Quality control documentation
        - Engineering drawing analysis
        """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Engineering Drawing (PDF)",
        type=["pdf"],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name
        
        try:
            # Process PDF
            pdf_processor = PDFProcessor()
            pdf_images = pdf_processor.pdf_to_images(pdf_path)
            processed_images = [pdf_processor.preprocess_image(img) for img in pdf_images]
            
            # Detect dimensions
            detector = DimensionDetector(drawing_standard)
            all_dimensions = []
            all_balloons = []
            
            for page_num, img in enumerate(processed_images):
                dimensions = detector.detect_dimensions(img, page_num)
                all_dimensions.extend(dimensions)
                
                # Create balloon engine for this page
                img_height, img_width = img.shape[:2]
                balloon_engine = BalloonEngine(img_width, img_height)
                
                # Place balloons
                for dimension in dimensions:
                    balloon_engine.place_balloon(dimension)
                
                all_balloons.extend(balloon_engine.balloons)
                
                # Draw balloons on original image
                original_img = pdf_images[page_num]
                img_with_balloons = balloon_engine.draw_balloons(original_img)
                
                # Display results
                st.subheader(f"Page {page_num+1}")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.image(original_img, caption="Original Drawing", use_column_width=True)
                
                with col2:
                    st.image(img_with_balloons, caption="Ballooned Drawing", use_column_width=True)
                
                # Show debug info if enabled
                if show_debug:
                    with st.expander(f"Debug Info - Page {page_num+1}"):
                        st.write(f"Detected {len(dimensions)} dimensions")
                        st.write(dimensions)
                        st.image(img, caption="Processed Image", use_column_width=True)
            
            # Show summary
            st.success(f"✅ Processed {len(pdf_images)} pages with {len(all_dimensions)} dimensions detected")
            
            # Export options
            st.divider()
            st.subheader("Export Results")
            
            exporter = CMMExporter(all_balloons, drawing_standard)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Export to Excel"):
                    excel_path = exporter.to_excel()
                    st.success(f"Excel report saved to: {excel_path}")
                    with open(excel_path, "rb") as f:
                        st.download_button(
                            label="Download Excel Report",
                            data=f,
                            file_name="balloon_report.xlsx",
                            mime="application/vnd.ms-excel"
                        )
            
            with col2:
                if st.button("Export to CSV"):
                    csv_path = exporter.to_csv()
                    st.success(f"CSV report saved to: {csv_path}")
                    with open(csv_path, "rb") as f:
                        st.download_button(
                            label="Download CSV Report",
                            data=f,
                            file_name="balloon_report.csv",
                            mime="text/csv"
                        )
            
            with col3:
                if st.button("Generate PDF Report"):
                    pdf_path = exporter.to_pdf_report(uploaded_file.name)
                    st.success(f"PDF report saved to: {pdf_path}")
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download PDF Report",
                            data=f,
                            file_name="balloon_report.pdf",
                            mime="application/pdf"
                        )
        
        finally:
            # Clean up temporary files
            os.unlink(pdf_path)
    
    else:
        st.info("Please upload a PDF drawing to get started")

if __name__ == "__main__":
    main()
