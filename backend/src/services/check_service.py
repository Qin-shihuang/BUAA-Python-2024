from config import DB_NAME
from services.database_service import DatabaseService

class CheckService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_service = DatabaseService(DB_NAME)
        return cls._instance