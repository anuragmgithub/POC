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



                Clients / Job Submitters
                  (CLI, SDK, Airflow, StepFns)
                         |
                         v
          ┌─────────────────────────────────┐
          │            Master Node          │
          │---------------------------------│
          │ Resource Manager (YARN)         │
          │ NameNode (HDFS metadata)        │
          │ Spark Driver / HiveServer       │
          └─────────────────────────────────┘
       /                   |                     \
      v                    v                      v
┌──────────────┐   ┌──────────────┐      ┌──────────────┐
│  Core Node   │   │  Core Node   │ ...  │  Task Node   │
│ DataNode     │   │ DataNode     │      │ No HDFS      │
│ Executors    │   │ Executors    │      │ Executors    │
└──────────────┘   └──────────────┘      └──────────────┘
       \               \                      /
                        \
                        v
                   Amazon S3 / EMRFS
              (Primary storage in modern EMR)

---
## How Components Communicate Internally:  
EMR uses YARN for resource management  
- Driver submits job → ResourceManager allocates containers
- NodeManagers launch executors
- Task results → driver → output written to S3 or HDFS  

S3 + EMRFS = cheaper, elastic, persistent storage  

### EMRFS:  
- EMRFS (Elastic MapReduce File System) is a filesystem layer in EMR that allows Hadoop/Spark jobs to read   and write data directly to Amazon S3 as if S3 were a native Hadoop file system.  
- It acts as a bridge between S3 and Hadoop ecosystem inside EMR.  

Why EMRFS Exists?  
Traditional Hadoop clusters store data in HDFS, which is tightly coupled with the compute cluster.  
Problem with this traditional approach:  

|issue                     | why it's a limitation |
--------------------------- -------------------------
| Storage tied to cluster  | Stop cluster → lose data |
| Cannot scale storage independently| Need more compute to get more space|

EMRFS solves this by using S3 as a persistent storage layer decoupled from compute. 

Modern EMR setups use S3 as the primary data lake.  
When you run Spark/Hive on EMR:  
- Input data → read from S3 via EMRFS  
- Intermediate results → stored on HDFS or local SSD  
- Final output → written back to S3  
- This allows us to shut down EMR cluster without losing data  


           Persistent Storage Layer
      (Data Lake - Independent of Compute)
                     S3
                     ▲
                     │  EMRFS
                     ▼
   Master/Core/Task Nodes ↔ Executors run compute jobs
                     |
           Temporary Storage (HDFS/Local)

Role of HDFS in EMR:   
Even though S3 is main storage, HDFS is still used inside EMR for temporary and intermediate data.  
HDFS on Core Nodes: 	Shuffle data, temp storage, caching, spill	Lost when cluster terminates  

Why keep HDFS at all?  
- Spark shuffle is faster on HDFS/local disk than S3
- HDFS is needed by some Hadoop tools (MapReduce, HBase)
- Good for caching frequently accessed data






