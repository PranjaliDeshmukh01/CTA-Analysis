import io

import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.sql.functions import (avg, col, month, split, sum, to_date, when,
                                   year)

from app.const import CACHE_DIR

memory = joblib.Memory(CACHE_DIR, verbose=0)

@memory.cache
def get_precipitation_vs_total_rides():
    spark = SparkSession.builder.appName("WeatherData").getOrCreate()

    weather_csv_path = "./app/datasets/Weather_data.csv"
    weather_df = (
        spark.read.option("header", "true")
        .csv(weather_csv_path)
    )

    csv_file_path = "./app/datasets/Cleaned_CTA_Ridership_L_Daily_Total.csv"

    cta_df = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(csv_file_path)
    )    
    weather_df = weather_df.withColumn("date", to_date(col("Date"), "yyyy-MM-DD"))
    cta_df = cta_df.withColumn("date", to_date(col("date"), "MM/dd/yyyy"))

    cta_grouped = cta_df.groupBy("date").agg(sum("rides").alias("total_rides"))
    df = weather_df.join(cta_grouped, on="date", how="inner")
    joined_pd = df.select("date", "PRCP (Inches)", "total_rides").orderBy("PRCP (Inches)").toPandas()

    plt.switch_backend("Agg")

    # scatter plot
    # plt.figure(figsize=(12, 6))
    # plt.yscale("log")
    # sns.scatterplot(x="PRCP (Inches)", y="total_rides", data=joined_pd, marker="o")
    # plt.title("Precipitation vs. Total Rides")
    # plt.xlabel("Precipitation (Inches)")
    # plt.ylabel("Total Rides")
    # plt.tight_layout()

    plt.figure(figsize=(12, 6))
    plt.hexbin(joined_pd["PRCP (Inches)"], joined_pd["total_rides"], gridsize=20, cmap='viridis', mincnt=1, reduce_C_function='mean')

    # Add colorbar for reference
    plt.colorbar(label="Average Rides in Bin")

    plt.title("Hexbin Plot of Precipitation vs. Total Rides")
    plt.xlabel("Precipitation (Inches)")
    plt.ylabel("Total Rides")
    plt.tight_layout()
    plt.show()

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png")
    img_bytes.seek(0)
    plt.close()

    return img_bytes
