from kafka import KafkaProducer
import json
import time
from faker import Faker

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'clickhouse1'

# Initialize Faker
fake = Faker()

# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

print(f"Producing messages to Kafka topic: {KAFKA_TOPIC}")

# Generate and send fake data
while True:
    data = {
        "id": fake.uuid4(),
        "event_time": fake.iso8601(),
        "data": fake.text()
    }
    producer.send(KAFKA_TOPIC, value=data)
    print(f"Produced: {data}")
    time.sleep(1)  # Produce one record per second
