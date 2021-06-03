from Connectors.database_connector import DatabaseSolver
from downloader import Downloader
import logging
import configparser
import os
import pathlib

logger = logging.getLogger("main_file")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("process.log")
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    path = pathlib.Path(".")
    cfg.read(path.joinpath("config.cfg"))
    url_add = str(input("Add input to download"))
    db = DatabaseSolver("Arts", cfg)
    dwndlr = Downloader(db)
    dwndlr.download_music(url_add)
