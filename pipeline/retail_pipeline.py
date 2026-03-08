from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    # Start date in the past to allow immediate testing/running
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'retail_sales_pipeline',
    default_args=default_args,
    description='A daily pipeline to process retail sales data and train ML models',
    schedule_interval='@daily',
    catchup=False,
)

def finish_pipeline():
    """Print a success message when the pipeline completes."""
    print("Pipeline completed successfully")

# 1. Run Spark data processing script (using BashOperator because PySpark requires a specific environment usually)
process_sales_task = BashOperator(
    task_id='process_sales_data',
    # Replace the path with the absolute path if necessary for your Airflow environment
    bash_command='python spark_jobs/process_sales.py',
    dag=dag,
)

# 2. Run machine learning training script
train_model_task = BashOperator(
    task_id='train_sales_model',
    # Replace the path with the absolute path if necessary for your Airflow environment
    bash_command='python analysis/train_model.py',
    dag=dag,
)

# 3. Print "Pipeline completed successfully" (using PythonOperator)
finish_pipeline_task = PythonOperator(
    task_id='finish_pipeline',
    python_callable=finish_pipeline,
    dag=dag,
)

# Define the task dependencies
process_sales_task >> train_model_task >> finish_pipeline_task
