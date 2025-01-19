from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField
from pyspark.sql.functions import col, from_json

# Kafka Configurations
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "clickhouse1"

# Create Spark Session
spark = SparkSession.builder \
    .appName("KafkaReadExample") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

# Read data from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("startingOffsets", "earliest") \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

# Define schema for Kafka messages
schema = StructType([
    StructField("id", StringType(), True),
    StructField("event_time", StringType(), True),
    StructField("data", StringType(), True)
])

# Parse the Kafka message value
parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write the parsed data to the console
query = parsed_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()