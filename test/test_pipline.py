import pandas as pd
import matplotlib.pyplot as plt

PATH = "../data/raw/spot_summary2023.csv"

# CSV読み込み
df = pd.read_csv(PATH)

print("rows:", len(df))
print("columns:", df.columns.tolist())

# 簡単な処理（例：平均値）
numeric_cols = df.select_dtypes(include="number").columns
if len(numeric_cols) > 0:
    col = numeric_cols[0]
    mean_val = df[col].mean()
    print(f"mean({col}) =", mean_val)

    # 簡単なプロット
    df[col].head(200).plot(title=f"{col} (first 200 rows)")
    plt.show()
else:
    print("numeric column not found")