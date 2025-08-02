#!/bin/bash

# Academic Research Paper Analyzer - Setup Script

echo "📚 Academic Research Paper Analyzer - Setup"
echo "============================================"

# Check Python version
echo "🐍 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment package is available
echo "📦 Checking for python3-venv..."
python3 -m venv --help >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  python3-venv not found. Installing..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update
        sudo apt-get install -y python3-venv python3-dev python3-pip
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y python3-venv python3-devel python3-pip
    else
        echo "❌ Unable to install python3-venv automatically. Please install it manually."
        exit 1
    fi
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing..."
    rm -rf venv
fi
python3 -m venv venv

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    nltk.download('universal_tagset', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
    print('✅ NLTK data downloaded successfully')
except Exception as e:
    print(f'⚠️  Warning: Could not download NLTK data: {e}')
"

# Create executable permissions for run script
chmod +x run.sh

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To start the application, run:"
echo "   ./run.sh"
echo ""
echo "📖 Or manually:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "🌐 The application will be available at: http://localhost:8501"