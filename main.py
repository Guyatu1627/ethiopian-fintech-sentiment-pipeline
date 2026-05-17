from scripts.data_loader import get_bank_reviews
from scripts.preprocessor import DataPreprocessor
from scripts.database_manager import DBManager
import os

BANKS = {'CBE': 'com.cbe.cbebirr', 'BOA': 'com.boamobile.android', 'Dashen': 'com.dashenbank.mobile'}


def run_pipeline():
    # ensure data directories
    os.makedirs('data/raw', exist_ok=True)

    # 1. Scrape (or generate fallback synthetic) and save raw
    raw_df = get_bank_reviews(BANKS)
    raw_path = os.path.join('data', 'raw', 'reviews_raw.csv')
    raw_df.to_csv(raw_path, index=False)
    print(f"Raw reviews saved to {raw_path}")

    # 2. Preprocess
    clean_df = DataPreprocessor.clean(raw_df)

    # 3. Save cleaned CSV (ignored by git)
    clean_path = os.path.join('data', 'cleaned_reviews.csv')
    clean_df.to_csv(clean_path, index=False)
    print(f"Cleaned reviews saved to {clean_path}")

    # 4. Save to DB (will error if PostgreSQL not configured)
    try:
        db = DBManager('postgres', 'YOUR_PASSWORD', 'localhost', '5432', 'bank_analytics')
        db.save(clean_df, 'reviews')
        print("Saved cleaned data to PostgreSQL database 'bank_analytics'.")
    except Exception as e:
        print(f"DB save skipped/failed: {e}")


if __name__ == "__main__":
    run_pipeline()