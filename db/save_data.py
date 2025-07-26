import sqlite3

def save_raw_feedback(df, upload_id, db_path="data/feedai.db"):
    conn = sqlite3.connect(db_path)
    df_to_save = df[['text', 'topic', 'sentiment']].copy()
    df_to_save['upload_id'] = upload_id
    df_to_save.to_sql('raw_feedback', conn, if_exists='append', index=False)
    conn.close()

def save_summary(summary_df, upload_id, db_path="data/feedai.db"):
    conn = sqlite3.connect(db_path)
    df_to_save = summary_df.copy()
    df_to_save['upload_id'] = upload_id
    df_to_save.to_sql('feedback_summary', conn, if_exists='append', index=False)
    conn.close()
