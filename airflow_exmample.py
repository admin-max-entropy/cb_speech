from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from pathlib import Path


def save_current_date():
    # Saves the current date to "~/last_date.txt"
    with open(str(Path.home()) + "/last_date.txt", mode='w') as file:
        now = datetime.now()
        file.write(now.strftime("%Y-%m-%d %H:%M:%S"))


# Default parameters for the workflow
default_args = {
    'depends_on_past': False,
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
        'date_example_dag_2', # Name of the DAG / workflow
        default_args=default_args,
        catchup=False,
        schedule='* * * * *' # Every minute (You will need to change this!)
) as dag:
    # This operator does nothing.
    start_task = EmptyOperator(
        task_id='start_task', # The name of the sub-task in the workflow.
        dag=dag # When using the "with Dag(...)" syntax you could leave this out
    )

    # With the PythonOperator you can run a python function.
    save_date_task = PythonOperator(
        task_id='save_date',
        python_callable=save_current_date,
        dag=dag
    )

    # Define the order in which the tasks are supposed to run
    # You can also define paralell tasks by using an array
    # I.e. task1 >> [task2a, task2b] >> task3
    start_task >> save_date_task