Apache Kyuubi is a distributed, multi-tenant enterprise data gateway designed on top of Spark, Flink, Trino, and other computing engines. Its purpose is to offer serverless SQL services on top of Lakehouse.  

To run dbt with Apache Kyuubi on a Spark cluster, you need to configure dbt to connect to Kyuubi as a JDBC source. Kyuubi acts as a ThriftServer (like HiveServer2), so dbt can communicate with it via JDBC.  

## How dbt Connects to Kyuubi  
- Kyuubi runs on Spark: It provides a JDBC/Thrift interface.  
- dbt uses the dbt-spark adapter: This adapter allows dbt to run Spark SQL queries.  
- dbt connects to Kyuubi via JDBC: The connection string looks like:  
```jdbc:hive2://<kyuubi-host>:<kyuubi-port>/default;transportMode=http;httpPath=/cliservice```  

### Role of ZooKeeper in Kyuubi:  
Apache Kyuubi uses Apache ZooKeeper for service discovery and high availability when running in a distributed environment.  

🔹 Why Does Kyuubi Need ZooKeeper?  
Service Discovery 📌  
- Kyuubi can register itself in ZooKeeper, so clients (e.g., dbt, BI tools) don’t need to know specific Kyuubi instances.
- Clients connect to ZooKeeper, which redirects them to an available Kyuubi instance.  

High Availability (HA) & Load Balancing 🔄  
- Multiple Kyuubi servers can run in a cluster.
- If one server fails, ZooKeeper redirects clients to another healthy instance.  

Session Management 🕒  
  - ZooKeeper helps persist Spark SQL sessions across Kyuubi nodes.  
-  If a client disconnects and reconnects, it can resume the same session.  

Failover Support 🚦  
- If a Kyuubi server crashes, another instance can take over without affecting running queries.  

ZooKeeper acts as a central coordinator for Kyuubi, ensuring that sessions remain persistent even if a Kyuubi instance fails. This makes query execution more reliable and scalable for Spark SQL workloads.  

### Kyuubi Mimics HiveServer2 but Routes Queries to Spark SQL – How Does It Work?
Kyuubi does not use Hive, but it implements the HiveServer2 (HS2) protocol to provide an SQL gateway for Spark SQL.

This means:
✅ Kyuubi "pretends" to be HiveServer2 so that clients (like Beeline, JDBC, ODBC, dbt, or DBeaver) can connect to it just like they would connect to Hive.
✅ Instead of executing queries in Hive, Kyuubi forwards them to Spark SQL, which processes them on a Spark cluster.


## What is a StatefulSet in Kubernetes?   

A StatefulSet is a Kubernetes controller designed for stateful applications. Unlike a Deployment, a StatefulSet:
- Ensures stable pod names (e.g., kyuubi-0, kyuubi-1).
- Maintains ordered startup and shutdown.
- Associates persistent storage (e.g., PVCs) with specific pods.

## Why ZooKeeper Needs StatefulSet?   
ZooKeeper is a distributed coordination service that requires:  
✅ Persistent data storage (to store metadata and session information).  
✅ Stable pod names (zookeeper-0, zookeeper-1) for leader election.  
✅ Ordered startup/shutdown (because ZooKeeper nodes form a quorum).  

Why ZooKeeper is Needed?  
Kyuubi can work without ZooKeeper, but adding ZooKeeper improves: ✅ Session Persistence: If a client disconnects, it can reconnect to the same session.  
✅ High Availability: If a Kyuubi instance crashes, the client can reconnect to another instance.  
✅ Load Balancing: Multiple Kyuubi instances register with ZooKeeper, allowing clients to connect to an available instance.  
✅ Leader Election: If you have multiple Kyuubi instances, one will be elected as the leader.  

🔹 Without ZooKeeper: Sessions are lost when Kyuubi crashes.  
🔹 With ZooKeeper: Sessions persist, and failover is seamless.  

Create a Namespace:  
```kubectl create namespace dbeaver```   

# connect mysql from wsl  
```
mysql -h <windowsIPADDRS> -u root -p
```

## Exposing Kyuubi via LoadBalancer in Kubernetes  
By default, when you deploy a service in Kubernetes, it is only accessible within the cluster. To allow external access, Kubernetes   provides multiple service types, including ClusterIP, NodePort, and LoadBalancer.  

Understanding LoadBalancer in Kubernetes  
A LoadBalancer service in Kubernetes:  

Automatically provisions an external IP (if running on cloud platforms like AWS, GCP, or Azure).  
Distributes traffic across multiple pods running the same service.   
Allows external applications (like DBeaver) to access your service without using kubectl port-forward.  

## commands to edit service:  
```kubectl edit service kyuubi-service -n kyuubi```

Alternatively, Replace the Service:  
```kubectl delete service kyuubi-service -n kyuubi```

kyuubi-59585496-f2qcl

kubectl exec -it kyuubi-59585496-f2qcl -n kyuubi -- cat /opt/kyuubi/conf/kyuubi-defaults.conf


kubectl exec -n kyuubi -it kyuubi-59585496-f2qcl -- sh -c "spark-submit --version"

kubectl exec -n kyuubi -it kyuubi-59585496-f2qcl -- cat /etc/kyuubi/conf/kyuubi.conf

kubectl exec -n kyuubi -it  kyuubi-74bbf679b4-7f4tv -- lsof -i :10009

kubectl exec -n dbeaver -it dbeaver-75c5969cf7-5dbd5 -- nc -zv kyuubi-service.kyuubi.svc.cluster.local 10009

kubectl exec -n dbeaver -it dbeaver-75c5969cf7-5dbd5 -- /bin/sh

kubectl exec -n kyuubi -it kyuubi-74bbf679b4-7f4tv -- cat $KYUUBI_CONF_DIR/kyuubi-defaults.conf | grep authentication

The "Invalid status -128" error in Kyuubi logs indicates an authentication mismatch between the client (DBeaver) and the Kyuubi server. This happens when Kyuubi expects SASL authentication, but DBeaver does not support it or is misconfigured.

Since Kyuubi needs to manage Spark jobs, it requires permissions to watch and list pods in Kubernetes. You need to update the RBAC   (Role-Based Access Control) settings.


 kubectl auth can-i delete services --as=system:serviceaccount:kyuubi:default -n default
no

kubectl exec -it kyuubi-74bbf679b4-95dw4 -n kyuubi -- /bin/bash







