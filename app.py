import streamlit as st
import pandas as pd
from db.schema import get_topic_trends, get_sentiment_over_time

st.set_page_config(page_title="FeedAI Dashboard", layout="wide")
st.title("📊 FeedAI Feedback Trend Dashboard")

# --- Fetch data ---
trends_df = get_topic_trends()
sentiment_df = get_sentiment_over_time()

# Convert timestamps
trends_df["upload_time"] = pd.to_datetime(trends_df["upload_time"])
sentiment_df["upload_time"] = pd.to_datetime(sentiment_df["upload_time"])

# Drop rows with missing topic_name (if any)
trends_df = trends_df.dropna(subset=["topic_name"])

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎 Filters")

upload_ids = trends_df["upload_id"].unique()
selected_upload = st.sidebar.selectbox("Choose Upload ID", upload_ids)

topics = trends_df["topic_name"].unique()
selected_topic = st.sidebar.selectbox("Choose Topic", topics)

# --- Filtered Data ---
filtered_trends = trends_df[
    (trends_df["upload_id"] == selected_upload) & 
    (trends_df["topic_name"] == selected_topic)
]

# --- Charts ---
st.header("🧠 Average Sentiment Over Time")
if not sentiment_df.empty:
    st.line_chart(sentiment_df.set_index("upload_time")["avg_sentiment"])
else:
    st.warning("No sentiment data available.")

st.header("📌 Topic Mentions Trend")
mentions_chart = trends_df.pivot(index="upload_time", columns="topic_name", values="total_mentions")
if not mentions_chart.empty:
    st.line_chart(mentions_chart)
else:
    st.warning("No data available for topic mentions.")

st.header("📈 Topic Sentiment Over Time")
sentiment_chart = trends_df.pivot(index="upload_time", columns="topic_name", values="avg_sentiment")
if not sentiment_chart.empty:
    st.line_chart(sentiment_chart)
else:
    st.warning("No data available for topic sentiment.")

# --- Filtered Trend Visuals ---
st.subheader("📈 Mentions Over Time for Selected Topic")
if not filtered_trends.empty:
    st.line_chart(filtered_trends.set_index("upload_time")["total_mentions"])
else:
    st.warning("No data found for selected filters.")

st.subheader("🧠 Sentiment Over Time for Selected Topic")
if not filtered_trends.empty:
    st.line_chart(filtered_trends.set_index("upload_time")["avg_sentiment"])

# --- CSV Export ---
st.download_button(
    label="📥 Download as CSV",
    data=filtered_trends.to_csv(index=False),
    file_name=f"feedai_{selected_upload}_{selected_topic}.csv",
    mime="text/csv"
)


# # import streamlit as st
# # import sqlite3
# # import pandas as pd
# # import altair as alt

# # # --- Helper Functions ---
# # @st.cache_data
# # def load_table(table_name):
# #     conn = sqlite3.connect("data/feedai.db")
# #     df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
# #     conn.close()
# #     return df

# # @st.cache_data
# # def get_upload_ids(df):
# #     return df["upload_id"].unique().tolist()

# # # --- App UI ---
# # st.set_page_config(page_title="FeedAI Dashboard", layout="wide")
# # st.title("📊 FeedAI Dashboard")

# # # --- Sidebar Filters ---
# # table_option = st.sidebar.selectbox("Select Table", ["feedback_summary", "raw_feedback"])
# # df = load_table(table_option)

# # if "upload_id" in df.columns:
# #     upload_ids = get_upload_ids(df)
# #     selected_upload_id = st.sidebar.selectbox("Filter by upload_id", upload_ids)
# #     df = df[df["upload_id"] == selected_upload_id]

# # # --- Display Data ---
# # st.subheader(f"📄 Data: {table_option}")
# # st.dataframe(df, use_container_width=True)

# # # --- Trend Visualization ---
# # if table_option == "feedback_summary":
# #     st.subheader("📈 Trend: Avg Sentiment per Topic")
# #     chart = alt.Chart(df).mark_bar().encode(
# #         x=alt.X("topic_name", sort="-y"),
# #         y="avg_sentiment",
# #         tooltip=["topic_name", "avg_sentiment", "mentions"]
# #     ).properties(width=700, height=400)
# #     st.altair_chart(chart, use_container_width=True)

# # # --- Keyword Search ---
# # if table_option == "raw_feedback":
# #     st.subheader("🔍 Keyword Search")
# #     keyword = st.text_input("Search in feedback text")
# #     if keyword:
# #         filtered = df[df["text"].str.contains(keyword, case=False, na=False)]
# #         st.write(f"Found {len(filtered)} matching rows:")
# #         st.dataframe(filtered, use_container_width=True)

# # # --- Download CSV Report ---
# # st.subheader("📤 Download Report")
# # csv = df.to_csv(index=False).encode("utf-8")
# # st.download_button(
# #     label="Download CSV",
# #     data=csv,
# #     file_name=f"{table_option}_export.csv",
# #     mime="text/csv"
# # )

# # # --- Trigger Analysis Placeholder ---
# # st.sidebar.markdown("---")
# # st.sidebar.button("🚀 Run New Analysis (Coming Soon)")
# import streamlit as st
# import pandas as pd
# from db.schema import get_topic_trends, get_sentiment_over_time

# st.set_page_config(page_title="FeedAI Dashboard", layout="wide")
# st.title("📊 FeedAI Feedback Trend Dashboard")

# # --- Fetch data ---
# trends_df = get_topic_trends()
# sentiment_df = get_sentiment_over_time()

# # Convert timestamps
# trends_df["upload_time"] = pd.to_datetime(trends_df["upload_time"])
# sentiment_df["upload_time"] = pd.to_datetime(sentiment_df["upload_time"])

# # --- SIDEBAR FILTERS ---
# st.sidebar.header("🔎 Filters")

# upload_ids = trends_df["upload_id"].unique()
# selected_upload = st.sidebar.selectbox("Choose Upload ID", upload_ids)

# topics = trends_df["topic_name"].unique()
# selected_topic = st.sidebar.selectbox("Choose Topic", topics)

# # --- Filtered Data ---
# filtered_trends = trends_df[
#     (trends_df["upload_id"] == selected_upload) & 
#     (trends_df["topic_name"] == selected_topic)
# ]

# # --- Charts ---
# st.header("🧠 Average Sentiment Over Time")
# st.line_chart(sentiment_df.set_index("upload_time")["avg_sentiment"])

# st.header("📌 Topic Mentions Trend")
# mentions_chart = trends_df.pivot(index="upload_time", columns="topic_name", values="total_mentions")
# st.line_chart(mentions_chart)

# st.header("📈 Topic Sentiment Over Time")
# sentiment_chart = trends_df.pivot(index="upload_time", columns="topic_name", values="avg_sentiment")
# st.line_chart(sentiment_chart)

# # --- Filtered Trend Visuals ---
# st.subheader("📈 Mentions Over Time for Selected Topic")
# st.line_chart(filtered_trends.set_index("upload_time")["total_mentions"])

# st.subheader("🧠 Sentiment Over Time for Selected Topic")
# st.line_chart(filtered_trends.set_index("upload_time")["avg_sentiment"])

# # --- CSV Export ---
# st.download_button(
#     label="📥 Download as CSV",
#     data=filtered_trends.to_csv(index=False),
#     file_name=f"feedai_{selected_upload}_{selected_topic}.csv",
#     mime="text/csv"
# )
