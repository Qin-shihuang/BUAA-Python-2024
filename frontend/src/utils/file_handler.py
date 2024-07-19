import os

from config import DOWNLOAD_DIR

class FileHandler:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FileHandler, cls).__new__(cls)
            cls._instance._initiated = False
        return cls._instance
    
    
    def __init__(self, *args, **kwargs):
        if self._initiated:
            return
        username = args[0]
        super().__init__()
        self._initiated = True
        self.username = username
        self.file_path = os.path.join(DOWNLOAD_DIR, username)
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        

    def read_file(file_path) -> bytes:
        with open(file_path, 'rb') as file:
            return file.read()

    def write_file(self, file_id, file_name, content):
        file_path = os.path.join(self.file_path, f"{file_id}_{file_name}")
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as file:
                file.write(content)
