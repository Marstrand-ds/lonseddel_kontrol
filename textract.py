import boto3
import json
import sys
from pprint import pprint
import time
import random

# Document
s3BucketName = "textract"
documentName = "lonseddel_17.08.2020_20.09.2020.pdf"

bucket = 'textract-console-us-east-2-93670593-4169-4d03-883c-b1e56ed9e822'
path = '/Users/andersmarstrand/Documents/GitHub/lonseddel_kontrol/'
filename = 'Lonseddel_17.08.2020-20.09.2020.PDF'

s3 = boto3.resource('s3')
print(f'uploading {filename} to s3')
s3.Bucket(bucket).upload_file(path+filename, filename)

client = boto3.client('textract')
response = client.start_document_text_detection(
                   DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': filename} })

response = client.get_document_text_detection(JobId=jobid)