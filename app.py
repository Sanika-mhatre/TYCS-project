import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import json
from datetime import datetime

# Import custom modules
from utils.pdf_processor import PDFProcessor
from utils.text_analyzer import TextAnalyzer
from utils.citation_extractor import CitationExtractor
from utils.visualization import VisualizationHelper

# Page configuration
st.set_page_config(
    page_title="Academic Research Paper Analyzer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .analysis-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Title and description
    st.markdown('<h1 class="main-header">📚 Academic Research Paper Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("""
    **Comprehensive tool for analyzing academic research papers**
    
    Upload your research papers and get detailed insights including:
    - Text statistics and readability analysis
    - Keyword extraction and topic modeling
    - Citation analysis and reference extraction
    - Sentiment analysis and writing quality assessment
    - Interactive visualizations and summaries
    """)

    # Initialize session state
    if 'analyzed_papers' not in st.session_state:
        st.session_state.analyzed_papers = []
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None

    # Sidebar for navigation and controls
    with st.sidebar:
        st.header("📋 Analysis Dashboard")
        
        # File upload section
        st.subheader("📄 Upload Research Papers")
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more academic papers in PDF format"
        )
        
        # Analysis options
        st.subheader("🔧 Analysis Options")
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Complete Analysis", "Text Statistics", "Keyword Analysis", 
             "Citation Analysis", "Readability Assessment", "Topic Modeling"]
        )
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            max_keywords = st.slider("Max Keywords to Extract", 10, 100, 20)
            min_word_length = st.slider("Minimum Word Length", 3, 8, 4)
            include_stopwords = st.checkbox("Include Common Words", False)
            language = st.selectbox("Document Language", ["english", "spanish", "french", "german"])

    # Main content area
    if uploaded_files:
        # Process uploaded files
        if st.button("🚀 Analyze Papers", type="primary"):
            process_papers(uploaded_files, analysis_type, {
                'max_keywords': max_keywords,
                'min_word_length': min_word_length,
                'include_stopwords': include_stopwords,
                'language': language
            })
        
        # Display existing analyses
        if st.session_state.analyzed_papers:
            display_analysis_results()
    else:
        # Welcome screen with sample data option
        display_welcome_screen()

def process_papers(uploaded_files, analysis_type, settings):
    """Process uploaded papers and perform analysis"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    pdf_processor = PDFProcessor()
    text_analyzer = TextAnalyzer()
    citation_extractor = CitationExtractor()
    
    total_files = len(uploaded_files)
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        progress_bar.progress((i + 1) / total_files)
        
        try:
            # Extract text from PDF
            text_content = pdf_processor.extract_text(uploaded_file)
            
            if not text_content.strip():
                st.error(f"Could not extract text from {uploaded_file.name}")
                continue
            
            # Perform analysis based on selected type
            analysis_results = perform_analysis(
                text_content, uploaded_file.name, analysis_type, 
                text_analyzer, citation_extractor, settings
            )
            
            # Store results
            st.session_state.analyzed_papers.append(analysis_results)
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    
    progress_bar.empty()
    status_text.empty()
    st.success(f"Successfully analyzed {len(uploaded_files)} papers!")

def perform_analysis(text, filename, analysis_type, text_analyzer, citation_extractor, settings):
    """Perform the selected type of analysis on the text"""
    results = {
        'filename': filename,
        'timestamp': datetime.now(),
        'text_length': len(text),
        'word_count': len(text.split())
    }
    
    if analysis_type in ["Complete Analysis", "Text Statistics"]:
        results['text_stats'] = text_analyzer.get_text_statistics(text)
        results['readability'] = text_analyzer.get_readability_scores(text)
    
    if analysis_type in ["Complete Analysis", "Keyword Analysis"]:
        results['keywords'] = text_analyzer.extract_keywords(
            text, 
            max_keywords=settings['max_keywords'],
            min_length=settings['min_word_length']
        )
        results['phrases'] = text_analyzer.extract_key_phrases(text)
    
    if analysis_type in ["Complete Analysis", "Citation Analysis"]:
        results['citations'] = citation_extractor.extract_citations(text)
        results['references'] = citation_extractor.extract_references(text)
    
    if analysis_type in ["Complete Analysis", "Topic Modeling"]:
        results['topics'] = text_analyzer.extract_topics(text)
        results['sentiment'] = text_analyzer.analyze_sentiment(text)
    
    return results

def display_analysis_results():
    """Display the analysis results for all processed papers"""
    st.markdown('<h2 class="sub-header">📊 Analysis Results</h2>', unsafe_allow_html=True)
    
    # Paper selection
    paper_names = [paper['filename'] for paper in st.session_state.analyzed_papers]
    selected_paper = st.selectbox("Select Paper to View", paper_names)
    
    if selected_paper:
        paper_data = next(paper for paper in st.session_state.analyzed_papers 
                         if paper['filename'] == selected_paper)
        
        # Display results in tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overview", "🔤 Text Analysis", "🔍 Keywords", 
            "📚 Citations", "📊 Visualizations"
        ])
        
        with tab1:
            display_overview(paper_data)
        
        with tab2:
            display_text_analysis(paper_data)
        
        with tab3:
            display_keyword_analysis(paper_data)
        
        with tab4:
            display_citation_analysis(paper_data)
        
        with tab5:
            display_visualizations(paper_data)

def display_overview(paper_data):
    """Display overview metrics for the paper"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Word Count", f"{paper_data['word_count']:,}")
    
    with col2:
        st.metric("Character Count", f"{paper_data['text_length']:,}")
    
    with col3:
        pages_estimate = paper_data['word_count'] // 250  # Rough estimate
        st.metric("Estimated Pages", pages_estimate)
    
    with col4:
        if 'readability' in paper_data:
            reading_time = paper_data['word_count'] // 200  # Words per minute
            st.metric("Reading Time (min)", reading_time)
    
    # Readability scores
    if 'readability' in paper_data:
        st.subheader("📖 Readability Assessment")
        readability = paper_data['readability']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Flesch Reading Ease", f"{readability.get('flesch_reading_ease', 0):.1f}")
            st.metric("Flesch-Kincaid Grade", f"{readability.get('flesch_kincaid_grade', 0):.1f}")
        
        with col2:
            st.metric("Automated Readability Index", f"{readability.get('automated_readability_index', 0):.1f}")
            st.metric("Average Sentence Length", f"{readability.get('avg_sentence_length', 0):.1f}")

def display_text_analysis(paper_data):
    """Display detailed text analysis"""
    if 'text_stats' in paper_data:
        stats = paper_data['text_stats']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Text Statistics")
            st.metric("Sentences", stats.get('sentence_count', 0))
            st.metric("Paragraphs", stats.get('paragraph_count', 0))
            st.metric("Unique Words", stats.get('unique_words', 0))
            st.metric("Lexical Diversity", f"{stats.get('lexical_diversity', 0):.3f}")
        
        with col2:
            st.subheader("📝 Writing Metrics")
            st.metric("Average Words per Sentence", f"{stats.get('avg_words_per_sentence', 0):.1f}")
            st.metric("Average Syllables per Word", f"{stats.get('avg_syllables_per_word', 0):.1f}")
            
            if 'sentiment' in paper_data:
                sentiment = paper_data['sentiment']
                st.metric("Sentiment Score", f"{sentiment.get('compound', 0):.3f}")

def display_keyword_analysis(paper_data):
    """Display keyword and phrase analysis"""
    if 'keywords' in paper_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔑 Top Keywords")
            keywords_df = pd.DataFrame(paper_data['keywords'], columns=['Keyword', 'Score'])
            st.dataframe(keywords_df, use_container_width=True)
        
        with col2:
            st.subheader("💭 Key Phrases")
            if 'phrases' in paper_data:
                phrases_df = pd.DataFrame(paper_data['phrases'], columns=['Phrase', 'Relevance'])
                st.dataframe(phrases_df, use_container_width=True)

def display_citation_analysis(paper_data):
    """Display citation and reference analysis"""
    if 'citations' in paper_data:
        st.subheader("📚 Citations Found")
        citations = paper_data['citations']
        
        if citations:
            citations_df = pd.DataFrame(citations)
            st.dataframe(citations_df, use_container_width=True)
            
            # Citation statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Citations", len(citations))
            with col2:
                unique_authors = len(set(cit.get('author', 'Unknown') for cit in citations))
                st.metric("Unique Authors", unique_authors)
            with col3:
                years = [cit.get('year') for cit in citations if cit.get('year')]
                if years:
                    st.metric("Date Range", f"{min(years)}-{max(years)}")
        else:
            st.info("No citations found in this document.")

def display_visualizations(paper_data):
    """Display various visualizations"""
    viz_helper = VisualizationHelper()
    
    # Word cloud
    if 'keywords' in paper_data:
        st.subheader("☁️ Word Cloud")
        wordcloud_fig = viz_helper.create_wordcloud(paper_data['keywords'])
        st.pyplot(wordcloud_fig)
    
    # Keyword frequency chart
    if 'keywords' in paper_data:
        st.subheader("📊 Keyword Frequency")
        keywords_chart = viz_helper.create_keyword_chart(paper_data['keywords'])
        st.plotly_chart(keywords_chart, use_container_width=True)
    
    # Citation timeline
    if 'citations' in paper_data and paper_data['citations']:
        st.subheader("📅 Citation Timeline")
        timeline_chart = viz_helper.create_citation_timeline(paper_data['citations'])
        st.plotly_chart(timeline_chart, use_container_width=True)

def display_welcome_screen():
    """Display welcome screen with instructions"""
    st.markdown("""
    ## 🎯 How to Use This Tool
    
    1. **Upload PDFs**: Use the sidebar to upload one or more research papers in PDF format
    2. **Choose Analysis**: Select the type of analysis you want to perform
    3. **Configure Settings**: Adjust advanced settings in the sidebar if needed
    4. **Analyze**: Click the "Analyze Papers" button to start processing
    5. **Explore Results**: View comprehensive analysis results in interactive tabs
    
    ## 🔍 What You'll Get
    
    - **Text Statistics**: Word count, readability scores, sentence structure analysis
    - **Keyword Extraction**: Important terms and phrases from your papers
    - **Citation Analysis**: Referenced works and citation patterns
    - **Visualizations**: Word clouds, charts, and interactive graphs
    - **Quality Assessment**: Writing quality and complexity metrics
    
    ## 📚 Supported Features
    
    - Multiple PDF upload and batch processing
    - Advanced text mining and NLP analysis
    - Citation and reference extraction
    - Interactive visualizations
    - Export capabilities for results
    """)
    
    # Sample data option
    if st.button("🧪 Try with Sample Data"):
        # This would load sample analysis results for demonstration
        load_sample_data()

def load_sample_data():
    """Load sample data for demonstration purposes"""
    sample_data = {
        'filename': 'sample_paper.pdf',
        'timestamp': datetime.now(),
        'text_length': 15000,
        'word_count': 3000,
        'text_stats': {
            'sentence_count': 150,
            'paragraph_count': 25,
            'unique_words': 800,
            'lexical_diversity': 0.267,
            'avg_words_per_sentence': 20.0,
            'avg_syllables_per_word': 1.8
        },
        'readability': {
            'flesch_reading_ease': 45.2,
            'flesch_kincaid_grade': 12.3,
            'automated_readability_index': 13.1,
            'avg_sentence_length': 20.0
        },
        'keywords': [
            ('machine learning', 0.95),
            ('neural networks', 0.87),
            ('deep learning', 0.82),
            ('artificial intelligence', 0.78),
            ('data science', 0.71)
        ],
        'sentiment': {'compound': 0.125}
    }
    
    st.session_state.analyzed_papers = [sample_data]
    st.success("Sample data loaded! Check the analysis results below.")

if __name__ == "__main__":
    main()