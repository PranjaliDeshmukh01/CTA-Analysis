import csv
import io

import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql.functions import col, sum, when

from app.const import CACHE_DIR
from app.queries.data.daily_bording_total import get_daily_boarding_total

memory = joblib.Memory(CACHE_DIR, verbose=0)

@memory.cache
def get_top_stations_by_day_type(day_type: str, limit: int = 30):
    df = get_daily_boarding_total('get_top_stations_by_day_type' + day_type + str(limit))
    valid_day_types = ["holiday", "saturday", "weekday"]
    if day_type not in valid_day_types:
        raise Exception(
            "invalid daytype %s, must be one of %s".format(day_type, valid_day_types)
        )

    top_stations = (
        df.withColumn(
            "daytype",
            when(col("daytype") == "U", "holiday")
            .when(col("daytype") == "A", "saturday")
            .when(col("daytype") == "W", "weekday")
            .otherwise(col("daytype")),
        )
        .filter(col("daytype") == day_type)
        .groupBy("stationname")
        .agg(sum("rides").alias("total_rides"))
        .orderBy(col("total_rides").desc())
        .limit(limit)
        # .collect()
    ) .toPandas()

    plt.switch_backend("Agg")

    # Create a horizontal bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_stations, y="stationname", x="total_rides", color='lightblue')

    plt.xlabel("Total Rides")
    plt.ylabel("Station Name")
    plt.title("Total Rides by Station")
    # plt.show()  # Display the plot

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png")
    img_bytes.seek(0)
    plt.close()

    return img_bytes



    output_csv = io.StringIO()

    csv_writer = csv.writer(output_csv)
    csv_writer.writerow(["stationname", "total_rides"])

    for row in top_stations:
        csv_writer.writerow([row["stationname"], row["total_rides"]])

    return output_csv.getvalue()
