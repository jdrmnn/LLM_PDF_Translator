from .base import Database
from enum import Enum
from typing import Optional
from loguru import logger

# database_name = "pdf_translator_files.db"

class FileStatus(Enum):
    NOT_TRANSLATED = 0
    TRANSLATING = 1
    TRANSLATED = 2

class FileDatabase(Database):
    def __init__(
        self,
        database_name,
        table_name="pdf_translator_files",
        table_format={
            "file": str,
            "src_path": str,
            "target_path": str,
            "status": int,
        },
    ):
        super().__init__(database_name, table_name, table_format=table_format)
        self.check_table()
        self.clear_unfinished_files()

    def clear_unfinished_files(self):
        conn, c = self.new_cursor()
        c.execute(
            f"DELETE FROM {self.table_name} WHERE status = ?", (FileStatus.TRANSLATING.value,)
        )
        conn.commit()
        # delete NOT_TRANSLATED files
        c.execute(
            f"DELETE FROM {self.table_name} WHERE status = ?", (FileStatus.NOT_TRANSLATED.value,)
        )
        conn.commit()
        conn.close()
        
    def set_translating_to_not_translated(self):
        conn, c = self.new_cursor()
        c.execute(
            f"UPDATE {self.table_name} SET status = ? WHERE status = ?",
            (FileStatus.NOT_TRANSLATED.value, FileStatus.TRANSLATING.value),
        )
        conn.commit()
        conn.close()
        
    def set_translating(self, file: str):
        conn, c = self.new_cursor()
        while True:
            try:
                c.execute(
                    f"UPDATE {self.table_name} SET status = ? WHERE file = ?",
                    (FileStatus.TRANSLATING.value, file),
                )
                conn.commit()
                break
            except Exception as e:
                logger.error(f"Error updating {file} status to TRANSLATING: {e}")
                continue
        conn.close()
        
    def set_translated(self, file: str):
        conn, c = self.new_cursor()
        c.execute(
            f"UPDATE {self.table_name} SET status = ? WHERE file = ?",
            (FileStatus.TRANSLATED.value, file),
        )
        conn.commit()
        conn.close()

    def add_file(self, file, src_path, target_path, status: FileStatus | int):
        if isinstance(status, FileStatus):
            status = status.value
        conn, c = self.new_cursor()
        c.execute(
            f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?)",
            (file, src_path, target_path, status),
        )
        conn.commit()
        conn.close()
    
    def remove_file(self, file):
        conn, c = self.new_cursor()
        c.execute(f"DELETE FROM {self.table_name} WHERE file = ?", (file,))
        conn.commit()
        conn.close()

    def update_file_status(self, file, status):
        conn, c = self.new_cursor()
        c.execute(
            f"UPDATE {self.table_name} SET status = ? WHERE file = ?", (status, file)
        )
        conn.commit()
        conn.close()
    
    def get_files(self, status: Optional[FileStatus]):
        conn, c = self.new_cursor()
        if status is None:
            c.execute(f"SELECT * FROM {self.table_name}")
        else:
            c.execute(f"SELECT * FROM {self.table_name} WHERE status = ?", (status.value,))
        result = c.fetchall()
        conn.commit()
        conn.close()
        return result
    
    def check_file_exists(self, file):
        conn, c = self.new_cursor()
        c.execute(f"SELECT * FROM {self.table_name} WHERE file = ?", (file,))
        result = c.fetchone() is not None
        conn.commit()
        conn.close()
        return result