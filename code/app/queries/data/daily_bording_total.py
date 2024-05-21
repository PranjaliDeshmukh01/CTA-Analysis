from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import (DateType, IntegerType, StringType, StructField,
                               StructType)


def get_daily_boarding_total(name):
    spark = SparkSession.builder.appName(name).getOrCreate()

    csv_file_path = "./app/datasets/Cleaned_CTA_Ridership_L_Daily_Total.csv"


    schema = StructType(
        [
            StructField("station_id", IntegerType(), True),
            StructField("stationname", StringType(), True),
            StructField("date", StringType(), True),
            StructField("daytype", StringType(), True),
            StructField("rides", IntegerType(), True),
        ]
    )

    cta_df = spark.read.schema(schema).option("header", "true").csv(csv_file_path)

    return cta_df
