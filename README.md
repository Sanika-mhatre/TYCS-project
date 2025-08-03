# 🎓 Academic Paper Reviewer

An AI-powered research paper analysis and review system built with Streamlit, PyMuPDF, and machine learning technologies. This application provides comprehensive analysis of academic papers with beautiful visualizations, intelligent suggestions, and user feedback capabilities.

## ✨ Features

### 📊 Interactive Dashboard
- Real-time metrics and statistics
- Beautiful pie charts and visualizations
- Score distribution analysis
- Category-based performance tracking

### 📄 PDF Paper Analysis
- **PDF Text Extraction**: Uses PyMuPDF for accurate text extraction
- **ML-Based Analysis**: Advanced natural language processing
- **Sentiment Analysis**: TextBlob integration for sentiment scoring
- **Content Quality Assessment**: Academic keyword density analysis
- **Structure Analysis**: Automatic detection of paper sections
- **Readability Scoring**: Quantitative readability assessment

### 🤖 AI-Powered Features
- **Intelligent Scoring System**: Multi-dimensional quality assessment
- **Smart Suggestions**: Personalized improvement recommendations
- **Content Analysis**: Academic terminology and structure validation
- **Innovation Assessment**: Novelty and contribution evaluation

### 📈 Advanced Analytics
- Score trends over time
- Category performance comparison
- Word cloud of common suggestions
- Interactive visualizations with Plotly

### 💬 Feedback System
- User feedback collection and analysis
- Rating distribution visualization
- Feedback type categorization
- Recent feedback display

### 📋 Review History
- Complete review management
- Search and filter functionality
- Detailed review examination
- Progress tracking with visual indicators

## 🎨 Design Features

### Beautiful UI/UX
- **Modern Color Schemes**: Gradient backgrounds and attractive color combinations
- **Responsive Layout**: Mobile-friendly design with Streamlit's wide layout
- **Custom CSS Styling**: Professional cards and components
- **Interactive Elements**: Hover effects and smooth transitions
- **Intuitive Navigation**: Sidebar-based page navigation

### Color Palette
- Primary: Purple-Blue gradient (`#667eea` to `#764ba2`)
- Secondary: Pink gradient (`#f093fb` to `#f5576c`)
- Accent: Blue gradient (`#4facfe` to `#00f2fe`)
- Chart colors: Viridis, Blues, and custom color sequences

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the repository**
```bash
git clone <repository-url>
cd academic-paper-reviewer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data** (if needed)
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
The application will automatically open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Dashboard Overview
- View key metrics and statistics
- Analyze score distributions with pie charts
- Monitor category performance
- Track daily review counts

### 2. Upload & Review Papers
- Upload PDF research papers
- Enter paper details (title, category, author)
- Get instant AI-powered analysis
- View detailed scoring and suggestions

### 3. Analytics Section
- Examine score trends over time
- Compare performance across categories
- View suggestion word clouds
- Analyze review patterns

### 4. Feedback System
- Submit feedback and suggestions
- Rate the application
- View feedback statistics
- Browse recent user feedback

### 5. Review History
- Search and filter past reviews
- Sort by date or score
- View detailed analysis reports
- Manage review database

## 🔬 ML Analysis Components

### Scoring Algorithm
The application uses a sophisticated multi-dimensional scoring system:

- **Content Score** (0-10): Based on academic keyword density and structure
- **Technical Score** (0-10): Readability and objectivity assessment
- **Innovation Score** (0-10): Novelty and contribution evaluation
- **Overall Score**: Weighted average of all components

### Analysis Metrics
- Word count and sentence analysis
- Academic keyword density
- Sentiment polarity and subjectivity
- Paper structure validation
- Readability assessment

### Smart Suggestions
The system provides intelligent recommendations including:
- Content expansion suggestions
- Structure improvement advice
- Academic terminology enhancement
- Language and tone improvements

## 🛠️ Technical Stack

### Backend
- **Streamlit**: Web application framework
- **PyMuPDF (fitz)**: PDF text extraction
- **scikit-learn**: Machine learning algorithms
- **TextBlob**: Natural language processing
- **NLTK**: Text analysis and preprocessing

### Visualization
- **Plotly**: Interactive charts and graphs
- **Matplotlib**: Statistical visualizations
- **Seaborn**: Advanced data visualization
- **WordCloud**: Text visualization

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Collections**: Data structure utilities

## 📊 Sample Analysis Output

When you upload a paper, you'll receive:

```
🏆 Overall Score: 7.8/10
├── Content Quality: 8.2/10
├── Technical Quality: 7.1/10
└── Innovation Score: 8.1/10

📊 Metrics:
├── Word Count: 4,250
├── Readability: 7.5/10
├── Keyword Density: 3.2%
├── Sentiment: 0.15
└── Structure Score: 5/6

📋 Paper Structure:
├── ✅ Abstract
├── ✅ Introduction
├── ✅ Methodology
├── ✅ Results
├── ✅ Conclusion
└── ❌ References

💡 Suggestions:
├── 📄 Add a comprehensive references section
├── 🎯 Increase academic terminology usage
└── 📝 Consider expanding the methodology section
```

## 🎯 Future Enhancements

- Integration with academic databases
- Advanced ML models (transformers, BERT)
- Multi-language support
- Collaboration features
- Export functionality
- API integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📝 License

This project is open source and available under the MIT License.

## 🌟 Acknowledgments

- Streamlit team for the amazing framework
- PyMuPDF developers for robust PDF processing
- The open-source ML community for powerful tools

---

**Made with ❤️ for the academic community**