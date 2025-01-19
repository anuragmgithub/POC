## ClickHouse offers a variety of table engines, each optimized for specific use cases. Below are the most commonly used ClickHouse engines and their purposes:

- MergeTree Family:  
a. MergeTree:  
Use Case: General-purpose storage for analytics with support for indexing and partitions.  
Key Features:  
Indexing for fast queries.  
Partitioning and primary key support.  
Background data merging.      

```
CREATE TABLE example_table (
    id UInt32,
    event_time DateTime,
    value String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (id, event_time);
```

b. ReplacingMergeTree:    
Use Case: Deduplication and retaining the latest version of data.  
Key Features:  
Automatically replaces rows with the same primary key using a specified column (e.g., version or timestamp).  

```
CREATE TABLE deduplicated_table (
    id UInt32,
    event_time DateTime,
    value String
)
ENGINE = ReplacingMergeTree(event_time)
PARTITION BY toYYYYMM(event_time)
ORDER BY id;
```

c. CollapsingMergeTree:   
Use Case: Row-level deletion via sign column.   
Key Features:  
Rows are collapsed (deleted or updated) based on the sign column during merges.  

```
CREATE TABLE collapsing_table (
    id UInt32,
    value String,
    sign Int8
)
ENGINE = CollapsingMergeTree(sign)
PARTITION BY id
ORDER BY id;
```

Kafka:  
Key Features:
Directly reads data from Kafka for real-time ingestion.  

```
CREATE TABLE kafka_table (
    id UInt32,
    value String
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'localhost:9092',
         kafka_topic_list = 'your_topic',
         kafka_group_name = 'clickhouse_group',
         kafka_format = 'JSONEachRow';
```

 File Engines:  
 Use Case: Read data from external files (e.g., CSV, JSON).  

 ```
 CREATE TABLE csv_table (id UInt32, value String)
ENGINE = File('CSV');
```
---

The MergeTree engine in ClickHouse does not enforce uniqueness of the primary key. This means that if you insert multiple rows with the same primary key values, all of them will be stored as separate rows in the table.  

This design is intentional because ClickHouse prioritizes analytical workloads, where storing duplicates is often desirable for use cases like event tracking, detailed logs, or aggregations. However, if you want to handle duplicates or maintain only the latest data for a given primary key, you need to use a specific engine or implement additional logic.  