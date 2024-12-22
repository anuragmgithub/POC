# Use the official Spark Operator image as a base image
FROM gcr.io/spark-operator/spark-operator:v1beta2-3.1.1-1.1.0

# Set the working directory
WORKDIR /opt/spark

# Install necessary dependencies: Java, wget, curl, etc.
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    wget \
    curl \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Kubeflow SDK (for potential Kubeflow Pipelines integration)
RUN pip3 install kfp

# Install Spark (if not already in the base image)
RUN wget https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz \
    && tar -xzvf spark-3.1.1-bin-hadoop3.2.tgz \
    && mv spark-3.1.1-bin-hadoop3.2 /opt/spark

# Download Kafka and Iceberg jars and place them into the Spark jars directory
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.1/spark-sql-kafka-0-10_2.12-3.1.1.jar -P /opt/spark/jars \
    && wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark3-runtime/0.12.0/iceberg-spark3-runtime-0.12.0.jar -P /opt/spark/jars

# Set environment variables for Spark
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Expose necessary ports (Spark Web UI, etc.)
EXPOSE 8080 4040

# Default entry point to run Spark Operator
ENTRYPOINT ["/usr/local/bin/spark-operator"]

# Optional: You can also pass Spark job configurations here if needed
# CMD ["--spark-job.namespace=spark-operator"]
