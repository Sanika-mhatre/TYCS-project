import re
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import streamlit as st

class CitationExtractor:
    """Class for extracting and analyzing citations from academic papers"""
    
    def __init__(self):
        # Common citation patterns
        self.citation_patterns = {
            'apa_author_year': r'\(([A-Z][a-zA-Z\s,&]+),?\s*(\d{4}[a-c]?)\)',
            'numbered_citation': r'\[(\d+(?:,\s*\d+)*)\]',
            'superscript_citation': r'(\w+)\^(\d+)',
            'author_year_inline': r'([A-Z][a-zA-Z]+\s+(?:et\s+al\.?\s*)?)\((\d{4}[a-c]?)\)',
            'journal_citation': r'([A-Z][a-zA-Z\s,&]+)\.\s*([^.]+)\.\s*([^,]+),?\s*(\d{4})',
        }
        
        # Reference section patterns
        self.reference_patterns = {
            'references_header': r'(?:REFERENCES?|BIBLIOGRAPHY|WORKS\s+CITED)',
            'reference_line': r'^([A-Z][^.]*\.)\s*(.*)$',
            'doi_pattern': r'doi:?\s*(10\.\d+\/[^\s]+)',
            'url_pattern': r'https?://[^\s]+',
            'journal_volume': r'(\w+)\s*,?\s*(\d+)\s*\(\s*(\d+)\s*\)',
            'page_numbers': r'pp?\.\s*(\d+(?:-\d+)?)',
        }
        
        # Academic venues and journals (sample list)
        self.academic_venues = {
            'nature', 'science', 'cell', 'lancet', 'nejm', 'pnas', 'jama',
            'ieee', 'acm', 'springer', 'elsevier', 'wiley', 'oxford',
            'journal', 'proceedings', 'conference', 'workshop', 'symposium'
        }
    
    def extract_citations(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract citations from text using multiple patterns
        
        Args:
            text: Input text to analyze
            
        Returns:
            list: List of citation dictionaries
        """
        if not text:
            return []
        
        citations = []
        
        try:
            # Extract different types of citations
            for pattern_name, pattern in self.citation_patterns.items():
                matches = re.finditer(pattern, text, re.MULTILINE)
                
                for match in matches:
                    citation = self._parse_citation(match, pattern_name)
                    if citation:
                        citations.append(citation)
            
            # Remove duplicates and clean
            citations = self._deduplicate_citations(citations)
            
            return citations
            
        except Exception as e:
            st.warning(f"Error extracting citations: {str(e)}")
            return []
    
    def extract_references(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract references from the reference section
        
        Args:
            text: Input text to analyze
            
        Returns:
            list: List of reference dictionaries
        """
        if not text:
            return []
        
        references = []
        
        try:
            # Find references section
            ref_section = self._find_references_section(text)
            if not ref_section:
                return []
            
            # Split into individual references
            ref_lines = self._split_references(ref_section)
            
            for ref_line in ref_lines:
                reference = self._parse_reference(ref_line)
                if reference:
                    references.append(reference)
            
            return references
            
        except Exception as e:
            st.warning(f"Error extracting references: {str(e)}")
            return []
    
    def _parse_citation(self, match, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Parse a citation match into structured data"""
        try:
            citation = {
                'type': pattern_name,
                'raw_text': match.group(0),
                'position': match.start()
            }
            
            if pattern_name == 'apa_author_year':
                citation['authors'] = match.group(1).strip()
                citation['year'] = match.group(2)
                
            elif pattern_name == 'numbered_citation':
                citation['numbers'] = [int(n.strip()) for n in match.group(1).split(',')]
                
            elif pattern_name == 'author_year_inline':
                citation['authors'] = match.group(1).strip()
                citation['year'] = match.group(2)
                
            elif pattern_name == 'journal_citation':
                citation['authors'] = match.group(1).strip()
                citation['title'] = match.group(2).strip()
                citation['journal'] = match.group(3).strip()
                citation['year'] = match.group(4)
            
            return citation
            
        except Exception:
            return None
    
    def _parse_reference(self, ref_text: str) -> Optional[Dict[str, Any]]:
        """Parse a reference line into structured data"""
        if not ref_text or len(ref_text.strip()) < 10:
            return None
        
        try:
            reference = {
                'raw_text': ref_text.strip(),
                'type': 'reference'
            }
            
            # Extract DOI
            doi_match = re.search(self.reference_patterns['doi_pattern'], ref_text)
            if doi_match:
                reference['doi'] = doi_match.group(1)
            
            # Extract URL
            url_match = re.search(self.reference_patterns['url_pattern'], ref_text)
            if url_match:
                reference['url'] = url_match.group(0)
            
            # Extract year
            year_match = re.search(r'\b(19|20)\d{2}\b', ref_text)
            if year_match:
                reference['year'] = int(year_match.group(0))
            
            # Extract potential journal/venue info
            journal_match = re.search(self.reference_patterns['journal_volume'], ref_text)
            if journal_match:
                reference['journal'] = journal_match.group(1)
                reference['volume'] = journal_match.group(2)
                reference['issue'] = journal_match.group(3)
            
            # Extract page numbers
            page_match = re.search(self.reference_patterns['page_numbers'], ref_text)
            if page_match:
                reference['pages'] = page_match.group(1)
            
            # Extract authors (first part before period)
            author_match = re.match(r'^([^.]+)\.', ref_text)
            if author_match:
                reference['authors'] = author_match.group(1).strip()
            
            # Extract title (look for quoted or capitalized text)
            title_patterns = [
                r'"([^"]+)"',  # Quoted title
                r'\.([A-Z][^.]*)\.',  # Capitalized sentence after period
            ]
            
            for pattern in title_patterns:
                title_match = re.search(pattern, ref_text)
                if title_match:
                    reference['title'] = title_match.group(1).strip()
                    break
            
            # Determine reference type based on content
            ref_lower = ref_text.lower()
            if any(venue in ref_lower for venue in self.academic_venues):
                reference['publication_type'] = 'journal'
            elif 'arxiv' in ref_lower:
                reference['publication_type'] = 'preprint'
            elif 'proceedings' in ref_lower or 'conference' in ref_lower:
                reference['publication_type'] = 'conference'
            elif 'book' in ref_lower or 'press' in ref_lower:
                reference['publication_type'] = 'book'
            else:
                reference['publication_type'] = 'unknown'
            
            return reference
            
        except Exception:
            return None
    
    def _find_references_section(self, text: str) -> Optional[str]:
        """Find and extract the references section"""
        # Look for references header
        header_pattern = self.reference_patterns['references_header']
        header_match = re.search(header_pattern, text, re.IGNORECASE)
        
        if not header_match:
            return None
        
        # Extract text from header to end of document
        start_pos = header_match.end()
        ref_section = text[start_pos:]
        
        # Try to find where references end (next major section)
        end_patterns = [
            r'\n\s*(?:APPENDIX|ACKNOWLEDGMENTS?|AUTHOR\s+INFORMATION)',
            r'\n\s*[A-Z][A-Z\s]*\n',  # All caps section header
        ]
        
        for pattern in end_patterns:
            end_match = re.search(pattern, ref_section, re.IGNORECASE)
            if end_match:
                ref_section = ref_section[:end_match.start()]
                break
        
        return ref_section.strip()
    
    def _split_references(self, ref_section: str) -> List[str]:
        """Split references section into individual references"""
        # Split by patterns that typically indicate new references
        split_patterns = [
            r'\n(?=\[\d+\])',  # Numbered references
            r'\n(?=[A-Z][a-zA-Z]+,\s+[A-Z])',  # Author last name, first initial
            r'\n(?=[A-Z][a-zA-Z\s]+\(\d{4}\))',  # Author (year) format
        ]
        
        references = []
        current_ref = ref_section
        
        for pattern in split_patterns:
            parts = re.split(pattern, current_ref)
            if len(parts) > 1:
                references = parts
                break
        
        # If no splitting pattern worked, try simpler line-based splitting
        if not references:
            lines = ref_section.split('\n')
            references = [line.strip() for line in lines if len(line.strip()) > 20]
        
        # Clean and filter references
        references = [ref.strip() for ref in references if ref.strip()]
        references = [ref for ref in references if len(ref) > 20]  # Filter too short
        
        return references
    
    def _deduplicate_citations(self, citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate citations"""
        seen = set()
        unique_citations = []
        
        for citation in citations:
            # Create a signature for deduplication
            signature = citation.get('raw_text', '').strip().lower()
            
            if signature and signature not in seen:
                seen.add(signature)
                unique_citations.append(citation)
        
        return unique_citations
    
    def analyze_citation_patterns(self, citations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in citations"""
        if not citations:
            return {}
        
        analysis = {
            'total_citations': len(citations),
            'citation_types': defaultdict(int),
            'years': [],
            'authors': [],
        }
        
        for citation in citations:
            # Count citation types
            analysis['citation_types'][citation.get('type', 'unknown')] += 1
            
            # Collect years
            if 'year' in citation:
                try:
                    year = int(str(citation['year'])[:4])  # Handle year formats like "2021a"
                    analysis['years'].append(year)
                except (ValueError, TypeError):
                    pass
            
            # Collect authors
            if 'authors' in citation:
                analysis['authors'].append(citation['authors'])
        
        # Calculate statistics
        if analysis['years']:
            analysis['year_range'] = (min(analysis['years']), max(analysis['years']))
            analysis['most_recent_year'] = max(analysis['years'])
            analysis['oldest_year'] = min(analysis['years'])
            analysis['avg_citation_year'] = sum(analysis['years']) / len(analysis['years'])
        
        # Convert defaultdict to regular dict
        analysis['citation_types'] = dict(analysis['citation_types'])
        
        return analysis
    
    def extract_author_network(self, references: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract author collaboration network information"""
        if not references:
            return {}
        
        authors = []
        author_counts = defaultdict(int)
        
        for ref in references:
            if 'authors' in ref:
                author_text = ref['authors']
                
                # Split authors by common separators
                author_list = re.split(r',|&|and|\band\b', author_text)
                author_list = [author.strip() for author in author_list if author.strip()]
                
                for author in author_list:
                    # Clean author name
                    author = re.sub(r'\b[A-Z]\.\s*', '', author)  # Remove initials
                    author = re.sub(r'\s+', ' ', author).strip()
                    
                    if len(author) > 2:  # Valid author name
                        authors.append(author)
                        author_counts[author] += 1
        
        # Find most cited authors
        top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_unique_authors': len(author_counts),
            'total_author_mentions': len(authors),
            'top_authors': top_authors,
            'collaboration_index': len(authors) / len(references) if references else 0
        }
    
    def get_citation_statistics(self, text: str) -> Dict[str, Any]:
        """Get comprehensive citation statistics"""
        citations = self.extract_citations(text)
        references = self.extract_references(text)
        
        stats = {
            'total_citations': len(citations),
            'total_references': len(references),
            'citation_density': len(citations) / len(text.split()) if text else 0,
        }
        
        # Analyze citation patterns
        if citations:
            citation_analysis = self.analyze_citation_patterns(citations)
            stats.update(citation_analysis)
        
        # Analyze author network
        if references:
            author_network = self.extract_author_network(references)
            stats.update(author_network)
        
        return stats