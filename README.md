# airflow-dbt 
# Installation instructions
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.0.2/docker-compose.yaml'

mkdir ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

docker-compose up

https://airflow.apache.org/docs/apache-airflow/2.0.2/start/docker.html
```

