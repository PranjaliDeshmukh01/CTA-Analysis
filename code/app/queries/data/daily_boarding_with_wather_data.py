from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from pyspark.sql.types import (DateType, IntegerType, StringType, StructField,
                               StructType)


def get_daily_boarding_total_with_weather_data():
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
    joined_df = weather_df.join(cta_grouped, on="date", how="inner")
    return joined_df
