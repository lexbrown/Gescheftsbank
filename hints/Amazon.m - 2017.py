import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''amazon = pd.read_csv("from/amzn.csv", index_col=0, parse_dates=True)["Adj Close"]
fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_ylabel("price")
amazon.plot(ax=ax, label="Amazon")
amazon.rolling(window=20).mean().plot(ax=ax, label="Rolling mean - 20")
#amazon.rolling(window=10).mean().plot(ax=ax, label="Rolling mean - 10")
#amazon.rolling(window=10).std().plot(ax=ax, label="std -10")
ax.legend(loc="best")
ax.set_title("Amazon price and rolling mean", fontsize=25)
#fig.savefig("amzn.png")'''

'''fig = plt.figure(figsize=(16, 8))
pisos = fig.add_subplot(1, 1, 1)
amazon = pd.read_csv("from/amzn.csv", index_col=0, parse_dates=True)["Adj Close"]
pfizer = pd.read_csv("from/pfe.csv", index_col=0, parse_dates=True)["Adj Close"]
pg = pd.read_csv("from/pg.csv", index_col=0, parse_dates=True)["Adj Close"]
all = pd.DataFrame(index=amazon.index)
all["amazon"] = pd.DataFrame(amazon)
all["pfizer"] = pd.DataFrame(pfizer)
all["pg"] = pd.DataFrame(pg)
all_std = all.rolling(window=20).std()
all_std.plot(ax=pisos, logy = True)
pisos.set_title("Logarithmic std", fontsize=25)
#fig.savefig("std.png")'''

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(1, 1, 1)
amazon = pd.read_csv("from/amzn.csv", index_col=0, parse_dates=True)["Adj Close"]
amazon.rolling(window=40).mean().plot(ax=ax, label="Rolling mean")
amazon.ewm(span=40).mean().plot(ax=ax, label="Exp mean",
linestyle="--", color="red")
amazon.plot(ax=ax, label="Amazon price")
ax.legend(loc="best")
ax.set_title("Exponentially weighted functions", fontsize=25)
fig.savefig("meanhz.png")