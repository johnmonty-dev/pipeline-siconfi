import boto3
from dotenv import load_dotenv
import os

load_dotenv()

import os

print("MINIO_ENDPOINT existe?", os.getenv("MINIO_ENDPOINT") is not None)
print("MINIO_ACCESS_KEY existe?", os.getenv("MINIO_ACCESS_KEY") is not None)
print("MINIO_SECRET_KEY existe?", os.getenv("MINIO_SECRET_KEY") is not None)

cliente = boto3.client(
    's3',
    endpoint_url='http://' + os.getenv('MINIO_ENDPOINT'),
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY')
)

buckets = cliente.list_buckets()

print('Buckets encontrados:')
for bucket in buckets['Buckets']:
    print('-', bucket['Name'])