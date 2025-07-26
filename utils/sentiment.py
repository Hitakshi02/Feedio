from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd

# Ensure VADER is available
nltk.download("vader_lexicon")

def analyze_sentiment(text_series):
    sia = SentimentIntensityAnalyzer()
    sentiments = text_series.apply(lambda text: sia.polarity_scores(text)['compound'])
    return sentiments

def summarize_sentiment_by_topic(df):
    """
    Assumes df has 'topic' and 'sentiment' columns.
    Returns a DataFrame with topic, mentions, and avg_sentiment.
    """
    summary = df.groupby('topic')['sentiment'].agg(['count', 'mean']).reset_index()
    summary.columns = ['topic', 'mentions', 'avg_sentiment']
    return summary
