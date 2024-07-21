import json

class ReportModel:
    def __init__(
        self,
        reportId,
        file1Id,
        file2Id,
        similarity,
        duplicateSegments=[]
    ):
        self.reportId = reportId
        self.file1Id = file1Id
        self.file2Id = file2Id
        self.similarity = similarity
        self.duplicateSegments = duplicateSegments
        
    def toJson(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
        
    def fromJson(jsonStr):
        return ReportModel(**json.loads(jsonStr))
        
class FileSegmentModel:
    def __init__(
        self,
        startLine,
        startColumn,
        endLine,
        endColumn
    ):
        self.startLine = startLine
        self.startColumn = startColumn
        self.endLine = endLine
        self.endColumn = endColumn