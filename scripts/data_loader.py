import pandas as pd
from google_play_scraper import Sort, reviews_all
import logging

# Configure logging to track progress/errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReviewScraper:
    def __init__(self, banks):
        """
        banks: dict of {bank_name: app_id}
        Example: {'CBE': 'com.cbe.cbebirr'}
        """
        self.banks = banks

    def scrape_all(self):
        all_data = []
        for bank_name, app_id in self.banks.items():
            try:
                logging.info(f"Starting scrape for {bank_name}...")
                reviews = reviews_all(
                    app_id,
                    lang='en', 
                    country='us', # Ensures English reviews for NLP tasks
                    sort=Sort.NEWEST
                )
                df = pd.DataFrame(reviews)
                df['bank'] = bank_name
                df['source'] = 'Google Play Store'
                all_data.append(df)
                logging.info(f"Successfully scraped {len(df)} reviews for {bank_name}.")
            except Exception as e:
                logging.error(f"Failed to scrape {bank_name}: {str(e)}")
        
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()