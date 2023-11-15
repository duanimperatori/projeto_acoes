from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

def exec_notebook(pipeline):
    with open(f'./notebook/{pipeline}.py', 'r') as script_file:
        script_code = script_file.read()
        exec(script_code)


default_args = {
    'owner': 'duanimperatori',
    'start_date': datetime(2023, 11, 12),
    'schedule_interval': None,
    'catchup': False
}

with DAG('dim_teste', default_args=default_args) as dag:
    
    run_test_task = PythonOperator(
        task_id='run_test_script',
        python_callable=exec_notebook,
        op_kwargs={'pipeline': 'dim_ticker'},
        dag=dag
    )


