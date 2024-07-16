import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal
import grpc

from utils.api_client import ApiClient
class ServerHealthChecker(QObject):
    server_status_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.api_client = ApiClient()
        self.is_running = False
        self.last_status = None
        self.check_interval = 5

    def start(self):
        self.is_running = True
        threading.Thread(target=self._run_check, daemon=True).start()

    def stop(self):
        self.is_running = False

    def _run_check(self):
        while self.is_running:
            try:
                status = self.api_client.ping()
            except grpc.RpcError:
                status = False

            if status != self.last_status:
                self.last_status = status
                self.server_status_changed.emit(status)

            time.sleep(self.check_interval)

