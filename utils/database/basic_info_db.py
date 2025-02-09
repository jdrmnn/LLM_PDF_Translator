from .base import Database
from loguru import logger

class BasicInfoDatabase(Database):
    def __init__(
        self,
        database_name,
        table_name="basic_info",
        table_format={
            "key": str,
            "value": str
        }
    ):
        super().__init__(database_name, table_name, table_format=table_format)
        self.check_table()

    def get_value(self, key: str):
        conn, c = self.new_cursor()
        c.execute(
            f"SELECT value FROM {self.table_name} WHERE key = ?", (key,)
        )
        value = c.fetchone()
        conn.commit()
        conn.close()
        logger.info(f"The value of {key} is {value}")
        if value:
            return value[0]
        return None
    
    def update_value(self, key: str, value: str):
        conn, c = self.new_cursor()
        c.execute(
            f"UPDATE {self.table_name} SET value = ? WHERE key = ?",
            (value, key),
        )
        conn.commit()
        conn.close()
        logger.info(f"Updated {key} to {value}")

    def set_value(self, key: str, value: str):
        conn, c = self.new_cursor()
        c.execute(
            f"INSERT INTO {self.table_name} VALUES (?, ?)",
            (key, value),
        )
        conn.commit()
        conn.close()
        logger.info(f"Set {key} to {value}")