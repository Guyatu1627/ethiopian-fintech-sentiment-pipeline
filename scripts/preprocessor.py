import pandas as pd
import logging

class DataPreprocessor:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def process(self, df):
        """
        Cleans the raw scraped data into an analysis-ready format.
        """
        initial_count = len(df)
        
        # 3a. Remove duplicate reviews based on ID (if ID was collected)
        # If scraper doesn't provide 'at' or 'reviewId', use 'content' and 'at'
        if 'reviewId' in df.columns:
            df = df.drop_duplicates(subset=['reviewId'])
        
        # 3b. Handle missing values
        # Drop rows missing review text (content) or rating (score)
        df = df.dropna(subset=['content', 'score'])
        missing_count = initial_count - len(df)
        self.logger.info(f"Dropped {missing_count} rows due to missing data/duplicates.")

        # 3c. Normalize dates to YYYY-MM-DD
        df['at'] = pd.to_datetime(df['at'])
        df['date'] = df['at'].dt.strftime('%Y-%m-%d')

        # 3d. Rename and select columns to match the 5 required: 
        # [review, rating, date, bank, source]
        df = df.rename(columns={
            'content': 'review',
            'score': 'rating'
        })
        
        # Ensure source column exists
        df['source'] = 'Google Play'
        
        final_df = df[['review', 'rating', 'date', 'bank', 'source']]
        
        return final_df