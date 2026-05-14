from google_play_scraper import Sort, reviews_all
import pandas as pd

def scrape_bank_data(bank_dict):
    """
    bank_dict: {'CBE': 'com.cbe.cbebirr', ...}
    """
    all_reviews = []
    for bank_name, app_id in bank_dict.items():
        # Using reviews_all to ensure we get 400+ per bank
        result = reviews_all(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST
        )
        df = pd.DataFrame(result)
        df['bank'] = bank_name
        all_reviews.append(df)
    
    return pd.concat(all_reviews, ignore_index=True)