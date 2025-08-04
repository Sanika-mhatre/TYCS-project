#!/usr/bin/env python3
"""
Demo script for Academic Research Paper Reviewer
This script demonstrates the core functionality of the application.
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_processor import PDFProcessor
from utils.text_analyzer import TextAnalyzer
from utils.review_generator import ReviewGenerator

def load_sample_paper():
    """Load the sample paper text."""
    try:
        with open('sample_paper.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        Machine Learning in Natural Language Processing: A Survey
        
        Abstract
        This paper surveys recent advances in machine learning approaches for natural language processing tasks. We examine various neural architectures and their applications across different domains.
        
        1. Introduction
        Natural language processing has experienced significant advancement through machine learning techniques. This work provides a comprehensive analysis of current methodologies and their effectiveness.
        
        2. Methodology
        We conducted a systematic review of machine learning applications in NLP, focusing on deep learning architectures including transformers, LSTM networks, and attention mechanisms.
        
        3. Results
        Our analysis shows that transformer-based models achieve state-of-the-art performance across multiple NLP benchmarks, with BERT and GPT variants leading in most categories.
        
        4. Conclusion
        Machine learning has revolutionized natural language processing, enabling unprecedented capabilities in text understanding and generation. Future work should focus on efficiency and interpretability.
        
        References
        [1] Attention Is All You Need. Vaswani et al. 2017.
        [2] BERT: Pre-training of Deep Bidirectional Transformers. Devlin et al. 2018.
        """

def demo_pdf_processing():
    """Demonstrate PDF processing capabilities."""
    print("=" * 60)
    print("📄 PDF PROCESSING DEMO")
    print("=" * 60)
    
    processor = PDFProcessor()
    sample_text = load_sample_paper()
    
    print(f"✅ Loaded sample paper ({len(sample_text)} characters)")
    
    # Demonstrate section extraction
    sections = processor.extract_sections(sample_text)
    print(f"📑 Extracted {len(sections)} sections:")
    for section, content in sections.items():
        word_count = len(content.split())
        print(f"  • {section.title()}: {word_count} words")
    
    # Demonstrate citation analysis
    citations = processor.count_citations(sample_text)
    print(f"📚 Citation Analysis:")
    print(f"  • Total citations: {citations['total_citations']}")
    print(f"  • Recent citations: {citations['recent_citations']}")
    print(f"  • Citation density: {citations['citation_density']:.2f} per 1000 words")
    
    return sample_text

def demo_text_analysis(text):
    """Demonstrate text analysis capabilities."""
    print("\n" + "=" * 60)
    print("📊 TEXT ANALYSIS DEMO")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    results = analyzer.analyze_paper(text)
    
    # Basic statistics
    basic_stats = results['basic_stats']
    print(f"📈 Basic Statistics:")
    print(f"  • Word count: {basic_stats['word_count']}")
    print(f"  • Sentence count: {basic_stats['sentence_count']}")
    print(f"  • Paragraph count: {basic_stats['paragraph_count']}")
    print(f"  • Avg words per sentence: {basic_stats['avg_words_per_sentence']:.1f}")
    
    # Readability analysis
    readability = results['readability']
    print(f"\n📖 Readability Analysis:")
    print(f"  • Flesch Reading Ease: {readability['flesch_score']:.1f}")
    print(f"  • Grade Level: {readability['grade_level']}")
    print(f"  • Avg sentence length: {readability['avg_sentence_length']:.1f}")
    print(f"  • Complex words: {readability['complex_words_percent']:.1f}%")
    
    # Keyword analysis
    keywords = results['keywords']
    print(f"\n🔑 Keyword Analysis:")
    print(f"  • Top keywords:")
    for i, (word, freq) in enumerate(keywords['top_keywords'][:5]):
        print(f"    {i+1}. {word} ({freq} occurrences)")
    
    # Academic quality
    quality = results['academic_quality']
    print(f"\n🎓 Academic Quality Indicators:")
    print(f"  • Research gap score: {quality['research_gap_score']:.3f}")
    print(f"  • Contribution clarity: {quality['contribution_clarity']:.3f}")
    print(f"  • Methodology rigor: {quality['methodology_rigor']:.3f}")
    print(f"  • Evidence strength: {quality['evidence_strength']:.3f}")
    
    return results

def demo_review_generation(text, analysis_results):
    """Demonstrate review generation capabilities."""
    print("\n" + "=" * 60)
    print("✍️ REVIEW GENERATION DEMO")
    print("=" * 60)
    
    review_gen = ReviewGenerator()
    
    # Set up review criteria
    criteria = {
        'novelty': 8,
        'methodology': 7,
        'clarity': 8,
        'significance': 7
    }
    
    print(f"⚙️ Review Criteria:")
    for criterion, weight in criteria.items():
        print(f"  • {criterion.title()}: {weight}/10")
    
    # Generate review
    review = review_gen.generate_review(
        text, 
        criteria, 
        "Academic Conference", 
        analysis_results
    )
    
    print(f"\n🎯 Overall Assessment:")
    print(f"  • Overall Score: {review['overall_score']:.1f}/10")
    print(f"  • Recommendation: {review['recommendation']}")
    
    print(f"\n📊 Detailed Scores:")
    for criterion, score in review['detailed_scores'].items():
        print(f"  • {criterion.title()}: {score:.1f}/10")
    
    print(f"\n💪 Strengths ({len(review['strengths'])}):")
    for i, strength in enumerate(review['strengths'][:3]):
        print(f"  {i+1}. {strength}")
    
    print(f"\n⚠️ Areas for Improvement ({len(review['weaknesses'])}):")
    for i, weakness in enumerate(review['weaknesses'][:3]):
        print(f"  {i+1}. {weakness}")
    
    print(f"\n💡 Suggestions ({len(review['suggestions'])}):")
    for i, suggestion in enumerate(review['suggestions'][:3]):
        print(f"  {i+1}. {suggestion}")
    
    return review

def main():
    """Run the complete demo."""
    print("🚀 Academic Research Paper Reviewer - DEMO")
    print("This demo showcases the core functionality of the application.")
    print("For the full interactive experience, run: streamlit run app.py")
    
    try:
        # Load and process the sample paper
        sample_text = demo_pdf_processing()
        
        # Analyze the text
        analysis_results = demo_text_analysis(sample_text)
        
        # Generate a review
        review = demo_review_generation(sample_text, analysis_results)
        
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("✨ Key Features Demonstrated:")
        print("  ✅ Text extraction and processing")
        print("  ✅ Comprehensive text analysis")
        print("  ✅ Academic quality assessment") 
        print("  ✅ Intelligent review generation")
        print("\n🌐 To experience the full interactive web interface:")
        print("   Run: streamlit run app.py")
        print("   Or: ./run_app.sh")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please ensure all dependencies are installed correctly.")
        print("Run: python3 test_app.py to diagnose issues.")

if __name__ == "__main__":
    main()