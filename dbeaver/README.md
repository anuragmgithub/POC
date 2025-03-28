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












