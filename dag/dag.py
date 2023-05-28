from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Default arguments for DAGs
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG for dim_ticker table
dim_ticker_dag = DAG(
    'dim_ticker_dag',
    default_args=default_args,
    description='Load and transform data for dim_ticker table',
    schedule_interval='@daily',
)

# Define the DAG for fact_price table
fact_prices_dag = DAG(
    'fact_price_dag',
    default_args=default_args,
    description='Load and transform data for fact_prices table',
    schedule_interval='@daily',
)

# Define the DAG for fact_dividend table
fact_dividend_dag = DAG(
    'fact_dividend_dag',
    default_args=default_args,
    description='Load and transform data for fact_dividend table',
    schedule_interval='@daily',
)

def transform_dim_ticker():
    # Perform transformation logic for dim_ticker table
    # Your code here
    pass

def transform_fact_price():
    # Perform transformation logic for fact_price table
    # Your code here
    pass

def transform_fact_dividend():
    # Perform transformation logic for fact_dividend table
    # Your code here
    pass

# Define tasks for dim_ticker DAG
dim_ticker_task = PythonOperator(
    task_id='transform_dim_ticker',
    python_callable=transform_dim_ticker,
    dag=dim_ticker_dag,
)

# Define tasks for fact_prices DAG
fact_prices_task = PythonOperator(
    task_id='transform_fact_prices',
    python_callable=transform_fact_price,
    dag=fact_prices_dag,
)

# Define tasks for fact_dividend DAG
fact_dividend_task = PythonOperator(
    task_id='transform_fact_dividend',
    python_callable=transform_fact_dividend,
    dag=fact_dividend_dag,
)

# Set dependencies
fact_prices_task.set_upstream(dim_ticker_task)
fact_dividend_task.set_upstream(dim_ticker_task)