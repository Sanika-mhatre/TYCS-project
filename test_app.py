#!/usr/bin/env python3
"""
Test script for Academic Research Paper Analyzer
This script tests the core functionality without Streamlit UI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.text_analyzer import TextAnalyzer
from utils.citation_extractor import CitationExtractor
from utils.visualization import VisualizationHelper

def test_text_analyzer():
    """Test the TextAnalyzer functionality"""
    print("🔍 Testing Text Analyzer...")
    
    analyzer = TextAnalyzer()
    
    # Sample academic text
    sample_text = """
    Machine learning has revolutionized many fields of computer science and artificial intelligence.
    This paper presents a comprehensive analysis of deep learning algorithms and their applications.
    The methodology involves training neural networks on large datasets to achieve state-of-the-art performance.
    Our results demonstrate significant improvements over traditional approaches.
    In conclusion, deep learning represents a paradigm shift in how we approach complex problems.
    """
    
    try:
        # Test text statistics
        stats = analyzer.get_text_statistics(sample_text)
        print(f"  ✅ Text Statistics: {stats['word_count']} words, {stats['sentence_count']} sentences")
        
        # Test readability scores
        readability = analyzer.get_readability_scores(sample_text)
        print(f"  ✅ Readability: Flesch Score = {readability.get('flesch_reading_ease', 'N/A')}")
        
        # Test keyword extraction
        keywords = analyzer.extract_keywords(sample_text, max_keywords=5)
        print(f"  ✅ Keywords extracted: {len(keywords)} keywords")
        
        # Test sentiment analysis
        sentiment = analyzer.analyze_sentiment(sample_text)
        print(f"  ✅ Sentiment: {sentiment.get('compound', 'N/A')} compound score")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Text Analyzer Error: {e}")
        return False

def test_citation_extractor():
    """Test the CitationExtractor functionality"""
    print("📚 Testing Citation Extractor...")
    
    extractor = CitationExtractor()
    
    # Sample text with citations
    sample_text = """
    Recent studies have shown promising results (Smith et al., 2021). 
    The work by Johnson (2020) provides important insights.
    Multiple approaches have been explored [1, 2, 3].
    
    REFERENCES
    [1] Smith, J., Doe, A., & Brown, B. (2021). Deep Learning Applications. Journal of AI, 15(3), 45-67.
    [2] Johnson, M. (2020). Neural Network Architectures. Proceedings of ICML, 123-145.
    [3] Williams, K. (2019). Machine Learning Fundamentals. MIT Press.
    """
    
    try:
        # Test citation extraction
        citations = extractor.extract_citations(sample_text)
        print(f"  ✅ Citations extracted: {len(citations)} citations")
        
        # Test reference extraction
        references = extractor.extract_references(sample_text)
        print(f"  ✅ References extracted: {len(references)} references")
        
        # Test citation statistics
        stats = extractor.get_citation_statistics(sample_text)
        print(f"  ✅ Citation statistics: {stats.get('total_citations', 0)} total citations")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Citation Extractor Error: {e}")
        return False

def test_visualization():
    """Test the VisualizationHelper functionality"""
    print("📊 Testing Visualization Helper...")
    
    viz = VisualizationHelper()
    
    try:
        # Sample data for testing
        sample_keywords = [
            ('machine learning', 0.95),
            ('neural networks', 0.87),
            ('deep learning', 0.82),
            ('artificial intelligence', 0.78),
            ('data science', 0.71)
        ]
        
        # Test keyword chart creation
        chart = viz.create_keyword_chart(sample_keywords)
        print(f"  ✅ Keyword chart created: {type(chart).__name__}")
        
        # Test sentiment gauge
        sentiment_chart = viz.create_sentiment_gauge(0.25)
        print(f"  ✅ Sentiment gauge created: {type(sentiment_chart).__name__}")
        
        # Test readability radar
        readability_data = {
            'flesch_reading_ease': 45.2,
            'flesch_kincaid_grade': 12.3,
            'gunning_fog': 14.1,
            'automated_readability_index': 13.1
        }
        radar_chart = viz.create_readability_radar(readability_data)
        print(f"  ✅ Readability radar created: {type(radar_chart).__name__}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Visualization Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Academic Research Paper Analyzer - Core Functionality Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Run individual tests
    if test_text_analyzer():
        tests_passed += 1
    
    if test_citation_extractor():
        tests_passed += 1
        
    if test_visualization():
        tests_passed += 1
    
    # Results
    print("=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! The application core functionality is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())