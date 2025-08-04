#!/bin/bash

# Academic Research Paper Reviewer - Startup Script
# This script sets up the environment and starts the Streamlit application

echo "🚀 Starting Academic Research Paper Reviewer..."
echo "================================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit, pandas, numpy, matplotlib, plotly, PyPDF2, nltk, textstat, wordcloud, sklearn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Some dependencies are missing. Please run: pip3 install -r requirements.txt"
    exit 1
fi

echo "✅ All dependencies verified"

# Check if NLTK data is available
echo "🔤 Checking NLTK data..."
python3 -c "import nltk; nltk.data.find('tokenizers/punkt'); nltk.data.find('corpora/stopwords')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Downloading required NLTK data..."
    python3 -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('omw-1.4')"
fi

# Set PATH to include local bin if needed
export PATH="/home/ubuntu/.local/bin:$PATH"

echo "✅ Environment ready"
echo "================================================"
echo "📚 Academic Research Paper Reviewer"
echo "================================================"
echo ""
echo "🌐 The application will open in your default browser"
echo "📍 URL: http://localhost:8501"
echo ""
echo "To stop the application, press Ctrl+C"
echo ""

# Start the Streamlit application
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --browser.gatherUsageStats false