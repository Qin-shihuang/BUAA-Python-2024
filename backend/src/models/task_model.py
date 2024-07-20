import json

class TaskModel:
    def __init__(
        self,
        id,
        type,
        mainFileId=None,
        fileIds=[],
        reportIds=[],
        clusters=[]
    ):
        self.taskId = id
        # 0: oneToMany, 1: manyToMany
        self.type = type
        if type == 0 and mainFileId is None:
            raise ValueError("mainFileId is required for oneToMany task")
        self.mainFileId = mainFileId
        self.fileIds = fileIds
        self.reportIds = reportIds
        if type == 1:
            self.clusters = clusters
        
    def toJson(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)