import PyPDF2
import io
import re
from typing import Optional, List, Dict, Any
import streamlit as st

class PDFProcessor:
    """Class for processing PDF files and extracting text content"""
    
    def __init__(self):
        self.supported_extensions = ['.pdf']
    
    def extract_text(self, uploaded_file) -> str:
        """
        Extract text content from uploaded PDF file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text content
        """
        try:
            # Read the uploaded file
            pdf_bytes = uploaded_file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
            
            # Clean and preprocess the text
            cleaned_text = self._clean_text(text_content)
            
            return cleaned_text
            
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and preprocess extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace and newlines
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers (basic patterns)
        text = re.sub(r'\b\d+\b(?=\s*\n)', '', text)  # Standalone numbers
        text = re.sub(r'Page \d+', '', text, flags=re.IGNORECASE)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_metadata(self, uploaded_file) -> Dict[str, Any]:
        """
        Extract metadata from PDF file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            dict: PDF metadata
        """
        try:
            pdf_bytes = uploaded_file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            metadata = {}
            
            # Basic information
            metadata['num_pages'] = len(pdf_reader.pages)
            metadata['file_size'] = len(pdf_bytes)
            
            # Document information
            if pdf_reader.metadata:
                metadata['title'] = pdf_reader.metadata.get('/Title', 'Unknown')
                metadata['author'] = pdf_reader.metadata.get('/Author', 'Unknown')
                metadata['subject'] = pdf_reader.metadata.get('/Subject', 'Unknown')
                metadata['creator'] = pdf_reader.metadata.get('/Creator', 'Unknown')
                metadata['producer'] = pdf_reader.metadata.get('/Producer', 'Unknown')
                metadata['creation_date'] = pdf_reader.metadata.get('/CreationDate', 'Unknown')
                metadata['modification_date'] = pdf_reader.metadata.get('/ModDate', 'Unknown')
            
            return metadata
            
        except Exception as e:
            st.warning(f"Could not extract metadata: {str(e)}")
            return {'num_pages': 0, 'file_size': 0}
    
    def extract_by_sections(self, uploaded_file) -> Dict[str, str]:
        """
        Attempt to extract text by common academic paper sections
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            dict: Text content organized by sections
        """
        full_text = self.extract_text(uploaded_file)
        
        if not full_text:
            return {}
        
        sections = {}
        
        # Common section patterns in academic papers
        section_patterns = {
            'abstract': r'abstract\s*:?\s*(.*?)(?=\n\s*(?:keywords?|introduction|1\.?\s*introduction))',
            'introduction': r'(?:1\.?\s*)?introduction\s*:?\s*(.*?)(?=\n\s*(?:2\.?\s*|\bmethods?\b|\bmethodology\b|\brelated work\b))',
            'methodology': r'(?:2\.?\s*)?(?:methods?|methodology)\s*:?\s*(.*?)(?=\n\s*(?:3\.?\s*|\bresults?\b|\bexperiments?\b))',
            'results': r'(?:3\.?\s*)?(?:results?|experiments?|findings?)\s*:?\s*(.*?)(?=\n\s*(?:4\.?\s*|\bdiscussion\b|\bconclusion\b))',
            'discussion': r'(?:4\.?\s*)?discussion\s*:?\s*(.*?)(?=\n\s*(?:5\.?\s*|\bconclusion\b|\breferences?\b))',
            'conclusion': r'(?:5\.?\s*)?conclusion\s*:?\s*(.*?)(?=\n\s*(?:6\.?\s*|\breferences?\b|\bbibliography\b))',
            'references': r'(?:references?|bibliography)\s*:?\s*(.*?)$'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                section_text = match.group(1).strip()
                sections[section_name] = section_text[:5000]  # Limit length
        
        # If no sections found, return the full text
        if not sections:
            sections['full_text'] = full_text
        
        return sections
    
    def get_text_stats(self, text: str) -> Dict[str, int]:
        """
        Get basic statistics about the extracted text
        
        Args:
            text: Text content
            
        Returns:
            dict: Text statistics
        """
        if not text:
            return {'words': 0, 'characters': 0, 'sentences': 0, 'paragraphs': 0}
        
        words = len(text.split())
        characters = len(text)
        sentences = len(re.findall(r'[.!?]+', text))
        paragraphs = len([p for p in text.split('\n\n') if p.strip()])
        
        return {
            'words': words,
            'characters': characters,
            'sentences': sentences,
            'paragraphs': paragraphs
        }
    
    def validate_pdf(self, uploaded_file) -> bool:
        """
        Validate if the uploaded file is a valid PDF
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            bool: True if valid PDF, False otherwise
        """
        try:
            pdf_bytes = uploaded_file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Try to access the first page
            if len(pdf_reader.pages) > 0:
                return True
            return False
            
        except Exception:
            return False