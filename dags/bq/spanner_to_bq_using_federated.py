from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

# Custom Python logic for retrieving date value
yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

# Default arguments
default_args = {
    'start_date': yesterday,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}



# DAG definitions
with DAG(
    dag_id='SPN_TO_BQ_FED_v5',
    catchup=False,
    schedule_interval=timedelta(days=1),
    default_args=default_args
) as dag:
    # Dummy start task
    start = DummyOperator(
        task_id='start',
        dag=dag
    )

# Define your Spanner and BigQuery configurations
spanner_instance = 'span-demo-01'
spanner_database = 'demo-db-01'
spanner_table = 'products'
spanner_conn_name = 'span-con-01'
bigquery_project = 'burner-mankumar24-02'
bigquery_dataset = 'span_to_bq_demo'
bigquery_table = 'products'
location = 'us-central1'



#federated_query = f'INSERT INTO {bigquery_dataset}.{bigquery_table} (product_id, product_name, product_description) SELECT * FROM EXTERNAL_QUERY("{bigquery_project}.{location}.{spanner_conn_name}", "SELECT * FROM {spanner_table};")'



date_format = datetime.now().strftime("%Y%m%d")

# insert_query_job = BigQueryInsertJobOperator(
#     task_id="insert_query_job",
#     configuration={
#         "query": {
#             "query": [
#                 f"INSERT INTO {bigquery_dataset}.{bigquery_table} (product_id, product_name, product_description) values(3,'d','e')"
#             ],
#             "useLegacySql": False
#         }
#     },
#     location = 'us-central1',
#     dag=dag
# )

insert_spanner_result_to_bq = BigQueryInsertJobOperator(
    task_id="insert_spanner_result_to_bq",
    configuration={
        "query": {
            "query": f'INSERT INTO {bigquery_dataset}.{bigquery_table} (product_id, product_name, product_description) SELECT * FROM EXTERNAL_QUERY("burner-mankumar24-02.us-central1.span-con-01", "SELECT * FROM products")',
            "useLegacySql": False
        }
    },
    location = 'us-central1',
    dag=dag
)


# Dummy end task
end = DummyOperator(
    task_id='end',
    dag=dag
)

start >> insert_spanner_result_to_bq >> end
