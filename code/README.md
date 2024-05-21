# big-data-project

### Instructions

* setup python virtual env
    ```sh
    python3 -m venv venv

    ./venv/bin/activate

    pip install -r requirements.txt
    ```

* run spark
    ```sh
    docker pull apache/spark

    docker run -d -p 7077:7077 -p 8080:8080 --name spark-master apache/spark:latest /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
    ```

* download dataset
    * link https://drive.google.com/file/d/1VqwappRAT5jV48Ws6xf4yLbx7QuY7htv/view?usp=sharing
    * extract all files in `app/datasets`

* run project
    ```sh
    python3 -m app
    # http://localhost:5000/
    ```