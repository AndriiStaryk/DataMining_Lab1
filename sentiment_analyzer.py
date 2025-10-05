import pandas as pd
from textblob import TextBlob
import os

def get_sentiment_polarity(text):
    """
    Analyzes the text and returns its polarity score.
    Polarity is a float within the range [-1.0, 1.0].
    """
    if not isinstance(text, str) or not text.strip():
        return 0.0  # Return neutral for empty or non-string text
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def classify_sentiment(polarity):
    """
    Classifies the polarity score into 'Positive', 'Negative', or 'Neutral'.
    """
    # We'll use a small threshold to classify neutral more accurately.
    # Scores very close to 0 are likely neutral.
    if polarity > 0.05:
        return 'Positive'
    elif polarity < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def main():
    """
    Main function to load cleaned data, perform sentiment analysis, and save the results.
    """
    input_filename = 'reddit_data_cleaned.csv'
    output_filename = 'reddit_data_with_sentiments.csv'

    if not os.path.exists(input_filename):
        print(f"Error: The file '{input_filename}' was not found.")
        print("Please run the data_preprocessor.py script first.")
        return

    print(f"Loading cleaned data from {input_filename}...")
    df = pd.read_csv(input_filename)
    
    # Ensure the cleaned_text column exists
    if 'cleaned_text' not in df.columns:
        print("Error: 'cleaned_text' column not found. Please ensure the preprocessing script ran correctly.")
        return
        
    # Drop rows where cleaned_text might be empty after processing
    df.dropna(subset=['cleaned_text'], inplace=True)

    print("Analyzing sentiment... This might take a moment.")
    # 1. Calculate the polarity score for each post
    df['sentiment_score'] = df['cleaned_text'].apply(get_sentiment_polarity)

    # 2. Classify the score into a human-readable label
    df['sentiment_label'] = df['sentiment_score'].apply(classify_sentiment)

    # Save the final data with sentiment analysis
    df.to_csv(output_filename, index=False)
    print(f"\nSentiment analysis complete!")
    print(f"Data with sentiment scores saved to {os.path.abspath(output_filename)}")

    # Show a preview of the new columns
    print("\n--- Analysis Preview ---")
    print(df[['cleaned_text', 'sentiment_score', 'sentiment_label']].head())
    print("------------------------")
    
    # Show a summary of the results
    print("\n--- Sentiment Distribution ---")
    print(df['sentiment_label'].value_counts())
    print("------------------------------")


if __name__ == '__main__':
    main()
