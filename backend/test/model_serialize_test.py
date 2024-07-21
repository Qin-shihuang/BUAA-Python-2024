import sys

sys.path.append("src")

from models.task_model import TaskModel
from models.report_model import ReportModel, FileSegmentModel

if __name__ == "__main__":
    oneToManyTask = TaskModel(1, 0, 1, [2, 3], [1])
    manyToManyTask = TaskModel(2, 1, mainFileId=None, fileIds=[4, 5, 6], reportIds=[4, 5, 6], clusters=[{"clusterId": 1, "fileIds": [4, 5]}, {"clusterId": 2, "fileIds": [6]}])
    
    assert TaskModel.fromJson(oneToManyTask.toJson()).toJson() == oneToManyTask.toJson()
    assert TaskModel.fromJson(manyToManyTask.toJson()).toJson() == manyToManyTask.toJson()
    
    report = ReportModel(1, 1, 2, 0.9, [{"file1": FileSegmentModel(1, 1, 2, 2), "file2": FileSegmentModel(3, 3, 4, 4)}])
    assert ReportModel.fromJson(report.toJson()).toJson() == report.toJson()