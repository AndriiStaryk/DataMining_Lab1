import praw
import pandas as pd
from dotenv import load_dotenv
import os
import sys
import config # Import our new configuration file

def main():
    """
    Main function to fetch posts and their top comments from Reddit.
    """
    
    load_dotenv()
    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    
    if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
        print("Error: Reddit API credentials not found in .env file.")
        sys.exit(1)
    
    os.makedirs(config.DATA_DIR, exist_ok=True)
    output_filepath = config.RAW_DATA_PATH
    
    # --- Reddit API Connection ---
    try:
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT
        )
        print(f"Read-only connection: {reddit.read_only}")
    except Exception as e:
        print(f"Error connecting to Reddit API: {e}")
        sys.exit(1)

    # --- Data Fetching ---
    print(f"Fetching top {config.POST_LIMIT} posts and their top {config.COMMENT_LIMIT_PER_POST} comments from r/{config.TARGET_SUBREDDIT}...")
    posts_data = []
    try:
        subreddit = reddit.subreddit(config.TARGET_SUBREDDIT)
        for post in subreddit.hot(limit=config.POST_LIMIT):
            print(f"  Fetching post: '{post.title[:50]}...'")
            
            # Fetching top comments for the post
            all_comments_text = []
            if config.COMMENT_LIMIT_PER_POST > 0:
                try:
                    post.comments.replace_more(limit=0) # Flatten the comment tree
                    comment_count = 0
                    for comment in post.comments.list():
                        if comment_count >= config.COMMENT_LIMIT_PER_POST:
                            break
                        all_comments_text.append(comment.body)
                        comment_count += 1
                except Exception as e:
                    print(f"      - Could not fetch comments for post {post.id}: {e}")

            posts_data.append({
                "id": post.id,
                "title": post.title,
                "score": post.score,
                "num_comments": post.num_comments,
                "created_utc": post.created_utc,
                "url": post.url,
                "text": post.selftext,
                "comments": " ".join(all_comments_text)
            })
    except Exception as e:
        print(f"An error occurred while fetching posts: {e}")
        return

    if not posts_data:
        print("No posts were fetched.")
        return

    print(f"\nSuccessfully fetched data from {len(posts_data)} posts.")
    
    # --- Save to CSV ---
    df = pd.DataFrame(posts_data)
    df.to_csv(output_filepath, index=False)
    print(f"Data saved to {os.path.abspath(output_filepath)}")

if __name__ == '__main__':
    main()

