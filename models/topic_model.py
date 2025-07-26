from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

def generate_topics(texts):
    # Step 1: Load embedding model
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 2: Batch embedding for speed
    embeddings = embedding_model.encode(
        texts.tolist(),
        show_progress_bar=True,
        batch_size=32,
        convert_to_tensor=False
    )

    # Step 3: Fit BERTopic with embeddings
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(texts.tolist(), embeddings)

    # Step 4: Get topic map and assign readable names
    topic_map = topic_model.get_topic_info()
    topic_map['Name'] = topic_map['Topic'].apply(lambda t: generate_clean_name(topic_model, t))

    return topics, topic_map, topic_model

def generate_clean_name(model, topic_id):
    if topic_id == -1:
        return "Miscellaneous / Noise"
    
    words = model.get_topic(topic_id)
    if not words:
        return "Unnamed Topic"
    
    top_words = [word for word, _ in words[:2]]  # top 2 keywords
    return " & ".join(top_words).title()  # e.g., 'Login & Error'
