#!/bin/bash

# Enhanced Academic Research Paper Reviewer - Startup Script
# This script sets up the environment and starts the enhanced Streamlit application

echo "🚀 Starting Enhanced Academic Research Paper Reviewer..."
echo "================================================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking enhanced dependencies..."
python3 -c "import streamlit, pandas, numpy, matplotlib, plotly, fitz, nltk, textstat, wordcloud, sklearn, streamlit_option_menu" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Some enhanced dependencies are missing."
    echo "📥 Installing required packages..."
    pip3 install --break-system-packages -r requirements.txt
    pip3 install --break-system-packages PyMuPDF streamlit-option-menu
fi

echo "✅ All enhanced dependencies verified"

# Check if NLTK data is available
echo "🔤 Checking NLTK data..."
python3 -c "import nltk; nltk.data.find('tokenizers/punkt'); nltk.data.find('corpora/stopwords')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Downloading required NLTK data..."
    python3 -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet'); nltk.download('omw-1.4')"
fi

# Set PATH to include local bin if needed
export PATH="/home/ubuntu/.local/bin:$PATH"

echo "✅ Enhanced environment ready"
echo "================================================================"
echo "📚 Enhanced Academic Research Paper Reviewer"
echo "================================================================"
echo ""
echo "🎨 New Features:"
echo "  • Beautiful gradient dashboard design"
echo "  • Interactive pie charts and visualizations"
echo "  • PyMuPDF integration for superior PDF processing"
echo "  • Comprehensive user feedback system"
echo "  • Enhanced suggestions with smart formatting"
echo "  • Professional review generation"
echo ""
echo "🌐 The enhanced application will open in your browser"
echo "📍 URL: http://localhost:8501"
echo ""
echo "To stop the application, press Ctrl+C"
echo ""

# Start the enhanced Streamlit application
streamlit run app_enhanced.py --server.port 8501 --server.address 0.0.0.0 --browser.gatherUsageStats false