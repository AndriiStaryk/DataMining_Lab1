import pandas as pd
from textblob import TextBlob
import os
import config

def get_sentiment_polarity(text):
    """ Analyzes the text and returns its polarity score. """
    if not isinstance(text, str) or not text.strip():
        return 0.0
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def classify_sentiment(polarity):
    """ Classifies the polarity score into 'Positive', 'Negative', or 'Neutral'. """
    if polarity > 0.05:
        return 'Positive'
    elif polarity < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def main():
    """ Main function to load cleaned data, perform sentiment analysis, and save the results. """
    
    input_filepath = config.CLEANED_DATA_PATH
    output_filepath = config.SENTIMENT_DATA_PATH

    if not os.path.exists(input_filepath):
        print(f"Error: The file '{input_filepath}' was not found.")
        print("Please run the data_preprocessor.py script first.")
        return

    print(f"Loading cleaned data from {input_filepath}...")
    df = pd.read_csv(input_filepath)
    
    if 'cleaned_text' not in df.columns:
        print("Error: 'cleaned_text' column not found. Please ensure the preprocessing script ran correctly.")
        return
        
    df.dropna(subset=['cleaned_text'], inplace=True)

    print("Analyzing sentiment... This might take a moment.")
    df['sentiment_score'] = df['cleaned_text'].apply(get_sentiment_polarity)
    df['sentiment_label'] = df['sentiment_score'].apply(classify_sentiment)

    df.to_csv(output_filepath, index=False)
    print(f"\nSentiment analysis complete!")
    print(f"Data with sentiment scores saved to {os.path.abspath(output_filepath)}")

    print("\n--- Analysis Preview ---")
    print(df[['cleaned_text', 'sentiment_score', 'sentiment_label']].head())
    print("------------------------")
    
    print("\n--- Sentiment Distribution ---")
    print(df['sentiment_label'].value_counts())
    print("------------------------------")

if __name__ == '__main__':
    main()

