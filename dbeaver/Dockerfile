# Use the official Apache Kyuubi image
FROM apache/kyuubi:1.8.3-all

# Switch to root user to install additional utilities
USER root

RUN apt update && apt install -y \
    netcat \
    telnet \
    lsof \
    net-tools \
    curl \
    vim \
    nano \
    jq \
    less \
    iputils-ping


# Set working directory
WORKDIR /opt/kyuubi

# Ensure the conf directory exists
RUN mkdir -p /opt/kyuubi/conf

COPY conf/kyuubi-defaults.conf /opt/kyuubi/conf/kyuubi-defaults.conf
RUN chmod 644 /opt/kyuubi/conf/kyuubi-defaults.conf

# Set environment variables for Spark and Kyuubi
ENV SPARK_KUBERNETES_CONTAINER_IMAGE=bitnami/spark:3.4.2
ENV KYUUBI_SESSION_ENGINE_TIMEOUT=360000

# Copy custom configurations for Kyuubi (if you have any)
#COPY conf/kyuubi-defaults.conf /opt/kyuubi/conf/
# COPY conf/kyuubi-env.sh /opt/kyuubi/conf/

# Set appropriate permissions
#RUN chmod -R 755 /opt/kyuubi/conf/

# Switch back to non-root user (default user in Kyuubi)
USER 10009

# Start Kyuubi server
# CMD ["/opt/kyuubi/bin/kyuubi"]
