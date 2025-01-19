from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField
from pyspark.sql.functions import col, from_json, date_format

# Kafka and ClickHouse configurations
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "clickhouse1"
CLICKHOUSE_JDBC_URL = "jdbc:clickhouse://localhost:8123/default"
CLICKHOUSE_TABLE = "kafka_data"

# Create Spark Session
spark = SparkSession.builder \
    .appName("KafkaToClickHouse") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,ru.yandex.clickhouse:clickhouse-jdbc:0.3.2") \
    .getOrCreate()

# Kafka message schema
schema = StructType([
    StructField("id", StringType(), True),
    StructField("event_time", StringType(), True),
    StructField("data", StringType(), True)
])

# Read from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Parse Kafka messages
parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("event_time", date_format(col("event_time"), "yyyy-MM-dd HH:mm:ss"))

# Write to ClickHouse
def write_to_clickhouse_safe(batch_df, batch_id):
    try:
        batch_df.write \
            .format("jdbc") \
            .option("url", CLICKHOUSE_JDBC_URL) \
            .option("dbtable", CLICKHOUSE_TABLE) \
            .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
            .mode("append") \
            .save()
    except Exception as e:
        print(f"Error writing batch {batch_id}: {e}")

# Write stream
query = parsed_stream.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_clickhouse_safe) \
    .start()

query.awaitTermination()
