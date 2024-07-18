from generated import plagiarism_detection_pb2 as pb
from generated import plagiarism_detection_pb2_grpc as pb_grpc

from services.auth_service import verify_token
from services.storage_service import StorageService

from utils.error_codes import UploadFileStatus as Status
class FileServiceServicer(pb_grpc.FileServiceServicer):
    def __init__(self):
        self.storage_service = StorageService()
        
    def UploadFile(self, request, context):
        CHUNK_SIZE = 4096
        user_id = None
        file_metadata = None
        file_content = b''
        try:
            for req in request:
                if req.HasField("metadata"):
                    file_metadata = req.metadata
                    token = file_metadata.token
                    if file_metadata.size > 2 * 1024 * 1024:
                        return pb.UploadFileResponse(status=Status.FILE_TOO_LARGE.value[0])
                    auth_status, auth_payload = verify_token(token)
                    if not auth_status:
                        return pb.UploadFileResponse(status=Status.UNAUTHORIZED.value[0])
                    else:
                        user_id = auth_payload
                elif req.HasField("chunk"):
                    if file_metadata is None:
                        return pb.UploadFileResponse(status=Status.BAD_REQUEST.value[0])
                    file_content += req.chunk.data        
        except Exception as e:
            return pb.UploadFileResponse(status=Status.UNKNOWN_ERROR.value[0])
        if len(file_content) != file_metadata.size:
            return pb.UploadFileResponse(status=Status.BAD_REQUEST.value[0])
        status, file_id = self.storage_service.save_file(user_id, file_metadata.filename, file_content)
        if status:
            return pb.UploadFileResponse(status=Status.UPLOAD_SUCCESS.value[0], file_id=file_id)
        else:
            return pb.UploadFileResponse(status=Status.UNKNOWN_ERROR.value[0])