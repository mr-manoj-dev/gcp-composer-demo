import os
from datetime import datetime, timedelta
from airflow import models
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow.providers.google.cloud.operators.kubernetes_engine import GKEStartPodOperator

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

def get_app_01_xcom_res(app_01_job_dict, ti):
    print("app_01_job_dict: ", app_01_job_dict)
    component = ti.xcom_pull('app_01_using_gke_start_pod')
    
    return_value = ti.xcom_pull(task_ids='app_01_using_gke_start_pod', key='return_value')
    print(f"get_app_01_xcom_res : >>>> : {component}")
    print(f"get_app_01_xcom_res : return_value >>>> : {return_value}")


def get_app_02_xcom_res(app_02_job_dict, ti):
    print("app_02_job_dict: ", app_02_job_dict)
    component = ti.xcom_pull('app_02_using_gke_start_pod')
    
    return_value = ti.xcom_pull(task_ids='app_02_using_gke_start_pod', key='return_value')
    print(f"get_app_02_xcom_res : >>>> : {component}")
    print(f"get_app_02_xcom_res : return_value >>>> : {return_value}")

# DAG definitions   
with DAG(
    dag_id='XCOM_USIN_JSON_SCHEMA_MULTI_TASK_V1',
    catchup=False,
    schedule_interval=timedelta(days=1),
    default_args=default_args
) as dag:
    # Dummy start task   
    start = DummyOperator(
        task_id='start',
        dag=dag
    )

    
    PROJECT_ID='burner-mankumar24-02'
    CLUSTER_REGION='us-central1-a'
    CLUSTER_NAME='demo-cluster'


    app_01_using_gke_start_pod = GKEStartPodOperator(
        # The ID specified for the task.
        task_id="app_01_using_gke_start_pod",
        # Name of task you want to run, used to generate Pod ID.
        name="app_01_using_gke_start_pod",
        project_id=PROJECT_ID,
        location=CLUSTER_REGION,
        cluster_name=CLUSTER_NAME,

        #xcom push to True
        do_xcom_push=True,
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=["bash", "-c", "/usr/local/bin/greet_from_01.sh"],
        # The namespace to run within Kubernetes, default namespace is
        # `default`.
        namespace="default",
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images and the service account that Composer
        # uses has permission to access the Google Container Registry
        # (the default service account has permission)
        image="us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-01-image:v2.1.0",
    )

    get_xcom_app_01_res = PythonOperator(
        task_id='get_xcom_app_01_res',
        python_callable=get_app_01_xcom_res,
        op_kwargs={'app_01_job_dict': {'a': 1, 'b': 2}}
    )


    app_02_using_gke_start_pod = GKEStartPodOperator(
        # The ID specified for the task.
        task_id="app_02_using_gke_start_pod",
        # Name of task you want to run, used to generate Pod ID.
        name="app_02_using_gke_start_pod",
        project_id=PROJECT_ID,
        location=CLUSTER_REGION,
        cluster_name=CLUSTER_NAME,
        
        #xcom push to True
        do_xcom_push=True,

        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=["bash", "-c", "/usr/local/bin/greet_from_02.sh"],
        # The namespace to run within Kubernetes, default namespace is
        # `default`.
        namespace="default",
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images and the service account that Composer
        # uses has permission to access the Google Container Registry
        # (the default service account has permission)
        image="us-central1-docker.pkg.dev/burner-mankumar24-02/app-img/app-02-image:v2.1.0",
    )

    get_xcom_app_02_res = PythonOperator(
        task_id='get_xcom_app_02_res',
        python_callable=get_app_02_xcom_res,
        op_kwargs={'app_02_job_dict': {'a': 3, 'b': 4}}
    )    


    # Dummy end task
    end = DummyOperator(
        task_id='end',
        dag=dag
    )

start >> app_01_using_gke_start_pod >> get_xcom_app_01_res >> app_02_using_gke_start_pod >> get_xcom_app_02_res >> end