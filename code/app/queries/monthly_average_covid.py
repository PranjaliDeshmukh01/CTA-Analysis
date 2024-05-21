import io

import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql.functions import (avg, col, month, split, sum, to_date, when,
                                   year)

from app.const import CACHE_DIR
from app.queries.data.daily_bording_total import get_daily_boarding_total

memory = joblib.Memory(CACHE_DIR, verbose=0)

@memory.cache
def get_monthly_average_covid():
    df = get_daily_boarding_total('get_monthly_average_covid')

    df.withColumn("date", to_date(col("date"), "MM/DD/yyyy"))

    df = df.withColumn("date_split", split(col("date"), "/"))
    df = df.withColumn("month", df["date_split"][0].cast("int"))
    df = df.withColumn("year", df["date_split"][2].cast("int"))

    avg_monthly_rides = (
        df.groupBy("year", "month")
        .agg(avg("rides").alias("average_rides"))
        .orderBy("year", "month")
    )

    out = avg_monthly_rides.toPandas()
    out["year_month"] = out["year"].astype(str) + "-" + out["month"].astype(str)
    covid_start = (out["year"] == 2020) & (out["month"] >= 2)

    plt.switch_backend("Agg")

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        x="year_month",
        y="average_rides",
        data=out,
        marker="o",
        label="All Months",
        color="lightblue",
    )
    sns.lineplot(
        x="year_month",
        y="average_rides",
        data=out[covid_start],
        marker="o",
        color="red",
        label="COVID-19 😱",
    )

    plt.title("Average Daily Boarding")
    plt.xlabel("Timeline")
    plt.ylabel("Average Daily Boarding")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.gca().axes.get_xaxis().set_visible(False)

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png")
    img_bytes.seek(0)
    plt.close()

    return img_bytes
