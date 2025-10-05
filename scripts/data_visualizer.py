import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
import config 


def create_sentiment_distribution_plots(df):
    """Generates and saves a bar and pie chart for sentiment distribution."""
    print("Generating sentiment distribution plots...")
    sns.set_theme(style="whitegrid")
    sentiment_counts = df['sentiment_label'].value_counts()
    
    # Bar Chart
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis")
    plt.title('Sentiment Distribution of r/Apple Posts', fontsize=16)
    plt.xlabel('Sentiment', fontsize=12)
    plt.ylabel('Number of Posts', fontsize=12)
    plt.xticks(fontsize=11)
    bar_chart_path = os.path.join(config.VISUALIZATIONS_DIR, 'sentiment_distribution_bar.png')
    plt.savefig(bar_chart_path, dpi=300)
    print(f"  - Bar chart saved to {os.path.abspath(bar_chart_path)}")
    plt.close()

    # Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
            startangle=140, colors=sns.color_palette("viridis", len(sentiment_counts)))
    plt.title('Sentiment Distribution of r/Apple Posts', fontsize=16)
    plt.ylabel('')
    pie_chart_path = os.path.join(config.VISUALIZATIONS_DIR, 'sentiment_distribution_pie.png')
    plt.savefig(pie_chart_path, dpi=300) # Added dpi for higher quality
    print(f"  - Pie chart saved to {os.path.abspath(pie_chart_path)}")
    plt.close()

def create_word_clouds(df):
    """Generates and saves high-resolution (4K) word clouds."""
    print("Generating high-resolution word clouds (4K)...")

    # Positive Word Cloud
    positive_text = " ".join(text for text in df[df['sentiment_label'] == 'Positive']['cleaned_text'])
    if positive_text:
        # Increased width and height for 4K resolution
        wordcloud_positive = WordCloud(width=3840, height=2160, background_color='white').generate(positive_text)
        plt.figure(figsize=(16, 9)) # Aspect ratio for 4K
        plt.imshow(wordcloud_positive, interpolation='bilinear')
        plt.axis("off")
        plt.title('Most Common Words in Positive Posts (4K)', fontsize=20)
        positive_wc_path = os.path.join(config.VISUALIZATIONS_DIR, 'wordcloud_positive_4k.png')
        plt.savefig(positive_wc_path, dpi=300, bbox_inches='tight') # High DPI and tight layout
        print(f"  - Positive word cloud saved to {os.path.abspath(positive_wc_path)}")
        plt.close()
    else:
        print("  - No positive text found to generate a word cloud.")

    # Negative Word Cloud
    negative_text = " ".join(text for text in df[df['sentiment_label'] == 'Negative']['cleaned_text'])
    if negative_text:
        # Increased width and height for 4K resolution
        wordcloud_negative = WordCloud(width=3840, height=2160, background_color='black', colormap='Reds').generate(negative_text)
        plt.figure(figsize=(16, 9)) # Aspect ratio for 4K
        plt.imshow(wordcloud_negative, interpolation='bilinear')
        plt.axis("off")
        plt.title('Most Common Words in Negative Posts (4K)', fontsize=20)
        negative_wc_path = os.path.join(config.VISUALIZATIONS_DIR, 'wordcloud_negative_4k.png')
        plt.savefig(negative_wc_path, dpi=300, bbox_inches='tight') # High DPI and tight layout
        print(f"  - Negative word cloud saved to {os.path.abspath(negative_wc_path)}")
        plt.close()
    else:
        print("  - No negative text found to generate a word cloud.")

def main():
    """Main function to load data and generate all visualizations."""
    os.makedirs(config.VISUALIZATIONS_DIR, exist_ok=True)
    input_filepath = config.SENTIMENT_DATA_PATH
    
    if not os.path.exists(input_filepath):
        print(f"Error: The file '{input_filepath}' was not found.")
        print("Please run the previous scripts in order: scraper -> preprocessor -> analyzer.")
        return

    print(f"Loading data from {input_filepath}...")
    df = pd.read_csv(input_filepath)
    df['cleaned_text'] = df['cleaned_text'].astype(str)

    create_sentiment_distribution_plots(df)
    create_word_clouds(df)

    print("\nVisualization complete!")
    print(f"All plots have been saved in the '{config.VISUALIZATIONS_DIR}' directory.")

if __name__ == '__main__':
    main()