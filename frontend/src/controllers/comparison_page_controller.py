"""
Author: Iz0
Date: 2024-07-26
License: MIT License
Description: 
"""

from PyQt5.QtCore import QObject

from models.report_model import ReportModel

from utils.api_client import ApiClient
from utils.info_container import InfoContainer

class ComparisonPageController(QObject):
    def __init__(self):
        self.api_client = ApiClient()
        self.info_container = InfoContainer()
        
    def set_report(self, reportId):
        report_content = self.info_container.get_report(reportId)
        self.report = ReportModel.fromJson(report_content)
        file1_content = self.info_container.get_file_content(self.report.file1Id)
        file2_content = self.info_container.get_file_content(self.report.file2Id)
        self.left_content = file1_content
        self.right_content = file2_content
        self.left_highlight_areas = self.get_file1_highlight_areas()
        self.right_highlight_areas = self.get_file2_highlight_areas()
    
    def get_file1_highlight_areas(self):
        areas = []
        for segment in self.report.duplicateSegments:
            areas.append(segment['file1'])
        return areas
        
    def get_file2_highlight_areas(self):
        areas = []
        for segment in self.report.duplicateSegments:
            areas.append(segment['file2'])
        return areas
    
    def add_highlight_area(self, areas):
        seg = {
            "file1": areas[0],
            "file2": areas[1]
        }
        self.report.duplicateSegments.append(seg)
        new_report = self.report.toJson()
        self.api_client.UpdateReport(self.report.reportId, new_report)