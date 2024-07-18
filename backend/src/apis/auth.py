from generated import plagiarism_detection_pb2 as pb
from generated import plagiarism_detection_pb2_grpc as pb_grpc

from services.auth_service import AuthService

class AuthServiceServicer(pb_grpc.AuthServiceServicer):
    def __init__(self):
        self.auth_service = AuthService()
    
    def Login(self, request, context):
        username = request.username
        password = request.password
        status, token = self.auth_service.login(username, password)
        return pb.LoginResponse(status=status.value[0], token=token)
    
    def Register(self, request, context):
        username = request.username
        password = request.password
        status = self.auth_service.register(username, password)
        return pb.RegisterResponse(status=status.value[0])