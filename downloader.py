from pytube import YouTube
from Connectors.database_connector import DatabaseSolver
import datetime
import logging

logger = logging.getLogger("main_file.downloader")


def get_metadata(yt: YouTube = None, url: str = None) -> tuple:
    if yt is not None:
        return 1, yt.author, yt.title, yt.publish_date, yt.length, datetime.datetime.now()
    if url is not None:
        yt = YouTube(url)
        return 1, yt.author, yt.title, yt.publish_date, yt.length, datetime.datetime.now()
    logger.info("Empty metadata")
    return tuple()


class Downloader:
    def __init__(self, database):
        self.database = database

    def download_music(self, url: str) -> None:
        logger.info("Try to download music from %s", url)
        try:
            yt = YouTube(url)
            yt.streams.first().download()
            self.write_to_db(self.database, get_metadata(yt))
        except ConnectionError:
            logger.error("Download or write to db fcked up.")

    @staticmethod
    def write_to_db(database: DatabaseSolver, data: tuple) -> None:
        database.test_connection()
        database.insert_music(data)
