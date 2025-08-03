#!/usr/bin/env python3
"""
Demo script for Academic Paper Reviewer
This script demonstrates the functionality with sample data
"""

import streamlit as st
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample review and feedback data for demonstration"""
    
    # Sample reviews
    sample_reviews = [
        {
            'title': 'Machine Learning Approaches in Computer Vision',
            'category': 'Computer Science',
            'author': 'Dr. Jane Smith, Prof. John Doe',
            'date': datetime.now() - timedelta(days=1),
            'filename': 'ml_computer_vision.pdf',
            'analysis': {
                'overall_score': 8.5,
                'content_score': 8.8,
                'technical_score': 8.2,
                'innovation_score': 8.5,
                'word_count': 4200,
                'sentence_count': 180,
                'readability_score': 7.8,
                'keyword_density': 3.4,
                'sentiment_polarity': 0.2,
                'sentiment_subjectivity': 0.6,
                'structure_score': 6,
                'suggestions': [
                    '📝 Consider expanding the related work section',
                    '🎯 Increase technical terminology usage'
                ],
                'has_sections': {
                    'abstract': True,
                    'introduction': True,
                    'methodology': True,
                    'results': True,
                    'conclusion': True,
                    'references': True
                }
            },
            'overall_score': 8.5
        },
        {
            'title': 'Quantum Computing Applications in Cryptography',
            'category': 'Physics',
            'author': 'Dr. Alice Johnson',
            'date': datetime.now() - timedelta(days=3),
            'filename': 'quantum_crypto.pdf',
            'analysis': {
                'overall_score': 7.2,
                'content_score': 7.5,
                'technical_score': 6.8,
                'innovation_score': 7.3,
                'word_count': 3800,
                'sentence_count': 165,
                'readability_score': 6.9,
                'keyword_density': 2.8,
                'sentiment_polarity': 0.1,
                'sentiment_subjectivity': 0.7,
                'structure_score': 5,
                'suggestions': [
                    '📄 Add an abstract to summarize your research',
                    '🔬 Include a detailed methodology section',
                    '📝 Consider expanding the content'
                ],
                'has_sections': {
                    'abstract': False,
                    'introduction': True,
                    'methodology': True,
                    'results': True,
                    'conclusion': True,
                    'references': True
                }
            },
            'overall_score': 7.2
        },
        {
            'title': 'Biodiversity Conservation in Urban Environments',
            'category': 'Biology',
            'author': 'Dr. Emily Brown, Dr. Michael Green',
            'date': datetime.now() - timedelta(days=5),
            'filename': 'urban_biodiversity.pdf',
            'analysis': {
                'overall_score': 9.1,
                'content_score': 9.3,
                'technical_score': 8.8,
                'innovation_score': 9.2,
                'word_count': 5100,
                'sentence_count': 220,
                'readability_score': 8.5,
                'keyword_density': 4.1,
                'sentiment_polarity': 0.3,
                'sentiment_subjectivity': 0.5,
                'structure_score': 6,
                'suggestions': [
                    '🎯 Excellent use of academic terminology',
                    '📊 Strong methodology and results presentation'
                ],
                'has_sections': {
                    'abstract': True,
                    'introduction': True,
                    'methodology': True,
                    'results': True,
                    'conclusion': True,
                    'references': True
                }
            },
            'overall_score': 9.1
        }
    ]
    
    # Sample feedback data
    sample_feedback = [
        {
            'name': 'Dr. Sarah Wilson',
            'email': 'sarah.wilson@university.edu',
            'type': '⭐ General Feedback',
            'rating': 5,
            'feedback': 'Excellent tool for academic paper review! The AI analysis is very comprehensive and helpful.',
            'date': datetime.now() - timedelta(hours=2),
            'id': 1
        },
        {
            'name': 'Prof. David Miller',
            'email': 'david.miller@research.org',
            'type': '💡 Feature Request',
            'rating': 4,
            'feedback': 'Would love to see integration with academic databases like PubMed or IEEE Xplore.',
            'date': datetime.now() - timedelta(days=1),
            'id': 2
        },
        {
            'name': 'Dr. Lisa Chen',
            'email': 'lisa.chen@institute.edu',
            'type': '📈 Improvement Suggestion',
            'rating': 4,
            'feedback': 'The scoring algorithm is great! Maybe add more detailed citation analysis?',
            'date': datetime.now() - timedelta(days=2),
            'id': 3
        }
    ]
    
    return sample_reviews, sample_feedback

def load_demo_data():
    """Load sample data into session state"""
    if 'demo_loaded' not in st.session_state:
        reviews, feedback = create_sample_data()
        st.session_state.reviews = reviews
        st.session_state.feedback_data = feedback
        st.session_state.demo_loaded = True
        return True
    return False

def show_demo_info():
    """Display demo information"""
    st.info("""
    🎯 **Demo Mode Active**
    
    This application is now loaded with sample data to demonstrate its features:
    - 3 sample paper reviews with different scores
    - Sample feedback from users
    - Interactive analytics and visualizations
    
    You can still upload your own PDF papers to test the real functionality!
    """)

if __name__ == "__main__":
    print("Academic Paper Reviewer Demo")
    print("This demo creates sample data for testing the application.")
    print("\nSample data includes:")
    print("- 3 research paper reviews")
    print("- User feedback entries")
    print("- Various categories and scores")
    print("\nTo run the demo:")
    print("1. Run 'streamlit run app.py'")
    print("2. The demo data will be automatically loaded")
    print("3. Navigate through different sections to see features")