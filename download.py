import subprocess
import sys
import os
import zipfile
import shutil

# ===== Step 0: Auto-install required library =====
try:
    import requests
except ImportError:
    print("requests module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# ===== Step 1: Define paths =====
desktop_folder = r"C:\Users\Administrator\Desktop\data"
zip_file = os.path.join(desktop_folder, "artifact.zip")

# Create desktop folder if not exists
os.makedirs(desktop_folder, exist_ok=True)

# ===== Step 2: Get download URL from server =====
get_url_endpoint = "https://azcaptchahh.pythonanywhere.com/geturl"
print(f"Fetching download URL from: {get_url_endpoint}")
response = requests.get(get_url_endpoint)
response.raise_for_status()

data = response.json()
download_url = data.get("url")
if not download_url:
    raise Exception("No URL found in server response.")

print(f"Download URL obtained: {download_url}")

# ===== Step 3: Download the ZIP file =====
print(f"Downloading artifact to {zip_file} ...")
r = requests.get(download_url, stream=True)
r.raise_for_status()

with open(zip_file, "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)

print("Download completed.")

# ===== Step 4: Extract ZIP =====
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
