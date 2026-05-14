import logging
from sqlalchemy import create_engine
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, db_url):
        """
        Initializes the connection engine.
        Example URL: postgresql://postgres:password@localhost:5432/bank_analytics
        """
        self.db_url = db_url
        self.engine = create_engine(self.db_url)

    def save_to_db(self, df, table_name='bank_reviews'):
        """Saves a DataFrame to PostgreSQL."""
        try:
            if df.empty:
                logging.warning("DataFrame is empty. Skipping database migration.")
                return
            
            # We use 'replace' for the first run, but 'append' is better for ongoing scrapes
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            logging.info(f"Successfully migrated {len(df)} rows to table '{table_name}'.")
        except Exception as e:
            logging.error(f"Failed to migrate data to PostgreSQL: {e}")