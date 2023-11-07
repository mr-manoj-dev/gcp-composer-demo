from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryExecuteQueryOperator,
    BigQueryInsertJobOperator
)



# Custom Python logic for retrieving date value
yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())


DATASET_NAME = 'gcs_to_bq_demo'
SALES_TABLE = 'sales_records'
PRODUCTS_TABLE = 'products'
GCS_BUCKET = 'us-central1-ccpv1-01-124da4b5-bucket'
GCS_SALES_OBJ_PATH = 'data/sales_records.csv'
GCS_PRODUCTS_OBJ_PATH = 'data/products.csv'

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
    dag_id='GCS_to_BQ_and_AGG_to_GCS_v1.1',
    catchup=False,
    schedule_interval=timedelta(days=1),
    default_args=default_args
) as dag:
    # Dummy start task
    start = DummyOperator(
        task_id='start',
        dag=dag
    )


    gcs_to_bq_load_sales_data = GCSToBigQueryOperator(
        task_id="gcs_to_bq_load_sales_data",
        bucket=GCS_BUCKET,
        source_objects=[GCS_SALES_OBJ_PATH],
        destination_project_dataset_table='burner-mankumar24-02.gcs_to_bq_demo.sales_records',
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

    gcs_to_bq_load_products_data = GCSToBigQueryOperator(
        task_id="gcs_to_bq_load_products_data",
        bucket=GCS_BUCKET,
        source_objects=[GCS_PRODUCTS_OBJ_PATH],
        destination_project_dataset_table='burner-mankumar24-02.gcs_to_bq_demo.products',
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

    aggr_and_create_bq_view = BigQueryExecuteQueryOperator(
        task_id="aggr_and_create_bq_view",
        sql="CREATE OR REPLACE view gcs_to_bq_demo.daily_sales AS \
        SELECT sales.date as date, sales.product_name as product_name, products.category as category, SUM(SAFE_CAST(sales.quantity AS INT64)) as quantity, ROUND(SUM(SAFE_CAST(sales.total_price AS FLOAT64)), 2) as total_price \
        FROM `burner-mankumar24-02.gcs_to_bq_demo.sales_records` as sales, `burner-mankumar24-02.gcs_to_bq_demo.products` as products \
        group by date, product_name, category",
        use_legacy_sql=False,
        location = 'us-central1',
        dag=dag
    )

    # Define the date format
    date_format = datetime.now().strftime("%Y%m%d")

    query_bq_and_export_data_to_gcs = BigQueryInsertJobOperator(
        task_id='query_bq_and_export_data_to_gcs',
        configuration = {
            "query": {
                "query": f"""
                EXPORT DATA OPTIONS (
                    uri = 'gs://us-central1-ccpv1-01-124da4b5-bucket/data/extracts/daily_sales_records_{date_format}_*.csv',
                    format = 'CSV',
                    overwrite = true,
                    header = false,
                    field_delimiter = ','
                ) AS SELECT date, product_name, category, quantity, total_price FROM `burner-mankumar24-02.gcs_to_bq_demo.daily_sales`;
                """,
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

start >> [gcs_to_bq_load_sales_data, gcs_to_bq_load_products_data] >> aggr_and_create_bq_view >> query_bq_and_export_data_to_gcs >> end
