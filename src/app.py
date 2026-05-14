# main.py
from scripts.data_loader import ReviewScraper
from scripts.preprocessor import DataPreprocessor
from scripts.database_manager import DatabaseManager

# 1. Define your Targets
BANKS = {
    'CBE': 'com.cbe.cbebirr',
    'BOA': 'com.boamobile.android',
    'Dashen': 'com.dashenbank.mobile'
}

# 2. Scrape (Task 1.1)
scraper = ReviewScraper(BANKS)
raw_df = scraper.scrape_all()

# 3. Clean (Task 1.2)
preprocessor = DataPreprocessor()
clean_df = preprocessor.process(raw_df)

# 4. Store (Task 1.3)
# Replace with your actual pgAdmin credentials
DB_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/bank_analytics"
db_manager = DatabaseManager(DB_URL)
db_manager.save_to_db(clean_df)