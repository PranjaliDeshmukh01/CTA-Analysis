#!/bin/bash

set -e

docker pull apache/spark
# docker run -d --name spark -p 7077:7077 -p 8080:8080 -p 8081:8081 apache/spark
# docker run -d --name spark-master -p 7077:7077 -p 8080:8080 -p 8081:8081 apache/spark bin/spark-class org.apache.spark.deploy.master.Master -h localhost
# docker run -p 7077:7077 -p 8080:8080 apache/spark:latest /apache/spark

# docker run -p 7077:7077 -p 8080:8080 -it apache/spark:latest /opt/spark/bin/spark-shell


# docker run -d -p 7077:7077 -p 8080:8080 --name spark-master spark /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
docker run -d -p 7077:7077 -p 8080:8080 --name spark-master apache/spark:latest /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
