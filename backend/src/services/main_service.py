import os
import hashlib

from generated import plagiarism_detection_pb2_grpc
from generated import plagiarism_detection_pb2

from services.auth_service import AuthService
from services.storage_service import StorageService
from utils.error_codes import UploadFileStatus


class MainService(plagiarism_detection_pb2_grpc.PlagiarismDetectionServiceServicer):
    def __init__(self):
        self.storage_service = StorageService()
    

    def UploadFile(self, request, context):
        token = None
        user_id = None
        filename = None
        content = b''
        
        for chunk in request:
            if not token:
                token = chunk.token
                auth_status, auth_payload = self.auth_service.verify_token(token)
                if auth_status:
                    user_id = auth_payload
                else:
                    return plagiarism_detection_pb2.UploadFileResponse(status=UploadFileStatus.UNAUTHORIZED.value[0])
                filename = chunk.filename
            content += chunk.data
            
        if self.storage_service.save_file(user_id, filename, content):
            return plagiarism_detection_pb2.UploadFileResponse(status=UploadFileStatus.UPLOAD_SUCCESS.value[0])
        else:
            return plagiarism_detection_pb2.UploadFileResponse(status=UploadFileStatus.UNKNOWN_ERROR.value[0])