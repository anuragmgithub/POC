# spark-helm-kube/app/Dockerfile

FROM bitnami/spark:latest

# Copy wordcount.py and file.txt to /opt/spark-apps/ directory
COPY wordcount.py /opt/spark-apps/wordcount.py
COPY file.txt /opt/spark-apps/file.txt

# Set the entrypoint for Spark
ENTRYPOINT [ "/opt/bitnami/scripts/spark/entrypoint.sh" ]
