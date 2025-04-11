import logging
import os
import sys


class DirectoryFilter(logging.Filter):
    def filter(self, record):
        pathname = record.pathname
        dirpath = os.path.dirname(pathname)
        record.dirname = os.path.basename(dirpath)
        if not record.dirname:
            record.dirname = '.'
        return True
    

def configure_logging(level=logging.INFO):
    log_format = "[%(asctime)s.%(msecs)03d] %(dirname)s/%(module)s:%(lineno)d %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logger = logging.getLogger()
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(log_format, datefmt=date_format)
        handler.setFormatter(formatter)
        dir_filter = DirectoryFilter()
        handler.addFilter(dir_filter)
        logger.addHandler(handler)