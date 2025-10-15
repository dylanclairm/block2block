import requests
import json

# Your Reddit app credentials (just for User-Agent)
USER_AGENT = 'blocktoblock by u/Inevitable_Bowl_2019'  # ← Your Reddit username

# List of subreddits to scrape
subreddits = [
    "Atlanta",
    "Athens",
    "Savannah",
    "Augusta",
    "Macon",
    "ColumbusGA",
    "Decatur",
    "Alpharetta",
    "Statesboro",
    "Valdosta"
]

# Scrape posts from each subreddit
print("\n🚀 Starting to scrape posts...\n")

all_posts = {}  # Dictionary to store posts by subreddit

for subreddit in subreddits:
    print(f"--- 📌 {subreddit} ---")
    url = f'https://www.reddit.com/r/{subreddit}/new.json'
    
    try:
        # Use User-Agent only — no authentication needed for public posts
        headers = {'User-Agent': USER_AGENT}
        res = requests.get(url, headers=headers, params={'limit': 100})
        
        # Debug: Print status and raw response
        print(f"  Status Code: {res.status_code}")
        if res.status_code != 200:
            print(f"  ❌ Error: {res.text}")
            continue  # Skip to next subreddit
        
        # Parse JSON response
        data = res.json()
        
        # Extract posts (children)
        if 'data' not in data or 'children' not in data['data']:
            print("  ❌ No 'data' or 'children' in response")
            continue
        
        posts = data['data']['children']
        print(f"  ✅ Found {len(posts)} posts")
        
        # Save posts to all_posts dictionary
        all_posts[subreddit] = posts
        
        # Print each post
        for i, post in enumerate(posts, 1):
            post_data = post['data']
            
            if post_data.get('score', 0) < 10:
                continue  # Skip posts with less than 10 upvotes
            
            title = post_data.get('title', 'No title')
            flair = post_data.get('link_flair_text', 'No flair')
            url = post_data.get('url', 'No URL')
            created_utc = post_data.get('created_utc', 'Unknown time')
            score = post_data.get('score', 0)
            
            print(f"  {i}. Title: {title}")
            print(f"     Flair: {flair}")
            print(f"     URL: {url}")
            print(f"     Created: {created_utc}")
            print(f"     Upvotes: {score}") 
            print("     ---")
            
    except Exception as e:
        print(f"  ❌ Unexpected error scraping {subreddit}: {e}")
        continue  # Skip to next subreddit

# Save all_posts to a JSON file
with open('scraped_posts.json', 'w') as f:
    json.dump(all_posts, f, indent=2)

print("\n✅ Scraping complete! Posts saved to 'scraped_posts.json'")