# main.py

from modules.logging.logger import setup_logger, set_logging_level, logging
from modules.RSSFeedReaderUI import RSSFeedReaderUI
import tkinter as tk

set_logging_level(logging.DEBUG)  

logger = setup_logger('main')


if __name__ == "__main__":
    root = tk.Tk()
    app = RSSFeedReaderUI(root)
    root.mainloop()