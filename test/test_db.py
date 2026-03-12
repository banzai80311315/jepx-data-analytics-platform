import pandas as pd
from app.db import get_engine


def main():
    engine = get_engine()

    query = "SELECT * FROM areas ORDER BY area_id;"
    df = pd.read_sql(query, engine)

    print("DB接続成功")
    print(df)


if __name__ == "__main__":
    main()