from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'spanner_to_bigquery_v8',
    default_args=default_args,
    description='DAG to export data from Spanner to BigQuery',
    schedule_interval=timedelta(days=1),  # Set the interval as per your requirement
)

# Define your Spanner and BigQuery configurations
spanner_instance = 'span-demo-01'
spanner_database = 'demo-db-01'
spanner_table = 'products'
bigquery_project = 'burner-mankumar24-02'
bigquery_dataset = 'span_to_bq_demo'
bigquery_table = 'products'


# Define the SQL query for federated query
sql_query = f"""
SELECT *
FROM `{spanner_instance}.{spanner_database}.{spanner_table}`
"""

# Dummy start task
start = DummyOperator(
    task_id='start',
    dag=dag
)

# Define the BashOperator to run the gcloud command
query_to_spanner = BashOperator(
    task_id='query_to_spanner',
    bash_command=f'gcloud spanner databases execute-sql {spanner_database} --instance={spanner_instance} --sql="SELECT * FROM {spanner_table}" --project={bigquery_project}',
    dag=dag,
)

# [2023-10-16, 21:10:09 UTC] {task_command.py:381} INFO - Running <TaskInstance: spanner_to_bigquery_v8.query_to_spanner manual__2023-10-16T21:10:05.425546+00:00 [running]> on host airflow-worker-74779776c5-pp5gb
# [2023-10-16, 21:10:09 UTC] {taskinstance.py:1592} INFO - Exporting the following env vars:
# AIRFLOW_CTX_DAG_OWNER=data_engineer
# AIRFLOW_CTX_DAG_ID=spanner_to_bigquery_v8
# AIRFLOW_CTX_TASK_ID=query_to_spanner
# AIRFLOW_CTX_EXECUTION_DATE=2023-10-16T21:10:05.425546+00:00
# AIRFLOW_CTX_TRY_NUMBER=1
# AIRFLOW_CTX_DAG_RUN_ID=manual__2023-10-16T21:10:05.425546+00:00
# [2023-10-16, 21:10:09 UTC] {subprocess.py:63} INFO - Tmp dir root location: 
#  /tmp
# [2023-10-16, 21:10:09 UTC] {subprocess.py:75} INFO - Running command: ['/usr/bin/bash', '-c', 'gcloud spanner databases execute-sql demo-db-01 --instance=span-demo-01 --sql="SELECT * FROM products" --project=burner-mankumar24-02']
# [2023-10-16, 21:10:09 UTC] {subprocess.py:86} INFO - Output:
# [2023-10-16, 21:10:12 UTC] {subprocess.py:93} INFO - product_id  product_name  product_description
# [2023-10-16, 21:10:12 UTC] {subprocess.py:93} INFO - 1           Product A     Description of Product A
# [2023-10-16, 21:10:12 UTC] {subprocess.py:93} INFO - 2           Product B     Description of Product B
# [2023-10-16, 21:10:12 UTC] {subprocess.py:93} INFO - 3           Product C     Description of Product C
# [2023-10-16, 21:10:12 UTC] {subprocess.py:93} INFO - 4           Product D     Description of Product D
# [2023-10-16, 21:10:12 UTC] {subprocess.py:93} INFO - 5           Product E     Description of Product E
# [2023-10-16, 21:10:12 UTC] {subprocess.py:97} INFO - Command exited with return code 0



upload_to_gcs = BashOperator(
    task_id='upload_to_gcs',
    bash_command=f'ls -al',
    dag=dag,
)

# Dummy end task
end = DummyOperator(
    task_id='end',
    dag=dag
)

start >> query_to_spanner >> upload_to_gcs >> end
