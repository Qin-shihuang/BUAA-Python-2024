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
from utils.error_codes import ErrorCode

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
        self.check_stub = pb_grpc.CheckServiceStub(channel)
        self.report_stub = pb_grpc.ReportServiceStub(channel)
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
            if response.status == ErrorCode.SUCCESS.value:
                self.token = response.token
                self.file_handler = FileHandler(username)
                return ErrorCode.SUCCESS
            else:
                return ErrorCode.from_value(response.status)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR
            return ErrorCode.UNKNOWN_ERROR
    
    def register(self, username, password) -> ErrorCode:
        try:
            response = self.auth_stub.Register(pb.RegisterRequest(username=username, password=hash_password(password)))
            return ErrorCode.from_value(response.status)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR
            return ErrorCode.UNKNOWN_ERROR
        
    def get_login_history(self, limit=1):
        try:
            response = self.auth_stub.GetLoginHistory(pb.GetLoginHistoryRequest(token=self.token, limit=limit))
            status = response.status
            if status == ErrorCode.SUCCESS.value:
                return ErrorCode.SUCCESS, [(login.login_time, login.success) for login in response.record]
            else:
                return ErrorCode.from_value(status), []
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, []
            return ErrorCode.UNKNOWN_ERROR, []
        
    # MARK: - File
    def upload_file(self, file_path):
        content = FileHandler.read_file(file_path)
        
        def request_generator():
            try:
                CHUNK_SIZE = 4096
                metadata = pb.FileMetadata(token=self.token, file_path=file_path, size=len(content))
                yield pb.UploadFileRequest(metadata=metadata)
                for i in range(0, len(content), CHUNK_SIZE):
                    file_chunk = pb.FileChunk(data=content[i:i+CHUNK_SIZE])
                    yield pb.UploadFileRequest(chunk=file_chunk)
            except Exception as e:
                print(e)
        
        try:
            response = self.file_stub.UploadFile(request_generator())
            status = response.status
            if status == ErrorCode.SUCCESS.value:
                return ErrorCode.SUCCESS, response.file_id
            else:
                return ErrorCode.from_value(status), -1
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, -1
            return ErrorCode.UNKNOWN_ERROR, -1       
    
    def get_uploaded_file_list(self):
        try:
            response = self.file_stub.GetUploadedFileList(pb.GetUploadedFileListRequest(token=self.token))
            status = response.status
            if status == ErrorCode.SUCCESS.value:
                return ErrorCode.SUCCESS, [(file.id, file.file_path, file.size, file.uploaded_at) for file in response.files]
            else:
                return ErrorCode.from_value(status), []
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, []
            return ErrorCode.UNKNOWN_ERROR, []
        
    def download_file(self, file_id):
        try:
            responses = self.file_stub.DownloadFile(pb.DownloadFileRequest(token=self.token, file_id=file_id))
            status = None
            content = b''
            for resp in responses:
                if resp.HasField('status'):
                    status = resp.status
                    if status != ErrorCode.SUCCESS.value:
                        return ErrorCode.from_value(status), b''
                elif resp.HasField('chunk'):
                    if status is None:
                        return ErrorCode.UNKNOWN_ERROR, b''
                    content += resp.chunk.data
            return ErrorCode.SUCCESS, content
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, b''
            return ErrorCode.UNKNOWN_ERROR, b''
    
    def download_multiple_files(self, file_ids):
        try:
            filename = f"{time.time()}.zip"
            responses = self.file_stub.DownloadMultipleFiles(pb.DownloadMultipleFilesRequest(token=self.token, file_ids=file_ids))
            status = None
            content = b''
            for resp in responses:
                if resp.HasField('status'):
                    status = resp.status
                    if status != ErrorCode.SUCCESS.value:
                        return ErrorCode.from_value(status), b''
                elif resp.HasField('chunk'):
                    if status is None:
                        return ErrorCode.UNKNOWN_ERROR, b''
                    content += resp.chunk.data
            self.file_handler.write_file('pack', filename, content)
            return ErrorCode.SUCCESS, content
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, b''
            return ErrorCode.UNKNOWN_ERROR, b''
        
    def delete_file(self, file_id):
        try:
            response = self.file_stub.DeleteFile(pb.DeleteFileRequest(token=self.token, file_id=file_id))
            status = response.status
            if status == ErrorCode.SUCCESS.value:
                return ErrorCode.SUCCESS
            else:
                return ErrorCode.from_value(status)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR
            return ErrorCode.UNKNOWN_ERROR

    # MARK: - Check
    def one_to_many_check(self, task_name, main_file_id, file_ids, signal):
        try:
            responses = self.check_stub.OneToManyCheck(pb.OneToManyCheckRequest(token=self.token, task_name=task_name, main_file_id=main_file_id, file_ids=file_ids))
            for resp in responses:
                if resp.HasField('status'):
                    status = resp.status
                    if status != ErrorCode.SUCCESS.value:
                        return ErrorCode.from_value(status), ''
                elif resp.HasField('empty'):
                    if signal:
                        signal.emit(0)
                elif resp.HasField('task'):
                    return ErrorCode.SUCCESS, resp.task
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, ''
            return ErrorCode.UNKNOWN_ERROR, ''
    
    def many_to_many_check(self, task_name, file_ids, signal):
        try:
            responses = self.check_stub.ManyToManyCheck(pb.ManyToManyCheckRequest(token=self.token, task_name=task_name, file_ids=file_ids))
            for resp in responses:
                if resp.HasField('status'):
                    status = resp.status
                    if status != ErrorCode.SUCCESS.value:
                        return ErrorCode.from_value(status), ''
                elif resp.HasField('empty'):
                    if signal:
                        signal.emit(0)
                elif resp.HasField('task'):
                    return ErrorCode.SUCCESS, resp.task
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, ''
            return ErrorCode.UNKNOWN_ERROR, ''
    
    # MARK: - Report
    def GetTaskList(self):
        try:
            response = self.report_stub.GetTaskList(pb.GetTaskListRequest(token=self.token))
            status = response.status
            if status == ErrorCode.SUCCESS.value:
                return ErrorCode.SUCCESS, [(task.id, task.task_name, task.type, task.main_file_id, task.file_count, task.created_at) for task in response.task_previews]
            else:
                return ErrorCode.from_value(status), []
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, []
            return ErrorCode.UNKNOWN_ERROR, []
        
    def GetTask(self, task_id):
        try:
            response = self.report_stub.GetTask(pb.GetTaskRequest(token=self.token, task_id=task_id))
            status = response.status
            if status == ErrorCode.SUCCESS.value:
                return ErrorCode.SUCCESS, response.task
            else:
                return ErrorCode.from_value(status), None
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, None
            return ErrorCode.UNKNOWN_ERROR, None
        
    def GetReport(self, report_id):
        try:
            response = self.report_stub.GetReport(pb.GetReportRequest(token=self.token, report_id=report_id))
            status = response.status
            if status == ErrorCode.SUCCESS.value:
                return ErrorCode.SUCCESS, response.report
            else:
                return ErrorCode.from_value(status), None
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR, None
            return ErrorCode.UNKNOWN_ERROR, None
        
    def UpdateReport(self, report_id, report):
        try:
            response = self.report_stub.UpdateReport(pb.UpdateReportRequest(token=self.token, report_id=report_id, report=report))
            status = response.status
            if status == ErrorCode.SUCCESS.value:
                return ErrorCode.SUCCESS
            else:
                return ErrorCode.from_value(status)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return ErrorCode.NETWORK_ERROR
            return ErrorCode.UNKNOWN_ERROR

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()