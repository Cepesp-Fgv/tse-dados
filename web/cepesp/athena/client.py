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

    def execute(self, query, wait=False, min_wait=16):
        response = self.athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': self.database
            },
            ResultConfiguration={
                'OutputLocation': f"s3://{self.output_bucket}/{self.output_directory}",
            }
        )
        qid = response['QueryExecutionId']
        print(query)

        if wait:
            status = self.wait_finished(qid, min_wait)
            if status[0] == 'FAILED':
                raise AthenaQueryFailed(query, status[1])

        return qid

    def wait_finished(self, qid, min_wait=16):
        status = ('QUEUED', None)
        count = 0
        sleep = 1
        while status[0] in ['RUNNING', 'QUEUED']:
            time.sleep(sleep)
            count += sleep
            sleep = sleep * 2

            try:
                status = self.status(qid)
            except ClientError:
                status = ('RUNNING', None)

            # wait a few more seconds before next checkup
            if status in ['RUNNING', 'QUEUED'] and count == 1:
                sleep = min_wait

        print(f'{qid} took {count}s')
        return status

    def status(self, query_id):
        response = self.athena.batch_get_query_execution(
            QueryExecutionIds=[query_id]
        )

        state = response['QueryExecutions'][0]['Status']['State']
        reason = response['QueryExecutions'][0]['Status']['StateChangeReason'] if state == 'FAILED' else None

        if state == "SUCCEEDED":
            time.sleep(1)  # Give more time for athenas to write the file object
            try:
                self._get_obj(query_id)
            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    state = "FAILED"
                    reason = "Output file not found. Please, try running the query again."

        return state, reason

    def _get_obj(self, query_id):
        return self.s3.get_object(
            Bucket=self.output_bucket,
            Key=f"{self.output_directory}/{query_id}.csv"
        )

    def get_stream(self, query_id) -> StreamingBody:
        s3_obj = self._get_obj(query_id)

        return s3_obj['Body']

    def read(self, query_id, nrows=None, skiprows=0) -> pd.DataFrame:
        s3_obj = self._get_obj(query_id)
        df = pd.read_csv(s3_obj['Body'], sep=',', header=0, dtype=str, nrows=nrows, skiprows=skiprows)
        df.columns = [x.upper() for x in df.columns]

        return df


class AthenaQueryFailed(Exception):
    def __init__(self, query, error):
        super().__init__(f'{error} - SQL: "{query}"')
