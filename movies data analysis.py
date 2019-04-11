import pandas as pd
import os
import matplotlib.pyplot as plt

data = pd.read_csv("movies.csv")

print(data)

print(data.columns)

print(data.length.mean())
print(data["length"].mean())

print(data.rating.median())
print(data["rating"].median())

data.mpaa = data.mpaa.apply(lambda x : x.strip())
data_mpaa = data[data.mpaa == "PG"].mpaa.count()
print(data_mpaa)

data_mpaa_count = data.mpaa[data.mpaa != ""].value_counts().sort_values()
print(data_mpaa_count)

data_mpaa_count.plot(kind = "bar", rot = 0)
plt.show()

print()
action_budget = data.budget[(data.Action == 1) & (data.budget > 0)].mean()
print(action_budget)

data["CostPerMinute"] = data.budget / data.length
data_subset = data[data.Short == 0].sort_values(by = "CostPerMinute", ascending =  False).CostPerMinute.iloc[0]

print(data_subset)