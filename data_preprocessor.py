import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# --- One-time setup for NLTK ---
# You only need to run these download commands once.
# They download the necessary resources for tokenization and stop words.
try:
    stopwords.words('english')
except LookupError:
    print("Downloading NLTK resources (stopwords)...")
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK resources (punkt)...")
    nltk.download('punkt')
# Added this to fix the LookupError based on the traceback
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading NLTK resources (punkt_tab)...")
    nltk.download('punkt_tab')
# --- End of NLTK setup ---

def preprocess_text(text):
    """
    Cleans and preprocesses a single piece of text.
    - Removes URLs
    - Removes non-alphanumeric characters
    - Converts to lowercase
    - Tokenizes the text
    - Removes stop words
    """
    if not isinstance(text, str):
        return ""

    # 1. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # 2. Remove mentions and hashtags (less common on Reddit but good practice)
    text = re.sub(r'\@\w+|\#', '', text)
    # 3. Remove non-alphanumeric characters (and keep spaces)
    text = re.sub(r'[^A-Za-z\s]+', '', text)
    # 4. Convert to lowercase
    text = text.lower()
    # 5. Tokenize the text (split into words)
    tokens = word_tokenize(text)
    # 6. Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return " ".join(filtered_tokens)


def main():
    """
    Main function to load, process, and save the data.
    """
    input_filename = 'reddit_data.csv'
    output_filename = 'reddit_data_cleaned.csv'

    if not os.path.exists(input_filename):
        print(f"Error: The file '{input_filename}' was not found.")
        print("Please run the reddit_scraper.py script first.")
        return

    print(f"Loading data from {input_filename}...")
    df = pd.read_csv(input_filename)

    # Combine 'title' and 'text' for a complete analysis
    # Use .fillna('') to handle posts that might not have body text
    df['combined_text'] = df['title'].fillna('') + " " + df['text'].fillna('')

    print("Preprocessing text data... This may take a moment.")
    # Apply the cleaning function to our combined text
    df['cleaned_text'] = df['combined_text'].apply(preprocess_text)

    # Save the processed data
    df.to_csv(output_filename, index=False)
    print(f"\nPreprocessing complete!")
    print(f"Cleaned data saved to {os.path.abspath(output_filename)}")

    # Show a preview of the changes
    print("\n--- Data Preview ---")
    print("Original Text:\n", df['combined_text'].iloc[0])
    print("\nCleaned Text:\n", df['cleaned_text'].iloc[0])
    print("--------------------")


if __name__ == '__main__':
    main()

