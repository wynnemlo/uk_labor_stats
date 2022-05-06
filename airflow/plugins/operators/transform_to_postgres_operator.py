from airflow.models.baseoperator import BaseOperator
from airflow.models import Variable
from airflow.hooks.S3_hook import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

class TransformToPostgresOperator(BaseOperator):
    def __init__(
            self, 
            table_name,
            field_name,
            **kwargs) -> None:
        self.table_name = table_name
        self.field_name = field_name
        super().__init__(**kwargs)

    def execute(self, context):
        # read file from s3
        s3 = S3Hook('s3_conn').get_conn()
        bucket = Variable.get("bucket")
        filename = self.xcom_pull(context)
        obj = s3.get_object(Bucket=bucket, Key=f"raw/{self.table_name}/{filename}")

        # clean data
        df = pd.read_csv(obj['Body'])
        df = df.drop(df.index[0:7])
        df = df[df["Title"].apply(lambda x: len(x) >= 8)]
        df.columns = ["month", self.field_name]
        df["month"] = df["month"].apply(lambda x: datetime.strptime(x, '%Y %b'))
        df[self.field_name] = df[self.field_name].apply(pd.to_numeric)

        # insert to postgres
        engine = create_engine(PostgresHook('rds_connection').get_uri())
        df.to_sql(name=self.table_name, con=engine, if_exists='replace', index=False)
    
    