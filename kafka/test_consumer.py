from kafka import KafkaConsumer
import json
import time

# Initialize the Kafka consumer
consumer = KafkaConsumer(
    'test1',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group1',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
)

# Function to consume data from Kafka with a timeout
def consume_data(timeout=30):
    start_time = time.time()
    while True:
        message = consumer.poll(timeout_ms=1000)
        if message:
            for tp, messages in message.items():
                for msg in messages:
                    if msg.value is not None:
                        print(f"Received message: {msg.value}")
            start_time = time.time()  # Reset the timer on receiving a message
        elif time.time() - start_time > timeout:
            print("No messages received for 30 seconds. Exiting.")
            break

# Example usage
if __name__ == "__main__":
    consume_data()