import queue
import threading
import sqlite3


class DatabaseService:
    def __init__(self, db_name):
        self.db_path = f"data/{db_name}.db"
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.worker, daemon=True)
        self.thread.start()

    def worker(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        while True:
            query, result_queue = self.queue.get()
            if query is None:
                break
            try:
                cursor.execute(query)
                conn.commit()
                result_queue.put(cursor.fetchall())
            except Exception as e:
                result_queue.put(e)
        conn.close()

    def query(self, query):
        result_queue = queue.Queue()
        self.queue.put((query, result_queue))
        result = result_queue.get()
        if isinstance(result, Exception):
            raise result
        return result

    def close(self):
        self.queue.put((None, None))
        self.thread.join()