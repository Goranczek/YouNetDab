import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger("main_file.connector")


class DatabaseSolver:
    def __init__(self, name, cfg):
        self.name = name
        logger.info(Path(cfg['Databases']['Path']).joinpath(name + ".db"))
        self.con: sqlite3 = sqlite3.connect(Path(cfg['Databases']['Path']).joinpath(name + ".db"))

    def reconnect_to_db(self):
        self.con: sqlite3 = sqlite3.connect(self.name + ".db")

    def disconnect_from_db(self):
        self.con.close()

    def test_connection(self):
        test = self.con.cursor()
        try:
            test.execute('select * from movies')
            logger.info("Connected to database.")

        except ConnectionError:
            logger.error("Cannot connect to database. Reconnecting")
            self.reconnect_to_db()

    def insert_movie(self, data: tuple):
        cur = self.con.cursor()
        cur.execute("INSERT INTO movies VALUES(?, ?, ?, ?, ?)", data)
        cur.close()
        self.con.commit()

    def insert_music(self, data: tuple):
        cur = self.con.cursor()
        cur.execute("INSERT INTO music VALUES(?, ?, ?, ?, ?, ?)", data)
        cur.close()
        self.con.commit()

    def create_table(self, name: str, table_col: tuple):
        cur = self.con.cursor()
        print(table_col)
        cur.execute(f"CREATE TABLE {name} {table_col}")
