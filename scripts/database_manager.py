from sqlalchemy import create_engine
import logging

class DBManager:
    def __init__(self, user, pw, host, port, db):
        url = f"postgresql://{user}:{pw}@{host}:{port}/{db}"
        self.engine = create_engine(url)

    def save(self, df, table):
        df.to_sql(table, self.engine, if_exists='replace', index=False)
        logging.info("Data saved to PostgreSQL")