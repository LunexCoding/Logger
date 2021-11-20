import logging
import os

class Log:
    def __init__(self):
        try:
            os.mkdir('./logs')
            os.chdir('./logs')
        except OSError:
            os.chdir('./logs')

    def getLogger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('app.log')
        fh.setLevel(logging.DEBUG)

        logFormat = '[%(asctime)s] -> %(name)s -> [%(levelname)s]: %(message)s'
        dateFormat = '%d-%b-%y %H:%M'

        formatter = logging.Formatter(logFormat, dateFormat)

        fh.setFormatter(formatter)

        logger.addHandler(fh)
        return logger

logger = Log()