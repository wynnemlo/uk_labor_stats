from airflow.models.baseoperator import BaseOperator
from airflow.hooks.S3_hook import S3Hook

class LoadToS3Operator(BaseOperator):
    def __init__(
            self, 
            path_to_local_home,
            filename_prefix,
            bucket,
            **kwargs) -> None:
        self.path_to_local_home = path_to_local_home
        self.filename_prefix = filename_prefix
        self.bucket = bucket
        super().__init__(**kwargs)

    def execute(self, context):
        filename = self.xcom_pull(context)
        hook = S3Hook('s3_conn')
        hook.load_file(
            filename=f"{self.path_to_local_home}/{filename}", 
            key=f"raw/{filename_prefix}/{filename}",
            bucket_name=self.bucket,
            replace=True)
        return filename
    
    