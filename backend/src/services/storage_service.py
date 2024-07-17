import os
import hashlib

from config import UPLOAD_FOLDER
from services.database_service import DatabaseService

class StorageService:
    def __init__(self):
        self.db_service = DatabaseService('storage')
        
    def __del__(self):
        self.db_service.close()
        
    def save_file(self, user_id, originalFilename, content):
        storage_path = os.path.join(UPLOAD_FOLDER, generate_filename(user_id, originalFilename, content))
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        try:
            with open(storage_path, 'wb') as f:
                f.write(content)
            query = "INSERT INTO uploaded_files (storage_name, original_name, uploader_id) VALUES (?, ?, ?)"
            args = (storage_path, originalFilename, user_id)
            self.db_service.query(query, args)
            return True
        except Exception as e:
            return False
        
        
def generate_filename(user_id, filename, content):
    original_extension = filename.split('.')[-1]
    hash_input = f"{user_id}_{filename}_{len(content)}"
    return hashlib.sha256(hash_input.encode()).hexdigest() + f".{original_extension}"