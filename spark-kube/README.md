# Running Spark Streaming Jobs on EKS with Spot Instances

This README provides detailed steps and best practices for deploying fault-tolerant Spark Streaming jobs on Amazon Elastic Kubernetes Service (EKS) using Spot Instances. The guide ensures that the application remains highly available and cost-efficient.

---

## **Overview**

Spark Streaming is a distributed data processing engine designed for real-time processing of streaming data. Deploying it on EKS using Spot Instances significantly reduces costs but requires careful strategies to handle potential Spot Instance interruptions.

---

## **Architecture**

### **Components**
1. **Spark Driver**: Coordinates the execution of the streaming job.
2. **Spark Executors**: Perform the actual computation and storage tasks.
3. **Amazon S3**: Stores intermediate states (checkpoints) and output data.
4. **Kubernetes Cluster**:
   - Runs Spark Driver and Executor pods.
   - Manages Spot and On-Demand node groups.

### **Instance Types**
- Driver: `m5.large` (2 vCPUs, 8 GB RAM).
- Executors: `m5.xlarge` (4 vCPUs, 16 GB RAM).

---

## **Setup Guide**

### **1. Prerequisites**
- **AWS CLI** installed and configured.
- **kubectl** installed.
- **Helm** installed for deploying Kubernetes applications.
- **Spark Docker Image** prepared with your application.

---

### **2. Kubernetes Configuration**

#### **Node Groups**
1. **On-Demand Node Group**:
   - Dedicated to critical pods (e.g., Spark Driver).
   - Configured with `nodeSelector` and `taints/tolerations`.

2. **Spot Node Group**:
   - Used for Spark Executors to reduce costs.
   - Includes multiple instance types for flexibility.

#### **Cluster Autoscaler**
Enable the Kubernetes Cluster Autoscaler to handle scaling and replacement of Spot nodes.

```yaml
# Example configuration for a Spot node group
resources:
  requests:
    cpu: "2"
    memory: "4Gi"
  limits:
    cpu: "2"
    memory: "4Gi"
tolerations:
  - key: "kubernetes.azure.com/scalesetpriority"
    operator: "Equal"
    value: "spot"
    effect: "NoSchedule"
```

---

### **3. Fault Tolerance Setup**

#### **Checkpointing**
Store Spark Streaming checkpoints in Amazon S3 to resume processing in case of failures.

```python
streamingQuery = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "topic") \
    .load() \
    .writeStream \
    .format("parquet") \
    .option("checkpointLocation", "s3://your-bucket/checkpoints/") \
    .start()
```

#### **Dynamic Resource Allocation**
Enable dynamic scaling of executors to handle Spot Instance interruptions effectively.

```bash
spark.dynamicAllocation.enabled=true
spark.dynamicAllocation.minExecutors=1
spark.dynamicAllocation.maxExecutors=10
spark.dynamicAllocation.executorIdleTimeout=60s
```

#### **Graceful Decommissioning**
Ensure Spark executors offload tasks before termination.

```bash
spark.executor.allowSparkContextTermination=true
spark.storage.decommission.rddBlocks=true
spark.executor.decommission.enabled=true
```

---

### **4. Helm Deployment**
Use Helm charts for managing Spark job deployments.

#### **Example `values.yaml`**
```yaml
spark:
  driver:
    cores: 2
    memory: "8Gi"
    nodeSelector:
      lifecycle: "OnDemand"

  executor:
    instances: 6
    cores: 2
    memory: "4Gi"
    tolerations:
      - key: "kubernetes.azure.com/scalesetpriority"
        operator: "Equal"
        value: "spot"
        effect: "NoSchedule"
checkpointLocation: "s3://your-bucket/checkpoints/"
```

---

### **5. Monitoring and Resilience**

#### **Liveness and Readiness Probes**
Add health checks for your Spark pods to ensure they are restarted if they fail.

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 20
  periodSeconds: 10
```

#### **Monitoring Tools**
- **Prometheus** and **Grafana** for real-time metrics.
- **Spark Web UI** for job-specific insights.

---

## **Best Practices**
1. **Diversify Spot Instances**: Use multiple instance types (e.g., `m5.large`, `c5.large`) and regions.
2. **Fallback Mechanisms**: Configure fallback to On-Demand instances for critical workloads.
3. **Proactive Replacement**: Use Spot Capacity Rebalancing to replace instances before termination.
4. **Autoscaling**: Leverage Kubernetes Autoscaler to manage interruptions.
5. **Job Checkpointing**: Store intermediate states in Amazon S3 to recover seamlessly.

---

## **Summary**
Running Spark Streaming jobs on EKS with Spot Instances can achieve high availability and cost efficiency when paired with fault-tolerant configurations. Using Kubernetes features, Spark-specific setups, and monitoring tools ensures the application remains robust even during Spot Instance interruptions.

For more details, refer to the [AWS Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/) and the [Apache Spark on Kubernetes documentation](https://spark.apache.org/docs/latest/running-on-kubernetes.html).

---

🔹 Kubernetes Volumes & VolumeMounts Explained:  
A volume is a Kubernetes object that provides storage inside a pod. It can be backed by:  

- emptyDir → Temporary storage for a pod  
- hostPath → Uses host machine’s filesystem   
- PersistentVolumeClaim (PVC) → Connects to persistent storage like AWS EBS, Azure Disk, etc.  
- ConfigMap/Secret → Stores configuration data  

Example of defining a volume:  
```
volumes:
  -name: my-volume
  emptyDir: {} # This creates empty directory inside pod 

```

🔹 What is a VolumeMount?  
A volumeMount specifies where in the container the volume should be mounted (attached).  

```
volumneMounts:
  - name: my-volume
  mountPath: /app/data # the volumne is available inside /app/data inside the container 

```

- Mounting an emptyDir Volume:  
```
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: busybox
      command: [ "sh", "-c", "echo 'Hello World' > /app/data/hello.txt && sleep 3600" ]
      volumeMounts:
        - name: my-volume
          mountPath: /app/data
  volumes:
    - name: my-volume
      emptyDir: {}

```

-  Mounting a PersistentVolumeClaim (PVC):  
```
apiVersion: v1
kind: Pod
metadata:
  name: my-persistent-pod
spec:
  volumes:
    - name: my-pvc-volume
      persistentVolumeClaim:
        claimName: my-pvc  # Uses an existing PVC
  containers:
    - name: my-container
      image: busybox
      volumeMounts:
        - name: my-pvc-volume
          mountPath: /app/storage  # Mounts PVC to this directory
```

### Difference Between emptyDir and PersistentVolumeClaim (PVC) in Volumes:  

Volume Type	                   Purpose
emptyDir	                     Creates temporary storage inside the pod. Data is lost when the pod is deleted or restarted.  
PersistentVolumeClaim (PVC)	   Uses persistent storage (EBS, Azure Disk, NFS, etc.). Data persists even if the pod restarts or is deleted.  

A PersistentVolumeClaim (PVC) is a request for storage from a PersistentVolume (PV), which is managed by Kubernetes.  
- Define a PVC:  
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce  # Pod can read & write
  resources:
    requests:
      storage: 1Gi   # Request 1Gi of storage
```
- Use PVC in a Pod:  
```
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  volumes:
    - name: my-pvc-volume
      persistentVolumeClaim:
        claimName: my-pvc  # Use the PVC created earlier
  containers:
    - name: my-container
      image: busybox
      command: [ "sh", "-c", "echo 'Hello PVC' > /app/data/hello.txt && sleep 3600" ]
      volumeMounts:
        - name: my-pvc-volume
          mountPath: /app/data  # Mount the PVC at this path
```

- The PVC requests storage from Kubernetes.
- The Pod mounts the PVC at /app/data.
- Any data written to /app/data persists even if the pod is deleted.
- A new pod using the same PVC will see the same data.  
📌 Use Case: Storing logs, databases, or any persistent files.






