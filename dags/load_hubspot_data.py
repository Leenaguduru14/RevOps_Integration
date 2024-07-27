from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import sys

# Add the source code directory to the Python path
sys.path.append('/opt/airflow/src')

# Import the main function from main.py
from main import main

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    'load_hubspot_data',
    default_args=default_args,
    description='A DAG to load HubSpot data',
    schedule_interval=timedelta(hours=1),
    start_date=days_ago(1),
    catchup=False,
)

# Define the PythonOperator
run_main_function = PythonOperator(
    task_id='run_main_function',
    python_callable=main,
    dag=dag,
)

# Set the task dependencies
run_main_function