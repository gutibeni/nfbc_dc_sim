# Import necessary libraries
import pandas as pd
from pybaseball import batting_stats, pitching_stats, fielding_stats

# Define the categories and positions for analysis
batting_categories = ["HR", "RBI", "R", "SB", "AVG"]
pitching_categories = ["W", "SV", "SO", "ERA", "WHIP"]

# Retrieve data using pybaseball for given range
start_year = 2022
end_year = 2024
batting_data = pd.concat([batting_stats(year) for year in range(start_year, end_year + 1)])
pitching_data = pd.concat([pitching_stats(year) for year in range(start_year, end_year + 1)])
fielding_data = pd.concat([fielding_stats(year) for year in range(start_year, end_year + 1)])


# Filter pitching data to include relevant stats
pitching_data = pitching_data[["Season", "Name", "W", "SV", "SO", "ERA", "WHIP"]]

# Calculate variability factors for batters and pitchers
variability_factors = {}

# Batting variability
batting_variability = {}
for category in batting_categories:
    if category in batting_data.columns:
        mean = batting_data[category].mean()
        std_dev = batting_data[category].std()
        variability_factor = std_dev / mean if mean != 0 else 0
        batting_variability[category] = variability_factor
variability_factors["Batters"] = batting_variability

# Pitching variability
pitching_variability = {}
for category in pitching_categories:
    if category in pitching_data.columns:
        mean = pitching_data[category].mean()
        std_dev = pitching_data[category].std()
        variability_factor = std_dev / mean if mean != 0 else 0
        pitching_variability[category] = variability_factor
variability_factors["Pitchers"] = pitching_variability

# Output the variability factors for the last 3 years
print(variability_factors)








