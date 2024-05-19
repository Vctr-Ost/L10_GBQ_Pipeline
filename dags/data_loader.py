from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate a DAG object
dag = DAG(
    'data_loader',
    default_args=default_args,
    start_date=datetime(2022, 8, 9),
    end_date=datetime(2022, 8, 11),
    schedule_interval=  "0 1 * * *",
    max_active_runs=1,
    catchup=True,
)

# Define tasks
start_task = DummyOperator(task_id='start', dag=dag)

BUCKET_NAME='bucket_de_hw_10_viktor_ostapenko'
FILE_NAME='src/sales/v1/' + '{{ execution_date.strftime("%Y/%m/%d") }}' + '/file.avro'
UPLOAD_FILE_PATH='/opt/airflow/stg/sales/' + '{{ ds }}' + '/file.avro'     

upload_file = LocalFilesystemToGCSOperator(
    task_id="upload_file",
    src=UPLOAD_FILE_PATH,
    dst=FILE_NAME,
    bucket=BUCKET_NAME,
    gcp_conn_id='googlecloud',
    dag=dag,
)

end_task = DummyOperator(task_id='end', dag=dag)

# Define task dependencies
start_task >> upload_file >> end_task
