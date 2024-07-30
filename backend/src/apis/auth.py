from datetime import datetime
import pytz

from generated import plagiarism_detection_pb2 as pb
from generated import plagiarism_detection_pb2_grpc as pb_grpc

from config import TIME_ZONE
from services.auth_service import AuthService, verify_token
from utils.error_codes import ErrorCode

class AuthServiceServicer(pb_grpc.AuthServiceServicer):
    def __init__(self):
        self.auth_service = AuthService()
    
    def Login(self, request, context):
        username = request.username
        password = request.password
        status, token = self.auth_service.login(username, password)
        return pb.LoginResponse(status=status.value, token=token)
    
    def Register(self, request, context):
        username = request.username
        password = request.password
        status = self.auth_service.register(username, password)
        return pb.RegisterResponse(status=status.value)
    
    def GetLoginHistory(self, request, context):
        token = request.token
        limit = request.limit
        auth_status, user_id = verify_token(token)
        if not auth_status:
            return pb.GetLoginHistoryResponse(status=ErrorCode.UNAUTHORIZED.value)
        try:
            records = []
            for h in self.auth_service.get_login_history(user_id, limit):
                local_time = datetime.strptime(h[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc).astimezone(pytz.timezone(TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
                records.append(pb.LoginRecord(login_time=local_time, success=h[1]))
            return pb.GetLoginHistoryResponse(status=ErrorCode.SUCCESS.value, record=records)
        except Exception as e:
            return pb.GetLoginHistoryResponse(status=ErrorCode.UNKNOWN_ERROR.value)