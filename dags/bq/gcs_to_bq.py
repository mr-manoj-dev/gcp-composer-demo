import os
import uuid
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from google.cloud import bigquery
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
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
    dag_id='GCS_to_BQ_and_AGG_to_GCS_v9',
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
        bucket='us-central1-ccpv1-01-8d14313a-bucket',
        source_objects=['data/sales_records.csv'],
        destination_project_dataset_table='burner-mankumar24-02.gcs_to_bg_demo.sales_records',
        schema_fields=[
            {'name': 'date', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'product_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'quantity', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'unit_price', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'total_price', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        skip_leading_rows=1,
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        dag=dag
    )

    # GCS to BigQuery data load Operator and task for sales data
    gcs_to_bq_load_products_data = GoogleCloudStorageToBigQueryOperator(
        task_id='gcs_to_bq_load_products_data',
        bucket='us-central1-ccpv1-01-8d14313a-bucket',
        source_objects=['data/products.csv'],
        destination_project_dataset_table='burner-mankumar24-02.gcs_to_bg_demo.products',
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
    aggr_and_create_bq_view = BigQueryOperator(
        task_id='aggr_and_create_bq_view',
        use_legacy_sql=False,
        allow_large_results=True,
        sql="CREATE OR REPLACE view gcs_to_bg_demo.daily_sales AS \
        SELECT sales.date as date, sales.product_name as product_name, products.category as category, SUM(SAFE_CAST(sales.quantity AS INT64)) as quantity, ROUND(SUM(SAFE_CAST(sales.total_price AS FLOAT64)), 2) as total_price \
        FROM `burner-mankumar24-02.gcs_to_bg_demo.sales_records` as sales, `burner-mankumar24-02.gcs_to_bg_demo.products` as products \
        group by date, product_name, category",
        dag=dag
    )

    # Define the date format
    date_format = datetime.now().strftime("%Y%m%d")
    
    # Generate a UUID
    unique_id = str(uuid.uuid4().hex)


    query_bq_and_export_data_to_gcs = BigQueryInsertJobOperator(
        task_id='query_bq_and_export_data_to_gcs',
        configuration = {
            "query": {
                "query": f"""
                EXPORT DATA OPTIONS (
                    uri = 'gs://us-central1-ccpv1-01-8d14313a-bucket/data/extracts/daily_sales_records_{date_format}_*.csv',
                    format = 'CSV',
                    overwrite = true,
                    header = false,
                    field_delimiter = ','
                ) AS SELECT date, product_name, category, quantity, total_price FROM `burner-mankumar24-02.gcs_to_bg_demo.daily_sales`;
                """,
                "useLegacySql": False
            }
        },
        location = 'us-central1'
    )

    # Dummy end task
    end = DummyOperator(
        task_id='end',
        dag=dag
    )

start >> [gcs_to_bq_load_sales_data, gcs_to_bq_load_products_data] >> aggr_and_create_bq_view >> query_bq_and_export_data_to_gcs >> end
