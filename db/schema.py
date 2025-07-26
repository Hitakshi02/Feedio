import sqlite3
import pandas as pd

def create_tables(db_path="feedai.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Raw feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id TEXT,
        text TEXT,
        topic INTEGER,
        sentiment REAL,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Aggregated summary table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id TEXT,
        topic INTEGER,
        topic_name TEXT,
        mentions INTEGER,
        avg_sentiment REAL,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def get_topic_trends(db_path="feedai.db"):
    conn = sqlite3.connect(db_path)
    query = """
    SELECT topic_name, upload_id, upload_time,
           SUM(mentions) AS total_mentions,
           ROUND(AVG(avg_sentiment), 3) AS avg_sentiment
    FROM feedback_summary
    GROUP BY topic_name, upload_id
    ORDER BY upload_time
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_sentiment_over_time(db_path="feedai.db"):
    conn = sqlite3.connect(db_path)
    query = """
    SELECT upload_id, upload_time,
           ROUND(AVG(sentiment), 3) AS avg_sentiment
    FROM raw_feedback
    GROUP BY upload_id
    ORDER BY upload_time
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
