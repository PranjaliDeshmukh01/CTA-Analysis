import pandas as pd


def get_unique_stations():
    df = pd.read_csv("./app/datasets/Cleaned_CTA_Ridership_L_Daily_Total.csv")

    # Get unique station names
    unique_station_names = df["stationname"].unique()  # Returns an array of unique values

    # Convert to a list
    unique_station_names = unique_station_names.tolist()  # Convert numpy array to list

    return unique_station_names
