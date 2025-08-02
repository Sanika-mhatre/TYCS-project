import PyPDF2
from docx import Document
import io
import re
from typing import Optional


class PDFProcessor:
    """Handles text extraction from PDF and DOCX files."""
    
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, uploaded_file) -> Optional[str]:
        """
        Extract text from uploaded PDF file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Extracted text as string or None if extraction fails
        """
        try:
            # Read the PDF file
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            # Clean up the text
            text = self._clean_text(text)
            
            return text if text.strip() else None
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    def extract_text_from_docx(self, uploaded_file) -> Optional[str]:
        """
        Extract text from uploaded DOCX file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Extracted text as string or None if extraction fails
        """
        try:
            # Read the DOCX file
            doc = Document(io.BytesIO(uploaded_file.read()))
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + " "
                text += "\n"
            
            # Clean up the text
            text = self._clean_text(text)
            
            return text if text.strip() else None
            
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers (basic patterns)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Remove excessive newlines
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        # Clean up special characters
        text = text.replace('\x00', '')
        text = text.replace('\ufffd', '')
        
        return text.strip()
    
    def extract_sections(self, text: str) -> dict:
        """
        Attempt to identify and extract common paper sections.
        
        Args:
            text: Full paper text
            
        Returns:
            Dictionary with section names as keys and content as values
        """
        sections = {}
        
        # Common section patterns
        section_patterns = {
            'abstract': r'(?i)\babstract\b.*?(?=\n\s*(?:introduction|keywords|1\.|§))',
            'introduction': r'(?i)(?:introduction|1\.\s*introduction).*?(?=\n\s*(?:related work|literature review|methodology|2\.|§))',
            'methodology': r'(?i)(?:methodology|methods|approach|2\.).*?(?=\n\s*(?:results|experiments|evaluation|3\.|§))',
            'results': r'(?i)(?:results|experiments|evaluation|3\.).*?(?=\n\s*(?:discussion|conclusion|4\.|§))',
            'conclusion': r'(?i)(?:conclusion|conclusions|4\.).*?(?=\n\s*(?:references|bibliography|acknowledgments|§|\Z))',
            'references': r'(?i)(?:references|bibliography).*?(?=\n\s*(?:appendix|§|\Z))'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections[section_name] = match.group(0).strip()
        
        return sections
    
    def count_citations(self, text: str) -> dict:
        """
        Count and analyze citations in the text.
        
        Args:
            text: Paper text
            
        Returns:
            Dictionary with citation statistics
        """
        # Pattern for common citation formats
        citation_patterns = [
            r'\[(\d+)\]',  # [1], [2], etc.
            r'\[(\d+[-,\s]*\d*)\]',  # [1-3], [1, 2], etc.
            r'\(([A-Z][a-z]+\s+(?:et al\.?,\s*)?\d{4}[a-z]?)\)',  # (Author 2020)
            r'\(([A-Z][a-z]+\s+&\s+[A-Z][a-z]+,\s*\d{4})\)',  # (Author & Author, 2020)
        ]
        
        all_citations = []
        for pattern in citation_patterns:
            citations = re.findall(pattern, text)
            all_citations.extend(citations)
        
        # Estimate recent citations (rough heuristic)
        recent_citations = len([c for c in all_citations if '202' in str(c) or '201' in str(c)])
        
        return {
            'total_citations': len(all_citations),
            'recent_citations': recent_citations,
            'citation_density': len(all_citations) / max(len(text.split()), 1) * 1000  # per 1000 words
        }