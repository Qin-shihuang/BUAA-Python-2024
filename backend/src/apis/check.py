import time

from generated import plagiarism_detection_pb2 as pb
from generated import plagiarism_detection_pb2_grpc as pb_grpc

from services.auth_service import verify_token
from services.check_service import CheckService
from services.storage_service import StorageService

from utils.error_codes import ErrorCode

class CheckServiceServicer(pb_grpc.CheckServiceServicer):
    def __init__(self):
        self.check_service = CheckService()
        self.storage_service = StorageService()
        
    def OneToManyCheck(self, request, context):
        token = request.token
        auth_status, user_id = verify_token(token)
        if not auth_status:
            return pb.OneToManyCheckResponse(status=ErrorCode.UNAUTHORIZED.value)
        task_name = request.task_name
        main_file_id = request.main_file_id
        file_ids = []
        for file_id in request.file_ids:
            file_status, owner_id = self.storage_service.get_file_owner(file_id)
            if not file_status:
                return pb.OneToManyCheckResponse(status=ErrorCode.FILE_NOT_FOUND.value)
            if owner_id != user_id:
                return pb.OneToManyCheckResponse(status=ErrorCode.UNAUTHORIZED.value)
            file_ids.append(file_id)
        task = self.check_service.create_task(0, user_id, task_name, main_file_id=main_file_id, file_ids=file_ids)
        if task is None:
            return pb.OneToManyCheckResponse(status=ErrorCode.UNKNOWN_ERROR.value)
        def generate_responses():
            yield pb.OneToManyCheckResponse(status=ErrorCode.SUCCESS.value)
            for file_id in file_ids:
                self.check_service.do_single_check(task, user_id, main_file_id, file_id)
                yield pb.OneToManyCheckResponse(empty=pb.Empty())
            self.check_service.finish_task(task)
            yield pb.OneToManyCheckResponse(task=task.toJson())
        return generate_responses()
            
    def ManyToManyCheck(self, request, context):
        token = request.token
        auth_status, user_id = verify_token(token)
        if not auth_status:
            return pb.ManyToManyCheckResponse(status=ErrorCode.UNAUTHORIZED.value)
        file_ids = []
        task_name = request.task_name   
        for file_id in request.file_ids:
            file_status, owner_id = self.storage_service.get_file_owner(file_id)
            if not file_status:
                return pb.ManyToManyCheckResponse(status=ErrorCode.FILE_NOT_FOUND.value)
            if owner_id != user_id:
                return pb.ManyToManyCheckResponse(status=ErrorCode.UNAUTHORIZED.value)
            file_ids.append(file_id)
        task = self.check_service.create_task(1, user_id, task_name, file_ids=file_ids)
        def generate_responses():
            yield pb.ManyToManyCheckResponse(status=ErrorCode.SUCCESS.value)
            matrix = [[0.0 for _ in range(len(file_ids))] for _ in range(len(file_ids))]
            for i in range(len(file_ids)):
                for j in range(i + 1, len(file_ids)):
                    matrix[i][j] = self.check_service.do_single_check(task, user_id, file_ids[i], file_ids[j])
                    yield pb.ManyToManyCheckResponse(empty=pb.Empty())
            self.check_service.finish_task(task, file_ids=file_ids, matrix=matrix)
            yield pb.ManyToManyCheckResponse(task=task.toJson())
        return generate_responses()
        
