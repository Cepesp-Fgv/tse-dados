import os
import boto3
import errno

from web.cepesp.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
bucket = s3.Bucket(AWS_STORAGE_BUCKET)
prefix = ''
output_path = 'storage'

for obj_file in bucket.objects.filter(Prefix=prefix):
    internal_path = str(obj_file.key)
    storage_path = os.path.join(dir_name, output_path, internal_path)
    storage_path_dir = os.path.dirname(storage_path)

    if not os.path.exists(storage_path_dir):
        try:
            os.makedirs(storage_path_dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    if os.path.exists(storage_path):
        continue

    if not storage_path.endswith('.gz'):
        continue

    print(obj_file.key + "\t====>\t" + storage_path)
    bucket.download_file(obj_file.key, storage_path)
