import json

class TaskModel:
    def __init__(
        self,
        taskId,
        taskType,
        mainFileId=None,
        fileIds=[],
        reportIds=[]
    ):
        self.taskId = taskId
        # 0: oneToMany, 1: manyToMany
        self.taskType = taskType
        if taskType == 0 and mainFileId is None:
            raise ValueError("mainFileId is required for oneToMany task")
        self.mainFileId = mainFileId
        self.fileIds = fileIds
        self.reportIds = reportIds
        self.clusters = {}
        
    def toJson(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
        
    def fromJson(jsonStr):
        return TaskModel(**json.loads(jsonStr))