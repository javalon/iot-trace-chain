import os

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, to_timestamp, when

from persistence_worker.utils.logger_config import setup_logger
from persistence_worker.utils.time_profiling import measure_time


def is_running_in_docker():
    return os.path.exists("/.dockerenv") or os.environ.get("RUNNING_IN_DOCKER") == "1"


class DeltaWriter:
    def __init__(self, aws_access_key, aws_secret_key, aws_s3_endpoint_url, aws_s3_secure, delta_path):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_s3_endpoint_url = aws_s3_endpoint_url
        self.aws_s3_secure = aws_s3_secure
        self.delta_path = delta_path
        self.extra_packages = [
            "org.apache.hadoop:hadoop-aws:3.3.4",
            "org.apache.hadoop:hadoop-common:3.3.4",
            "software.amazon.awssdk:bundle:2.31.5",
            "io.netty:netty-transport-native-epoll:4.1.119.Final",
        ]
        self.logger = setup_logger(__name__)

        self.builder = (
            SparkSession.builder.appName("iot-data")
            .master("local[*]")
            .config("spark.driver.host", "127.0.0.1")
            .config("spark.executor.heartbeatInterval", "60s")
            .config("spark.network.timeout", "120s")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.hadoop.fs.s3a.access.key", self.aws_access_key)
            .config("spark.hadoop.fs.s3a.secret.key", self.aws_secret_key)
            .config("spark.hadoop.fs.s3a.endpoint", self.aws_s3_endpoint_url)
            .config("spark.hadoop.fs.s3a.connection.ssl.enabled", self.aws_s3_secure)
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            # Disable warning messages
            .config("spark.setLogLevel", "ERROR")
            .config("spark.driver.memory", "2g")
            .config("spark.executor.memory", "2g")
            .config("spark.sql.debug.maxToStringFields", 100)
        )
        if is_running_in_docker():
            self.logger.info("Running in Docker, adding extra packages to Spark session.")
            self.builder.config(
                "spark.jars",
                ",".join(
                    [f"/opt/spark-jars/{pkg.split(':')[1]}-{pkg.split(':')[2]}.jar" for pkg in self.extra_packages]
                ),
            )
        else:
            self.builder.config("spark.jars.packages", ",".join(self.extra_packages))
        self.spark = None

    def start(self):
        if is_running_in_docker():
            self.spark = configure_spark_with_delta_pip(self.builder).getOrCreate()
        else:
            self.spark = configure_spark_with_delta_pip(self.builder, extra_packages=self.extra_packages).getOrCreate()
        self.spark.sparkContext.setLogLevel("ERROR")
        self.logger.info("Spark session started")

    def stop(self):
        if self.spark:
            self.spark.stop()
        self.logger.info("Spark session stopped")

    @measure_time
    def save_data(self, device_id, iot_data):
        if not isinstance(iot_data, list):
            iot_data = [iot_data]

        for data in iot_data:
            data["device_id"] = device_id

        df = self.spark.createDataFrame(iot_data)
        df = df.filter(df["timestamp"].isNotNull())
        df = df.withColumn(
            "ts_cast",
            when(col("timestamp").cast("bigint").isNotNull(), to_timestamp(col("timestamp").cast("bigint"))).otherwise(
                to_timestamp(col("timestamp"))
            ),
        )
        df = df.withColumn("date_raw", to_date(col("ts_cast")))

        failed_cast_count = df.filter(df["date_raw"].isNull()).count()
        if failed_cast_count > 0:
            self.logger.warning(f"⚠️ {failed_cast_count} record(s) failed to cast timestamp to date.")

        df = df.filter(df["date_raw"].isNotNull()).withColumnRenamed("date_raw", "date")
        self.logger.info(f"📦 Saving {df.count()} valid record(s) to Delta Lake.")

        df.write.format("delta").mode("append").partitionBy("date").save(self.delta_path)
        self.logger.info("✅ Data saved in Delta Lake.")
