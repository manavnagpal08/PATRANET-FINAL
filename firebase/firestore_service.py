import os
import json
import uuid
from datetime import datetime
from firebase.firebase_config import db, is_mock

# Mock local JSON database path
MOCK_DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage"))
DOCUMENTS_JSON = os.path.join(MOCK_DB_DIR, "mock_documents.json")
RESULTS_JSON = os.path.join(MOCK_DB_DIR, "mock_results.json")

def _load_json_db(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_json_db(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, default=str)

def add_document(doc_data):
    """
    Adds a document record. If Firestore is mock, writes to local JSON database.
    """
    doc_id = doc_data.get('id', str(uuid.uuid4()))
    doc_data['id'] = doc_id
    if 'created_at' not in doc_data:
        doc_data['created_at'] = datetime.now().isoformat()

    if is_mock:
        db_data = _load_json_db(DOCUMENTS_JSON)
        db_data[doc_id] = doc_data
        _save_json_db(DOCUMENTS_JSON, db_data)
        return doc_id
    else:
        try:
            db.collection("documents").document(doc_id).set(doc_data)
            return doc_id
        except Exception as e:
            print(f"Firestore add_document error: {e}. Falling back to Mock.")
            db_data = _load_json_db(DOCUMENTS_JSON)
            db_data[doc_id] = doc_data
            _save_json_db(DOCUMENTS_JSON, db_data)
            return doc_id

def get_documents(user_id=None):
    """
    Gets all documents for a specific user, or all documents if user_id is None.
    """
    if is_mock:
        db_data = _load_json_db(DOCUMENTS_JSON)
        docs = list(db_data.values())
        if user_id:
            docs = [d for d in docs if d.get('user_id') == user_id]
        # Sort by created_at descending
        docs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return docs
    else:
        try:
            query = db.collection("documents")
            if user_id:
                query = query.where("user_id", "==", user_id)
            docs = query.order_by("created_at", direction="DESCENDING").stream()
            return [d.to_dict() for d in docs]
        except Exception as e:
            print(f"Firestore get_documents error: {e}. Falling back to Mock.")
            db_data = _load_json_db(DOCUMENTS_JSON)
            docs = list(db_data.values())
            if user_id:
                docs = [d for d in docs if d.get('user_id') == user_id]
            docs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return docs

def save_result(result_data):
    """
    Saves the extraction results for a document.
    """
    doc_id = result_data.get('document_id')
    if not doc_id:
        raise ValueError("document_id is required to save results.")

    if is_mock:
        db_data = _load_json_db(RESULTS_JSON)
        db_data[doc_id] = result_data
        _save_json_db(RESULTS_JSON, db_data)
        return True
    else:
        try:
            db.collection("results").document(doc_id).set(result_data)
            return True
        except Exception as e:
            print(f"Firestore save_result error: {e}. Falling back to Mock.")
            db_data = _load_json_db(RESULTS_JSON)
            db_data[doc_id] = result_data
            _save_json_db(RESULTS_JSON, db_data)
            return True

def get_result(doc_id):
    """
    Retrieves the extraction result for a specific document.
    """
    if is_mock:
        db_data = _load_json_db(RESULTS_JSON)
        return db_data.get(doc_id)
    else:
        try:
            doc_ref = db.collection("results").document(doc_id).get()
            if doc_ref.exists:
                return doc_ref.to_dict()
            return None
        except Exception as e:
            print(f"Firestore get_result error: {e}. Falling back to Mock.")
            db_data = _load_json_db(RESULTS_JSON)
            return db_data.get(doc_id)
