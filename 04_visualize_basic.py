import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("news_clean.csv", encoding="utf-8-sig")

# 1) 카테고리별 조회수 합계 막대그래프
by_cat = df.groupby("category")["views"].sum().sort_values(ascending=False)

plt.figure()
by_cat.plot(kind="bar")
plt.title("Category Views Sum")
plt.xlabel("category")
plt.ylabel("views_sum")
plt.tight_layout()
plt.show()

# 2) 조회수 분포 히스토그램
plt.figure()
df["views"].plot(kind="hist", bins=10)
plt.title("Views Distribution")
plt.xlabel("views")
plt.ylabel("count")
plt.tight_layout()
plt.show()
