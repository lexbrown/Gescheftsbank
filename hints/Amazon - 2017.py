import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

amazon = pd.read_csv("from/amzn.csv", index_col=0, parse_dates=True)["Adj Close"]
fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_ylabel("price")
amazon.plot(ax=ax, label="Amazon")
amazon.rolling(window=20).mean().plot(ax=ax, label="Rolling mean - 20")
amazon.rolling(window=10).mean().plot(ax=ax, label="Rolling mean - 10")
amazon.rolling(window=50).mean().plot(ax=ax, label="Rolling mean - 50")
ax.legend(loc="best")
ax.set_title("Amazon price and rolling mean", fontsize=25)
fig.savefig("amzn2.png")
