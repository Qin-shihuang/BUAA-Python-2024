from generated import plagarism_detection_pb2_grpc
from generated import plagarism_detection_pb2

from services.auth_service import AuthService
from utils.error_codes import LoginStatus, RegisterStatus


class MainService(plagarism_detection_pb2_grpc.PlagarismDetectionServiceServicer):
    def __init__(self):
        self.auth_service = AuthService()

    def Ping(self, request, context):
        return plagarism_detection_pb2.PingResponse(status=1)
    
    def Login(self, request, context):
        username = request.username
        password = request.password
        status, token = self.auth_service.login(username, password)
        return plagarism_detection_pb2.LoginResponse(status=status.value[0], token=token)

    def Register(self, request, context):
        username = request.username
        password = request.password
        status = self.auth_service.register(username, password)
        return plagarism_detection_pb2.RegisterResponse(status=status.value[0])

    def UploadFile(self, request, context):
        return plagarism_detection_pb2.UploadFileResponse(token="1")
    
    def CheckTwoFiles(self, request, context):
        return plagarism_detection_pb2.CheckTwoFilesResponse(token="1")
        