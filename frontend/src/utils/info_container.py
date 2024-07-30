import os
import csv
import pandas as pd

from utils.api_client import ApiClient

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
        self.api_client = ApiClient()

        if not os.path.exists('cache'):
            os.makedirs('cache')
            os.makedirs('cache/files')
            os.makedirs('cache/reports')
            with open("cache/file_info.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["id", "name", "size", "path", "time"])

    def add_file_info(self, file_id, file_name, file_size, file_path, file_time):
        with open("cache/file_info.csv", "a", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([file_id, file_name, file_size, file_path, file_time])

    def get_file_info(self, file_id):
        df = pd.read_csv('cache/file_info.csv', index_col=0, encoding='utf-8')
        return df.loc[file_id].tolist()
    
    def get_file_name(self, file_id):
        return self.get_file_info(file_id)[0]
    
    def get_file_content(self, file_id):
        try:
            with open(f'cache/files/file_{file_id}.py', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            _, file_content = self.api_client.download_file(file_id)
            with open(f'cache/files/file_{file_id}.py', 'wb') as f:
                f.write(file_content)
            return file_content.decode('utf-8')
    
    def get_report(self, report_id):
        try:
            with open(f'cache/reports/report_{report_id}.json', 'r') as f:
                return f.read()
        except FileNotFoundError:
            _, report_content = self.api_client.GetReport(report_id)
            with open(f'cache/reports/report_{report_id}.json', 'w') as f:
                f.write(report_content)
            return report_content
        
    def update_report(self,  report_id, new_report):
        with open(f'cache/reports/report_{report_id}.json', 'w') as f:
            f.write(new_report)
        
    def update_file_info(self):
        df = pd.read_csv('cache/file_info.csv', index_col=0, encoding='utf-8')
        df = df[~df.index.duplicated()]
        with open(f'cache/file_info.csv', 'w', encoding='utf-8') as f:
            f.write(df.to_csv(lineterminator="\n"))