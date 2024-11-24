from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define the default arguments dictionary
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 21),  # Set to today or a past date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'sample_hello_world_dag',  # Name of the DAG
    default_args=default_args,
    description='A simple Hello World DAG',
    schedule_interval=None,  # Run once a day
)

# Define the Python function
def hello_world():
    print("Hello, World!")

# Define the task using PythonOperator
hello_world_task = PythonOperator(
    task_id='hello_world_task',  # Name of the task
    python_callable=hello_world,  # Function to execute
    dag=dag,  # Attach the task to the DAG
)

# Setting task dependencies (optional for this simple DAG)
# hello_world_task depends on nothing in this case, so no upstream tasks
