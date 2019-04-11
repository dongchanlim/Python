import pandas as pd
import matplotlib
import seaborn as sns
import numpy as np

players = pd.read_csv("nba_basketball_data/basketball_players.csv")

master = pd.read_csv("nba_basketball_data/basketball_master.csv")

data = pd.merge(players, master, how = "left", left_on = "playerID", right_on = "bioID")

print(data)

print(data.columns)


# part 1

# part 1-1: Calculate the mean and median number of points scored

points_mean = data.points.mean()

print("The mean number of points scored: {}".format(points_mean))

print()

points_median = data.points.median()

print("The median number of points scored: {}".format(points_mean))

print()

# part 1-2: Determine the highest number of points recorded in a single season.
# Identify who scored those points and the year they did so.

highest_points = data.points.max()

print("The highest number of points: {}".format(highest_points))

print()

highest_points_year = data[data.points == highest_points][["points","year","firstName","middleName","lastName","nameSuffix"]]

print("The year of highest number of points: \n {}".format(highest_points_year))
print()

# part 1-3: Produce a boxplot that shows the distribution of total points, total assists, and total rebounds

data["total_points"] = data.points + data.PostPoints
data["total_assists"] = data.assists + data.PostAssists
data["total_rebounds"] = data.rebounds + data.PostRebounds

data[["total_points","total_assists","total_rebounds"]].plot(kind = "box")

matplotlib.pyplot.show()

# part 1-4: Produce a plot that shows how the number of points scored has changed over time
# by showing the median of points scored per year, over time.

year_points = data[["year","points"]].groupby("year").median()
year_points.plot(kind ="line")
matplotlib.pyplot.show()

# part 2
# part 2-1: are there some that are much more efficient (points per attempt) than others?
data["PointsPerAttempt"] = data.points / (data.fgAttempted + data.ftAttempted)

player_points_attempted = data[["playerID","PointsPerAttempt"]].groupby("playerID").mean()
player_points_attempted = player_points_attempted[player_points_attempted.PointsPerAttempt != np.inf]
print(player_points_attempted)

top10_points_player = player_points_attempted.nlargest(10,"PointsPerAttempt")["PointsPerAttempt"]
print(top10_points_player)

pd.merge(top10_points_player, master, how = "left", left_on = "playerID", right_on = "bioID")[["firstName","middleName","lastName","nameSuffix","PointsPerAttempt"]]

# part 2-2: Are there any players that are exceptional across many categories?
statistical_category = ["points","rebounds","assists","steals","blocks","turnovers"]
exceptional_player = data[statistical_category + ["playerID"]].groupby("playerID").mean().nlargest(10, statistical_category)

for i in statistical_category:
    exceptional_player[i+ "Rank"] = exceptional_player[i].rank(ascending = True, pct =  True)

print(exceptional_player[exceptional_player.columns[-6:]])

pd.merge(exceptional_player[exceptional_player.columns[-6:]], master, how = "left", left_on = "playerID", right_on = "bioID")[["firstName","middleName","lastName","nameSuffix"]]

exceptional_player[exceptional_player.columns[-6:]].plot(kind = "bar")
matplotlib.pyplot.show()

# part 2-3: do you see a trend of more three-point shots either across the league or among certain groups of players?
# Is there a point at which popularity increased dramatically?

data["total_threeAttempted"] = data.threeAttempted + data.PostthreeAttempted
data["total_threeMade"] = data.threeMade + data.PostthreeMade

three_data_per_year = data.groupby(["lgID","year"]).mean().reset_index()[["lgID","year","total_threeAttempted","total_threeMade"]]
three_data_per_year = three_data_per_year[(three_data_per_year.total_threeAttempted > 0) & (three_data_per_year.total_threeMade > 0)]
three_data_per_year = three_data_per_year.melt(["lgID","year"])

print(three_data_per_year)

grid = sns.FacetGrid(three_data_per_year, col = "lgID", hue= "variable")

grid.map(sns.lineplot, "year", "value").add_legend()

matplotlib.pyplot.show()



plot = sns.lineplot(x = "year", y = "total_threeAttempted", data = data)
plot2 = sns.lineplot(x = "year", y = "total_threeMade", data = data)

matplotlib.pyplot.legend(['threeAttempted','threeMade'])
matplotlib.pyplot.show()


# part 3
# part 3-1: which player is the GOAT (the Greatest Of All Time) ?
stats = ["points","rebounds","assists","steals","blocks","turnovers"]
player_stat = data[["playerID"] + stats].groupby("playerID").mean()

for i in stats:
    player_stat[i+ "Rank"] = player_stat[i].rank(ascending = True, pct =  True)
    
print(player_stat)

player_stat_rank = player_stat.iloc[:,[x for x in range(6,12)]]
player_stat_rank_goat = player_stat_rank * [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
player_stat_rank_goat["GOAT_score"] = player_stat_rank_goat.sum(axis = 1)
top_10_goat = player_stat_rank_goat.nlargest(10,"GOAT_score")

print(player_stat_rank)
top_10_goat = pd.merge(top_10_goat["GOAT_score"],master, how = "inner", left_on = "playerID", right_on = "bioID")[["firstName","middleName","lastName","nameSuffix","GOAT_score"]]
print(top_10_goat)
sns.barplot(x = "firstName", y = "GOAT_score", data = top_10_goat)

matplotlib.pyplot.ylim(0.9, 1)
matplotlib.pyplot.show()

# part 3-2 : Can you find anything interesting about players who came from a similar location?
print(master.columns)

location_group_height = master.groupby(["birthState"]).mean()["height"].sort_values(ascending = False).nlargest(10)
location_group_weight = master.groupby(["birthState"]).mean()["weight"].sort_values(ascending = False).nlargest(10)
print(location_group_height)
print(location_group_weight)

location_group_height.plot(kind = 'barh', x = "birthState", y = "height")

matplotlib.pyplot.show()

location_group_weight.plot(kind = 'barh', x = "birthState", y = "weight")

matplotlib.pyplot.show()

# part 3-3 : Find something else in this dataset that you consider interesting. Produce a graph to communicate your insight.

# The correlation between weight and height per position
data_r = data[["pos","height","weight"]].replace([np.inf, -np.inf], np.nan).dropna()

grid = sns.FacetGrid(data_r[data_r.height > 0][data_r.weight > 0], col = "pos")
grid.map(sns.scatterplot, "height", "weight").add_legend()
matplotlib.pyplot.show()

# how much height have been changed over years per position
data_r2 = data[["pos","year","height","weight"]].replace([np.inf, -np.inf], np.nan).dropna()[data.height > 0][data.weight > 0]

sns.lineplot(x = "year", y = "height", data = data_r2, hue = "pos")
matplotlib.pyplot.show()