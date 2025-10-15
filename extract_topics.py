import json
from collections import Counter

# Load scraped posts from JSON file
with open('scraped_posts.json', 'r') as f:
    all_posts = json.load(f)

# Define topic keywords (you can expand this)
topic_keywords = {
    'library': 'Library Funding',
    'housing': 'Affordable Housing',
    'traffic': 'Traffic Safety',
    'safety': 'Public Safety',
    'petition': 'Petition',
    'event': 'Event',
    'recommendation': 'Recommendation',
    'question': 'Question',
    'politics': 'Politics',
    'health': 'Health',
    'food': 'Food',
    'music': 'Music',
    'sports': 'Sports',
    'education': 'Education',
    'environment': 'Environment',
    'election': 'Election',
    'vote': 'Election',
    'power': 'Electricity Rates',
    'bill': 'Electricity Rates',
    'dhs': 'DHS Shutdown',
    'halloween': 'Halloween Events',
    'haunted': 'Halloween Events',
    'concert': 'Music Events',
    'movie': 'Movie Events',
    'game': 'Gaming',
    'dog': 'Pets',
    'cat': 'Pets',
    'car': 'Transportation',
    'bus': 'Transportation',
    'train': 'Transportation',
    'bike': 'Transportation',
    'walk': 'Transportation',
    'park': 'Parks',
    'trail': 'Parks',
    'garden': 'Parks',
    'beach': 'Parks',
    'lake': 'Parks',
    'river': 'Parks',
    'mountain': 'Parks',
    'forest': 'Parks',
    'camping': 'Parks',
    'hiking': 'Parks',
    'fishing': 'Parks',
    'boating': 'Parks',
    'swimming': 'Parks',
    'skiing': 'Parks',
    'snowboarding': 'Parks',
    'snow': 'Parks',
    'ice': 'Parks',
    'frost': 'Parks',
    'freeze': 'Parks',
    'thaw': 'Parks',
    'melt': 'Parks',
    'dry': 'Parks',
    'wet': 'Parks',
    'damp': 'Parks',
    'humid': 'Parks',
    'arid': 'Parks',
    'desert': 'Parks',
    'jungle': 'Parks',
    'swamp': 'Parks',
    'marsh': 'Parks',
    'bog': 'Parks',
    'fen': 'Parks',
    'moor': 'Parks',
    'heath': 'Parks',
    'meadow': 'Parks',
    'field': 'Parks',
    'plain': 'Parks',
    'steppe': 'Parks',
    'prairie': 'Parks',
    'savanna': 'Parks',
    'grassland': 'Parks',
    'tundra': 'Parks',
    'taiga': 'Parks',
    'boreal': 'Parks',
    'alpine': 'Parks',
    'montane': 'Parks',
    'subalpine': 'Parks',
    'subarctic': 'Parks',
    'arctic': 'Parks',
    'antarctic': 'Parks',
    'tropical': 'Parks',
    'subtropical': 'Parks',
    'temperate': 'Parks',
    'polar': 'Parks',
    'equatorial': 'Parks',
}

# Extract topics for each subreddit
trending_topics = {}

for subreddit, posts in all_posts.items():
    topic_scores = {}  # Dictionary to store weighted topic scores
    for post in posts:
        title = post['data']['title'].lower()
        flair = post['data']['link_flair_text']
        if flair:
            flair = flair.lower()
        score = post['data'].get('score', 0)  # Get upvote count

        # Extract topics from title and flair
        for keyword, topic in topic_keywords.items():
            if keyword in title or (flair and keyword in flair):
                if topic not in topic_scores:
                    topic_scores[topic] = 0
                topic_scores[topic] += score  # Weight topic by upvotes

    # Sort topics by score (highest first)
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
    trending_topics[subreddit] = sorted_topics[:5]  # Top 5 topics by upvote weight

# Save trending topics to a JSON file
with open('trending_topics_weighted.json', 'w') as f:
    json.dump(trending_topics, f, indent=2)

print("✅ Trending topics extracted and saved to 'trending_topics_weighted.json'")