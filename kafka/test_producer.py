from kafka import KafkaProducer
import json

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to send data to Kafka
def send_data(topic, data):
    producer.send(topic, data)
    producer.flush()

# Example usage
if __name__ == "__main__":
    topic = 'test1'
    data = {
        'user_id': 12346,
        'name': 'Anurag Mishra',
        'email': 'john.doe@example.com',
        'signup_date': '2023-10-01',
        'preferences': {
            'notifications': True,
            'theme': 'dark'
        },
        'purchase_history': [
            {'item_id': 1, 'item_name': 'Laptop', 'price': 999.99, 'purchase_date': '2023-09-15'},
            {'item_id': 2, 'item_name': 'Smartphone', 'price': 499.99, 'purchase_date': '2023-09-20'}
        ]
    }
    send_data(topic, data)
    print(f"Data sent to topic {topic}: {data}")