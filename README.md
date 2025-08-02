# Academic Research Paper Analyzer Assistant

A comprehensive Streamlit application for analyzing academic research papers using advanced natural language processing and machine learning techniques.

## Features

### 📄 PDF Processing
- Extract text from PDF research papers
- Support for multiple file uploads
- Automatic text cleaning and preprocessing
- Section-based analysis (Abstract, Introduction, Methods, etc.)

### 📊 Text Analysis
- **Comprehensive text statistics**: Word count, sentence analysis, paragraph structure
- **Readability assessment**: Flesch Reading Ease, Flesch-Kincaid Grade Level, and more
- **Keyword extraction**: TF-IDF based keyword identification
- **Sentiment analysis**: VADER sentiment analysis with detailed metrics
- **Topic modeling**: Latent Dirichlet Allocation for topic extraction
- **Named entity recognition**: Identify people, places, organizations
- **Writing quality metrics**: Lexical diversity, passive voice detection, transition word usage

### 📚 Citation Analysis
- **Citation extraction**: Multiple citation format support (APA, numbered, etc.)
- **Reference parsing**: Automatic reference section identification and parsing
- **Author network analysis**: Collaboration patterns and author frequency
- **Citation timeline**: Temporal analysis of cited works
- **Publication type classification**: Journal, conference, book, preprint identification

### 📈 Interactive Visualizations
- **Word clouds**: Visual representation of key terms
- **Interactive charts**: Plotly-powered dynamic visualizations
- **Citation timelines**: Track citation patterns over time
- **Readability radar charts**: Multi-dimensional readability assessment
- **Sentiment gauges**: Visual sentiment scoring
- **Comparative analysis**: Side-by-side paper comparison
- **Topic sunburst charts**: Hierarchical topic visualization

### 🔧 Advanced Features
- **Batch processing**: Analyze multiple papers simultaneously
- **Configurable settings**: Customizable analysis parameters
- **Export capabilities**: Save analysis results
- **Sample data**: Try the tool with pre-loaded examples
- **Real-time processing**: Live progress tracking

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the repository**
```bash
git clone <repository-url>
cd academic-research-paper-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data** (will be done automatically on first run)
The application will automatically download required NLTK datasets:
- punkt (tokenization)
- stopwords (text filtering)
- averaged_perceptron_tagger (POS tagging)
- vader_lexicon (sentiment analysis)

### Quick Start

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your web browser at `http://localhost:8501`

## Usage Guide

### 1. Upload Research Papers
- Use the sidebar file uploader to select PDF files
- Multiple files can be uploaded simultaneously
- Supported format: PDF only

### 2. Configure Analysis Settings
- **Analysis Type**: Choose from complete analysis or specific components
- **Advanced Settings**: 
  - Adjust keyword extraction parameters
  - Set minimum word length filters
  - Configure language settings

### 3. Run Analysis
- Click "🚀 Analyze Papers" to start processing
- Monitor progress with the real-time progress bar
- View results in organized tabs

### 4. Explore Results

#### Overview Tab 📈
- Basic document statistics
- Readability scores and metrics
- Estimated reading time and complexity

#### Text Analysis Tab 🔤
- Detailed linguistic statistics
- Part-of-speech distribution
- Writing quality assessment

#### Keywords Tab 🔍
- Top keywords and key phrases
- TF-IDF scores and relevance rankings
- Terminology frequency analysis

#### Citations Tab 📚
- Extracted citations and references
- Author collaboration networks
- Publication timeline analysis

#### Visualizations Tab 📊
- Interactive word clouds
- Citation timeline charts
- Readability radar plots
- Comparative analysis charts

## Technical Architecture

### Core Components

1. **PDF Processor** (`utils/pdf_processor.py`)
   - PyPDF2-based text extraction
   - Section identification and parsing
   - Metadata extraction
   - Text cleaning and preprocessing

2. **Text Analyzer** (`utils/text_analyzer.py`)
   - NLTK-powered linguistic analysis
   - Scikit-learn machine learning models
   - Multiple readability metrics
   - Advanced NLP processing

3. **Citation Extractor** (`utils/citation_extractor.py`)
   - Regex-based citation pattern matching
   - Reference section parsing
   - Author network analysis
   - Publication classification

4. **Visualization Helper** (`utils/visualization.py`)
   - Plotly interactive charts
   - Matplotlib word clouds
   - Custom dashboard creation
   - Comparative analysis tools

### Key Technologies
- **Frontend**: Streamlit
- **NLP**: NLTK, scikit-learn
- **Visualization**: Plotly, Matplotlib, Seaborn
- **PDF Processing**: PyPDF2
- **Data Analysis**: Pandas, NumPy

## Configuration Options

### Analysis Parameters
- **Max Keywords**: Number of keywords to extract (10-100)
- **Min Word Length**: Minimum character length for keywords (3-8)
- **Language**: Document language for stopword filtering
- **Include Stopwords**: Option to include common words in analysis

### Visualization Settings
- Multiple chart types available
- Customizable color schemes
- Interactive plot controls
- Export options for charts

## Sample Analysis Results

The application provides comprehensive insights including:

- **Text Complexity**: Grade level, readability scores
- **Content Quality**: Lexical diversity, sentence structure
- **Research Depth**: Citation count, reference quality
- **Temporal Analysis**: Publication timeline, citation years
- **Topic Coverage**: Main themes and subject areas
- **Writing Style**: Sentiment, passive voice usage

## Troubleshooting

### Common Issues

1. **PDF Text Extraction Fails**
   - Ensure PDF contains extractable text (not scanned images)
   - Try OCR preprocessing if needed
   - Check file permissions and corruption

2. **NLTK Download Errors**
   - Ensure stable internet connection
   - Check firewall settings
   - Manual download: `python -c "import nltk; nltk.download('all')"`

3. **Memory Issues with Large Files**
   - Process files individually
   - Reduce analysis scope
   - Check available system memory

4. **Visualization Display Problems**
   - Update browser to latest version
   - Clear browser cache
   - Check JavaScript enabled

### Performance Tips
- Process smaller batches for better performance
- Use specific analysis types instead of complete analysis
- Close unused browser tabs to free memory
- Restart application periodically for large workloads

## Contributing

Contributions are welcome! Areas for improvement:
- Additional citation format support
- Enhanced visualization options
- Multi-language analysis capabilities
- Advanced topic modeling techniques
- Export format options
- API development

## License

This project is open source and available under the MIT License.

## Support

For issues, feature requests, or questions:
- Check the troubleshooting section
- Review the configuration options
- Test with sample data first
- Ensure all dependencies are properly installed

## Future Enhancements

Planned features:
- 🔄 Document comparison tools
- 🌐 Multi-language support expansion
- 📊 Advanced statistical analysis
- 🤖 AI-powered summarization
- 📤 Multiple export formats
- 🔗 Integration with reference managers
- 📱 Mobile-responsive design
- ⚡ Performance optimizations