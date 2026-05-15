from scripts.data_loader import get_bank_reviews
from scripts.preprocessor import DataPreprocessor
from scripts.database_manager import DBManager

BANKS = {'CBE': 'com.cbe.cbebirr', 'BOA': 'com.boamobile.android', 'Dashen': 'com.dashenbank.mobile'}

def run_pipeline():
    # 1. Scrape
    raw_df = get_bank_reviews(BANKS)
    # 2. Preprocess
    clean_df = DataPreprocessor.clean(raw_df)
    # 3. Save locally (Ignored by Git)
    clean_df.to_csv('data/cleaned_reviews.csv', index=False)
    # 4. Save to DB
    db = DBManager('postgres', 'YOUR_PASSWORD', 'localhost', '5432', 'bank_analytics')
    db.save(clean_df, 'reviews')

if __name__ == "__main__":
    run_pipeline()