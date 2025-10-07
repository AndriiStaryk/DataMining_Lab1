import scripts.reddit_scraper as reddit_scraper
import scripts.data_preprocessor as data_preprocessor
import scripts.sentiment_analyzer as sentiment_analyzer
import scripts.data_visualizer as data_visualizer
import os
import config

def run_pipeline():
    """
    Runs the complete data analysis pipeline from data collection to visualization.
    """
    print("="*50)
    print("🚀 STARTING SENTIMENT ANALYSIS PIPELINE 🚀")
    print("="*50)

    # --- Step 1: Scrape data from Reddit ---
    print("\n[Step 1/4] Running Reddit Scraper...")
    try:
        reddit_scraper.main()
        print("[SUCCESS] Data scraping complete.")
    except Exception as e:
        print(f"[ERROR] Reddit scraper failed: {e}")
        return # Stop the pipeline if this step fails

    # --- Step 2: Preprocess the raw data ---
    print("\n[Step 2/4] Running Data Preprocessor...")
    try:
        data_preprocessor.main()
        print("[SUCCESS] Data preprocessing complete.")
    except Exception as e:
        print(f"[ERROR] Data preprocessor failed: {e}")
        return

    # --- Step 3: Analyze sentiment ---
    print("\n[Step 3/4] Running Sentiment Analyzer...")
    try:
        sentiment_analyzer.main()
        print("[SUCCESS] Sentiment analysis complete.")
    except Exception as e:
        print(f"[ERROR] Sentiment analyzer failed: {e}")
        return

    # --- Step 4: Generate visualizations ---
    print("\n[Step 4/4] Running Visualizer...")
    try:
        data_visualizer.main()
        print("[SUCCESS] Visualization generation complete.")
    except Exception as e:
        print(f"[ERROR] Visualizer failed: {e}")
        return

    print("\n" + "="*50)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY! ✅")
    print("="*50)

if __name__ == '__main__':
    # Ensure data and visualizations directories exist
    # This is a good practice to ensure the directories are ready before the pipeline starts.
    if not os.path.exists(config.DATA_DIR):
        os.makedirs(config.DATA_DIR)
    if not os.path.exists(config.VISUALIZATIONS_DIR):
        os.makedirs(config.VISUALIZATIONS_DIR)
        
    run_pipeline()