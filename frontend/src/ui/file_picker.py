from PyQt5.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from utils.api_client import ApiClient
from utils.error_codes import UploadFileStatus

class FileUploadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.api_client = ApiClient()
        self.initUI()
        self.setAttribute(Qt.WA_QuitOnClose, True)

    def show(self, token):
        self.token = token
        super().show()

    def initUI(self):
        self.setFixedSize(400, 500)
        layout = QVBoxLayout()
        self.select_button = QPushButton('Select Files')
        self.select_button.clicked.connect(self.selectFiles)
        layout.addWidget(self.select_button)
        self.setLayout(layout)

    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select files to upload")
        if files:
            self.startUpload(files)
            
    def startUpload(self, files):
        for file in files:
            status, file_id = self.api_client.upload_file(self.token, file)    
            if status == UploadFileStatus.UPLOAD_SUCCESS:
                print(f"File {file} uploaded successfully with id {file_id}")
            else:
                print(f"Failed to upload file {file}", status.value[1])