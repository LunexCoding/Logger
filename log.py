import logging
import os


try:
    os.mkdir('logs')
except OSError:
    pass


class Logger:
    def __init__(self):
        self._logFile = os.path.join(os.path.abspath('logs'), 'app.log')
        print(self._logFile)
        self._logFormat = '[%(asctime)s] -> %(name)s -> [%(levelname)s]: %(message)s'
        self._dateFormat = '%d-%b-%y %H:%M'

    def getFileHandler(self):
        file_handler = logging.FileHandler(self._logFile, encoding='utf-8')
        formatter = logging.Formatter(self._logFormat, self._dateFormat)
        file_handler.setFormatter(formatter)
        return file_handler

    def getLogger(self, loggerName):
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.getFileHandler())
        return logger


logger = Logger()
