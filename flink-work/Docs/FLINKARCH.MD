# Anatomy of a Flink Cluster  
The Flink runtime consists of two types of processes
- a JobManager 
- one or more TaskManagers

![alt text](image.png)

## JobManager:  
The JobManager has a number of responsibilities related to coordinating the distributed execution of Flink Applications:  
- it decides when to schedule the next task (or set of tasks)  
- reacts to finished tasks or execution failures  
- coordinates checkpoints  
- and coordinates recovery on failures  

This process consists of three different components:  
- ResourceManager  
- Dispatcher  
- JobMaster  

## TaskManagers:  
- The TaskManagers (also called workers) execute the tasks of a dataflow, and buffer and exchange the data streams.  
- The smallest unit of resource scheduling in a TaskManager is a task slot. The number of task slots in a TaskManager indicates the number of concurrent processing tasks.  


