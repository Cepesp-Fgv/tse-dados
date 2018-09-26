import time

import boto3
import pandas as pd
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

from web.cepesp.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class AthenaDatabaseClient:

    def __init__(self, database, output_bucket, output_directory):
        self.output_bucket = output_bucket
        self.output_directory = output_directory
        self.database = database
        self.athena = boto3.client('athena', region_name='us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        self.s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def execute(self, query):
        response = self.athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': self.database
            },
            ResultConfiguration={
                'OutputLocation': f"s3://{self.output_bucket}/{self.output_directory}",
            }
        )

        return response['QueryExecutionId']

    def execute_and_wait(self, query, sleep=5):
        qid = self.execute(query)
        status = ('RUNNING', None)
        count = 0
        while status[0] in ['RUNNING', 'QUEUED']:
            try:
                status = self.status(qid)
            except ClientError:
                status = ('RUNNING', None)
                time.sleep(sleep * 2)
            time.sleep(sleep)
            count += 1

        print('execution time %d seconds' % (count * sleep))

        if status[0] == 'FAILED':
            raise AthenaQueryFailed(query, status[1])

        return qid

    def status(self, query_id):
        response = self.athena.batch_get_query_execution(
            QueryExecutionIds=[query_id]
        )

        state = response['QueryExecutions'][0]['Status']['State']
        reason = response['QueryExecutions'][0]['Status']['StateChangeReason'] if state == 'FAILED' else None

        return state, reason

    def get_stream(self, query_id) -> StreamingBody:
        s3_obj = self.s3.get_object(
            Bucket=self.output_bucket,
            Key=f"{self.output_directory}/{query_id}.csv"
        )

        return s3_obj['Body']

    def read(self, query_id, nrows=None, skiprows=0) -> pd.DataFrame:
        file_path = f"s3://{self.output_bucket}/{self.output_directory}/{query_id}.csv"
        header = pd.read_csv(file_path, sep=',', dtype=str, nrows=0)
        columns = [c.upper() for c in header.columns.tolist()]
        df = pd.read_csv(file_path, sep=',', dtype=str, names=columns, nrows=nrows, skiprows=1 + skiprows)

        return df


class AthenaQueryFailed(Exception):
    def __init__(self, query, error):
        super().__init__(f'{error} - SQL: "{query}"')
