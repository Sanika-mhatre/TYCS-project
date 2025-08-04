import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import nltk
from collections import Counter
import re
import os
from datetime import datetime

# Import custom modules
from utils.pdf_processor import PDFProcessor
from utils.text_analyzer import TextAnalyzer
from utils.review_generator import ReviewGenerator

# Configure page
st.set_page_config(
    page_title="Academic Research Paper Reviewer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.section-header {
    font-size: 1.5rem;
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.5rem;
    margin: 1rem 0;
}
.metric-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #3498db;
}
.review-section {
    background-color: #f1f3f4;
    padding: 1.5rem;
    border-radius: 0.8rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 Academic Research Paper Reviewer</h1>', unsafe_allow_html=True)
    st.markdown("**Upload your research paper and get comprehensive analysis and reviews**")
    
    # Initialize session state
    if 'paper_text' not in st.session_state:
        st.session_state.paper_text = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'review_generated' not in st.session_state:
        st.session_state.review_generated = False
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Settings")
        
        # Review criteria
        st.markdown("#### Review Criteria")
        novelty_weight = st.slider("Novelty", 1, 10, 8)
        methodology_weight = st.slider("Methodology", 1, 10, 9)
        clarity_weight = st.slider("Clarity", 1, 10, 7)
        significance_weight = st.slider("Significance", 1, 10, 8)
        
        # Analysis options
        st.markdown("#### Analysis Options")
        show_readability = st.checkbox("Readability Analysis", True)
        show_structure = st.checkbox("Structure Analysis", True)
        show_keywords = st.checkbox("Keyword Analysis", True)
        show_sentiment = st.checkbox("Sentiment Analysis", False)
        
        # Review type
        st.markdown("#### Review Type")
        review_type = st.selectbox(
            "Select Review Style",
            ["Academic Conference", "Journal Review", "Thesis Defense", "Peer Review"]
        )
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload Paper", "📊 Analysis", "✍️ Review", "📈 Insights"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Upload Your Research Paper</h2>', unsafe_allow_html=True)
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a PDF or DOCX file",
            type=['pdf', 'docx'],
            help="Upload your research paper for analysis"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing paper..."):
                processor = PDFProcessor()
                
                if uploaded_file.type == "application/pdf":
                    text = processor.extract_text_from_pdf(uploaded_file)
                else:
                    text = processor.extract_text_from_docx(uploaded_file)
                
                st.session_state.paper_text = text
                
                if text:
                    st.success("✅ Paper processed successfully!")
                    
                    # Display basic info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Words", len(text.split()))
                    with col2:
                        st.metric("Total Characters", len(text))
                    with col3:
                        st.metric("Estimated Pages", len(text) // 3000)
                    
                    # Preview
                    with st.expander("📖 Preview Paper Content"):
                        st.text_area("Paper Content Preview", text[:2000] + "..." if len(text) > 2000 else text, height=300)
                else:
                    st.error("❌ Failed to extract text from the file.")
        
        # Manual text input option
        st.markdown("### Or Paste Your Paper Text")
        manual_text = st.text_area("Paste your paper content here", height=200)
        if manual_text and st.button("Process Text"):
            st.session_state.paper_text = manual_text
            st.success("✅ Text processed successfully!")
    
    with tab2:
        st.markdown('<h2 class="section-header">Paper Analysis</h2>', unsafe_allow_html=True)
        
        if st.session_state.paper_text:
            if st.button("🔍 Run Analysis", type="primary"):
                with st.spinner("Analyzing paper..."):
                    analyzer = TextAnalyzer()
                    results = analyzer.analyze_paper(st.session_state.paper_text)
                    st.session_state.analysis_results = results
            
            if st.session_state.analysis_results:
                results = st.session_state.analysis_results
                
                # Overview metrics
                st.markdown("### 📊 Overview Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Readability Score", f"{results['readability']['flesch_score']:.1f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Avg Sentence Length", f"{results['readability']['avg_sentence_length']:.1f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Complex Words %", f"{results['readability']['complex_words_percent']:.1f}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Academic Level", results['readability']['grade_level'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Structure Analysis
                if show_structure and 'structure' in results:
                    st.markdown("### 🏗️ Paper Structure")
                    structure = results['structure']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # Section distribution
                        if structure['sections']:
                            sections_df = pd.DataFrame(list(structure['sections'].items()), 
                                                     columns=['Section', 'Word Count'])
                            fig = px.pie(sections_df, values='Word Count', names='Section', 
                                       title="Section Distribution")
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Structure quality metrics
                        st.markdown("#### Structure Quality")
                        st.progress(structure['abstract_quality'])
                        st.caption("Abstract Quality")
                        st.progress(structure['conclusion_quality'])
                        st.caption("Conclusion Quality")
                        st.progress(structure['balance_score'])
                        st.caption("Section Balance")
                
                # Keyword Analysis
                if show_keywords and 'keywords' in results:
                    st.markdown("### 🔑 Keyword Analysis")
                    keywords = results['keywords']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # Word cloud
                        if keywords['top_keywords']:
                            wordcloud_text = ' '.join([word for word, _ in keywords['top_keywords']])
                            wordcloud = WordCloud(width=400, height=300, background_color='white').generate(wordcloud_text)
                            
                            fig, ax = plt.subplots(figsize=(8, 6))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                    
                    with col2:
                        # Top keywords
                        st.markdown("#### Top Keywords")
                        keywords_df = pd.DataFrame(keywords['top_keywords'], columns=['Keyword', 'Frequency'])
                        st.dataframe(keywords_df, use_container_width=True)
                
                # Citations and References
                if 'citations' in results:
                    st.markdown("### 📚 Citations Analysis")
                    citations = results['citations']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Citations", citations['total_citations'])
                    with col2:
                        st.metric("Recent Citations (5 years)", citations['recent_citations'])
                    with col3:
                        st.metric("Citation Density", f"{citations['citation_density']:.2f}")
        else:
            st.info("📄 Please upload a paper first in the 'Upload Paper' tab.")
    
    with tab3:
        st.markdown('<h2 class="section-header">Generate Review</h2>', unsafe_allow_html=True)
        
        if st.session_state.paper_text:
            if st.button("✍️ Generate Review", type="primary"):
                with st.spinner("Generating comprehensive review..."):
                    review_gen = ReviewGenerator()
                    
                    # Prepare review criteria
                    criteria = {
                        'novelty': novelty_weight,
                        'methodology': methodology_weight,
                        'clarity': clarity_weight,
                        'significance': significance_weight
                    }
                    
                    review = review_gen.generate_review(
                        st.session_state.paper_text,
                        criteria,
                        review_type,
                        st.session_state.analysis_results
                    )
                    
                    st.session_state.review = review
                    st.session_state.review_generated = True
            
            if st.session_state.review_generated and 'review' in st.session_state:
                review = st.session_state.review
                
                # Overall Score
                st.markdown('<div class="review-section">', unsafe_allow_html=True)
                st.markdown("### 🎯 Overall Assessment")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    score = review['overall_score']
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = score,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Overall Score"},
                        delta = {'reference': 7.0},
                        gauge = {
                            'axis': {'range': [None, 10]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 5], 'color': "lightgray"},
                                {'range': [5, 8], 'color': "gray"},
                                {'range': [8, 10], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 8.5
                            }
                        }
                    ))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### Recommendation")
                    recommendation = review['recommendation']
                    if recommendation == "Accept":
                        st.success(f"✅ **{recommendation}**")
                    elif recommendation == "Minor Revision":
                        st.warning(f"⚠️ **{recommendation}**")
                    elif recommendation == "Major Revision":
                        st.warning(f"🔄 **{recommendation}**")
                    else:
                        st.error(f"❌ **{recommendation}**")
                    
                    # Score breakdown
                    st.markdown("#### Score Breakdown")
                    scores_df = pd.DataFrame(list(review['detailed_scores'].items()), 
                                           columns=['Criteria', 'Score'])
                    fig = px.bar(scores_df, x='Criteria', y='Score', 
                               title="Detailed Scores by Criteria")
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Detailed Review Sections
                st.markdown("### 📝 Detailed Review")
                
                sections = ['strengths', 'weaknesses', 'suggestions', 'detailed_comments']
                section_titles = ['💪 Strengths', '⚠️ Weaknesses', '💡 Suggestions for Improvement', '📋 Detailed Comments']
                
                for section, title in zip(sections, section_titles):
                    if section in review and review[section]:
                        with st.expander(title, expanded=True):
                            if isinstance(review[section], list):
                                for item in review[section]:
                                    st.markdown(f"• {item}")
                            else:
                                st.markdown(review[section])
                
                # Export options
                st.markdown("### 📥 Export Review")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📄 Download as PDF"):
                        # TODO: Implement PDF generation
                        st.info("PDF export feature coming soon!")
                with col2:
                    if st.button("📧 Email Review"):
                        # TODO: Implement email functionality
                        st.info("Email feature coming soon!")
        else:
            st.info("📄 Please upload a paper first in the 'Upload Paper' tab.")
    
    with tab4:
        st.markdown('<h2 class="section-header">Research Insights</h2>', unsafe_allow_html=True)
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Comparative Analysis
            st.markdown("### 📊 Comparative Analysis")
            
            # Create mock benchmark data for demonstration
            benchmark_data = {
                'Metric': ['Readability', 'Citation Density', 'Structure Quality', 'Keyword Relevance'],
                'Your Paper': [results['readability']['flesch_score']/10, 
                             results.get('citations', {}).get('citation_density', 0.5),
                             results.get('structure', {}).get('balance_score', 0.7),
                             0.8],
                'Field Average': [6.5, 0.8, 0.75, 0.7],
                'Top 10%': [8.2, 1.2, 0.9, 0.9]
            }
            
            df = pd.DataFrame(benchmark_data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Metric'], y=df['Your Paper'], name='Your Paper', mode='lines+markers'))
            fig.add_trace(go.Scatter(x=df['Metric'], y=df['Field Average'], name='Field Average', mode='lines+markers'))
            fig.add_trace(go.Scatter(x=df['Metric'], y=df['Top 10%'], name='Top 10%', mode='lines+markers'))
            
            fig.update_layout(title="Paper Performance vs Benchmarks", yaxis_title="Score")
            st.plotly_chart(fig, use_container_width=True)
            
            # Improvement Recommendations
            st.markdown("### 🎯 Improvement Recommendations")
            
            recommendations = [
                "Consider simplifying complex sentences to improve readability",
                "Add more recent citations to strengthen the literature review",
                "Expand the methodology section for better clarity",
                "Include more visual aids (figures, tables) to support arguments",
                "Strengthen the conclusion with clearer implications"
            ]
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
            
            # Trends and Patterns
            st.markdown("### 📈 Writing Pattern Analysis")
            
            if 'writing_patterns' in results:
                patterns = results['writing_patterns']
                
                col1, col2 = st.columns(2)
                with col1:
                    # Sentence length distribution
                    if 'sentence_lengths' in patterns:
                        fig = px.histogram(x=patterns['sentence_lengths'], 
                                         title="Sentence Length Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Word frequency
                    if 'word_frequencies' in patterns:
                        top_words = dict(list(patterns['word_frequencies'].items())[:20])
                        fig = px.bar(x=list(top_words.keys()), y=list(top_words.values()),
                                   title="Most Frequent Words")
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Run analysis first to see insights.")
    
    # Footer
    st.markdown("---")
    st.markdown("**Academic Research Paper Reviewer** - Powered by Advanced NLP and AI")

if __name__ == "__main__":
    main()