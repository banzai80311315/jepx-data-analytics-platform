from sqlalchemy import create_engine
from app.config import DB_CONFIG


def get_engine():
    user = DB_CONFIG["user"]
    password = DB_CONFIG["password"]
    host = DB_CONFIG["host"]
    port = DB_CONFIG["port"]
    database = DB_CONFIG["database"]

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    return engine