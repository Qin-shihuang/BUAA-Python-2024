import os
import hashlib

from generated import plagiarism_detection_pb2_grpc
from generated import plagiarism_detection_pb2

from services.auth_service import AuthService
from services.storage_service import StorageService
from utils.error_codes import UploadFileStatus


class MainService(plagiarism_detection_pb2_grpc.PlagiarismDetectionServiceServicer):
    def __init__(self):
        self.auth_service = AuthService()
        self.storage_service = StorageService()

    def Ping(self, request, context):
        return plagiarism_detection_pb2.PingResponse(status=1)
    
    def Login(self, request, context):
        username = request.username
        password = request.password
        status, token = self.auth_service.login(username, password)
        return plagiarism_detection_pb2.LoginResponse(status=status.value[0], token=token)

    def Register(self, request, context):
        username = request.username
        password = request.password
        status = self.auth_service.register(username, password)
        return plagiarism_detection_pb2.RegisterResponse(status=status.value[0])

    def UploadFile(self, request, context):
        token = None
        user_id = None
        filename = None
        content = b''
        
        CHUNK_SIZE = 4096 # 4KB
        # Max file size: 2MB
        if len(request) > 512:
            return plagiarism_detection_pb2.UploadFileResponse(status=UploadFileStatus.FILE_TOO_LARGE.value[0])
        
        for i, chunk in enumerate(request):
            if i == 0:
                token = chunk.token
                auth_status, auth_payload = self.auth_service.verify_token(token)
                if auth_status:
                    user_id = auth_payload
                else:
                    return plagiarism_detection_pb2.UploadFileResponse(status=UploadFileStatus.UNAUTHORIZED.value[0])
                filename = chunk.filename
                chunk = chunk.content
            else:
                content += chunk.content
            
        if self.storage_service.save_file(user_id, filename, content):
            return plagiarism_detection_pb2.UploadFileResponse(status=UploadFileStatus.UPLOAD_SUCCESS.value[0])
        else:
            return plagiarism_detection_pb2.UploadFileResponse(status=UploadFileStatus.UNKNOWN_ERROR.value[0])