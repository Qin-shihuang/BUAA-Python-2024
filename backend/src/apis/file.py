from generated import plagiarism_detection_pb2 as pb
from generated import plagiarism_detection_pb2_grpc as pb_grpc

class FileServiceServicer(pb_grpc.FileServiceServicer):
    def UploadFile(self, request, context):
        pass

    