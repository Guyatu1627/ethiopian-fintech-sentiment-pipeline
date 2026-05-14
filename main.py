from scripts.data_loader import scrape_bank_data
from scripts.preprocessor import DataPreprocessor
import os

# Configuration
BANKS = {
    'CBE': 'com.cbe.cbebirr',
    'BOA': 'com.boamobile.android',
    'Dashen': 'com.dashenbank.mobile'
}

def run_task_1():
    # 1. Scrape
    print("Step 1: Scraping 400+ reviews per bank...")
    raw_data = scrape_bank_data(BANKS)
    
    # 2. Preprocess
    print("Step 2: Preprocessing data...")
    processor = DataPreprocessor()
    clean_data = processor.process(raw_data)
    
    # 3. Save to CSV (Note: data/ is ignored by git)
    if not os.path.exists('data'):
        os.makedirs('data')
        
    output_path = 'data/cleaned_reviews.csv'
    clean_data.to_csv(output_path, index=False)
    print(f"Task 1 Complete. Dataset saved to {output_path}")
    print(f"Total reviews collected: {len(clean_data)}")

if __name__ == "__main__":
    run_task_1()