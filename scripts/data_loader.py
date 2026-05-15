from google_play_scraper import Sort, reviews_all
import pandas as pd

def get_bank_reviews(bank_dict):
    all_data = []
    for name, app_id in bank_dict.items():
        print(f"Scraping {name}...")
        results = reviews_all(app_id, lang='en', country='us', sort=Sort.NEWEST)
        df = pd.DataFrame(results)
        df['bank'] = name
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)