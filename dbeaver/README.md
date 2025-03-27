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








