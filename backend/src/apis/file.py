from generated import plagiarism_detection_pb2 as pb
from generated import plagiarism_detection_pb2_grpc as pb_grpc

from services.auth_service import verify_token
from services.storage_service import StorageService

from config import CHUNK_SIZE
from utils.error_codes import UploadFileStatus, GetUploadedFileListStatus, DownloadFileStatus, DeleteFileStatus
class FileServiceServicer(pb_grpc.FileServiceServicer):
    def __init__(self):
        self.storage_service = StorageService()
        
    def UploadFile(self, request, context):
        user_id = None
        file_metadata = None
        file_content = b''
        try:
            for req in request:
                if req.HasField("metadata"):
                    file_metadata = req.metadata
                    token = file_metadata.token
                    auth_status, auth_payload = verify_token(token)
                    if not auth_status:
                        return pb.UploadFileResponse(status=UploadFileStatus.UNAUTHORIZED.value[0])
                    else:
                        user_id = auth_payload
                    if file_metadata.size > 2 * 1024 * 1024:
                        return pb.UploadFileResponse(status=UploadFileStatus.FILE_TOO_LARGE.value[0])
                elif req.HasField("chunk"):
                    if file_metadata is None:
                        return pb.UploadFileResponse(status=UploadFileStatus.BAD_REQUEST.value[0])
                    file_content += req.chunk.data        
        except Exception as e:
            return pb.UploadFileResponse(status=UploadFileStatus.UNKNOWN_ERROR.value[0])
        if len(file_content) != file_metadata.size:
            return pb.UploadFileResponse(status=UploadFileStatus.BAD_REQUEST.value[0])
        status, file_id = self.storage_service.save_file(user_id, file_metadata.file_path, file_content)
        if status:
            return pb.UploadFileResponse(status=UploadFileStatus.SUCCESS.value[0], file_id=file_id)
        else:
            return pb.UploadFileResponse(status=UploadFileStatus.UNKNOWN_ERROR.value[0])
        
    def GetUploadedFileList(self, request, context):
        token = request.token
        auth_status, auth_payload = verify_token(token)
        if not auth_status:
            return pb.GetUploadedFileListResponse(status=GetUploadedFileListStatus.UNAUTHORIZED.value[0])
        else:
            user_id = auth_payload
        try:
            info_list = [pb.FileInfo(id=id, file_path=file_path, size=size, uploaded_at=uploaded_at) for id, file_path, size, uploaded_at in self.storage_service.get_file_list(user_id)]
            return pb.GetUploadedFileListResponse(status=GetUploadedFileListStatus.SUCCESS.value[0], files=info_list)
        except Exception as e:
            return pb.GetUploadedFileListResponse(status=GetUploadedFileListStatus.UNKNOWN_ERROR.value[0])
        
    def DownloadFile(self, request, context):
        token = request.token
        auth_status, auth_payload = verify_token(token)
        if not auth_status:
            return pb.DownloadFileResponse(status=DownloadFileStatus.UNAUTHORIZED.value[0])
        else:
            user_id = auth_payload
        file_id = request.file_id
        owner_status, owner_id = self.storage_service.get_file_owner(file_id)
        if not owner_status:
            return pb.DownloadFileResponse(status=DownloadFileStatus.FILE_NOT_FOUND.value[0])
        elif owner_id != user_id:
            return pb.DownloadFileResponse(status=DownloadFileStatus.UNAUTHORIZED.value[0])
        status, content = self.storage_service.get_file(file_id)
        if not status:
            return pb.DownloadFileResponse(status=DownloadFileStatus.FILE_NOT_FOUND.value[0])
        
        def generate_chunks():
            yield pb.DownloadFileResponse(status=DownloadFileStatus.SUCCESS.value[0])
            for i in range(0, len(content), CHUNK_SIZE):
                yield pb.DownloadFileResponse(chunk=pb.FileChunk(data=content[i:i+CHUNK_SIZE]))
        
        return generate_chunks()
    
    def DeleteFile(self, request, context):
        token = request.token
        auth_status, auth_payload = verify_token(token)
        if not auth_status:
            return pb.DeleteFileResponse(status=DeleteFileStatus.UNAUTHORIZED.value[0])
        else:
            user_id = auth_payload
        file_id = request.file_id
        owner_status, owner_id = self.storage_service.get_file_owner(file_id)
        if not owner_status:
            return pb.DeleteFileResponse(status=DeleteFileStatus.FILE_NOT_FOUND.value[0])
        elif owner_id != user_id:
            return pb.DeleteFileResponse(status=DeleteFileStatus.UNAUTHORIZED.value[0])
        if self.storage_service.delete_file(file_id):
            return pb.DeleteFileResponse(status=DeleteFileStatus.SUCCESS.value[0])
        else:
            return pb.DeleteFileResponse(status=DeleteFileStatus.UNKNOWN_ERROR.values[0])
    
    def DownloadMultipleFiles(self, request, context):
        token = request.token
        auth_status, auth_payload = verify_token(token)
        if not auth_status:
            return pb.DownloadMultipleFilesResponse(status=DownloadFileStatus.UNAUTHORIZED.value[0])
        else:
            user_id = auth_payload
        file_ids = []
        for file_id in request.file_ids:
            owner_status, owner_id = self.storage_service.get_file_owner(file_id)
            if not owner_status:
                return pb.DownloadMultipleFilesResponse(status=DownloadFileStatus.FILE_NOT_FOUND.value[0])
            elif owner_id != user_id:
                return pb.DownloadMultipleFilesResponse(status=DownloadFileStatus.UNAUTHORIZED.value[0])
            file_ids.append(file_id)
        content = self.storage_service.get_multiple_files_zip(file_ids)
        def generate_chunks():
            yield pb.DownloadMultipleFilesResponse(status=DownloadFileStatus.SUCCESS.value[0])
            for i in range(0, len(content), CHUNK_SIZE):
                yield pb.DownloadMultipleFilesResponse(chunk=pb.FileChunk(data=content[i:i+CHUNK_SIZE]))
        
        return generate_chunks()