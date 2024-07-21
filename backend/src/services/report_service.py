from services.database_service import DatabaseService
from config import DB_NAME

class ReportService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_service = DatabaseService(DB_NAME)
        return cls._instance
    
    def __del__(self):
        self.db_service.close()
        
    def get_task_list(self, user_id):
        query = "SELECT id, task_name, type, main_file_id, file_count, created_at FROM tasks WHERE owner_id = ? ORDER BY created_at DESC"
        args = (user_id,)
        result = self.db_service.query(query, args)
        return result
    
    def get_task_owner(self, task_id):
        query = "SELECT owner_id FROM tasks WHERE id = ?"
        args = (task_id,)
        result = self.db_service.query(query, args)
        if not result:
            return False, None
        return True, result[0][0]
    
    def get_report_owner(self, report_id):
        query = "SELECT owner_id FROM reports WHERE id = ?"
        args = (report_id,)
        result = self.db_service.query(query, args)
        if not result:
            return False, None
        return True, result[0][0]