"""
Author: Iz0
Date: 2024-07-16
License: MIT License
Description: 
"""

import hashlib
import grpc

import generated.plagiarism_detection_pb2 as pb
import generated.plagiarism_detection_pb2_grpc as pb_grpc

from utils.file_handler import read_file
from utils.error_codes import LoginStatus, RegisterStatus, UploadFileStatus
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
        
    def ping(self):
        try:
            response = self.ping_stub.Ping(pb.PingRequest(), timeout=5)
            return response.status == 1
        except grpc.RpcError:
            return False
    
    def login(self, username, password):
        try:
            response = self.auth_stub.Login(pb.LoginRequest(username=username, password=hash_password(password)))
            if response.status == LoginStatus.LOGIN_SUCCESS.value[0]:
                self.token = response.token
                return LoginStatus.LOGIN_SUCCESS, response.token
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
        
    def upload_file(self, token, file_path):
        filename = file_path.split('/')[-1]
        content = read_file(file_path)
        

    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()