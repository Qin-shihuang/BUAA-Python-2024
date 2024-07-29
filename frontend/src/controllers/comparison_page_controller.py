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

report_content = '''{
    "distance": 0.11658977339743665,
    "duplicateSegments": [
        {
            "file1": [
                1,
                3
            ],
            "file2": [
                1,
                3
            ]
        },
        {
            "file1": [
                4,
                19
            ],
            "file2": [
                4,
                18
            ]
        },
        {
            "file1": [
                20,
                23
            ],
            "file2": [
                19,
                22
            ]
        }
    ],
    "file1Id": 24,
    "file2Id": 25,
    "reportId": 17
}'''

file1_content='''def is_valid(char):
    return char.isdigit() or char.isalpha()

def expand_range(s):
    if '-' not in s:
        return s

    result = []
    i = 0
    while i < len(s):
        if i + 2 < len(s) and s[i + 1] == '-' and is_valid(s[i]) and is_valid(s[i + 2]) and s[i] <= s[i + 2]:
            result.append(''.join(chr(c) for c in range(ord(s[i]), ord(s[i + 2]) + 1) if is_valid(chr(c))))
            i += 3
        else:
            result.append(s[i])
            i += 1

    return ''.join(result)

if __name__ == "__main__":
    s = input()
    print(expand_range(s))

'''

file2_content='''def is_valid(char):
    return char.isdigit() or char.isalpha()

def expand_range(s):
    def generate():
        i = 0
        while i < len(s):
            if i + 2 < len(s) and s[i + 1] == '-' and is_valid(s[i]) and is_valid(s[i + 2]) and s[i] <= s[i + 2]:
                for c in range(ord(s[i]), ord(s[i + 2]) + 1):
                    if is_valid(chr(c)):
                        yield chr(c)
                i += 3
            else:
                yield s[i]
                i += 1

    return ''.join(generate())

if __name__ == "__main__":
    s = input()
    print(expand_range(s))
'''

class ComparisonPageController(QObject):
    def __init__(self):
        self.api_client = ApiClient()
        self.info_container = InfoContainer()
        
    def set_report(self, reportId):
        self.report = ReportModel.fromJson(report_content)
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
        self.api_client.update_report(self.report.reportId, new_report)