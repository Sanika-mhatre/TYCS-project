#!/bin/bash

# Academic Research Paper Analyzer - Startup Script

echo "🚀 Starting Academic Research Paper Analyzer..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import streamlit, pandas, nltk, spacy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencies not found. Installing..."
    pip install -r requirements.txt
fi

echo "📚 Starting Streamlit application..."
echo "🌐 The application will be available at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the application"

# Run the application
streamlit run app.py --server.headless false