from generated import plagiarism_detection_pb2 as pb
from generated import plagiarism_detection_pb2_grpc as pb_grpc

from services.auth_service import verify_token
from services.report_service import ReportService

from utils.error_codes import ErrorCode

class ReportServiceServicer(pb_grpc.ReportServiceServicer):
    def __init__(self):
        self.report_service = ReportService()
        
    def GetTaskList(self, request, context):
        token = request.token
        auth_status, user_id = verify_token(token)
        if not auth_status:
            return pb.GetTaskListResponse(status=ErrorCode.UNAUTHORIZED.value)
        task_previews = []
        for task in self.report_service.get_task_list(user_id):
            if task[2] == 0:
                task_previews.append(pb.TaskPreview(id=task[0], task_name=task[1], type=task[2], main_file_id=task[3], file_count=task[4], created_at=task[5]))
            else:
                task_previews.append(pb.TaskPreview(id=task[0], task_name=task[1], type=task[2], file_count=task[4], created_at=task[5]))
        return pb.GetTaskListResponse(status=ErrorCode.SUCCESS.value, task_previews=task_previews)
    
    def GetTask(self, request, context):
        token = request.token
        auth_status, user_id = verify_token(token)
        if not auth_status:
            return pb.GetTaskResponse(status=ErrorCode.UNAUTHORIZED.value)
        task_id = request.task_id
        status, owner_id = self.report_service.get_task_owner(task_id)
        if not status:
            return pb.GetTaskResponse(status=ErrorCode.TASK_NOT_FOUND.value)
        if owner_id != user_id:
            return pb.GetTaskResponse(status=ErrorCode.UNAUTHORIZED.value)
        file_path = f"task/{task_id}.json"
        try:
            with open(file_path, "r") as f:
                task = f.read()
            return pb.GetTaskResponse(status=ErrorCode.SUCCESS.value, task=task)
        except Exception as e:
            return pb.GetTaskResponse(status=ErrorCode.UNKNOWN_ERROR.value)
    
    def GetReport(self, request, context):
        token = request.token
        auth_status, user_id = verify_token(token)
        if not auth_status:
            return pb.GetReportResponse(status=ErrorCode.UNAUTHORIZED.value)
        report_id = request.report_id
        status, owner_id = self.report_service.get_report_owner(report_id)
        if not status:
            return pb.GetReportResponse(status=ErrorCode.REPORT_NOT_FOUND.value)
        if owner_id != user_id:
            return pb.GetReportResponse(status=ErrorCode.UNAUTHORIZED.value)
        file_path = f"report/{report_id}.json"
        try:
            with open(file_path, "r") as f:
                report = f.read()
            return pb.GetReportResponse(status=ErrorCode.SUCCESS.value, report=report)
        except Exception as e:
            return pb.GetReportResponse(status=ErrorCode.UNKNOWN_ERROR.value)
    
    def UpdateReport(self, request, context):
        token = request.token
        auth_status, user_id = verify_token(token)
        if not auth_status:
            return pb.GetReportListResponse(status=ErrorCode.UNAUTHORIZED.value)
        report_id = request.report_id
        report = request.report
        status, owner_id = self.report_service.get_report_owner(report_id)
        if not status:
            return pb.UpdateReportResponse(status=ErrorCode.REPORT_NOT_FOUND.value)
        if owner_id != user_id:
            return pb.UpdateReportResponse(status=ErrorCode.UNAUTHORIZED.value)
        file_path = f"report/{report_id}.json"
        try:
            with open(file_path, "w") as f:
                f.write(report)
            return pb.UpdateReportResponse(status=ErrorCode.SUCCESS.value)
        except Exception as e:
            return pb.UpdateReportResponse(status=ErrorCode.UNKNOWN_ERROR.value)