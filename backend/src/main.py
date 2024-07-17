import grpc
from concurrent import futures
import time
import signal
import sys

from generated import plagiarism_detection_pb2_grpc
from config import SERVER_PORT
from services.main_service import MainService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    plagiarism_detection_pb2_grpc.add_PlagiarismDetectionServiceServicer_to_server(MainService(), server)
    server.add_insecure_port(f'[::]:{SERVER_PORT}')
    server.start()
    print(f"Server started on port {SERVER_PORT}")
    
    def signal_handler(sig, frame):
        event = server.stop(30)
        event.wait(30)
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
