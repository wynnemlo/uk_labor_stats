import os
from airflow.models.baseoperator import BaseOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.models import Variable

class LoadToS3Operator(BaseOperator):
    def __init__(
            self, 
            filename_prefix,
            **kwargs) -> None:
        self.filename_prefix = filename_prefix
        super().__init__(**kwargs)

    def execute(self, context):
        bucket = Variable.get("bucket")
        filename = self.xcom_pull(context)
        path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
        hook = S3Hook('s3_conn')
        hook.load_file(
            filename=f"{path_to_local_home}/{filename}", 
            key=f"raw/{self.filename_prefix}/{filename}",
            bucket_name=bucket,
            replace=True)
        return filename
    
    