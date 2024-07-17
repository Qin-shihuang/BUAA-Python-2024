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
        print(status)
        if status == LoginStatus.LOGIN_SUCCESS:
            return plagarism_detection_pb2.LoginResponse(token=token, status = plagarism_detection_pb2.LOGIN_SUCCESS)
        elif status == LoginStatus.INVALID_CREDENTIALS:
            return plagarism_detection_pb2.LoginResponse(token="", status = plagarism_detection_pb2.LOGIN_INVALID_CREDENTIALS)
        else:
            return plagarism_detection_pb2.LoginResponse(token="", status = plagarism_detection_pb2.LOGIN_UNKNOWN_ERROR)

    def Register(self, request, context):
        username = request.username
        password = request.password
        status = self.auth_service.register(username, password)
        if status == RegisterStatus.REGISTER_SUCCESS:
            return plagarism_detection_pb2.RegisterResponse(status = plagarism_detection_pb2.REGISTER_SUCCESS)
        elif status == RegisterStatus.USERNAME_TAKEN:
            return plagarism_detection_pb2.RegisterResponse(status = plagarism_detection_pb2.REGISTER_USERNAME_INVALID)
        elif status == RegisterStatus.PASSWORD_INVALID:
            return plagarism_detection_pb2.RegisterResponse(status = plagarism_detection_pb2.REGISTER_PASSWORD_INVALID)
        elif status == RegisterStatus.USERNAME_INVALID:
            return plagarism_detection_pb2.RegisterResponse(status = plagarism_detection_pb2.REGISTER_USERNAME_INVALID)
        else:
            return plagarism_detection_pb2.RegisterResponse(status = plagarism_detection_pb2.REGISTER_UNKNOWN_ERROR)

    def UploadFile(self, request, context):
        return plagarism_detection_pb2.UploadFileResponse(token="1")
    
    def CheckTwoFiles(self, request, context):
        return plagarism_detection_pb2.CheckTwoFilesResponse(token="1")
        