import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import nltk
from collections import Counter
import re
import os
from datetime import datetime
import time
import json

# Enhanced UI components
try:
    from streamlit_option_menu import option_menu
except ImportError:
    option_menu = None

try:
    import streamlit_lottie
    from streamlit_lottie import st_lottie
except ImportError:
    st_lottie = None

# Import custom modules
from utils.pdf_processor import PDFProcessor
from utils.text_analyzer import TextAnalyzer
from utils.review_generator import ReviewGenerator

# Enhanced color scheme
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'accent': '#F18F01',
    'success': '#C73E1D',
    'info': '#6A994E',
    'warning': '#F77F00',
    'light': '#F5F7FA',
    'dark': '#2C3E50',
    'background': '#FFFFFF',
    'text': '#2C3E50',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

# Configure page
st.set_page_config(
    page_title="Academic Research Paper Reviewer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: #27ae60;
        font-weight: 500;
    }
    
    /* Section styling */
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .section-header i {
        margin-right: 0.5rem;
    }
    
    /* Review section styling */
    .review-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    /* Score card styling */
    .score-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border-top: 4px solid #667eea;
        margin: 0.5rem;
    }
    
    .score-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .score-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Progress bar styling */
    .progress-bar {
        height: 10px;
        border-radius: 5px;
        background: #e9ecef;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 5px;
        transition: width 0.3s ease;
    }
    
    /* Suggestion card styling */
    .suggestion-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #f77f00;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .suggestion-card:hover {
        transform: translateX(5px);
    }
    
    /* Strength/weakness styling */
    .strength-item {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    
    .weakness-item {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #dc3545;
    }
    
    /* Feedback form styling */
    .feedback-form {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid #ffc107;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px 10px 0px 0px;
        color: #495057;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Hide streamlit menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

def create_animated_metric(title, value, delta=None, prefix="", suffix=""):
    """Create an animated metric card."""
    delta_html = ""
    if delta:
        delta_color = "#27ae60" if delta > 0 else "#e74c3c"
        delta_icon = "↗" if delta > 0 else "↘"
        delta_html = f'<div class="metric-delta" style="color: {delta_color};">{delta_icon} {abs(delta):.1f}%</div>'
    
    metric_html = f"""
    <div class="metric-card fade-in">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{prefix}{value}{suffix}</div>
        {delta_html}
    </div>
    """
    return metric_html

def create_score_card(label, score, max_score=10):
    """Create a score card with progress indicator."""
    percentage = (score / max_score) * 100
    color = "#28a745" if score >= 8 else "#ffc107" if score >= 6 else "#dc3545"
    
    return f"""
    <div class="score-card">
        <div class="score-value" style="color: {color};">{score:.1f}</div>
        <div class="score-label">{label}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%; background: {color};"></div>
        </div>
    </div>
    """

def create_suggestion_card(title, items, card_type="suggestion"):
    """Create styled suggestion cards."""
    icons = {
        "suggestion": "💡",
        "strength": "💪", 
        "weakness": "⚠️"
    }
    
    colors = {
        "suggestion": "#f77f00",
        "strength": "#28a745",
        "weakness": "#dc3545"
    }
    
    icon = icons.get(card_type, "📝")
    color = colors.get(card_type, "#6c757d")
    
    items_html = ""
    for i, item in enumerate(items[:5], 1):
        items_html += f"""
        <div class="{card_type}-item">
            <strong>{i}.</strong> {item}
        </div>
        """
    
    return f"""
    <div class="suggestion-card" style="border-left-color: {color};">
        <h4 style="color: {color}; margin-bottom: 1rem;">{icon} {title}</h4>
        {items_html}
    </div>
    """

def main():
    # Initialize session state
    if 'paper_text' not in st.session_state:
        st.session_state.paper_text = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'review_generated' not in st.session_state:
        st.session_state.review_generated = False
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 Academic Research Paper Reviewer</h1>
        <p>AI-Powered Analysis & Intelligent Review Generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Control Panel")
        
        # Review criteria with enhanced UI
        st.markdown("#### 📊 Review Criteria")
        st.markdown("*Adjust the importance weights for each criterion*")
        
        novelty_weight = st.slider("🔬 Novelty & Innovation", 1, 10, 8, 
                                  help="How novel and innovative is the research?")
        methodology_weight = st.slider("🛠️ Methodology & Rigor", 1, 10, 9,
                                     help="How sound is the research methodology?")
        clarity_weight = st.slider("📝 Clarity & Writing", 1, 10, 7,
                                 help="How clear and well-written is the paper?")
        significance_weight = st.slider("🎯 Significance & Impact", 1, 10, 8,
                                      help="How significant is the contribution?")
        
        # Analysis options with icons
        st.markdown("#### 🔍 Analysis Options")
        analysis_options = st.multiselect(
            "Select analyses to perform:",
            ["📖 Readability Analysis", "🏗️ Structure Analysis", "🔑 Keyword Analysis", 
             "📚 Citation Analysis", "🎭 Sentiment Analysis"],
            default=["📖 Readability Analysis", "🏗️ Structure Analysis", "🔑 Keyword Analysis", "📚 Citation Analysis"]
        )
        
        # Review type with enhanced selection
        st.markdown("#### 📋 Review Type")
        review_type = st.selectbox(
            "Select review format:",
            ["🎓 Academic Conference", "📰 Journal Review", "🎯 Thesis Defense", "👥 Peer Review"],
            help="Choose the type of review format that best fits your needs"
        )
        
        # Quick stats
        if st.session_state.paper_text:
            st.markdown("#### 📈 Quick Stats")
            word_count = len(st.session_state.paper_text.split())
            char_count = len(st.session_state.paper_text)
            
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <div style="text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">{word_count:,}</div>
                    <div style="color: #666; font-size: 0.9rem;">Words</div>
                </div>
                <div style="text-align: center; margin-top: 1rem;">
                    <div style="font-size: 1.2rem; font-weight: bold; color: #764ba2;">{char_count:,}</div>
                    <div style="color: #666; font-size: 0.9rem;">Characters</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced navigation
    if option_menu:
        selected = option_menu(
            menu_title=None,
            options=["📄 Upload", "📊 Analysis", "✍️ Review", "📈 Insights", "💬 Feedback"],
            icons=["upload", "graph-up", "pencil-square", "bar-chart", "chat-dots"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#667eea", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "10px",
                    "border-radius": "10px",
                    "background-color": "transparent",
                    "color": "#495057"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "color": "white"
                },
            }
        )
    else:
        # Fallback to regular tabs if option_menu is not available
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Upload", "📊 Analysis", "✍️ Review", "📈 Insights", "💬 Feedback"])
        selected = "📄 Upload"  # Default selection
    
    # Upload Section
    if not option_menu or selected == "📄 Upload":
        st.markdown('<div class="section-header">📄 Upload Your Research Paper</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📎 File Upload")
            uploaded_file = st.file_uploader(
                "Choose a PDF or DOCX file",
                type=['pdf', 'docx'],
                help="Upload your research paper for comprehensive analysis",
                label_visibility="collapsed"
            )
            
            if uploaded_file is not None:
                with st.spinner("🔄 Processing document..."):
                    progress_bar = st.progress(0)
                    
                    processor = PDFProcessor()
                    
                    # Simulate processing steps with progress
                    progress_bar.progress(25)
                    time.sleep(0.5)
                    
                    if uploaded_file.type == "application/pdf":
                        text = processor.extract_text_from_pdf(uploaded_file)
                        # Get additional formatting info
                        formatting_info = processor.extract_text_with_formatting(uploaded_file)
                    else:
                        text = processor.extract_text_from_docx(uploaded_file)
                        formatting_info = {'metadata': {}, 'page_count': 1, 'headings': []}
                    
                    progress_bar.progress(75)
                    time.sleep(0.5)
                    
                    st.session_state.paper_text = text
                    st.session_state.formatting_info = formatting_info
                    
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    progress_bar.empty()
                    
                    if text:
                        st.success("✅ Document processed successfully!")
                        
                        # Enhanced document info display
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.markdown(create_animated_metric(
                                "Total Words", 
                                f"{len(text.split()):,}"
                            ), unsafe_allow_html=True)
                        
                        with col_b:
                            st.markdown(create_animated_metric(
                                "Characters", 
                                f"{len(text):,}"
                            ), unsafe_allow_html=True)
                        
                        with col_c:
                            estimated_pages = len(text) // 3000
                            st.markdown(create_animated_metric(
                                "Est. Pages", 
                                f"{estimated_pages}"
                            ), unsafe_allow_html=True)
                        
                        # Document metadata
                        if formatting_info.get('metadata'):
                            metadata = formatting_info['metadata']
                            if any(metadata.values()):
                                with st.expander("📋 Document Information"):
                                    info_cols = st.columns(2)
                                    with info_cols[0]:
                                        if metadata.get('title'):
                                            st.write("**Title:**", metadata['title'])
                                        if metadata.get('author'):
                                            st.write("**Author:**", metadata['author'])
                                        if metadata.get('subject'):
                                            st.write("**Subject:**", metadata['subject'])
                                    with info_cols[1]:
                                        if metadata.get('creator'):
                                            st.write("**Created with:**", metadata['creator'])
                                        if formatting_info.get('page_count'):
                                            st.write("**Page Count:**", formatting_info['page_count'])
                    else:
                        st.error("❌ Failed to extract text from the file.")
        
        with col2:
            st.markdown("#### 💡 Tips for Best Results")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h5 style="color: #1565c0; margin-bottom: 1rem;">📝 Document Guidelines</h5>
                <ul style="color: #1976d2; margin: 0;">
                    <li>Use high-quality PDFs with selectable text</li>
                    <li>Ensure proper academic structure</li>
                    <li>Include abstract, methodology, results</li>
                    <li>File size should be under 50MB</li>
                    <li>Use standard academic formatting</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Alternative text input
        st.markdown("#### ✏️ Or Paste Your Paper Text")
        manual_text = st.text_area(
            "Paste your paper content here",
            height=200,
            placeholder="Paste the full text of your academic paper here...",
            label_visibility="collapsed"
        )
        
        if manual_text and st.button("🚀 Process Text", type="primary"):
            st.session_state.paper_text = manual_text
            st.success("✅ Text processed successfully!")
            st.rerun()
    
    # Analysis Section
    elif selected == "📊 Analysis":
        st.markdown('<div class="section-header">📊 Comprehensive Paper Analysis</div>', unsafe_allow_html=True)
        
        if st.session_state.paper_text:
            if st.button("🔍 Run Complete Analysis", type="primary"):
                with st.spinner("🧠 Analyzing your paper..."):
                    analyzer = TextAnalyzer()
                    results = analyzer.analyze_paper(st.session_state.paper_text)
                    st.session_state.analysis_results = results
                    st.success("✅ Analysis completed!")
                    st.rerun()
            
            if st.session_state.analysis_results:
                results = st.session_state.analysis_results
                
                # Overview Dashboard
                st.markdown("### 🎯 Analysis Dashboard")
                
                # Key metrics row
                col1, col2, col3, col4 = st.columns(4)
                
                readability_score = results['readability']['flesch_score']
                with col1:
                    st.markdown(create_score_card("Readability", readability_score, 100), unsafe_allow_html=True)
                
                with col2:
                    structure_score = results['structure'].get('balance_score', 0.7) * 10
                    st.markdown(create_score_card("Structure", structure_score), unsafe_allow_html=True)
                
                with col3:
                    keyword_score = min(results['keywords'].get('academic_keyword_coverage', 3), 5) * 2
                    st.markdown(create_score_card("Keywords", keyword_score), unsafe_allow_html=True)
                
                with col4:
                    citation_score = min(results['citations'].get('citation_density', 0.5) * 10, 10)
                    st.markdown(create_score_card("Citations", citation_score), unsafe_allow_html=True)
                
                # Detailed Analysis Sections
                col_left, col_right = st.columns([3, 2])
                
                with col_left:
                    # Readability Analysis with enhanced visualization
                    if "📖 Readability Analysis" in analysis_options:
                        st.markdown("### 📖 Readability Analysis")
                        
                        readability = results['readability']
                        
                        # Create gauge chart for readability
                        fig_gauge = go.Figure(go.Indicator(
                            mode = "gauge+number+delta",
                            value = readability['flesch_score'],
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Flesch Reading Ease"},
                            delta = {'reference': 50},
                            gauge = {
                                'axis': {'range': [None, 100]},
                                'bar': {'color': COLORS['primary']},
                                'steps': [
                                    {'range': [0, 30], 'color': COLORS['warning']},
                                    {'range': [30, 60], 'color': COLORS['info']},
                                    {'range': [60, 100], 'color': COLORS['success']}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 70
                                }
                            }
                        ))
                        fig_gauge.update_layout(height=300, showlegend=False)
                        st.plotly_chart(fig_gauge, use_container_width=True)
                        
                        # Readability metrics
                        metrics_data = {
                            'Metric': ['Grade Level', 'Avg Sentence Length', 'Complex Words %'],
                            'Value': [
                                readability['grade_level'],
                                f"{readability['avg_sentence_length']:.1f}",
                                f"{readability['complex_words_percent']:.1f}%"
                            ],
                            'Score': [
                                8 if readability['flesch_grade'] <= 12 else 6,
                                8 if readability['avg_sentence_length'] <= 20 else 6,
                                8 if readability['complex_words_percent'] <= 30 else 6
                            ]
                        }
                        
                        df_metrics = pd.DataFrame(metrics_data)
                        
                        # Create horizontal bar chart
                        fig_metrics = px.bar(
                            df_metrics, 
                            x='Score', 
                            y='Metric', 
                            orientation='h',
                            color='Score',
                            color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
                            title="Readability Metrics Breakdown"
                        )
                        fig_metrics.update_layout(height=300, showlegend=False)
                        st.plotly_chart(fig_metrics, use_container_width=True)
                
                with col_right:
                    # Structure Analysis with pie chart
                    if "🏗️ Structure Analysis" in analysis_options and 'structure' in results:
                        st.markdown("### 🏗️ Structure Analysis")
                        
                        structure = results['structure']
                        
                        if structure['sections']:
                            # Create pie chart for section distribution
                            sections_df = pd.DataFrame(
                                list(structure['sections'].items()), 
                                columns=['Section', 'Words']
                            )
                            
                            # Custom colors for sections
                            section_colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
                            
                            fig_pie = px.pie(
                                sections_df, 
                                values='Words', 
                                names='Section',
                                title="Document Structure Distribution",
                                color_discrete_sequence=section_colors
                            )
                            fig_pie.update_traces(
                                textposition='inside', 
                                textinfo='percent+label',
                                hovertemplate='<b>%{label}</b><br>Words: %{value}<br>Percentage: %{percent}<extra></extra>'
                            )
                            fig_pie.update_layout(height=400, showlegend=True)
                            st.plotly_chart(fig_pie, use_container_width=True)
                            
                            # Structure quality indicators
                            quality_metrics = {
                                'Abstract Quality': structure.get('abstract_quality', 0.5),
                                'Conclusion Quality': structure.get('conclusion_quality', 0.5),
                                'Section Balance': structure.get('balance_score', 0.5)
                            }
                            
                            for metric, score in quality_metrics.items():
                                percentage = score * 100
                                color = "#28a745" if score >= 0.7 else "#ffc107" if score >= 0.4 else "#dc3545"
                                
                                st.markdown(f"""
                                <div style="margin: 1rem 0;">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                        <span style="font-weight: 600;">{metric}</span>
                                        <span style="color: {color}; font-weight: 600;">{percentage:.0f}%</span>
                                    </div>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {percentage}%; background: {color};"></div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                
                # Keyword Analysis with word cloud
                if "🔑 Keyword Analysis" in analysis_options and 'keywords' in results:
                    st.markdown("### 🔑 Keyword Analysis")
                    
                    col_wc, col_kw = st.columns([2, 1])
                    
                    with col_wc:
                        keywords = results['keywords']
                        
                        if keywords['top_keywords']:
                            # Create word cloud
                            wordcloud_text = ' '.join([f"{word} " * freq for word, freq in keywords['top_keywords'][:20]])
                            
                            wordcloud = WordCloud(
                                width=600, 
                                height=300, 
                                background_color='white',
                                colormap='viridis',
                                max_words=50,
                                relative_scaling=0.5,
                                stopwords=set()
                            ).generate(wordcloud_text)
                            
                            fig_wc, ax = plt.subplots(figsize=(10, 5))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            ax.set_title('Top Keywords Word Cloud', fontsize=16, fontweight='bold', pad=20)
                            st.pyplot(fig_wc)
                    
                    with col_kw:
                        st.markdown("#### 🏆 Top Keywords")
                        keywords_df = pd.DataFrame(keywords['top_keywords'][:10], columns=['Keyword', 'Frequency'])
                        
                        # Create bar chart for top keywords
                        fig_keywords = px.bar(
                            keywords_df,
                            x='Frequency',
                            y='Keyword',
                            orientation='h',
                            color='Frequency',
                            color_continuous_scale='Viridis',
                            title="Keyword Frequency"
                        )
                        fig_keywords.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                        st.plotly_chart(fig_keywords, use_container_width=True)
                
                # Citation Analysis
                if "📚 Citation Analysis" in analysis_options and 'citations' in results:
                    st.markdown("### 📚 Citation Analysis")
                    
                    citations = results['citations']
                    
                    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
                    
                    with col_c1:
                        st.markdown(create_animated_metric(
                            "Total Citations", 
                            citations['total_citations']
                        ), unsafe_allow_html=True)
                    
                    with col_c2:
                        st.markdown(create_animated_metric(
                            "Recent Citations", 
                            citations['recent_citations']
                        ), unsafe_allow_html=True)
                    
                    with col_c3:
                        st.markdown(create_animated_metric(
                            "Citation Density", 
                            f"{citations['citation_density']:.1f}",
                            suffix="/1k words"
                        ), unsafe_allow_html=True)
                    
                    with col_c4:
                        year_range = citations.get('year_range', 'N/A')
                        st.markdown(create_animated_metric(
                            "Year Range", 
                            year_range
                        ), unsafe_allow_html=True)
        else:
            st.info("📄 Please upload a paper first in the 'Upload' section.")
    
    # Review Section
    elif selected == "✍️ Review":
        st.markdown('<div class="section-header">✍️ Intelligent Review Generation</div>', unsafe_allow_html=True)
        
        if st.session_state.paper_text:
            if st.button("🎯 Generate Comprehensive Review", type="primary"):
                with st.spinner("🤖 Generating intelligent review..."):
                    review_gen = ReviewGenerator()
                    
                    # Clean review type (remove emoji)
                    clean_review_type = review_type.split(' ', 1)[1] if ' ' in review_type else review_type
                    
                    criteria = {
                        'novelty': novelty_weight,
                        'methodology': methodology_weight,
                        'clarity': clarity_weight,
                        'significance': significance_weight
                    }
                    
                    review = review_gen.generate_review(
                        st.session_state.paper_text,
                        criteria,
                        clean_review_type,
                        st.session_state.analysis_results
                    )
                    
                    st.session_state.review = review
                    st.session_state.review_generated = True
                    st.success("✅ Review generated successfully!")
                    st.rerun()
            
            if st.session_state.review_generated and 'review' in st.session_state:
                review = st.session_state.review
                
                # Overall Assessment
                st.markdown('<div class="review-section">', unsafe_allow_html=True)
                st.markdown("### 🎯 Overall Assessment")
                
                col_score, col_rec = st.columns([1, 2])
                
                with col_score:
                    # Overall score gauge
                    score = review['overall_score']
                    fig_score = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = score,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Overall Score"},
                        gauge = {
                            'axis': {'range': [None, 10]},
                            'bar': {'color': COLORS['primary']},
                            'steps': [
                                {'range': [0, 5], 'color': '#ffebee'},
                                {'range': [5, 7], 'color': '#fff3e0'},
                                {'range': [7, 8.5], 'color': '#e8f5e8'},
                                {'range': [8.5, 10], 'color': '#e3f2fd'}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 8.5
                            }
                        }
                    ))
                    fig_score.update_layout(height=300)
                    st.plotly_chart(fig_score, use_container_width=True)
                
                with col_rec:
                    # Recommendation with enhanced styling
                    recommendation = review['recommendation']
                    rec_colors = {
                        "Accept": "#28a745",
                        "Minor Revision": "#ffc107", 
                        "Major Revision": "#fd7e14",
                        "Reject": "#dc3545"
                    }
                    rec_color = rec_colors.get(recommendation, "#6c757d")
                    
                    st.markdown(f"""
                    <div style="background: {rec_color}20; border: 2px solid {rec_color}; border-radius: 15px; padding: 2rem; text-align: center; margin: 1rem 0;">
                        <h2 style="color: {rec_color}; margin-bottom: 1rem;">📋 Recommendation</h2>
                        <h1 style="color: {rec_color}; font-size: 2.5rem; margin: 0;">{recommendation}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Detailed scores
                    st.markdown("#### 📊 Detailed Scores")
                    scores_data = []
                    for criterion, score in review['detailed_scores'].items():
                        scores_data.append({'Criterion': criterion.title(), 'Score': score})
                    
                    scores_df = pd.DataFrame(scores_data)
                    
                    fig_scores = px.bar(
                        scores_df, 
                        x='Criterion', 
                        y='Score', 
                        color='Score',
                        color_continuous_scale='RdYlGn',
                        title="Score Breakdown by Criteria"
                    )
                    fig_scores.update_layout(height=300, showlegend=False)
                    st.plotly_chart(fig_scores, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Review Details
                st.markdown("### 📝 Detailed Review")
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    # Strengths
                    if 'strengths' in review and review['strengths']:
                        st.markdown(create_suggestion_card(
                            "Strengths", 
                            review['strengths'], 
                            "strength"
                        ), unsafe_allow_html=True)
                    
                    # Suggestions
                    if 'suggestions' in review and review['suggestions']:
                        st.markdown(create_suggestion_card(
                            "Suggestions for Improvement", 
                            review['suggestions'], 
                            "suggestion"
                        ), unsafe_allow_html=True)
                
                with col_right:
                    # Weaknesses
                    if 'weaknesses' in review and review['weaknesses']:
                        st.markdown(create_suggestion_card(
                            "Areas for Improvement", 
                            review['weaknesses'], 
                            "weakness"
                        ), unsafe_allow_html=True)
                    
                    # Detailed Comments
                    if 'detailed_comments' in review:
                        st.markdown("#### 📋 Detailed Comments")
                        st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #dee2e6;">
                            {review['detailed_comments'].replace('\n', '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Export Options
                st.markdown("### 📥 Export Options")
                col_e1, col_e2, col_e3 = st.columns(3)
                
                with col_e1:
                    if st.button("📄 Download as PDF", help="Export review as PDF document"):
                        st.info("🚀 PDF export feature coming soon!")
                
                with col_e2:
                    if st.button("📧 Email Review", help="Send review via email"):
                        st.info("📬 Email feature coming soon!")
                
                with col_e3:
                    if st.button("📋 Copy to Clipboard", help="Copy review text"):
                        review_text = f"""
                        ACADEMIC PAPER REVIEW
                        Overall Score: {review['overall_score']:.1f}/10
                        Recommendation: {review['recommendation']}
                        
                        STRENGTHS:
                        {chr(10).join([f"• {s}" for s in review.get('strengths', [])])}
                        
                        AREAS FOR IMPROVEMENT:
                        {chr(10).join([f"• {w}" for w in review.get('weaknesses', [])])}
                        
                        SUGGESTIONS:
                        {chr(10).join([f"• {s}" for s in review.get('suggestions', [])])}
                        """
                        st.code(review_text, language="text")
        else:
            st.info("📄 Please upload a paper first in the 'Upload' section.")
    
    # Insights Section  
    elif selected == "📈 Insights":
        st.markdown('<div class="section-header">📈 Advanced Insights & Analytics</div>', unsafe_allow_html=True)
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Comparative Analysis
            st.markdown("### 📊 Performance Benchmarking")
            
            # Create comparison data
            benchmark_data = {
                'Metric': ['Readability Score', 'Citation Density', 'Structure Quality', 'Keyword Relevance', 'Academic Tone'],
                'Your Paper': [
                    results['readability']['flesch_score']/10, 
                    min(results.get('citations', {}).get('citation_density', 0.5), 2.0),
                    results.get('structure', {}).get('balance_score', 0.7) * 10,
                    min(results['keywords'].get('academic_keyword_coverage', 3), 5) * 2,
                    results.get('writing_patterns', {}).get('academic_tone_score', 0.1) * 50
                ],
                'Field Average': [6.5, 0.8, 7.5, 7.0, 6.0],
                'Top 10%': [8.2, 1.2, 9.0, 9.0, 8.5]
            }
            
            df_benchmark = pd.DataFrame(benchmark_data)
            
            # Create radar chart
            fig_radar = go.Figure()
            
            categories = df_benchmark['Metric'].tolist()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=df_benchmark['Your Paper'],
                theta=categories,
                fill='toself',
                name='Your Paper',
                line_color=COLORS['primary']
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=df_benchmark['Field Average'],
                theta=categories,
                fill='toself',
                name='Field Average',
                line_color=COLORS['secondary']
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=df_benchmark['Top 10%'],
                theta=categories,
                fill='toself',
                name='Top 10%',
                line_color=COLORS['accent']
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )),
                showlegend=True,
                title="Performance Radar Chart",
                height=500
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Detailed Analytics
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("### 🎯 Improvement Recommendations")
                
                # Generate specific recommendations based on analysis
                recommendations = []
                
                if results['readability']['flesch_score'] < 40:
                    recommendations.append("📖 Simplify sentence structure for better readability")
                
                if results.get('citations', {}).get('citation_density', 0) < 0.5:
                    recommendations.append("📚 Increase citation density to strengthen arguments")
                
                if results.get('structure', {}).get('balance_score', 1) < 0.6:
                    recommendations.append("🏗️ Improve section balance and organization")
                
                if results['keywords'].get('academic_keyword_coverage', 5) < 3:
                    recommendations.append("🔑 Use more domain-specific terminology")
                
                if not recommendations:
                    recommendations = [
                        "✨ Excellent work! Your paper meets high academic standards",
                        "🔍 Consider minor refinements in presentation",
                        "📈 Add more visual aids to support your arguments"
                    ]
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); 
                                padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                                border-left: 4px solid #ffc107;">
                        <strong>{i}.</strong> {rec}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_right:
                st.markdown("### 📊 Quality Metrics Overview")
                
                # Quality score calculation
                quality_scores = {
                    'Overall Quality': (
                        results['readability']['flesch_score']/10 + 
                        results.get('structure', {}).get('balance_score', 0.7) * 10 +
                        min(results['keywords'].get('academic_keyword_coverage', 3), 5) * 2 +
                        min(results.get('citations', {}).get('citation_density', 0.5) * 10, 10)
                    ) / 4,
                    'Writing Quality': results['readability']['flesch_score']/10,
                    'Content Quality': np.mean(list(results.get('academic_quality', {}).values())) * 10,
                    'Structure Quality': results.get('structure', {}).get('balance_score', 0.7) * 10,
                    'Research Quality': min(results.get('citations', {}).get('citation_density', 0.5) * 10, 10)
                }
                
                # Create quality metrics chart
                quality_df = pd.DataFrame(list(quality_scores.items()), columns=['Metric', 'Score'])
                
                fig_quality = px.bar(
                    quality_df,
                    x='Score',
                    y='Metric',
                    orientation='h',
                    color='Score',
                    color_continuous_scale='RdYlGn',
                    title="Quality Assessment Breakdown"
                )
                fig_quality.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_quality, use_container_width=True)
            
            # Writing Pattern Analysis
            if 'writing_patterns' in results:
                st.markdown("### 📝 Writing Pattern Analysis")
                
                patterns = results['writing_patterns']
                
                col_p1, col_p2 = st.columns(2)
                
                with col_p1:
                    # Sentence length distribution
                    if 'sentence_lengths' in patterns:
                        sentence_lengths = patterns['sentence_lengths']
                        
                        fig_sent = px.histogram(
                            x=sentence_lengths,
                            nbins=20,
                            title="Sentence Length Distribution",
                            labels={'x': 'Sentence Length (words)', 'y': 'Frequency'},
                            color_discrete_sequence=[COLORS['primary']]
                        )
                        fig_sent.update_layout(height=300)
                        st.plotly_chart(fig_sent, use_container_width=True)
                
                with col_p2:
                    # Word frequency analysis
                    if 'word_frequencies' in patterns:
                        top_words = dict(list(patterns['word_frequencies'].items())[:15])
                        
                        fig_words = px.bar(
                            x=list(top_words.values()),
                            y=list(top_words.keys()),
                            orientation='h',
                            title="Most Frequent Words",
                            color=list(top_words.values()),
                            color_continuous_scale='Viridis'
                        )
                        fig_words.update_layout(height=300, yaxis={'categoryorder': 'total ascending'})
                        st.plotly_chart(fig_words, use_container_width=True)
        
        else:
            st.info("📊 Run analysis first to see detailed insights.")
    
    # Feedback Section
    elif selected == "💬 Feedback":
        st.markdown('<div class="section-header">💬 User Feedback & Suggestions</div>', unsafe_allow_html=True)
        
        if not st.session_state.feedback_submitted:
            st.markdown("""
            <div class="feedback-form">
                <h3 style="color: #f57c00; margin-bottom: 1rem;">🌟 Help Us Improve!</h3>
                <p style="margin-bottom: 1.5rem;">Your feedback is invaluable in making our Academic Research Paper Reviewer even better. Please share your experience and suggestions.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("feedback_form"):
                col_f1, col_f2 = st.columns(2)
                
                with col_f1:
                    st.markdown("#### 👤 About You")
                    user_type = st.selectbox(
                        "I am a:",
                        ["Researcher", "Student", "Professor", "Reviewer", "Editor", "Other"]
                    )
                    
                    field = st.selectbox(
                        "Research Field:",
                        ["Computer Science", "Engineering", "Medicine", "Biology", "Chemistry", 
                         "Physics", "Mathematics", "Social Sciences", "Humanities", "Other"]
                    )
                    
                    experience = st.selectbox(
                        "Experience Level:",
                        ["Undergraduate", "Graduate", "PhD", "Postdoc", "Junior Researcher", "Senior Researcher"]
                    )
                
                with col_f2:
                    st.markdown("#### ⭐ Rating")
                    overall_rating = st.slider("Overall Experience", 1, 5, 4, 
                                             help="Rate your overall experience with the tool")
                    
                    usefulness = st.slider("How useful was the analysis?", 1, 5, 4)
                    accuracy = st.slider("How accurate were the results?", 1, 5, 4)
                    ease_of_use = st.slider("How easy was it to use?", 1, 5, 4)
                
                st.markdown("#### 💭 Your Feedback")
                
                col_fb1, col_fb2 = st.columns(2)
                
                with col_fb1:
                    liked_most = st.text_area(
                        "What did you like most?",
                        placeholder="Tell us about the features you found most valuable...",
                        height=100
                    )
                    
                    suggestions = st.text_area(
                        "Suggestions for improvement:",
                        placeholder="How can we make this tool better?",
                        height=100
                    )
                
                with col_fb2:
                    issues = st.text_area(
                        "Any issues or difficulties?",
                        placeholder="Did you encounter any problems or confusing aspects?",
                        height=100
                    )
                    
                    additional_features = st.text_area(
                        "What features would you like to see?",
                        placeholder="What additional functionality would be helpful?",
                        height=100
                    )
                
                # Contact information (optional)
                col_contact = st.columns(2)
                with col_contact[0]:
                    email = st.text_input("Email (optional)", placeholder="your.email@example.com")
                with col_contact[1]:
                    follow_up = st.checkbox("I'd like to be contacted about updates")
                
                submitted = st.form_submit_button("🚀 Submit Feedback", type="primary")
                
                if submitted:
                    # Save feedback (in a real app, this would go to a database)
                    feedback_data = {
                        'timestamp': datetime.now().isoformat(),
                        'user_type': user_type,
                        'field': field,
                        'experience': experience,
                        'ratings': {
                            'overall': overall_rating,
                            'usefulness': usefulness,
                            'accuracy': accuracy,
                            'ease_of_use': ease_of_use
                        },
                        'feedback': {
                            'liked_most': liked_most,
                            'suggestions': suggestions,
                            'issues': issues,
                            'additional_features': additional_features
                        },
                        'contact': {
                            'email': email,
                            'follow_up': follow_up
                        }
                    }
                    
                    # Simulate saving feedback
                    st.session_state.feedback_submitted = True
                    st.session_state.feedback_data = feedback_data
                    st.success("🎉 Thank you for your valuable feedback!")
                    st.rerun()
        
        else:
            # Thank you message with summary
            st.markdown("""
            <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                        padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;
                        border: 1px solid #28a745; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                <h2 style="color: #155724; margin-bottom: 1rem;">🎉 Thank You!</h2>
                <p style="color: #155724; font-size: 1.1rem; margin-bottom: 1rem;">
                    Your feedback has been successfully submitted and is greatly appreciated!
                </p>
                <p style="color: #155724; margin: 0;">
                    We're constantly working to improve our Academic Research Paper Reviewer based on user feedback like yours.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📝 Submit Another Feedback"):
                st.session_state.feedback_submitted = False
                st.rerun()
        
        # Community Insights
        st.markdown("### 📈 Community Insights")
        
        # Mock analytics (in a real app, this would come from actual data)
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            st.markdown(create_animated_metric("Total Users", "2,847"), unsafe_allow_html=True)
        with col_stats2:
            st.markdown(create_animated_metric("Papers Analyzed", "15,293"), unsafe_allow_html=True)
        with col_stats3:
            st.markdown(create_animated_metric("Avg Rating", "4.6", suffix="/5"), unsafe_allow_html=True)
        with col_stats4:
            st.markdown(create_animated_metric("Satisfaction", "94", suffix="%"), unsafe_allow_html=True)
        
        # Feature requests chart
        st.markdown("#### 🔥 Most Requested Features")
        
        feature_requests = {
            'Feature': ['Plagiarism Detection', 'Multi-language Support', 'Collaborative Reviews', 
                       'Reference Check', 'Export to LaTeX', 'Mobile App', 'Integration APIs'],
            'Requests': [156, 134, 98, 87, 76, 65, 54]
        }
        
        fig_features = px.bar(
            feature_requests,
            x='Requests',
            y='Feature',
            orientation='h',
            color='Requests',
            color_continuous_scale='Plasma',
            title="Community Feature Requests"
        )
        fig_features.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_features, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                border-radius: 10px; margin-top: 2rem;">
        <h4 style="color: #495057; margin-bottom: 1rem;">📚 Academic Research Paper Reviewer</h4>
        <p style="color: #6c757d; margin: 0;">
            Powered by Advanced NLP & AI | Made with ❤️ for the Research Community
        </p>
        <p style="color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;">
            Version 2.0 | Enhanced with PyMuPDF & Interactive Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()