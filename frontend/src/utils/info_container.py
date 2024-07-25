class InfoContainer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InfoContainer, cls).__new__(cls)
            cls._instance._initiated = False
        return cls._instance

    def __init__(self):
        if self._initiated:
            return
        super().__init__()
        self._initiated = True

        self.file_infos = {}
        # self.task_infos = {}

    def add_file_info(self, file_id, file_name, file_size, file_path, file_time):
        self.file_infos[file_id] = FileInfo(file_id, file_name, file_size, file_path, file_time)

    def get_file_info(self, file_id):
        return self.file_infos[file_id]


class FileInfo:
    def __init__(self, file_id, file_name, file_size, file_path, file_time):
        self.id = file_id
        self.name = file_name
        self.size = file_size
        self.path = file_path
        self.time = file_time
