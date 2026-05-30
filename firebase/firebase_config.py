import os
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Path to service account key (ignored by Git for safety)
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

_firebase_app = None
db = None
bucket = None
is_mock = False

def initialize_firebase():
    global _firebase_app, db, bucket, is_mock
    if _firebase_app is not None:
        return db, bucket, is_mock

    # Check if we can initialize Firebase Admin SDK
    if os.path.exists(SERVICE_ACCOUNT_PATH):
        try:
            cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
            # Configured to use user's Firebase bucket
            bucket_name = "haacky.firebasestorage.app"
            
            try:
                _firebase_app = firebase_admin.get_app()
            except ValueError:
                _firebase_app = firebase_admin.initialize_app(cred, {
                    'storageBucket': bucket_name
                })
            
            db = firestore.client()
            bucket = storage.bucket()
            is_mock = False
            print("Firebase Admin SDK successfully initialized.")
        except Exception as e:
            print(f"Error initializing real Firebase SDK: {e}. Falling back to Mock DB.")
            is_mock = True
    else:
        print("Firebase serviceAccountKey.json not found. Operating in local Mock DB mode.")
        is_mock = True
        
    return db, bucket, is_mock

# Self-initialize when module is loaded
db, bucket, is_mock = initialize_firebase()
