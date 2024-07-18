from generated import plagiarism_detection_pb2 as pb
from generated import plagiarism_detection_pb2_grpc as pb_grpc

class PingServiceServicer(pb_grpc.PingServiceServicer):
    def Ping(self, request, context):
        return pb.PingResponse(status=1)