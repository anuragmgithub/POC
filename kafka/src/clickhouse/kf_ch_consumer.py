from kafka import KafkaConsumer
import json
import clickhouse_connect
from datetime import datetime

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'clickhouse1'
CONSUMER_GROUP = 'clickhouse_consumer_group1'

# ClickHouse Configuration
CLICKHOUSE_HOST = 'localhost'
CLICKHOUSE_PORT = 8123
CLICKHOUSE_DATABASE = 'default'
CLICKHOUSE_TABLE = 'kafka_data'

# Connect to ClickHouse
client = clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT)

# Create ClickHouse table dynamically based on Kafka message schema
def create_clickhouse_table():
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {CLICKHOUSE_TABLE} (
        id String,
        event_time DateTime,
        data String
    ) ENGINE = MergeTree()
    ORDER BY event_time
    """
    client.command(create_table_query)
    print(f"Created or ensured table exists: {CLICKHOUSE_TABLE}")

# Insert data into ClickHouse
def insert_into_clickhouse(data):
    # Convert event_time from string to datetime
    event_time = datetime.fromisoformat(data['event_time'])
    client.insert(
        CLICKHOUSE_TABLE,
        [(data['id'], event_time, data['data'])],
        column_names=["id", "event_time", "data"]
    )
    print("Inserted data into ClickHouse.")

# Kafka Consumer Setup
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id=CONSUMER_GROUP,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Ensure the ClickHouse table exists
create_clickhouse_table()

print(f"Listening to Kafka topic: {KAFKA_TOPIC}")

# Process messages from Kafka
for message in consumer:
    kafka_data = message.value  # Assuming Kafka sends data as JSON
    print(f"Received message: {kafka_data}")
    try:
        insert_into_clickhouse(kafka_data)
    except Exception as e:
        print(f"Error inserting data into ClickHouse: {e}")