## AWS EMR Architecture:  
managed distributed data processing system that runs frameworks like Hadoop, Spark, Hive, Presto, HBase,  Flink on top of an EC2/YARN-based cluster integrated with AWS services like S3, IAM, CloudWatch,  VPC, EMRFS.     

EMR = Control plane + Compute plane + Storage layer + Orchestration   

Components of EMR Cluster:  

### AWS EMR Node Types

| Node Type                  | Services Running                                               | Responsibility                                  |
|---------------------------|----------------------------------------------------------------|-------------------------------------------------|
| **Master Node (Primary)** | YARN Resource Manager, HDFS NameNode, Spark Driver, Job History Server | Cluster coordination, scheduling, job monitoring |
| **Core Nodes**            | HDFS DataNode, YARN NodeManager, Spark Executors               | Stores data (HDFS) + runs tasks/executors       |
| **Task Nodes (Optional)** | YARN NodeManager, Spark Executors                              | Compute-only nodes — no HDFS storage            |

