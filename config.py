# Academic Research Paper Reviewer Configuration

# Application Settings
APP_TITLE = "Academic Research Paper Reviewer"
APP_ICON = "📚"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Analysis Settings
DEFAULT_CRITERIA_WEIGHTS = {
    'novelty': 8,
    'methodology': 9,
    'clarity': 7,
    'significance': 8
}

# Review Types and Templates
REVIEW_TYPES = [
    "Academic Conference",
    "Journal Review", 
    "Thesis Defense",
    "Peer Review"
]

# File Upload Settings
SUPPORTED_FILE_TYPES = ['pdf', 'docx']
MAX_FILE_SIZE_MB = 50

# Analysis Thresholds
READABILITY_THRESHOLDS = {
    'excellent': 70,
    'good': 60,
    'fair': 50,
    'poor': 40
}

CITATION_DENSITY_THRESHOLDS = {
    'high': 1.0,
    'medium': 0.5,
    'low': 0.2
}

# Scoring Ranges
SCORE_RANGES = {
    'accept': 8.5,
    'minor_revision': 7.0,
    'major_revision': 5.5,
    'reject': 0.0
}

# Academic Keywords Categories
ACADEMIC_KEYWORD_CATEGORIES = {
    'methodology': [
        'method', 'approach', 'technique', 'algorithm', 'framework', 
        'model', 'system', 'procedure', 'protocol', 'design'
    ],
    'evaluation': [
        'evaluation', 'experiment', 'test', 'validation', 'assessment', 
        'analysis', 'comparison', 'benchmark', 'metric', 'performance'
    ],
    'results': [
        'result', 'finding', 'outcome', 'performance', 'accuracy', 
        'precision', 'recall', 'effectiveness', 'efficiency', 'improvement'
    ],
    'novelty': [
        'novel', 'new', 'innovative', 'original', 'unique', 'contribution', 
        'advancement', 'breakthrough', 'pioneering', 'cutting-edge'
    ],
    'significance': [
        'significant', 'important', 'impact', 'implication', 'benefit', 
        'advantage', 'application', 'practical', 'relevant', 'valuable'
    ]
}

# UI Colors and Styling
UI_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#2c3e50',
    'accent': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Chart Configuration
CHART_CONFIG = {
    'height': 300,
    'use_container_width': True,
    'theme': 'streamlit'
}

# Text Processing Settings
TEXT_PROCESSING = {
    'min_word_length': 3,
    'max_keywords': 20,
    'max_phrases': 10,
    'sentence_analysis_limit': 100
}

# Error Messages
ERROR_MESSAGES = {
    'file_upload_error': "Failed to process the uploaded file. Please check the file format and try again.",
    'text_analysis_error': "An error occurred during text analysis. Please try with different content.",
    'review_generation_error': "Failed to generate review. Please ensure the paper text is available.",
    'empty_text_error': "No text content found. Please upload a valid document or enter text manually."
}

# Success Messages  
SUCCESS_MESSAGES = {
    'file_uploaded': "✅ File uploaded and processed successfully!",
    'analysis_complete': "✅ Analysis completed successfully!",
    'review_generated': "✅ Review generated successfully!",
    'text_processed': "✅ Text processed successfully!"
}