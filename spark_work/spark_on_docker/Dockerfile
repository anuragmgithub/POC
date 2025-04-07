    # Use an official Python runtime as a parent image
    FROM python:3.8-slim

    # Set environment variables
    ENV SPARK_VERSION=3.2.0
    ENV HADOOP_VERSION=3.3

    # Install OpenJDK, wget, and other utilities
    RUN apt-get update && \
        apt-get install -y --no-install-recommends \
            default-jdk \
            wget \
            curl \
        && rm -rf /var/lib/apt/lists/*

    # Install Apache Spark
    RUN wget -qO- https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | tar -xz -C /opt && \
        mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark

    # Set environment variables for Spark
    ENV SPARK_HOME=/opt/spark
    ENV PATH=$PATH:$SPARK_HOME/bin

    # Install pyspark package
    RUN pip install pyspark

    # Copy your PySpark script into the container
    COPY simple_pyspark_example.py /opt/spark_app/simple_pyspark_example.py

    # Set the working directory
    WORKDIR /opt/spark_app

    # Command to run your PySpark script
    CMD ["spark-submit", "--master", "local[*]", "simple_pyspark_example.py"]
