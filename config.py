import os

# --- Reddit Scraper Settings ---
TARGET_SUBREDDIT = "Apple"
POST_LIMIT = 2000
COMMENT_LIMIT_PER_POST = 10

# --- Directory Settings ---
# The main directory for all data files (CSVs)
DATA_DIR = 'data' + '_' + TARGET_SUBREDDIT

# The main directory for all output visualizations (PNGs)
VISUALIZATIONS_DIR = 'visualizations' + '_' + TARGET_SUBREDDIT


# --- Filename Settings ---
# Raw data fetched from Reddit
RAW_DATA_FILENAME = 'reddit_data.csv'

# Data after cleaning and preprocessing
CLEANED_DATA_FILENAME = 'reddit_data_cleaned.csv'

# Final data with sentiment scores and labels
SENTIMENT_DATA_FILENAME = 'reddit_data_with_sentiments.csv'

RAW_DATA_PATH = os.path.join(DATA_DIR, RAW_DATA_FILENAME)
CLEANED_DATA_PATH = os.path.join(DATA_DIR, CLEANED_DATA_FILENAME)
SENTIMENT_DATA_PATH = os.path.join(DATA_DIR, SENTIMENT_DATA_FILENAME)
