import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import config

# --- NLTK Resource Downloader ---
def download_nltk_resources():
    """Checks for and downloads required NLTK resources."""
    resources = {
        'stopwords': 'corpora/stopwords',
        'punkt': 'tokenizers/punkt',
        'punkt_tab': 'tokenizers/punkt_tab'
    }
    for name, path in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            print(f"Downloading NLTK resource ({name})...")
            nltk.download(name, quiet=True)

download_nltk_resources()


def preprocess_text(text):
    """ Cleans and preprocesses a single piece of text. """
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^A-Za-z\s]+', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return " ".join(filtered_tokens)

def main():
    """ Main function to load, process, and save the data. """
    
    input_filepath = config.RAW_DATA_PATH
    output_filepath = config.CLEANED_DATA_PATH

    if not os.path.exists(input_filepath):
        print(f"Error: The file '{input_filepath}' was not found.")
        print("Please run the reddit_scraper.py script first.")
        return

    print(f"Loading data from {input_filepath}...")
    df = pd.read_csv(input_filepath)
    df['combined_text'] = df['title'].fillna('') + " " + df['text'].fillna('')

    print("Preprocessing text data... This may take a moment.")
    df['cleaned_text'] = df['combined_text'].apply(preprocess_text)

    df.to_csv(output_filepath, index=False)
    print(f"\nPreprocessing complete!")
    print(f"Cleaned data saved to {os.path.abspath(output_filepath)}")

    print("\n--- Data Preview ---")
    print("Original Text:\n", df['combined_text'].iloc[0])
    print("\nCleaned Text:\n", df['cleaned_text'].iloc[0])
    print("--------------------")

if __name__ == '__main__':
    main()

