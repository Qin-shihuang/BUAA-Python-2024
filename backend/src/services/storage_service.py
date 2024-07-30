import io
import os
import time
import hashlib
import zipfile

from config import DB_NAME, UPLOAD_FOLDER
from services.database_service import DatabaseService
from utils.pyac.submission import Submission

class StorageService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_service = DatabaseService(DB_NAME)
            cls._instance.submissions = {}
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
        return cls._instance
        
    def __del__(self):
        self.db_service.close()
        
    def save_file(self, userId, filePath, content):
        try:
            filePath = filePath[:255]
            hash_sha256 = hashlib.sha256(content).hexdigest()
            # check if file already exists
            query = "SELECT (storage_name) FROM uploaded_files WHERE hash = ?"
            args = (hash_sha256,)
            result = self.db_service.query(query, args)
            if result:
                storage_name = result[0][0]
            else:
                storage_name = generate_filename(userId, filePath, content)
                storage_path = os.path.join(UPLOAD_FOLDER, storage_name)
                with open(storage_path, 'wb') as f:
                    f.write(content)
            query = "INSERT INTO uploaded_files (storage_name, original_path, size, hash, uploader_id) VALUES (?, ?, ?, ?, ?)"
            args = (storage_name, filePath, len(content), hash_sha256, userId)
            self.db_service.query(query, args)
            query = "SELECT id FROM uploaded_files WHERE storage_name = ? ORDER BY id DESC LIMIT 1"
            args = (storage_name,)
            result = self.db_service.query(query, args) 
            return True, result[0][0]
        except Exception as e:
            print(e)
            return False, -1
    
    def get_file_owner(self, fileId, deleted_ok=True):
        result = -1
        if deleted_ok:
            query = "SELECT (uploader_id) FROM uploaded_files WHERE id = ?"
            args = (fileId,)
            result = self.db_service.query(query, args)
        else:
            query = "SELECT (uploader_id) FROM uploaded_files WHERE id = ? AND deleted = FALSE"
            args = (fileId,)
            result = self.db_service.query(query, args)
        if not result:
            return False, None
        return True, result[0][0]
        
    def get_file(self, fileId):
        query = "SELECT (storage_name) FROM uploaded_files WHERE id = ?"
        args = (fileId,)
        result = self.db_service.query(query, args)
        if not result:
            return False, None
        storage_name = result[0][0]
        file_path = os.path.join(UPLOAD_FOLDER, storage_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError
        with open(file_path, 'rb') as f:
            content = f.read()
        return True, content
    
    def delete_file(self, fileId):
        try:
            query = "UPDATE uploaded_files SET deleted = TRUE WHERE id = ?"
            args = (fileId,)
            self.db_service.query(query, args)
            return True
        except Exception as e:
            print(e)
            return False
        
        
    def get_file_list(self, userId):
        query = "SELECT id, original_path, size, uploaded_at, deleted FROM uploaded_files WHERE uploader_id = ?"
        args = (userId,)
        return self.db_service.query(query, args)
        
    def get_multiple_files_zip(self, fileIds):
        placeholders = ','.join(['?'] * len(fileIds))
        query = f"SELECT id, storage_name, original_path FROM uploaded_files WHERE id IN ({placeholders})"
        args = fileIds
        result = self.db_service.query(query, args)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as z:
            for id, storage_name, original_path in result:
                file_path = os.path.join(UPLOAD_FOLDER, storage_name)
                original_name = original_path.split('/')[-1]
                z.write(file_path, f"{id}_{original_name}")
        zip_buffer.seek(0)
        return zip_buffer.read()
    
    def get_submission(self, file_id):
        if file_id not in self.submissions:
            status, content = self.get_file(file_id)
            if not status:
                return None
            self.submissions[file_id] = Submission(content.decode('utf-8').rstrip())
        return self.submissions[file_id]
    
def generate_filename(user_id, file_path, content):
    original_extension = file_path.split('.')[-1]
    hash_input = f"{user_id}_{file_path}_{len(content)}_{time.time()}"
    return hashlib.sha256(hash_input.encode()).hexdigest() + f".{original_extension}"