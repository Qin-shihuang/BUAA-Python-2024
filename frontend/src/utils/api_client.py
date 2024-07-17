"""
Author: Iz0
Date: 2024-07-16
License: MIT License
Description: 
"""

import hashlib
import grpc

import generated.plagiarism_detection_pb2 as plagiarism_detection_pb2
import generated.plagiarism_detection_pb2_grpc as plagiarism_detection_pb2_grpc

from utils.error_codes import LoginStatus, RegisterStatus
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
        self.stub = plagiarism_detection_pb2_grpc.PlagiarismDetectionServiceStub(channel)
        self.token = None
        
    def ping(self):
        try:
            response = self.stub.Ping(plagiarism_detection_pb2.PingRequest(), timeout=5)
            return response.status == 1
        except grpc.RpcError:
            return False
    
    def login(self, username, password):
        try:
            response = self.stub.Login(plagiarism_detection_pb2.LoginRequest(username=username, password=hash_password(password)))
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
            response = self.stub.Register(plagiarism_detection_pb2.RegisterRequest(username=username, password=hash_password(password)))
            return RegisterStatus.from_value(response.status)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return RegisterStatus.NETWORK_ERROR
            return RegisterStatus.UNKNOWN_ERROR
    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()