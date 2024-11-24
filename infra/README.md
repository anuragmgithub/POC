## kafka installation 
wget https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz  
tar -xzf kafka_2.13-3.8.0.tgz   
cd kafka_2.13-3.8.0   
bin/zookeeper-server-start.sh config/zookeeper.properties &   
bin/kafka-server-start.sh config/server.properties &   
bin/kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1  
bin/kafka-topics.sh --list --bootstrap-server localhost:9092   
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic   
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning   
