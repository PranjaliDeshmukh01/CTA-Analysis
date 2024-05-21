import os
import sys

from flask import (Flask, Response, render_template, request,
                   send_from_directory)
from flask_caching import Cache
from pyspark.sql import SparkSession

from app.const import VALID_DAY_TYPES
from app.queries.avg_trips_by_station import get_avg_trips_by_station
from app.queries.data.unique_stations import get_unique_stations
from app.queries.monthly_average_covid import get_monthly_average_covid
from app.queries.precipitation_vs_total_rides import \
    get_precipitation_vs_total_rides
from app.queries.snow_vs_total_rides import get_snow_vs_total_rides
from app.queries.top_stations_by_daytype import get_top_stations_by_day_type

cache = Cache(config={
    'CACHE_TYPE': 'filesystem',       # Use filesystem-based caching
    'CACHE_DIR': 'cache_directory',   # Directory to store cached files
    'CACHE_DEFAULT_TIMEOUT': 300,     # Default timeout for cache (5 minutes)
})


app = Flask(__name__, static_folder='static', static_url_path='/static')
cache.init_app(app)

def create_spark_session():
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

    return SparkSession.builder \
        .master("spark://localhost:7077") \
        .appName('App1') \
        .getOrCreate()

@app.route('/')
def index():
    return render_template('index.html', station_names=get_unique_stations())

@app.route('/avg-daily-boarding-total')
def avg_daily_boarding_total():
    station = request.args.get('station', '').strip()
    if not station:
        raise Exception("query param 'station' is required")

    img = get_avg_trips_by_station(station)
    return Response(img, mimetype="image/png")

@app.route('/top-stations-by-day-type')
def top_stations_by_day_type():
    limit = int(request.args.get('limit', '0'))

    day_type = request.args.get('daytype', '').strip()
    if not day_type or day_type not in VALID_DAY_TYPES:
        raise Exception(
            "invalid day type %s, must be one of %s".format(day_type, VALID_DAY_TYPES)
        )

    img = get_top_stations_by_day_type(day_type, limit)
    return Response(img, mimetype="image/png")

@app.route('/monthly-avg-rides-covid')
def get_monthly_avg_rides_covid():
    img = get_monthly_average_covid()
    return Response(img, mimetype="image/png")


@app.route('/precipitation-vs-total-rides')
def precipitation_vs_total_rides():
    img = get_precipitation_vs_total_rides()
    return Response(img, mimetype="image/png")



@app.route('/snow-vs-total-rides')
def snow_vs_total_rides():
    img = get_snow_vs_total_rides()
    return Response(img, mimetype="image/png")


if __name__ == '__main__':
    app.run(debug=True)
