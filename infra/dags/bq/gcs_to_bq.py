import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator

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
    dag_id='GCS_to_BQ_and_AGG_v1',
    catchup=False,
    schedule_interval=timedelta(days=1),
    default_args=default_args
) as dag:
    # Dummy start task
    start = DummyOperator(
        task_id='start',
        dag=dag
    )

    # GCS to BigQuery data load Operator and task for sales data
    gcs_to_bq_load_sales_data = GoogleCloudStorageToBigQueryOperator(
        task_id='gcs_to_bq_load_sales_data',
        bucket='us-central1-ccpv1-01-e2191e76-bucket',
        source_objects=['data/sales_records.csv'],
        destination_project_dataset_table='burner-mankumar24-02.gcs_to_bg_demo.sales_records',
        schema_fields=[
            {'name': 'date', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'product', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'quantity', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'price', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'category', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        skip_leading_rows=1,
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        dag=dag
    )

    # GCS to BigQuery data load Operator and task for sales data
    gcs_to_bq_load_products_data = GoogleCloudStorageToBigQueryOperator(
        task_id='gcs_to_bq_load_products_data',
        bucket='us-central1-ccpv1-01-e2191e76-bucket',
        source_objects=['data/stationary_products.csv'],
        destination_project_dataset_table='burner-mankumar24-02.gcs_to_bg_demo.stationary_products',
        schema_fields=[
            {'name': 'product_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'product_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'category', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        skip_leading_rows=1,
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        dag=dag
    )

    # BigQuery task, operator
    create_aggr_bq_view = BigQueryOperator(
        task_id='create_aggr_bq_view',
        use_legacy_sql=False,
        allow_large_results=True,
        sql="CREATE OR REPLACE view gcs_to_bg_demo.daily_sales AS \
        SELECT date, Product, Category FROM `burner-mankumar24-02.gcs_to_bg_demo.sales_records` group by date, Product, Category",
        dag=dag
    )

    # Dummy end task
    end = DummyOperator(
        task_id='end',
        dag=dag
    )

start >> [gcs_to_bq_load_sales_data, gcs_to_bq_load_products_data] >> create_aggr_bq_view >> end
