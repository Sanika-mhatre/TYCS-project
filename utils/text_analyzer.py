import nltk
import textstat
import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag


class TextAnalyzer:
    """Comprehensive text analysis for academic papers."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        # Academic keywords for relevance assessment
        self.academic_keywords = {
            'methodology': ['method', 'approach', 'technique', 'algorithm', 'framework', 'model', 'system'],
            'evaluation': ['evaluation', 'experiment', 'test', 'validation', 'assessment', 'analysis', 'comparison'],
            'results': ['result', 'finding', 'outcome', 'performance', 'accuracy', 'precision', 'recall'],
            'novelty': ['novel', 'new', 'innovative', 'original', 'unique', 'contribution', 'advancement'],
            'significance': ['significant', 'important', 'impact', 'implication', 'benefit', 'advantage']
        }
    
    def analyze_paper(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of the paper text.
        
        Args:
            text: Full paper text
            
        Returns:
            Dictionary containing all analysis results
        """
        results = {}
        
        # Basic text statistics
        results['basic_stats'] = self._get_basic_stats(text)
        
        # Readability analysis
        results['readability'] = self._analyze_readability(text)
        
        # Structure analysis
        results['structure'] = self._analyze_structure(text)
        
        # Keyword analysis
        results['keywords'] = self._analyze_keywords(text)
        
        # Citations analysis
        results['citations'] = self._analyze_citations(text)
        
        # Writing patterns
        results['writing_patterns'] = self._analyze_writing_patterns(text)
        
        # Academic quality indicators
        results['academic_quality'] = self._assess_academic_quality(text)
        
        return results
    
    def _get_basic_stats(self, text: str) -> Dict[str, int]:
        """Get basic text statistics."""
        words = text.split()
        sentences = sent_tokenize(text)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'character_count': len(text),
            'avg_words_per_sentence': len(words) / max(len(sentences), 1),
            'avg_sentences_per_paragraph': len(sentences) / max(len(paragraphs), 1)
        }
    
    def _analyze_readability(self, text: str) -> Dict[str, Any]:
        """Analyze text readability using multiple metrics."""
        try:
            flesch_score = textstat.flesch_reading_ease(text)
            flesch_grade = textstat.flesch_kincaid_grade(text)
            gunning_fog = textstat.gunning_fog(text)
            automated_readability = textstat.automated_readability_index(text)
            
            # Calculate additional metrics
            sentences = sent_tokenize(text)
            words = text.split()
            
            avg_sentence_length = len(words) / max(len(sentences), 1)
            
            # Complex words (>2 syllables)
            complex_words = [word for word in words if textstat.syllable_count(word) > 2]
            complex_words_percent = (len(complex_words) / max(len(words), 1)) * 100
            
            # Determine reading level
            if flesch_score >= 90:
                grade_level = "Elementary School"
            elif flesch_score >= 80:
                grade_level = "Middle School"
            elif flesch_score >= 70:
                grade_level = "High School"
            elif flesch_score >= 60:
                grade_level = "College"
            elif flesch_score >= 50:
                grade_level = "Graduate"
            else:
                grade_level = "Post-Graduate"
            
            return {
                'flesch_score': flesch_score,
                'flesch_grade': flesch_grade,
                'gunning_fog': gunning_fog,
                'automated_readability': automated_readability,
                'avg_sentence_length': avg_sentence_length,
                'complex_words_percent': complex_words_percent,
                'grade_level': grade_level
            }
        except Exception as e:
            print(f"Error in readability analysis: {e}")
            return {
                'flesch_score': 50.0,
                'flesch_grade': 12.0,
                'gunning_fog': 12.0,
                'automated_readability': 12.0,
                'avg_sentence_length': 20.0,
                'complex_words_percent': 25.0,
                'grade_level': "Graduate"
            }
    
    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze paper structure and organization."""
        from utils.pdf_processor import PDFProcessor
        
        processor = PDFProcessor()
        sections = processor.extract_sections(text)
        
        # Calculate section word counts
        section_word_counts = {}
        for section, content in sections.items():
            section_word_counts[section] = len(content.split())
        
        # Assess abstract quality
        abstract_quality = 0.0
        if 'abstract' in sections:
            abstract_words = len(sections['abstract'].split())
            if 100 <= abstract_words <= 300:
                abstract_quality = 1.0
            elif 50 <= abstract_words < 100 or 300 < abstract_words <= 400:
                abstract_quality = 0.7
            else:
                abstract_quality = 0.3
        
        # Assess conclusion quality
        conclusion_quality = 0.0
        if 'conclusion' in sections:
            conclusion_words = len(sections['conclusion'].split())
            total_words = sum(section_word_counts.values())
            conclusion_ratio = conclusion_words / max(total_words, 1)
            
            if 0.05 <= conclusion_ratio <= 0.15:
                conclusion_quality = 1.0
            elif 0.02 <= conclusion_ratio < 0.05 or 0.15 < conclusion_ratio <= 0.25:
                conclusion_quality = 0.7
            else:
                conclusion_quality = 0.3
        
        # Calculate balance score
        if section_word_counts:
            word_counts = list(section_word_counts.values())
            balance_score = 1.0 - (np.std(word_counts) / max(np.mean(word_counts), 1))
            balance_score = max(0.0, min(1.0, balance_score))
        else:
            balance_score = 0.0
        
        return {
            'sections': section_word_counts,
            'total_sections': len(sections),
            'abstract_quality': abstract_quality,
            'conclusion_quality': conclusion_quality,
            'balance_score': balance_score,
            'has_methodology': 'methodology' in sections,
            'has_results': 'results' in sections
        }
    
    def _analyze_keywords(self, text: str) -> Dict[str, Any]:
        """Extract and analyze keywords from the text."""
        # Clean text for keyword extraction
        text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
        words = word_tokenize(text_clean)
        
        # Remove stopwords and short words
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        # Get word frequencies
        word_freq = Counter(words)
        top_keywords = word_freq.most_common(20)
        
        # Extract noun phrases as potential key terms
        sentences = sent_tokenize(text)
        noun_phrases = []
        
        for sentence in sentences[:100]:  # Limit for performance
            words_tagged = pos_tag(word_tokenize(sentence))
            current_phrase = []
            
            for word, tag in words_tagged:
                if tag.startswith('NN') or tag.startswith('JJ'):  # Nouns and adjectives
                    current_phrase.append(word.lower())
                else:
                    if len(current_phrase) > 1:
                        phrase = ' '.join(current_phrase)
                        if len(phrase) > 3 and phrase not in self.stop_words:
                            noun_phrases.append(phrase)
                    current_phrase = []
        
        phrase_freq = Counter(noun_phrases)
        top_phrases = phrase_freq.most_common(10)
        
        # Calculate keyword density
        total_words = len(text.split())
        keyword_density = {}
        for category, keywords in self.academic_keywords.items():
            category_count = sum(text.lower().count(keyword) for keyword in keywords)
            keyword_density[category] = (category_count / total_words) * 100
        
        return {
            'top_keywords': top_keywords,
            'top_phrases': top_phrases,
            'keyword_density': keyword_density,
            'academic_keyword_coverage': sum(1 for density in keyword_density.values() if density > 0.1)
        }
    
    def _analyze_citations(self, text: str) -> Dict[str, Any]:
        """Analyze citations in the paper."""
        from utils.pdf_processor import PDFProcessor
        
        processor = PDFProcessor()
        return processor.count_citations(text)
    
    def _analyze_writing_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze writing patterns and style."""
        sentences = sent_tokenize(text)
        words = text.split()
        
        # Sentence length analysis
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        
        # Word frequency analysis
        word_freq = Counter(word.lower().strip(string.punctuation) for word in words)
        
        # Passive voice detection (simple heuristic)
        passive_indicators = ['was', 'were', 'been', 'being', 'is', 'are', 'am']
        passive_count = sum(text.lower().count(indicator) for indicator in passive_indicators)
        passive_ratio = passive_count / max(len(words), 1)
        
        # Academic tone indicators
        academic_indicators = ['however', 'furthermore', 'therefore', 'moreover', 'nonetheless', 'consequently']
        academic_count = sum(text.lower().count(indicator) for indicator in academic_indicators)
        academic_tone_score = academic_count / max(len(sentences), 1)
        
        return {
            'sentence_lengths': sentence_lengths,
            'avg_sentence_length': np.mean(sentence_lengths),
            'sentence_length_std': np.std(sentence_lengths),
            'word_frequencies': dict(word_freq.most_common(50)),
            'passive_voice_ratio': passive_ratio,
            'academic_tone_score': academic_tone_score
        }
    
    def _assess_academic_quality(self, text: str) -> Dict[str, float]:
        """Assess various aspects of academic quality."""
        # Research gap identification
        gap_indicators = ['gap', 'limitation', 'lack', 'absence', 'missing', 'insufficient']
        gap_score = sum(text.lower().count(indicator) for indicator in gap_indicators) / len(text.split())
        
        # Contribution clarity
        contribution_indicators = ['contribution', 'novel', 'new', 'propose', 'introduce', 'present']
        contribution_score = sum(text.lower().count(indicator) for indicator in contribution_indicators) / len(text.split())
        
        # Methodology rigor
        method_indicators = ['method', 'approach', 'technique', 'algorithm', 'procedure', 'protocol']
        methodology_score = sum(text.lower().count(indicator) for indicator in method_indicators) / len(text.split())
        
        # Evidence strength
        evidence_indicators = ['result', 'finding', 'data', 'evidence', 'proof', 'demonstrate']
        evidence_score = sum(text.lower().count(indicator) for indicator in evidence_indicators) / len(text.split())
        
        return {
            'research_gap_score': min(gap_score * 1000, 1.0),  # Normalize
            'contribution_clarity': min(contribution_score * 1000, 1.0),
            'methodology_rigor': min(methodology_score * 1000, 1.0),
            'evidence_strength': min(evidence_score * 1000, 1.0)
        }