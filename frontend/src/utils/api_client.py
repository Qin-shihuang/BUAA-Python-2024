"""
Author: Iz0
Date: 2024-07-16
License: MIT License
Description: 
"""

import hashlib
import grpc
import time

import generated.plagiarism_detection_pb2 as pb
import generated.plagiarism_detection_pb2_grpc as pb_grpc

from utils.file_handler import FileHandler
from utils.error_codes import LoginStatus, RegisterStatus, UploadFileStatus, GetUploadedFileListStatus, DownloadFileStatus, DeleteFileStatus

from config import grpc_server_address


class ApiClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiClient, cls).__new__(cls)
            cls._instance._initiated = False
        return cls._instance
            
    def __init__(self):
        if self._initiated:
            return
        super().__init__()
        self._initiated = True
        
        channel = grpc.insecure_channel(grpc_server_address)
        self.ping_stub = pb_grpc.PingServiceStub(channel)
        self.auth_stub = pb_grpc.AuthServiceStub(channel)
        self.file_stub = pb_grpc.FileServiceStub(channel)
        self.token = None
        self.file_handler = None
    
    # MARK: - Ping
    def ping(self):
        try:
            response = self.ping_stub.Ping(pb.PingRequest(), timeout=5)
            return response.status == 1
        except grpc.RpcError:
            return False
    
    # MARK: - Auth
    def login(self, username, password):
        try:
            response = self.auth_stub.Login(pb.LoginRequest(username=username, password=hash_password(password)))
            if response.status == LoginStatus.SUCCESS.value[0]:
                self.token = response.token
                self.file_handler = FileHandler(username)
                return LoginStatus.SUCCESS, response.token
            else:
                return LoginStatus.from_value(response.status), ''
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return LoginStatus.NETWORK_ERROR, ''
            return LoginStatus.UNKNOWN_ERROR, ''
    
    def register(self, username, password) -> RegisterStatus:
        try:
            response = self.auth_stub.Register(pb.RegisterRequest(username=username, password=hash_password(password)))
            return RegisterStatus.from_value(response.status)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return RegisterStatus.NETWORK_ERROR
            return RegisterStatus.UNKNOWN_ERROR
        
    # MARK: - File
    def upload_file(self, token, file_path):
        content = FileHandler.read_file(file_path)
        
        def request_generator():
            try:
                CHUNK_SIZE = 4096
                metadata = pb.FileMetadata(token=token, file_path=file_path, size=len(content))
                yield pb.UploadFileRequest(metadata=metadata)
                for i in range(0, len(content), CHUNK_SIZE):
                    file_chunk = pb.FileChunk(data=content[i:i+CHUNK_SIZE])
                    yield pb.UploadFileRequest(chunk=file_chunk)
            except Exception as e:
                print(e)
        
        try:
            response = self.file_stub.UploadFile(request_generator())
            status = response.status
            if status == UploadFileStatus.SUCCESS.value[0]:
                return UploadFileStatus.SUCCESS, response.file_id
            else:
                return UploadFileStatus.from_value(status), -1
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return UploadFileStatus.NETWORK_ERROR, -1
            return UploadFileStatus.UNKNOWN_ERROR, -1       
    
    def get_uploaded_file_list(self, token):
        try:
            response = self.file_stub.GetUploadedFileList(pb.GetUploadedFileListRequest(token=token))
            status = response.status
            if status == GetUploadedFileListStatus.SUCCESS.value[0]:
                return GetUploadedFileListStatus.SUCCESS, [(file.id, file.file_path, file.size, file.uploaded_at) for file in response.files]
            else:
                return GetUploadedFileListStatus.from_value(status), []
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return UploadFileStatus.NETWORK_ERROR, []
            return UploadFileStatus.UNKNOWN_ERROR, []
        
    def download_file(self, token, file_id):
        try:
            responses = self.file_stub.DownloadFile(pb.DownloadFileRequest(token=token, file_id=file_id))
            status = None
            content = b''
            for resp in responses:
                if resp.HasField('status'):
                    status = resp.status
                    if status != DownloadFileStatus.SUCCESS.value[0]:
                        return DownloadFileStatus.from_value(status), b''
                elif resp.HasField('chunk'):
                    if status is None:
                        return DownloadFileStatus.UNKNOWN_ERROR, b''
                    content += resp.chunk.data
            return DownloadFileStatus.SUCCESS, content
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return DownloadFileStatus.NETWORK_ERROR, b''
            return DownloadFileStatus.UNKNOWN_ERROR, b''
    
    def download_multiple_files(self, token, file_ids):
        try:
            filename = f"{time.time()}.zip"
            responses = self.file_stub.DownloadMultipleFiles(pb.DownloadMultipleFilesRequest(token=token, file_ids=file_ids))
            status = None
            content = b''
            for resp in responses:
                if resp.HasField('status'):
                    status = resp.status
                    if status != DownloadFileStatus.SUCCESS.value[0]:
                        return DownloadFileStatus.from_value(status), b''
                elif resp.HasField('chunk'):
                    if status is None:
                        return DownloadFileStatus.UNKNOWN_ERROR, b''
                    content += resp.chunk.data
            self.file_handler.write_file('pack', filename, content)
            return DownloadFileStatus.SUCCESS, content
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return DownloadFileStatus.NETWORK_ERROR, b''
            return DownloadFileStatus.UNKNOWN_ERROR, b''
        
    def delete_file(self, token, file_id):
        try:
            response = self.file_stub.DeleteFile(pb.DeleteFileRequest(token=token, file_id=file_id))
            status = response.status
            if status == DeleteFileStatus.SUCCESS.value[0]:
                return DeleteFileStatus.SUCCESS
            else:
                return DeleteFileStatus.from_value(status)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return DeleteFileStatus.NETWORK_ERROR
            return DeleteFileStatus.UNKNOWN_ERROR
        

    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()