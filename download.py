import subprocess, sys, os, zipfile

# ===== Step 0: Ensure boto3 is installed =====
try:
    import boto3
except ImportError:
    print("boto3 not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "boto3"])
    import boto3

from botocore.client import Config

# ===== Step 1: Config =====
endpoint_url = "https://d2u6.or7.idrivee2-80.com"
access_key = "SUPwDwzLQ0K3thRSvETB"
secret_key = "ugekVFwTG6j9IkKg1w6DquotUm2Vw9KvR9iMqEk9"
bucket_name = "data"
object_key = "data.zip"

desktop_folder = r"C:\Users\Administrator\Desktop\data"
zip_file = os.path.join(desktop_folder, "artifact.zip")

# Always create the target folder before anything
os.makedirs(desktop_folder, exist_ok=True)

# ===== Step 2: Create S3 client =====
s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=endpoint_url,
    config=Config(signature_version="s3v4")
)

# ===== Step 3: Download from S3 =====
print(f"Downloading '{object_key}' from bucket '{bucket_name}' to {zip_file} ...")
s3.download_file(bucket_name, object_key, zip_file)
print("Download completed.")

# ===== Step 4: Extract ZIP =====
print(f"Ensuring path {desktop_folder} exists before extraction ...")
os.makedirs(desktop_folder, exist_ok=True)

print(f"Extracting ZIP to {desktop_folder} ...")
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(desktop_folder)

# ===== Step 5: Cleanup ZIP =====
os.remove(zip_file)
print("ZIP file removed.")

# ===== Step 6: List extracted contents =====
print(f"Contents of {desktop_folder}:")
for root, dirs, files in os.walk(desktop_folder):
    for name in dirs:
        print(os.path.join(root, name))
    for name in files:
        print(os.path.join(root, name))

print("Artifact downloaded and extracted successfully.")
