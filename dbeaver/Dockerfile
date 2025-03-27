FROM apache/kyuubi:1.8.3-all

USER root
RUN apt update && apt install -y netcat telnet lsof net-tools

# Switch back to non-root user (default user in Kyuubi)
USER 10009
