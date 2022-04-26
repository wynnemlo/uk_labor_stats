import os
import logging
from datetime import datetime

from airflow import DAG
from operators.ons_download_csv_operator import ONSDownloadCSVOperator
from operators.load_to_s3_operator import LoadToS3Operator
from operators.transform_to_postgres_operator import TransformToPostgresOperator

# AWS config
BUCKET = "labor-stats"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

# constant that points to our first file date
first_file_date = datetime(2022, 3, 14)

with DAG(
    default_args = {
        "owner": "airflow",
        "start_date": first_file_date,
        "depends_on_past": False,
        "retries": 1,
    },
    dag_id="ingest_female_employment_data",
    schedule_interval="0 6 27 * *",
    catchup=True,
    max_active_runs=2,
    tags=['ons_uk'],
) as dag:
    download_csv_to_local = ONSDownloadCSVOperator(
        task_id='download_csv_to_local',
        first_file_date=first_file_date,
        url_prefix='https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/lf25/lms/previous/v',
        filename_prefix='female_employment'
    )

    local_to_s3 = LoadToS3Operator(
        task_id='load_to_s3',
        path_to_local_home=path_to_local_home,
        bucket=BUCKET
    )

    transform_to_postgres = TransformToPostgresOperator(
        task_id="transform_to_postgres",
        bucket=BUCKET,
        table_name="female_employment",
        field_name="employment_rate"
    )

    download_csv_to_local >> local_to_s3 >> transform_to_postgres