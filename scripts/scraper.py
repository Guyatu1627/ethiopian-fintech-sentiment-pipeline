import pandas as pd
from google_play_scraper import Sort, reviews_all
import os

class ReviewScraper:
    def __init__(self, app_id, app_name):
        self.app_id = app_id
        self.app_name = app_name

    def scrape_reviews(self, count=500):
        """Scrapes reviews and returns a DataFrame."""
        try:
            print(f"Fetching reviews for {self.app_name}...")
            result = reviews_all(
                self.app_id,
                sleep_milliseconds=0, # Faster scraping
                lang='en',
                country='us', #Best for English reviews
                sort=Sort.NEWEST
            )
            df =pd.DataFrame(result)
            df['bank'] = self.app_name # Add label for identification
            return df
        except Exception as e:
            print(f"Error scrapting {self.app_name}: {e}")
            return None
        