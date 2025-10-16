import json
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Load scraped posts
with open('data/scraped_posts.json', 'r') as f:
    all_posts = json.load(f)

# Prepare documents: flatten all posts with subreddit context
documents = []
post_metadata = []  # To track which post belongs to which subreddit

for subreddit, posts in all_posts.items():
    for post in posts:
        title = post['data']['title']
        flair = post['data'].get('link_flair_text', '')
        # Combine title + flair for richer context
        doc = f"{title} {flair}".strip()
        documents.append(doc)
        post_metadata.append({
            'subreddit': subreddit,
            'post_id': post['data']['id'],
            'title': title,
            'flair': flair,
            'score': post['data'].get('score', 0),
            'url': post['data']['url']
        })

# Initialize BERTopic with HDBSCAN (default)
# You can customize vectorizer or embedding model if needed
topic_model = BERTopic(
    embedding_model="all-MiniLM-L6-v2",  # Lightweight, fast, good for short text
    min_topic_size=5,                     # Minimum posts per topic
    nr_topics="auto",                     # Let BERTopic reduce topics
    vectorizer_model=CountVectorizer(stop_words="english", ngram_range=(1, 2))
)

# Fit model
topics, probs = topic_model.fit_transform(documents)

# Get topic info
topic_info = topic_model.get_topic_info()
topic_labels = {}
for _, row in topic_info.iterrows():
    topic_id = row['Topic']
    if topic_id == -1:  # Outlier cluster
        continue
    # Use top 3 keywords as label
    keywords = row['Name'].split('_')[:3]  # BERTopic uses underscore-separated keywords
    label = " ".join(keywords).title()
    topic_labels[topic_id] = label

# Map each post to its topic
post_to_topic = {}
for i, topic_id in enumerate(topics):
    if topic_id == -1:
        continue  # Skip outliers
    post_to_topic[post_metadata[i]['post_id']] = {
        'topic_id': topic_id,
        'topic_label': topic_labels.get(topic_id, "Uncategorized"),
        'score': post_metadata[i]['score']
    }

# Aggregate by subreddit: group posts by topic, sum scores
trending_topics = {}

for subreddit, posts in all_posts.items():
    topic_scores = {}
    for post in posts:
        post_id = post['data']['id']
        if post_id not in post_to_topic:
            continue
        topic_label = post_to_topic[post_id]['topic_label']
        score = post_to_topic[post_id]['score']
        if topic_label not in topic_scores:
            topic_scores[topic_label] = 0
        topic_scores[topic_label] += score

    # Sort by score, take top 5
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    trending_topics[subreddit] = sorted_topics

# Save to JSON
with open('data/trending_topics_bertopic.json', 'w') as f:
    json.dump(trending_topics, f, indent=2)

print("✅ Dynamic topics extracted and saved to 'trending_topics_bertopic.json'")