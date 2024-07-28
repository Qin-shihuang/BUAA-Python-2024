import os
import csv
import pandas as pd

class InfoContainer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InfoContainer, cls).__new__(cls)
            cls._instance._initiated = False
        return cls._instance

    def __init__(self):
        if self._initiated:
            return
        super().__init__()
        self._initiated = True

        if not os.path.exists('src/cache'):
            os.makedirs('src/cache')
            os.makedirs('src/cache/files')
            os.makedirs('src/cache/reports')
            with open("src/cache/file_info.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["id", "name", "size", "path", "time"])

    def add_file_info(self, file_id, file_name, file_size, file_path, file_time):
        with open("src/cache/file_info.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([file_id, file_name, file_size, file_path, file_time])

    def get_file_info(self, file_id):
        df = pd.read_csv('src/cache/file_info.csv')
        # return df.iloc[file_id - 1].tolist()
        return df[df['id'] == file_id].values.tolist()[0][1:]
    
    def get_file_name(self, file_id):
        return self.get_file_info(file_id)[0]
    
    def get_file_content(self, file_id):
        with open(f'src/cache/files/file_{file_id}.py', 'r') as f:
            return f.read()
        
    def get_record(self, report_id):
        with open(f'src/cache/reports/report_{report_id}.json', 'r') as f:
            return f.read()

class FileInfo:
    def __init__(self, file_id, file_name, file_size, file_path, file_time):
        self.id = file_id
        self.name = file_name
        self.size = file_size
        self.path = file_path
        self.time = file_time
