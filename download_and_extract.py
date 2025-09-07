import os
import shutil
import zipfile
import subprocess
import sys

# ===== Step 0: Ensure requests module is installed =====
try:
    import requests
except ImportError:
    print("requests module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

import json

def main():
    # ===== Step 1: Create Admin folder if it doesn't exist =====
    admin_dir = r"C:\Users\administrator"
    os.makedirs(admin_dir, exist_ok=True)
    print(f"Administrator folder ensured at: {admin_dir}")

    # ===== Step 2: Fetch the latest artifact URL =====
    api_url = "https://azcaptchahh.pythonanywhere.com/geturl"
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    artifact_url = data.get("url")
    if not artifact_url:
        raise Exception("Artifact URL is empty")
    print(f"Artifact URL: {artifact_url}")

    # ===== Step 3: Hardcoded GitHub token for authenticated download =====
    github_token = "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"  # Hardcoded
    headers = {"Authorization": f"token {github_token}"}
    
    # ===== Step 4: Download the ZIP file =====
    zip_path = os.path.join(admin_dir, "artifact.zip")
    print(f"Downloading artifact to {zip_path} ...")
    r = requests.get(artifact_url, headers=headers, stream=True)
    r.raise_for_status()
    with open(zip_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    if not os.path.exists(zip_path):
        raise Exception("Download failed")
    print("Download completed.")

    # ===== Step 5: Clean target directory before extraction =====
    for item in os.listdir(admin_dir):
        item_path = os.path.join(admin_dir, item)
        if item_path == zip_path:
            continue
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        else:
            shutil.rmtree(item_path)
    print(f"Cleaned existing contents in {admin_dir}")

    # ===== Step 6: Extract ZIP =====
    print(f"Extracting ZIP to {admin_dir} ...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(admin_dir)

    # ===== Step 7: Remove the ZIP =====
    os.remove(zip_path)
    print("ZIP file removed.")

    # ===== Step 8: List extracted contents =====
    print("Contents of Administrator folder:")
    for root, dirs, files in os.walk(admin_dir):
        for name in dirs:
            print(os.path.join(root, name))
        for name in files:
            print(os.path.join(root, name))

if __name__ == "__main__":
    main()
