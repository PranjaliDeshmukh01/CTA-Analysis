import csv
import io

import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql.functions import avg, col, when

from app.const import CACHE_DIR
from app.queries.data.daily_bording_total import get_daily_boarding_total

memory = joblib.Memory(CACHE_DIR, verbose=0)

@memory.cache
def get_avg_trips_by_station(station_name: str):
    df = get_daily_boarding_total("avg trips " + station_name)

    station_df = df.filter(col("stationname") == station_name)
    average_rides_by_daytype = (
        station_df.withColumn(
            "daytype",
            when(col("daytype") == "U", "holiday")
            .when(col("daytype") == "A", "saturday")
            .when(col("daytype") == "W", "weekday")
            .otherwise(col("daytype")),
        )
        .groupBy("daytype")
        .agg(avg("rides").alias("average_rides"))
    ).toPandas()


    plt.switch_backend("Agg")

    plt.figure(figsize=(8, 6))
    sns.barplot(data=average_rides_by_daytype, y="average_rides", x="daytype", color='lightblue')

    # plt.bar(average_rides_by_daytype["daytype"], average_rides_by_daytype["average_rides"], color=['blue', 'orange', 'green'])
    plt.xlabel("Day Type")
    plt.ylabel("Average Rides")
    plt.title("Average Rides by Day Type")

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png")
    img_bytes.seek(0)
    plt.close()

    return img_bytes

    output_csv = io.StringIO()

    csv_writer = csv.writer(output_csv)
    csv_writer.writerow(["daytype", "average_rides"])

    for row in average_rides_by_daytype.collect():
        csv_writer.writerow([row["daytype"], row["average_rides"]])

    return output_csv.getvalue()
