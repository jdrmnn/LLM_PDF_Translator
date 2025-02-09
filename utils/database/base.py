# create a database to save (file, path, status)
# file: the name of the file
# path: the path of the file
# status: the status of the file (translated, not translated) -> True, False
import sqlite3

class Database:
    def __init__(self, database_name, table_name, table_format: dict):
        self.database = database_name
        self.table_name = table_name
        self.table_format = ""
        for key, value in table_format.items():
            if value == str:
                self.table_format += f"{key} text, "
            elif value == bool:
                self.table_format += f"{key} boolean, "
            elif value == int:
                self.table_format += f"{key} integer, "
            elif value == float:
                self.table_format += f"{key} real, "
            elif value == bytes:
                self.table_format += f"{key} blob, "
            else:
                print("Invalid data type")

    def new_cursor(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        conn = sqlite3.connect(self.database)
        return conn, conn.cursor()

    def check_table(self):
        # Check if the table exists
        conn, c = self.new_cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (self.table_name,),
        )
        if c.fetchone() is None:
            c.execute(
                f"""CREATE TABLE {self.table_name} ({self.table_format[:-2]})"""
            )
            conn.commit()
        conn.close()

    def delete_db(self):
        conn, c = self.new_cursor()
        c.execute(f"DROP TABLE {self.table_name}")
        conn.commit()
        conn.close()

    def recreate_db(
        self,
    ):
        # Check if the table exists
        conn, c = self.new_cursor()
        c.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.table_name,)
        )
        if c.fetchone() is not None:
            c.execute("DROP TABLE files")
        c.execute(
            f"""CREATE TABLE {self.table_name}
                        (file text, src_path text, target_path text, status boolean)"""
        )
        conn.commit()
        conn.close()
