from PyQt5.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

from utils.api_client import ApiClient
from utils.error_codes import UploadFileStatus, GetUploadedFileListStatus, DownloadFileStatus, DeleteFileStatus
from utils.file_handler import FileHandler
class FileUploadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.api_client = ApiClient()
        self.initUI()
        self.setAttribute(Qt.WA_QuitOnClose, True)

    def show(self, token):
        self.token = token
        self.updateList()
        self.file_handler = FileHandler()
        super().show()

    def initUI(self):
        self.resize(800, 600)
        layout = QVBoxLayout()
        self.select_button = QPushButton('Select Files')
        self.select_button.clicked.connect(self.selectFiles)
        # add a list
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['File ID', 'File Name', 'Size', 'Upload Time', 'Full Path'])
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.itemSelectionChanged.connect(self.onListItemSelected)
        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.downloadFile)
        self.download_button.setEnabled(False)
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.deleteFile)
        self.delete_button.setEnabled(False)
        layout.addWidget(self.select_button)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.download_button)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select files to upload")
        if files:
            self.startUpload(files)
            
    def startUpload(self, files):
        for file in files:
            status, file_id = self.api_client.upload_file(self.token, file)    
            if status == UploadFileStatus.SUCCESS:
                print(f"File {file} uploaded successfully with id {file_id}")
            else:
                print(f"Failed to upload file {file}", status.value[1])
            self.updateList()
                
    def updateList(self):
        status, file_list = self.api_client.get_uploaded_file_list(self.token)
        if status == GetUploadedFileListStatus.SUCCESS:
            self.tableWidget.setRowCount(0)
            for file in file_list:
                def add_file(file_id, file_path, size, upload_time):
                    if size < 1024:
                        size = f"{size} B"
                    elif size < 1024 * 1024:
                        size = f"{size / 1024:.2f} KB"
                    else:
                        size = f"{size / 1024 / 1024:.2f} MB"
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(str(file_id)))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(file_path.split('/')[-1]))
                    self.tableWidget.setItem(row, 2, QTableWidgetItem(size))
                    self.tableWidget.setItem(row, 3, QTableWidgetItem(upload_time))
                    self.tableWidget.setItem(row, 4, QTableWidgetItem(file_path))
                
                add_file(file[0], file[1], file[2], file[3])
    
    def onListItemSelected(self):
        if len(self.tableWidget.selectedItems()) > 0:
            self.download_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.download_button.setEnabled(False)
            self.delete_button.setEnabled(False)
        
    def downloadFile(self):
        if len(self.tableWidget.selectedItems()) == 0:
            return
        if len(self.tableWidget.selectedItems()) // 5 == 1:
            file_id = int(self.tableWidget.selectedItems()[0].text())
            file_name = self.tableWidget.selectedItems()[1].text()
            status, content = self.api_client.download_file(self.token, file_id)
            if status == DownloadFileStatus.SUCCESS:
                self.file_handler.write_file(file_id, file_name, content)
                print(f"File {file_name} downloaded successfully")
            else:
                print(f"Failed to download file {file_name}", status.value[1])
            return
        file_ids = []
        for i in range(0, len(self.tableWidget.selectedItems()), 5):
            file_id = int(self.tableWidget.selectedItems()[i].text())
            file_ids.append(file_id)
        status, content = self.api_client.download_multiple_files(self.token, file_ids)
        if status == DownloadFileStatus.SUCCESS:
            print(f"Files downloaded successfully")
        else:
            print(f"Failed to download file", status.value[1])
            
    def deleteFile(self):
        if len(self.tableWidget.selectedItems()) == 0:
            return
        for i in range(0, len(self.tableWidget.selectedItems()), 5):
            file_id = int(self.tableWidget.selectedItems()[i].text())
            status = self.api_client.delete_file(self.token, file_id)
            if status == DeleteFileStatus.SUCCESS:
                print(f"File {file_id} deleted successfully")
            else:
                print(f"Failed to delete file {file_id}", status.value[1])
        self.updateList()