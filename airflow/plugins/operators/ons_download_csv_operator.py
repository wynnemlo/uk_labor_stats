import requests
from datetime import datetime
from airflow.models.baseoperator import BaseOperator

class ONSDownloadCSVOperator(BaseOperator):
    def __init__(
            self, 
            first_file_date,
            url_prefix, 
            filename_prefix,
            **kwargs) -> None:
        self.first_file_date = first_file_date
        self.url_prefix = url_prefix
        self.filename_prefix = filename_prefix
        super().__init__(**kwargs)

    def execute(self, context):
        # get appropriate version to download
        execution_date = datetime.strptime(context['ds'], "%Y-%m-%d")
        delta = execution_date - self.first_file_date
        version_num = round((delta.days / 30)) + 4
        url = f"{self.url_prefix}{version_num}"
        filename = f"{self.filename_prefix}_v{version_num}_{execution_date.strftime('%Y-%m')}.csv"
        
        # download and rename CSV
        req = requests.get(url)
        csv_file = open(filename, 'wb').write(req.content)

        return filename