import logging
from logging.handlers import RotatingFileHandler
import tkinter as tk
from modules.RSSFeedReaderUI import RSSFeedReaderUI  


logger = logging.getLogger('main.py')
log_filename = 'RSS.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

rotating_handler = RotatingFileHandler(
    log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


def adjust_logging_level(level):
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    logger.setLevel(levels.get(level, logging.WARNING))


if __name__ == "__main__":
    logger.info("Welcome to the RSS Reader!")  
    root = tk.Tk()
    app = RSSFeedReaderUI(root)
    root.mainloop()