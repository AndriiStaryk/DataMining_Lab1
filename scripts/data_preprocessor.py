import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import os
import config # Import our new configuration file

def download_nltk_resources():
    """Downloads necessary NLTK resources if not already present."""
    try:
        # Check if resources are available, if not, download them
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading NLTK resources (stopwords)...")
        nltk.download('stopwords', quiet=True)
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK resources (punkt)...")
        nltk.download('punkt', quiet=True)

def preprocess_text(text):
    """
    Cleans and preprocesses a single string of text.
    - Removes URLs
    - Removes non-alphanumeric characters
    - Converts to lowercase
    - Tokenizes text
    - Removes stop words
    """
    if not isinstance(text, str):
        return ""
        
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user mentions and subreddit links
    text = re.sub(r'\@\w+|\/u\/\w+|\/r\/\w+', '', text)
    # Remove all non-alphanumeric characters (except spaces)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    return " ".join(filtered_tokens)

def main():
    """
    Main function to load raw data, preprocess it, and save the cleaned data.
    """
    download_nltk_resources()
    input_filepath = config.RAW_DATA_PATH
    output_filepath = config.CLEANED_DATA_PATH
    
    if not os.path.exists(input_filepath):
        print(f"Error: The file '{input_filepath}' was not found.")
        print("Please run the reddit_scraper.py script first.")
        return

    print(f"Loading data from {input_filepath}...")
    df = pd.read_csv(input_filepath)
    
    print("Preprocessing text data... This may take a moment.")
    # Combine title, post text, and comments into one field for analysis
    df['combined_text'] = df['title'].fillna('') + " " + df['text'].fillna('') + " " + df['comments'].fillna('')
    df['cleaned_text'] = df['combined_text'].apply(preprocess_text)
    
    # Save the cleaned data
    df.to_csv(output_filepath, index=False)
    print(f"Cleaned data saved to {os.path.abspath(output_filepath)}")

if __name__ == '__main__':
    main()


