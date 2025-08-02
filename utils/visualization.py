import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from typing import List, Dict, Any, Tuple, Optional
import streamlit as st
from collections import Counter

class VisualizationHelper:
    """Helper class for creating various visualizations for academic paper analysis"""
    
    def __init__(self):
        # Set style preferences
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Color schemes
        self.color_schemes = {
            'primary': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'academic': ['#2E4A62', '#8B4B91', '#FF6B35', '#F7931E', '#00A6FB'],
            'pastel': ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C']
        }
    
    def create_wordcloud(self, keywords: List[Tuple[str, float]], 
                        width: int = 800, height: int = 400) -> plt.Figure:
        """
        Create a word cloud from keywords
        
        Args:
            keywords: List of (keyword, score) tuples
            width: Width of the word cloud
            height: Height of the word cloud
            
        Returns:
            matplotlib.figure.Figure: Word cloud figure
        """
        if not keywords:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.text(0.5, 0.5, 'No keywords to display', 
                   ha='center', va='center', fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return fig
        
        try:
            # Create frequency dictionary
            word_freq = {word: score for word, score in keywords}
            
            # Create WordCloud
            wordcloud = WordCloud(
                width=width,
                height=height,
                background_color='white',
                colormap='viridis',
                max_words=100,
                relative_scaling=0.5,
                min_font_size=10
            ).generate_from_frequencies(word_freq)
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('Keyword Word Cloud', fontsize=16, fontweight='bold')
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            st.warning(f"Error creating word cloud: {str(e)}")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.text(0.5, 0.5, f'Error: {str(e)}', 
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return fig
    
    def create_keyword_chart(self, keywords: List[Tuple[str, float]], 
                           chart_type: str = 'bar') -> go.Figure:
        """
        Create an interactive keyword frequency chart
        
        Args:
            keywords: List of (keyword, score) tuples
            chart_type: Type of chart ('bar', 'horizontal_bar', 'bubble')
            
        Returns:
            plotly.graph_objects.Figure: Interactive chart
        """
        if not keywords:
            fig = go.Figure()
            fig.add_annotation(
                x=0.5, y=0.5,
                text="No keywords to display",
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Prepare data
        words, scores = zip(*keywords[:20])  # Limit to top 20
        
        df = pd.DataFrame({
            'keyword': words,
            'score': scores
        })
        
        if chart_type == 'horizontal_bar':
            fig = px.bar(
                df, 
                x='score', 
                y='keyword',
                orientation='h',
                title='Top Keywords by Relevance Score',
                labels={'score': 'Relevance Score', 'keyword': 'Keywords'},
                color='score',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=max(400, len(words) * 25))
            
        elif chart_type == 'bubble':
            df['size'] = df['score'] * 100
            fig = px.scatter(
                df,
                x=range(len(words)),
                y='score',
                size='size',
                hover_name='keyword',
                title='Keywords Bubble Chart',
                labels={'x': 'Keyword Index', 'y': 'Relevance Score'}
            )
            
        else:  # Default bar chart
            fig = px.bar(
                df,
                x='keyword',
                y='score',
                title='Top Keywords by Relevance Score',
                labels={'score': 'Relevance Score', 'keyword': 'Keywords'},
                color='score',
                color_continuous_scale='viridis'
            )
            fig.update_xaxes(tickangle=45)
        
        fig.update_layout(
            showlegend=False,
            height=500,
            margin=dict(l=50, r=50, t=80, b=100)
        )
        
        return fig
    
    def create_citation_timeline(self, citations: List[Dict[str, Any]]) -> go.Figure:
        """
        Create a timeline chart of citations by year
        
        Args:
            citations: List of citation dictionaries
            
        Returns:
            plotly.graph_objects.Figure: Timeline chart
        """
        if not citations:
            fig = go.Figure()
            fig.add_annotation(
                x=0.5, y=0.5,
                text="No citations to display",
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Extract years from citations
        years = []
        for citation in citations:
            if 'year' in citation:
                try:
                    year = int(str(citation['year'])[:4])
                    if 1900 <= year <= 2030:  # Reasonable year range
                        years.append(year)
                except (ValueError, TypeError):
                    continue
        
        if not years:
            fig = go.Figure()
            fig.add_annotation(
                x=0.5, y=0.5,
                text="No valid years found in citations",
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Count citations by year
        year_counts = Counter(years)
        years_sorted = sorted(year_counts.keys())
        counts = [year_counts[year] for year in years_sorted]
        
        # Create timeline chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years_sorted,
            y=counts,
            mode='lines+markers',
            name='Citations per Year',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, color='#ff7f0e')
        ))
        
        fig.update_layout(
            title='Citation Timeline',
            xaxis_title='Publication Year',
            yaxis_title='Number of Citations',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_readability_radar(self, readability_scores: Dict[str, float]) -> go.Figure:
        """
        Create a radar chart for readability metrics
        
        Args:
            readability_scores: Dictionary of readability scores
            
        Returns:
            plotly.graph_objects.Figure: Radar chart
        """
        if not readability_scores:
            fig = go.Figure()
            fig.add_annotation(
                x=0.5, y=0.5,
                text="No readability data to display",
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Select key readability metrics
        metrics = {
            'flesch_reading_ease': 'Reading Ease',
            'flesch_kincaid_grade': 'Grade Level',
            'gunning_fog': 'Fog Index',
            'automated_readability_index': 'ARI',
            'coleman_liau_index': 'Coleman-Liau'
        }
        
        # Prepare data
        categories = []
        values = []
        
        for key, label in metrics.items():
            if key in readability_scores:
                categories.append(label)
                # Normalize values to 0-100 scale for better visualization
                value = readability_scores[key]
                if key == 'flesch_reading_ease':
                    normalized_value = max(0, min(100, value))
                else:
                    # For grade-level metrics, cap at 20 and normalize
                    normalized_value = max(0, min(100, (value / 20) * 100))
                values.append(normalized_value)
        
        if not values:
            fig = go.Figure()
            fig.add_annotation(
                x=0.5, y=0.5,
                text="No valid readability metrics found",
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Close the radar chart
        categories.append(categories[0])
        values.append(values[0])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Readability Scores',
            line_color='#1f77b4'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Readability Analysis Radar Chart",
            height=500
        )
        
        return fig
    
    def create_sentiment_gauge(self, sentiment_score: float) -> go.Figure:
        """
        Create a gauge chart for sentiment analysis
        
        Args:
            sentiment_score: Sentiment compound score (-1 to 1)
            
        Returns:
            plotly.graph_objects.Figure: Gauge chart
        """
        # Convert score to 0-100 scale
        gauge_value = (sentiment_score + 1) * 50
        
        # Determine color based on sentiment
        if sentiment_score < -0.1:
            color = '#d62728'  # Red for negative
            sentiment_label = 'Negative'
        elif sentiment_score > 0.1:
            color = '#2ca02c'  # Green for positive
            sentiment_label = 'Positive'
        else:
            color = '#ff7f0e'  # Orange for neutral
            sentiment_label = 'Neutral'
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=gauge_value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Sentiment Analysis<br><span style='font-size:0.8em;color:gray'>{sentiment_label}</span>"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 60], 'color': "gray"},
                    {'range': [60, 100], 'color': "lightgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig
    
    def create_text_stats_dashboard(self, text_stats: Dict[str, Any]) -> go.Figure:
        """
        Create a dashboard of text statistics
        
        Args:
            text_stats: Dictionary of text statistics
            
        Returns:
            plotly.graph_objects.Figure: Dashboard figure
        """
        if not text_stats:
            fig = go.Figure()
            fig.add_annotation(
                x=0.5, y=0.5,
                text="No text statistics to display",
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Word Count Distribution', 
                'Sentence Length Analysis',
                'Lexical Diversity', 
                'Part-of-Speech Distribution'
            ),
            specs=[[{"type": "bar"}, {"type": "histogram"}],
                   [{"type": "indicator"}, {"type": "pie"}]]
        )
        
        # Word count bar chart
        basic_stats = ['word_count', 'sentence_count', 'paragraph_count']
        values = [text_stats.get(stat, 0) for stat in basic_stats]
        labels = ['Words', 'Sentences', 'Paragraphs']
        
        fig.add_trace(
            go.Bar(x=labels, y=values, name='Counts', marker_color='#1f77b4'),
            row=1, col=1
        )
        
        # Sentence length histogram (simulated data)
        if 'avg_words_per_sentence' in text_stats:
            avg_length = text_stats['avg_words_per_sentence']
            # Generate simulated sentence lengths for visualization
            sentence_lengths = np.random.normal(avg_length, avg_length/4, 100)
            sentence_lengths = np.clip(sentence_lengths, 1, None)
            
            fig.add_trace(
                go.Histogram(x=sentence_lengths, name='Sentence Lengths', 
                           marker_color='#ff7f0e', nbinsx=20),
                row=1, col=2
            )
        
        # Lexical diversity indicator
        if 'lexical_diversity' in text_stats:
            diversity_value = text_stats['lexical_diversity'] * 100
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=diversity_value,
                    title={'text': "Lexical Diversity %"},
                    gauge={'axis': {'range': [None, 100]},
                           'bar': {'color': '#2ca02c'},
                           'steps': [{'range': [0, 50], 'color': "lightgray"},
                                   {'range': [50, 100], 'color': "gray"}]},
                    domain={'x': [0, 1], 'y': [0, 1]}
                ),
                row=2, col=1
            )
        
        # Part-of-speech pie chart
        if 'pos_distribution' in text_stats and text_stats['pos_distribution']:
            pos_data = text_stats['pos_distribution']
            pos_labels = list(pos_data.keys())[:8]  # Top 8 POS tags
            pos_values = [pos_data[label] for label in pos_labels]
            
            fig.add_trace(
                go.Pie(labels=pos_labels, values=pos_values, name="POS"),
                row=2, col=2
            )
        
        fig.update_layout(height=600, showlegend=False, 
                         title_text="Text Analysis Dashboard")
        
        return fig
    
    def create_comparative_analysis(self, papers_data: List[Dict[str, Any]]) -> go.Figure:
        """
        Create a comparative analysis chart for multiple papers
        
        Args:
            papers_data: List of paper analysis data
            
        Returns:
            plotly.graph_objects.Figure: Comparative chart
        """
        if len(papers_data) < 2:
            fig = go.Figure()
            fig.add_annotation(
                x=0.5, y=0.5,
                text="Need at least 2 papers for comparison",
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Extract comparison metrics
        paper_names = [paper.get('filename', f'Paper {i+1}')[:20] 
                      for i, paper in enumerate(papers_data)]
        
        metrics = {
            'Word Count': [paper.get('word_count', 0) for paper in papers_data],
            'Readability Score': [paper.get('readability', {}).get('flesch_reading_ease', 0) 
                                for paper in papers_data],
            'Citation Count': [len(paper.get('citations', [])) for paper in papers_data],
            'Keyword Diversity': [len(paper.get('keywords', [])) for paper in papers_data]
        }
        
        # Create radar chart for comparison
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, paper_name in enumerate(paper_names):
            # Normalize values for radar chart
            normalized_values = []
            for metric, values in metrics.items():
                if values[i] > 0:
                    max_val = max(values) if max(values) > 0 else 1
                    normalized_values.append((values[i] / max_val) * 100)
                else:
                    normalized_values.append(0)
            
            # Close the polygon
            metric_names = list(metrics.keys())
            metric_names.append(metric_names[0])
            normalized_values.append(normalized_values[0])
            
            fig.add_trace(go.Scatterpolar(
                r=normalized_values,
                theta=metric_names,
                fill='toself',
                name=paper_name,
                line_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Comparative Paper Analysis",
            height=500
        )
        
        return fig
    
    def create_topic_visualization(self, topics: List[Dict[str, Any]]) -> go.Figure:
        """
        Create visualization for extracted topics
        
        Args:
            topics: List of topic dictionaries from LDA
            
        Returns:
            plotly.graph_objects.Figure: Topic visualization
        """
        if not topics:
            fig = go.Figure()
            fig.add_annotation(
                x=0.5, y=0.5,
                text="No topics to display",
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Prepare data for sunburst chart
        labels = []
        parents = []
        values = []
        
        # Add root
        labels.append("Topics")
        parents.append("")
        values.append(len(topics))
        
        # Add topics and their words
        for topic in topics:
            topic_id = topic.get('topic_id', 0)
            topic_label = f"Topic {topic_id + 1}"
            
            labels.append(topic_label)
            parents.append("Topics")
            values.append(len(topic.get('words', [])))
            
            # Add top words for each topic
            for word, weight in topic.get('words', [])[:5]:  # Top 5 words
                labels.append(f"{word} ({weight:.3f})")
                parents.append(topic_label)
                values.append(weight * 100)
        
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
        ))
        
        fig.update_layout(
            title="Topic Modeling Visualization",
            height=600
        )
        
        return fig