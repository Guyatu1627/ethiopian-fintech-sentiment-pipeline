import pandas as pd
import re

class DataPreprocessor:
    @staticmethod
    def process(df):
        """Standardized cleaning pipeline for financial reviews."""
        if df.empty:
            return df
        
        # 1. Deduplication based on unique Review ID
        df = df.drop_duplicates(subset=['reviewId'])
        
        # 2. Handling Missing Values (Critical for NLP)
        # We drop rows where the review 'content' is missing
        df = df.dropna(subset=['content'])
        
        # 3. Temporal Normalization (YYYY-MM-DD)
        df['at'] = pd.to_datetime(df['at'])
        df['date'] = df['at'].dt.strftime('%Y-%m-%d')
        
        # 4. Text Standardization
        # Lowercasing and removing noise (URLs, emojis, special chars)
        def clean_text(text):
            text = str(text).lower()
            text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
            return text.strip()
        
        df['content'] = df['content'].apply(clean_text)
        
        # 5. Requirement Alignment: Rename columns to match challenge doc
        df = df.rename(columns={'content': 'review', 'score': 'rating'})
        
        # Select only required columns
        required_cols = ['review', 'rating', 'date', 'bank', 'source']
        return df[required_cols]