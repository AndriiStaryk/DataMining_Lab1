import praw
import pandas as pd
import os
from dotenv import load_dotenv

def fetch_reddit_data(client_id, client_secret, user_agent, subreddit_name, limit=100):
    """
    Fetches data from a specified subreddit and saves it to a CSV file.

    Args:
        client_id (str): Your Reddit API client ID.
        client_secret (str): Your Reddit API client secret.
        user_agent (str): Your Reddit API user agent.
        subreddit_name (str): The name of the subreddit to scrape.
        limit (int): The number of posts to fetch.
    """
    # Authenticate with the Reddit API
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        # Verify that the connection is read-only
        print(f"Read-only connection: {reddit.read_only}")
    except Exception as e:
        print(f"Error authenticating with Reddit: {e}")
        return

    print(f"Fetching top {limit} posts from r/{subreddit_name}...")
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    # Fetch the top posts from the subreddit
    try:
        for post in subreddit.top(limit=limit):
            posts_data.append([
                post.id,
                post.title,
                post.score,
                post.selftext,
                post.created_utc,
                post.url
            ])
    except Exception as e:
        print(f"An error occurred while fetching posts: {e}")
        return

    # Create a pandas DataFrame
    df = pd.DataFrame(posts_data, columns=[
        'id', 'title', 'score', 'text', 'created_utc', 'url'
    ])

    # Save the DataFrame to a CSV file
    output_filename = 'reddit_data.csv'
    df.to_csv(output_filename, index=False)
    print(f"\nSuccessfully fetched {len(posts_data)} posts.")
    print(f"Data saved to {os.path.abspath(output_filename)}")


if __name__ == '__main__':

    load_dotenv()
    
    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    USER_AGENT = os.getenv("REDDIT_USER_AGENT")

    # The subreddit you want to analyze
    TARGET_SUBREDDIT = "Apple" 

    if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! Missing API credentials. Please create a .env file and add them. !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        fetch_reddit_data(CLIENT_ID, CLIENT_SECRET, USER_AGENT, TARGET_SUBREDDIT)
