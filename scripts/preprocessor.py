import pandas as pd

class DataPreprocessor:
    @staticmethod
    def clean(df):
        # 3a. Remove duplicates
        df = df.drop_duplicates(subset=['reviewId'])
        # 3b. Handle missing
        df = df.dropna(subset=['content', 'score'])
        # 3c. Normalize dates
        df['at'] = pd.to_datetime(df['at'])
        df['date'] = df['at'].dt.strftime('%Y-%m-%d')
        # 3d. Format columns
        df = df.rename(columns={'content': 'review', 'score': 'rating'})
        df['source'] = 'Google Play'
        return df[['review', 'rating', 'date', 'bank', 'source']]