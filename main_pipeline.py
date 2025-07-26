from utils.file_manager import load_csv
from utils.preprocessing import clean_texts
from models.topic_model import generate_topics
from utils.sentiment import analyze_sentiment, summarize_sentiment_by_topic
from tabulate import tabulate
from db.schema import create_tables
from db.save_data import save_raw_feedback, save_summary
import uuid  # for generating unique upload_id

from utils.file_manager import generate_simple_upload_id


import nltk
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


def test_pipeline(csv_path):
    # # Generate unique upload ID
    upload_id = generate_simple_upload_id()


# Create DB & tables if not exist
    create_tables()

    # Step 1: Load and clean data
    df = load_csv(csv_path)
    cleaned = clean_texts(df["text"])

    # Step 2: Topic modeling with BERTopic
    topics, topic_map, model = generate_topics(cleaned)
    df['topic'] = topics

    # Step 3: Sentiment analysis
    df['sentiment'] = analyze_sentiment(df["text"])

    # Step 4: Aggregate sentiment by topic
    summary = summarize_sentiment_by_topic(df)

    # Step 5: Add topic labels to summary
    topic_labels = model.get_topic_info()[['Topic', 'Name']]
    summary = summary.merge(topic_labels, left_on='topic', right_on='Topic', how='left')
    summary = summary[['topic', 'Name', 'mentions', 'avg_sentiment']]

    summary = summary.rename(columns={"Name": "topic_name"})

    # Step 6: Output results
    print("🔍 Topic Summary with Labels:\n")
    print(tabulate(summary, headers='keys', tablefmt='grid'))

    print("\n📋 Sample Row Assignments:\n")
    print(tabulate(df.head(), headers='keys', tablefmt='grid'))

    # Save to DB
    save_raw_feedback(df, upload_id)
    save_summary(summary, upload_id)
    print(f"\n✅ Data saved to SQLite with upload_id: {upload_id}")



# Example usage
test_pipeline("data/uploads/feedai_sample_feedback_v2.csv")
