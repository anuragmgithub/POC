kubectl exec -it emptydir-demo -- sh  

Breakdown of the Command  

Part	           Explanation  
kubectl	           The Kubernetes CLI command-line tool.  
exec	           Executes a command inside a running container of a Pod.  
-it	               Enables interactive mode with a terminal.  
emptydir-demo	   The name of the Pod in which the container is running.  
--	               Separates kubectl options from the command to run inside the container.  
sh	               The shell command to start a shell session inside the container.  

🔹 Force Delete a Stuck PVC:  
Sometimes, PVCs get stuck in Terminating state. Fix it using:  
```
kubectl patch pvc <pvc-name> -p '{"metadata":{"finalizers":null}}'
```

```
kubectl delete pvc <pvc-name>
```


