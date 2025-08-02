import re
import nltk
import textstat
import numpy as np
import pandas as pd
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
import streamlit as st

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

try:
    nltk.data.find('corpora/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class TextAnalyzer:
    """Comprehensive text analysis class for academic papers"""
    
    def __init__(self, language='english'):
        self.language = language
        self.stop_words = set(stopwords.words(language))
        self.stemmer = PorterStemmer()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Academic-specific stop words
        self.academic_stopwords = {
            'paper', 'study', 'research', 'analysis', 'method', 'approach',
            'result', 'conclusion', 'discussion', 'introduction', 'section',
            'figure', 'table', 'equation', 'reference', 'cite', 'author',
            'journal', 'publication', 'article', 'manuscript', 'thesis'
        }
    
    def get_text_statistics(self, text: str) -> Dict[str, Any]:
        """
        Calculate comprehensive text statistics
        
        Args:
            text: Input text to analyze
            
        Returns:
            dict: Text statistics
        """
        if not text:
            return {}
        
        # Basic counts
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Filter out non-alphabetic words for linguistic analysis
        alphabetic_words = [word for word in words if word.isalpha()]
        
        # Unique words and lexical diversity
        unique_words = set(alphabetic_words)
        lexical_diversity = len(unique_words) / len(alphabetic_words) if alphabetic_words else 0
        
        # Average metrics
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        avg_chars_per_word = sum(len(word) for word in alphabetic_words) / len(alphabetic_words) if alphabetic_words else 0
        
        # Syllable analysis
        syllable_count = sum(textstat.syllable_count(word) for word in alphabetic_words)
        avg_syllables_per_word = syllable_count / len(alphabetic_words) if alphabetic_words else 0
        
        # Part-of-speech analysis
        pos_tags = pos_tag(alphabetic_words[:1000])  # Limit for performance
        pos_counts = Counter(tag for _, tag in pos_tags)
        
        # Academic complexity indicators
        complex_words = [word for word in alphabetic_words if len(word) > 6]
        technical_ratio = len(complex_words) / len(alphabetic_words) if alphabetic_words else 0
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'character_count': len(text),
            'unique_words': len(unique_words),
            'lexical_diversity': round(lexical_diversity, 4),
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'avg_chars_per_word': round(avg_chars_per_word, 2),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2),
            'syllable_count': syllable_count,
            'technical_ratio': round(technical_ratio, 4),
            'pos_distribution': dict(pos_counts.most_common(10))
        }
    
    def get_readability_scores(self, text: str) -> Dict[str, float]:
        """
        Calculate various readability scores
        
        Args:
            text: Input text to analyze
            
        Returns:
            dict: Readability scores
        """
        if not text:
            return {}
        
        try:
            scores = {
                'flesch_reading_ease': textstat.flesch_reading_ease(text),
                'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
                'gunning_fog': textstat.gunning_fog(text),
                'smog_index': textstat.smog_index(text),
                'automated_readability_index': textstat.automated_readability_index(text),
                'coleman_liau_index': textstat.coleman_liau_index(text),
                'linsear_write_formula': textstat.linsear_write_formula(text),
                'dale_chall_readability_score': textstat.dale_chall_readability_score(text),
                'text_standard': textstat.text_standard(text, float_output=True)
            }
            
            # Additional metrics
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            scores['avg_sentence_length'] = len(words) / len(sentences) if sentences else 0
            scores['sentence_length_variance'] = np.var([len(word_tokenize(sent)) for sent in sentences]) if sentences else 0
            
            return {k: round(v, 2) if isinstance(v, (int, float)) else v for k, v in scores.items()}
            
        except Exception as e:
            st.warning(f"Could not calculate all readability scores: {str(e)}")
            return {'error': str(e)}
    
    def extract_keywords(self, text: str, max_keywords: int = 20, min_length: int = 4) -> List[Tuple[str, float]]:
        """
        Extract keywords using TF-IDF
        
        Args:
            text: Input text
            max_keywords: Maximum number of keywords to return
            min_length: Minimum word length
            
        Returns:
            list: List of (keyword, score) tuples
        """
        if not text:
            return []
        
        try:
            # Preprocess text
            words = word_tokenize(text.lower())
            words = [word for word in words if word.isalpha() and len(word) >= min_length]
            words = [word for word in words if word not in self.stop_words and word not in self.academic_stopwords]
            
            # Create sentences for TF-IDF
            sentences = sent_tokenize(text)
            
            if len(sentences) < 2:
                # Fallback to simple frequency counting
                word_freq = Counter(words)
                return word_freq.most_common(max_keywords)
            
            # Use TF-IDF for keyword extraction
            vectorizer = TfidfVectorizer(
                max_features=max_keywords * 2,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.8
            )
            
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Create keyword-score pairs
            keyword_scores = list(zip(feature_names, mean_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return keyword_scores[:max_keywords]
            
        except Exception as e:
            st.warning(f"Error in keyword extraction: {str(e)}")
            # Fallback to simple word frequency
            words = word_tokenize(text.lower())
            words = [word for word in words if word.isalpha() and len(word) >= min_length]
            word_freq = Counter(words)
            return word_freq.most_common(max_keywords)
    
    def extract_key_phrases(self, text: str, max_phrases: int = 15) -> List[Tuple[str, float]]:
        """
        Extract key phrases using n-gram analysis
        
        Args:
            text: Input text
            max_phrases: Maximum number of phrases to return
            
        Returns:
            list: List of (phrase, relevance) tuples
        """
        if not text:
            return []
        
        try:
            # Extract bigrams and trigrams
            vectorizer = TfidfVectorizer(
                ngram_range=(2, 3),
                max_features=max_phrases * 2,
                stop_words='english',
                min_df=1,
                max_df=0.8
            )
            
            sentences = sent_tokenize(text)
            if len(sentences) < 2:
                return []
            
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Create phrase-score pairs
            phrase_scores = list(zip(feature_names, mean_scores))
            phrase_scores.sort(key=lambda x: x[1], reverse=True)
            
            return phrase_scores[:max_phrases]
            
        except Exception as e:
            st.warning(f"Error in phrase extraction: {str(e)}")
            return []
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of the text
        
        Args:
            text: Input text
            
        Returns:
            dict: Sentiment scores
        """
        if not text:
            return {}
        
        try:
            # VADER sentiment analysis
            scores = self.sentiment_analyzer.polarity_scores(text)
            
            # Sentence-level analysis
            sentences = sent_tokenize(text)
            sentence_sentiments = [self.sentiment_analyzer.polarity_scores(sent) for sent in sentences]
            
            # Calculate additional metrics
            positive_sentences = sum(1 for s in sentence_sentiments if s['compound'] > 0.1)
            negative_sentences = sum(1 for s in sentence_sentiments if s['compound'] < -0.1)
            neutral_sentences = len(sentences) - positive_sentences - negative_sentences
            
            sentiment_variance = np.var([s['compound'] for s in sentence_sentiments])
            
            return {
                'compound': round(scores['compound'], 3),
                'positive': round(scores['pos'], 3),
                'negative': round(scores['neg'], 3),
                'neutral': round(scores['neu'], 3),
                'positive_sentences': positive_sentences,
                'negative_sentences': negative_sentences,
                'neutral_sentences': neutral_sentences,
                'sentiment_variance': round(sentiment_variance, 3)
            }
            
        except Exception as e:
            st.warning(f"Error in sentiment analysis: {str(e)}")
            return {}
    
    def extract_topics(self, text: str, num_topics: int = 5) -> List[Dict[str, Any]]:
        """
        Extract topics using Latent Dirichlet Allocation
        
        Args:
            text: Input text
            num_topics: Number of topics to extract
            
        Returns:
            list: List of topic dictionaries
        """
        if not text:
            return []
        
        try:
            sentences = sent_tokenize(text)
            
            if len(sentences) < num_topics:
                return []
            
            # Vectorize the text
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.8
            )
            
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            
            # LDA topic modeling
            lda = LatentDirichletAllocation(
                n_components=num_topics,
                random_state=42,
                max_iter=10
            )
            
            lda.fit(tfidf_matrix)
            
            # Extract topics
            topics = []
            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[-10:][::-1]
                top_words = [feature_names[i] for i in top_words_idx]
                top_weights = [topic[i] for i in top_words_idx]
                
                topics.append({
                    'topic_id': topic_idx,
                    'words': list(zip(top_words, top_weights)),
                    'top_terms': ', '.join(top_words[:5])
                })
            
            return topics
            
        except Exception as e:
            st.warning(f"Error in topic extraction: {str(e)}")
            return []
    
    def extract_named_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        
        Args:
            text: Input text
            
        Returns:
            dict: Named entities by category
        """
        if not text:
            return {}
        
        try:
            # Limit text length for performance
            text_sample = text[:5000] if len(text) > 5000 else text
            
            words = word_tokenize(text_sample)
            pos_tags = pos_tag(words)
            chunks = ne_chunk(pos_tags)
            
            entities = defaultdict(list)
            
            for chunk in chunks:
                if hasattr(chunk, 'label'):
                    entity_name = ' '.join([token for token, pos in chunk.leaves()])
                    entity_type = chunk.label()
                    entities[entity_type].append(entity_name)
            
            return dict(entities)
            
        except Exception as e:
            st.warning(f"Error in named entity extraction: {str(e)}")
            return {}
    
    def get_writing_quality_metrics(self, text: str) -> Dict[str, Any]:
        """
        Calculate writing quality metrics
        
        Args:
            text: Input text
            
        Returns:
            dict: Writing quality metrics
        """
        if not text:
            return {}
        
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text.lower())
            alphabetic_words = [word for word in words if word.isalpha()]
            
            # Sentence length analysis
            sentence_lengths = [len(word_tokenize(sent)) for sent in sentences]
            avg_sentence_length = np.mean(sentence_lengths)
            sentence_length_std = np.std(sentence_lengths)
            
            # Word length analysis
            word_lengths = [len(word) for word in alphabetic_words]
            avg_word_length = np.mean(word_lengths)
            
            # Vocabulary richness
            unique_words = set(alphabetic_words)
            type_token_ratio = len(unique_words) / len(alphabetic_words) if alphabetic_words else 0
            
            # Passive voice detection (simplified)
            passive_indicators = ['was', 'were', 'been', 'being', 'be']
            passive_count = sum(1 for word in words if word in passive_indicators)
            passive_ratio = passive_count / len(words) if words else 0
            
            # Transition words
            transitions = ['however', 'therefore', 'furthermore', 'moreover', 'nevertheless', 'consequently']
            transition_count = sum(1 for word in words if word in transitions)
            transition_ratio = transition_count / len(sentences) if sentences else 0
            
            return {
                'avg_sentence_length': round(avg_sentence_length, 2),
                'sentence_length_std': round(sentence_length_std, 2),
                'avg_word_length': round(avg_word_length, 2),
                'type_token_ratio': round(type_token_ratio, 4),
                'passive_voice_ratio': round(passive_ratio, 4),
                'transition_ratio': round(transition_ratio, 4),
                'sentence_count': len(sentences),
                'word_count': len(alphabetic_words)
            }
            
        except Exception as e:
            st.warning(f"Error in writing quality analysis: {str(e)}")
            return {}