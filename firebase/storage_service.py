import os
import shutil
from firebase.firebase_config import bucket, is_mock

# Local Storage Paths
LOCAL_STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage"))
LOCAL_UPLOADS = os.path.join(LOCAL_STORAGE_DIR, "uploads")
LOCAL_IMAGES = os.path.join(LOCAL_STORAGE_DIR, "images")
LOCAL_OUTPUTS = os.path.join(LOCAL_STORAGE_DIR, "outputs")

# Ensure local directories exist
for path in [LOCAL_UPLOADS, LOCAL_IMAGES, LOCAL_OUTPUTS]:
    os.makedirs(path, exist_ok=True)

def upload_file(local_path, remote_path):
    """
    Uploads a file to Firebase Storage or copy to local storage if running in mock mode.
    Returns the file URL or the local file path as a reference.
    """
    filename = os.path.basename(local_path)
    
    if is_mock:
        # Determine local target directory based on remote folder name
        if "uploads" in remote_path:
            dest = os.path.join(LOCAL_UPLOADS, filename)
        elif "images" in remote_path:
            dest = os.path.join(LOCAL_IMAGES, filename)
        else:
            dest = os.path.join(LOCAL_OUTPUTS, filename)
        
        if local_path != dest:
            shutil.copy2(local_path, dest)
        return dest
    else:
        try:
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_path)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            print(f"Error uploading to Firebase Storage: {e}. Defaulting to local copy.")
            # Fallback to mock behavior
            return upload_file(local_path, remote_path)

def download_file(remote_path, dest_local_path):
    """
    Downloads a file from Firebase Storage or copies it from local storage mock.
    """
    if is_mock:
        # Resolve source local file
        filename = os.path.basename(remote_path)
        if "uploads" in remote_path:
            src = os.path.join(LOCAL_UPLOADS, filename)
        elif "images" in remote_path:
            src = os.path.join(LOCAL_IMAGES, filename)
        else:
            src = os.path.join(LOCAL_OUTPUTS, filename)
            
        if os.path.exists(src):
            shutil.copy2(src, dest_local_path)
            return True
        return False
    else:
        try:
            blob = bucket.blob(remote_path)
            blob.download_to_filename(dest_local_path)
            return True
        except Exception as e:
            print(f"Error downloading from Firebase Storage: {e}")
            return False
