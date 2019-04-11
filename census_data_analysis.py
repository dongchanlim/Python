import pandas
import matplotlib.pyplot

data = pandas.read_csv("census.csv", header=None)

print(data)

maximum = data[0].max()
print(maximum)


data.columns = ["age","workclass","fnlwgt","education","education-num","marital-status","occupation","relationship",
                "race","sex","capital-gain","capital-loss","hours-per-week","native-country",">50K, <=50K"]

print(data)

median_age = data.age.median()

print(median_age)

sex_count = data.sex.value_counts()

print(sex_count)

country_count = data.groupby("native-country").age.mean().sort_values(ascending = False)
print(country_count)

country_count.plot(kind = "bar")

matplotlib.pyplot.show()

print(data.columns)

