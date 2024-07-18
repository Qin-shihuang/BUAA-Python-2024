import os
import time
import hashlib

from config import UPLOAD_FOLDER
from services.database_service import DatabaseService

class StorageService:
    def __init__(self):
        self.db_service = DatabaseService('storage')
        
    def __del__(self):
        self.db_service.close()
        
    def save_file(self, userId, originalFilename, content):
        storage_name = generate_filename(userId, originalFilename, content)
        storage_path = os.path.join(UPLOAD_FOLDER, storage_name)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        try:
            with open(storage_path, 'wb') as f:
                f.write(content)
            query = "INSERT INTO uploaded_files (storage_name, original_name, uploader_id) VALUES (?, ?, ?)"
            args = (storage_name, originalFilename, userId)
            self.db_service.query(query, args)
            query = "SELECT id FROM uploaded_files WHERE storage_name = ?"
            args = (storage_name,)
            result = self.db_service.query(query, args)
            return True, result[0][0]
        except Exception as e:
            print(e)
            return False, -1
        
        
def generate_filename(user_id, filename, content):
    original_extension = filename.split('.')[-1]
    hash_input = f"{user_id}_{filename}_{len(content)}_{time.time()}"
    return hashlib.sha256(hash_input.encode()).hexdigest() + f".{original_extension}"