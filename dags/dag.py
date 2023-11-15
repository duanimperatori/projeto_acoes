from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator


def exec_notebook(pipeline):
    with open(f'./notebook/{pipeline}.py', 'r') as script_file:
        script_code = script_file.read()
        exec(script_code)

dag_id = 'financial_data_pipeline'

default_args = {
    'owner': 'duanimperatori',
    'start_date': datetime(2023, 11, 12),
    'schedule_interval': None,
    'catchup': False
}

# Crie o objeto DAG
dag = DAG(dag_id, default_args=default_args, schedule_interval=None)

# Tarefas
dim_ticker = PythonOperator(
    task_id='dim_ticker',
    python_callable=exec_notebook,
    op_kwargs={'pipeline': 'dim_ticker'},
    dag=dag,
)

fact_balance = PythonOperator(
    task_id='fact_balance',
    python_callable=exec_notebook,
    op_kwargs={'pipeline': 'fact_balance'},
    dag=dag,
)

fact_cashflow_direct = PythonOperator(
    task_id='fact_cashflow_direct',
    python_callable=exec_notebook,
    op_kwargs={'pipeline': 'fact_cashflow_direct'},
    dag=dag,
)

fact_cashflow_indirect = PythonOperator(
    task_id='fact_cashflow_indirect',
    python_callable=exec_notebook,
    op_kwargs={'pipeline': 'fact_cashflow_indirect'},
    dag=dag,
)

fact_income_statement = PythonOperator(
    task_id='fact_income_statement',
    python_callable=exec_notebook,
    op_kwargs={'pipeline': 'fact_income_statement'},
    dag=dag,
)

fact_price = PythonOperator(
    task_id='fact_price',
    python_callable=exec_notebook,
    op_kwargs={'pipeline': 'fact_price'},
    dag=dag,
)

fact_dividend = PythonOperator(
    task_id='fact_dividend',
    python_callable=exec_notebook,
    op_kwargs={'pipeline': 'fact_dividend'},
    dag=dag,
)

# Dependencias
dim_ticker >> [fact_balance, fact_price]
fact_price >> fact_dividend
fact_balance >> fact_cashflow_direct
fact_cashflow_direct >> fact_cashflow_indirect
fact_cashflow_indirect >> fact_income_statement

