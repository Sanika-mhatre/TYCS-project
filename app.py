import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import fitz  # PyMuPDF
import io
import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# Download NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

# Page configuration
st.set_page_config(
    page_title="Academic Paper Reviewer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    
    .stTitle {
        color: #2E4057;
        font-size: 3rem !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .review-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .feedback-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .uploadedFile {
        border-radius: 10px;
        border: 2px dashed #667eea;
    }
    
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'reviews' not in st.session_state:
    st.session_state.reviews = []
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = []

# Import demo functionality
try:
    from demo import load_demo_data, show_demo_info
    # Load demo data if available
    demo_loaded = load_demo_data()
except ImportError:
    demo_loaded = False

def main():
    # Title
    st.title("🎓 Academic Paper Reviewer")
    st.markdown("### AI-Powered Research Paper Analysis & Review System")
    
    # Show demo info if demo data was loaded
    if demo_loaded:
        show_demo_info()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 📊 Navigation")
        page = st.selectbox(
            "Choose a section:",
            ["🏠 Dashboard", "📄 Paper Upload & Review", "📈 Analytics", "💬 Feedback & Suggestions", "📋 Review History"]
        )
        
        # Demo controls
        st.markdown("---")
        st.markdown("## 🎯 Demo Controls")
        if st.button("🔄 Reset Demo Data"):
            if 'demo_loaded' in st.session_state:
                del st.session_state['demo_loaded']
            load_demo_data()
            st.rerun()
        
        if st.button("🗑️ Clear All Data"):
            st.session_state.reviews = []
            st.session_state.feedback_data = []
            if 'demo_loaded' in st.session_state:
                del st.session_state['demo_loaded']
            st.rerun()
    
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📄 Paper Upload & Review":
        show_paper_review()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "💬 Feedback & Suggestions":
        show_feedback()
    elif page == "📋 Review History":
        show_history()

def show_dashboard():
    st.markdown("## 📊 Dashboard Overview")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📚 Papers Reviewed</h3>
            <h2>{}</h2>
        </div>
        """.format(len(st.session_state.reviews)), unsafe_allow_html=True)
    
    with col2:
        avg_score = np.mean([r['overall_score'] for r in st.session_state.reviews]) if st.session_state.reviews else 0
        st.markdown("""
        <div class="metric-card">
            <h3>⭐ Average Score</h3>
            <h2>{:.1f}/10</h2>
        </div>
        """.format(avg_score), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💬 Feedback Received</h3>
            <h2>{}</h2>
        </div>
        """.format(len(st.session_state.feedback_data)), unsafe_allow_html=True)
    
    with col4:
        today_reviews = sum(1 for r in st.session_state.reviews if r['date'].date() == datetime.now().date())
        st.markdown("""
        <div class="metric-card">
            <h3>📅 Today's Reviews</h3>
            <h2>{}</h2>
        </div>
        """.format(today_reviews), unsafe_allow_html=True)
    
    # Charts section
    if st.session_state.reviews:
        col1, col2 = st.columns(2)
        
        with col1:
            # Score distribution pie chart
            scores = [r['overall_score'] for r in st.session_state.reviews]
            score_ranges = ['Poor (0-3)', 'Fair (4-5)', 'Good (6-7)', 'Excellent (8-10)']
            score_counts = [
                sum(1 for s in scores if 0 <= s <= 3),
                sum(1 for s in scores if 4 <= s <= 5),
                sum(1 for s in scores if 6 <= s <= 7),
                sum(1 for s in scores if 8 <= s <= 10)
            ]
            
            fig_pie = px.pie(
                values=score_counts,
                names=score_ranges,
                title="📊 Review Score Distribution",
                color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            )
            fig_pie.update_layout(
                title_font_size=16,
                title_x=0.5,
                font=dict(size=12)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Review categories
            categories = [r.get('category', 'Other') for r in st.session_state.reviews]
            category_counts = Counter(categories)
            
            fig_bar = px.bar(
                x=list(category_counts.keys()),
                y=list(category_counts.values()),
                title="📈 Papers by Category",
                color=list(category_counts.values()),
                color_continuous_scale='Viridis'
            )
            fig_bar.update_layout(
                title_font_size=16,
                title_x=0.5,
                xaxis_title="Category",
                yaxis_title="Number of Papers"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    else:
        st.info("📝 Upload your first paper to see analytics!")

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file using PyMuPDF"""
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def analyze_paper_ml(text, title=""):
    """ML-based paper analysis using various NLP techniques"""
    if not text.strip():
        return None
    
    # Text preprocessing
    text_clean = re.sub(r'[^\w\s]', '', text.lower())
    
    # Sentiment analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment
    
    # Text statistics
    word_count = len(text.split())
    sentence_count = len(blob.sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Readability score (simple version)
    readability_score = min(10, max(1, 10 - (avg_sentence_length / 10)))
    
    # Content analysis
    academic_keywords = [
        'research', 'study', 'analysis', 'method', 'result', 'conclusion',
        'literature', 'review', 'experiment', 'data', 'hypothesis', 'theory',
        'findings', 'evidence', 'significance', 'contribution', 'novel'
    ]
    
    keyword_count = sum(1 for word in text_clean.split() if word in academic_keywords)
    keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0
    
    # Structure analysis
    has_abstract = 'abstract' in text.lower()
    has_introduction = 'introduction' in text.lower()
    has_methodology = any(term in text.lower() for term in ['methodology', 'methods', 'approach'])
    has_results = 'results' in text.lower() or 'findings' in text.lower()
    has_conclusion = 'conclusion' in text.lower()
    has_references = 'references' in text.lower() or 'bibliography' in text.lower()
    
    structure_score = sum([has_abstract, has_introduction, has_methodology, has_results, has_conclusion, has_references])
    
    # Overall scoring algorithm
    content_score = min(10, (keyword_density * 2) + (structure_score * 1.5))
    technical_score = min(10, readability_score + (sentiment.subjectivity * 5))
    innovation_score = min(10, 5 + (sentiment.polarity * 2.5) + (keyword_density * 0.5))
    
    overall_score = (content_score + technical_score + innovation_score) / 3
    
    # Generate suggestions
    suggestions = []
    if word_count < 3000:
        suggestions.append("📝 Consider expanding the content. Academic papers typically require more detailed analysis.")
    if not has_abstract:
        suggestions.append("📄 Add an abstract to summarize your research.")
    if not has_methodology:
        suggestions.append("🔬 Include a detailed methodology section.")
    if keyword_density < 2:
        suggestions.append("🎯 Increase the use of academic terminology and keywords.")
    if sentiment.polarity < 0:
        suggestions.append("💭 Consider using more positive and confident language.")
    if structure_score < 4:
        suggestions.append("📋 Improve paper structure with clear sections.")
    
    return {
        'overall_score': round(overall_score, 1),
        'content_score': round(content_score, 1),
        'technical_score': round(technical_score, 1),
        'innovation_score': round(innovation_score, 1),
        'word_count': word_count,
        'sentence_count': sentence_count,
        'readability_score': round(readability_score, 1),
        'keyword_density': round(keyword_density, 1),
        'sentiment_polarity': round(sentiment.polarity, 2),
        'sentiment_subjectivity': round(sentiment.subjectivity, 2),
        'structure_score': structure_score,
        'suggestions': suggestions,
        'has_sections': {
            'abstract': has_abstract,
            'introduction': has_introduction,
            'methodology': has_methodology,
            'results': has_results,
            'conclusion': has_conclusion,
            'references': has_references
        }
    }

def show_paper_review():
    st.markdown("## 📄 Paper Upload & Review")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Your Research Paper")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload your academic research paper in PDF format"
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Paper details
            st.markdown("### 📋 Paper Details")
            paper_title = st.text_input("Paper Title", placeholder="Enter the title of your paper")
            paper_category = st.selectbox(
                "Research Category",
                ["Computer Science", "Mathematics", "Physics", "Biology", "Chemistry", 
                 "Engineering", "Medicine", "Psychology", "Economics", "Other"]
            )
            author_name = st.text_input("Author(s)", placeholder="Enter author name(s)")
            
            if st.button("🔍 Analyze Paper", type="primary"):
                with st.spinner("🤖 Analyzing your paper with AI..."):
                    # Extract text from PDF
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    
                    if pdf_text:
                        # Perform ML analysis
                        analysis = analyze_paper_ml(pdf_text, paper_title)
                        
                        if analysis:
                            # Store review
                            review_data = {
                                'title': paper_title or uploaded_file.name,
                                'category': paper_category,
                                'author': author_name,
                                'date': datetime.now(),
                                'filename': uploaded_file.name,
                                'analysis': analysis,
                                'overall_score': analysis['overall_score']
                            }
                            st.session_state.reviews.append(review_data)
                            
                            st.success("✅ Analysis completed!")
                            st.balloons()
    
    with col2:
        if st.session_state.reviews and uploaded_file:
            latest_review = st.session_state.reviews[-1]
            if latest_review['filename'] == uploaded_file.name:
                st.markdown("### 📊 Analysis Results")
                analysis = latest_review['analysis']
                
                # Score display
                st.markdown(f"""
                <div class="review-card">
                    <h3>🏆 Overall Score: {analysis['overall_score']}/10</h3>
                    <p><strong>Content Quality:</strong> {analysis['content_score']}/10</p>
                    <p><strong>Technical Quality:</strong> {analysis['technical_score']}/10</p>
                    <p><strong>Innovation Score:</strong> {analysis['innovation_score']}/10</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed metrics
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("📝 Word Count", analysis['word_count'])
                    st.metric("📖 Readability", f"{analysis['readability_score']}/10")
                    st.metric("🎯 Keyword Density", f"{analysis['keyword_density']}%")
                
                with col_b:
                    st.metric("📑 Sentences", analysis['sentence_count'])
                    st.metric("😊 Sentiment", analysis['sentiment_polarity'])
                    st.metric("📋 Structure", f"{analysis['structure_score']}/6")
                
                # Paper structure
                st.markdown("### 📋 Paper Structure Analysis")
                sections = analysis['has_sections']
                for section, has_it in sections.items():
                    icon = "✅" if has_it else "❌"
                    st.markdown(f"{icon} **{section.title()}**")
                
                # Suggestions
                if analysis['suggestions']:
                    st.markdown("### 💡 Improvement Suggestions")
                    for suggestion in analysis['suggestions']:
                        st.info(suggestion)

def show_analytics():
    st.markdown("## 📈 Advanced Analytics")
    
    if not st.session_state.reviews:
        st.info("📊 No reviews available yet. Upload and review some papers first!")
        return
    
    # Create analytics dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        # Score trends over time
        df_reviews = pd.DataFrame([{
            'Date': r['date'].strftime('%Y-%m-%d'),
            'Score': r['overall_score'],
            'Category': r['category'],
            'Title': r['title']
        } for r in st.session_state.reviews])
        
        fig_line = px.line(
            df_reviews, 
            x='Date', 
            y='Score',
            title='📈 Review Scores Over Time',
            markers=True,
            color_discrete_sequence=['#667eea']
        )
        fig_line.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Score (0-10)"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col2:
        # Category performance
        category_scores = df_reviews.groupby('Category')['Score'].mean().reset_index()
        fig_bar = px.bar(
            category_scores,
            x='Category',
            y='Score',
            title='📊 Average Scores by Category',
            color='Score',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="Category",
            yaxis_title="Average Score"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Word cloud of suggestions
    st.markdown("### ☁️ Common Suggestions Word Cloud")
    all_suggestions = []
    for review in st.session_state.reviews:
        all_suggestions.extend(review['analysis']['suggestions'])
    
    if all_suggestions:
        suggestion_text = ' '.join(all_suggestions)
        try:
            wordcloud = WordCloud(
                width=800, 
                height=400, 
                background_color='white',
                colormap='viridis'
            ).generate(suggestion_text)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
            plt.close()
        except:
            st.info("Not enough suggestion data to generate word cloud yet.")

def show_feedback():
    st.markdown("## 💬 Feedback & Suggestions")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Submit Your Feedback")
        
        with st.form("feedback_form"):
            user_name = st.text_input("Your Name", placeholder="Enter your name")
            user_email = st.text_input("Email (Optional)", placeholder="your.email@example.com")
            
            feedback_type = st.selectbox(
                "Feedback Type",
                ["🐛 Bug Report", "💡 Feature Request", "📈 Improvement Suggestion", "⭐ General Feedback"]
            )
            
            rating = st.slider("Rate the Application", 1, 5, 4)
            
            feedback_text = st.text_area(
                "Your Feedback",
                placeholder="Please share your thoughts, suggestions, or report any issues...",
                height=150
            )
            
            submitted = st.form_submit_button("🚀 Submit Feedback", type="primary")
            
            if submitted and feedback_text and user_name:
                feedback_entry = {
                    'name': user_name,
                    'email': user_email,
                    'type': feedback_type,
                    'rating': rating,
                    'feedback': feedback_text,
                    'date': datetime.now(),
                    'id': len(st.session_state.feedback_data) + 1
                }
                
                st.session_state.feedback_data.append(feedback_entry)
                st.success("✅ Thank you for your feedback!")
                st.balloons()
    
    with col2:
        st.markdown("### 📊 Feedback Statistics")
        
        if st.session_state.feedback_data:
            # Rating distribution
            ratings = [f['rating'] for f in st.session_state.feedback_data]
            rating_counts = Counter(ratings)
            
            fig_rating = px.pie(
                values=list(rating_counts.values()),
                names=[f"{k} ⭐" for k in rating_counts.keys()],
                title="⭐ Rating Distribution",
                color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
            )
            st.plotly_chart(fig_rating, use_container_width=True)
            
            # Feedback type distribution
            types = [f['type'] for f in st.session_state.feedback_data]
            type_counts = Counter(types)
            
            fig_types = px.bar(
                x=list(type_counts.keys()),
                y=list(type_counts.values()),
                title="📈 Feedback Types",
                color=list(type_counts.values()),
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_types, use_container_width=True)
        else:
            st.info("No feedback received yet.")
    
    # Display recent feedback
    if st.session_state.feedback_data:
        st.markdown("### 📬 Recent Feedback")
        for feedback in reversed(st.session_state.feedback_data[-3:]):  # Show last 3
            st.markdown(f"""
            <div class="feedback-card">
                <h4>{feedback['type']} - ⭐{feedback['rating']}/5</h4>
                <p><strong>From:</strong> {feedback['name']}</p>
                <p><strong>Date:</strong> {feedback['date'].strftime('%Y-%m-%d %H:%M')}</p>
                <p>"{feedback['feedback']}"</p>
            </div>
            """, unsafe_allow_html=True)

def show_history():
    st.markdown("## 📋 Review History")
    
    if not st.session_state.reviews:
        st.info("📚 No reviews in history yet. Start by uploading and reviewing papers!")
        return
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search papers", placeholder="Search by title or author...")
    
    with col2:
        category_filter = st.selectbox(
            "Filter by category",
            ["All Categories"] + list(set([r['category'] for r in st.session_state.reviews]))
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            ["Date (Latest First)", "Date (Oldest First)", "Score (High to Low)", "Score (Low to High)"]
        )
    
    # Filter and sort reviews
    filtered_reviews = st.session_state.reviews.copy()
    
    if search_term:
        filtered_reviews = [r for r in filtered_reviews 
                          if search_term.lower() in r['title'].lower() or 
                             search_term.lower() in r.get('author', '').lower()]
    
    if category_filter != "All Categories":
        filtered_reviews = [r for r in filtered_reviews if r['category'] == category_filter]
    
    # Sort reviews
    if sort_by == "Date (Latest First)":
        filtered_reviews.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == "Date (Oldest First)":
        filtered_reviews.sort(key=lambda x: x['date'])
    elif sort_by == "Score (High to Low)":
        filtered_reviews.sort(key=lambda x: x['overall_score'], reverse=True)
    elif sort_by == "Score (Low to High)":
        filtered_reviews.sort(key=lambda x: x['overall_score'])
    
    # Display reviews
    st.markdown(f"### 📊 Found {len(filtered_reviews)} reviews")
    
    for i, review in enumerate(filtered_reviews):
        with st.expander(f"📄 {review['title']} - Score: {review['overall_score']}/10"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Author:** {review.get('author', 'Not specified')}")
                st.markdown(f"**Category:** {review['category']}")
                st.markdown(f"**Date:** {review['date'].strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**File:** {review['filename']}")
            
            with col2:
                analysis = review['analysis']
                st.metric("Overall Score", f"{analysis['overall_score']}/10")
                st.metric("Word Count", analysis['word_count'])
                st.metric("Readability", f"{analysis['readability_score']}/10")
            
            # Progress bars for scores
            st.markdown("**Detailed Scores:**")
            st.progress(analysis['content_score']/10, text=f"Content: {analysis['content_score']}/10")
            st.progress(analysis['technical_score']/10, text=f"Technical: {analysis['technical_score']}/10")
            st.progress(analysis['innovation_score']/10, text=f"Innovation: {analysis['innovation_score']}/10")
            
            if analysis['suggestions']:
                st.markdown("**Suggestions:**")
                for suggestion in analysis['suggestions']:
                    st.info(suggestion)
            
            # Delete button
            if st.button(f"🗑️ Delete Review", key=f"delete_{i}"):
                st.session_state.reviews.remove(review)
                st.rerun()

if __name__ == "__main__":
    main()