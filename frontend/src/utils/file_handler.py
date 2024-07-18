def read_file(file_path) -> bytes:
    with open(file_path, 'rb') as file:
        return file.read()