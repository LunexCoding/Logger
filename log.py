import shutil
from pathlib import Path
import logging
import datetime

from apscheduler.schedulers.background import BackgroundScheduler


DEFAULT_LOG_DIR_PATH = "logs"
DEFAULT_LOG_FILENAME = "app.log"
DEFAULT_DATE_FORMAT = "%d-%b-%y %H:%M"
DEFAULT_LOG_FORMAT = "[%(asctime)s] -> %(name)s -> [%(levelname)s]: %(message)s"
DEFAULT_LOG_MODE = "a"
DEFAULT_INTERVAL = "days"
DEFAULT_INTERVAL_VALUE = 1
DEFAULT_BACKUP_COUNT = 3


class Logger:
    def __init__(self,
                 dateFormat=DEFAULT_DATE_FORMAT,
                 logFormat=DEFAULT_LOG_FORMAT,
                 mode=DEFAULT_LOG_MODE,
                 backupCount=DEFAULT_BACKUP_COUNT,
                 scheduleBackup=False,
                 intervalType=DEFAULT_INTERVAL,
                 intervalValue=DEFAULT_INTERVAL_VALUE
                 ):
        self._dateFormat = dateFormat
        self._logFormat = logFormat
        self._mode = mode
        self._backupCount = backupCount
        self._scheduleBackup = scheduleBackup
        self._intervalType = intervalType
        self._intervalValue = intervalValue
        self._defaultLogSettings = {
            "default": (DEFAULT_LOG_DIR_PATH, DEFAULT_LOG_FILENAME),
        }
        
        if self._scheduleBackup and self._intervalType:
            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(self.backupLogs, "interval", **{self._intervalType: self._intervalValue})
            self.scheduler.start()

    def setLogSettings(self, logName, dir=None, filename=None):
        if logName in self._defaultLogSettings:
            currentDir, currenFilename = self._defaultLogSettings[logName]
            if dir is not None:
                currentDir = dir
            if filename is not None:
                currenFilename = filename
            self._defaultLogSettings[logName] = (currentDir, currenFilename)
        else:
            self._defaultLogSettings[logName] = (dir or DEFAULT_LOG_DIR_PATH, filename or DEFAULT_LOG_FILENAME)

    def clearLogs(self):
        logDir = Path(DEFAULT_LOG_DIR_PATH)
        if logDir.exists():
            shutil.rmtree(logDir)

    def createLog(self, dir, filename):
        logDir = Path(dir)
        logDir.mkdir(exist_ok=True)
        logFile = logDir / filename
        return logFile

    def getLogger(self, loggerName, logName="default"):
        dir, filename = self._defaultLogSettings.get(logName, (DEFAULT_LOG_DIR_PATH, DEFAULT_LOG_FILENAME))
        logger = logging.getLogger(loggerName)
        if not logger.hasHandlers():
            logFile = self.createLog(dir, filename)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(self._getFileHandler(logFile))
        return logger

    def _getFileHandler(self, logFile):
        fileHandler = logging.FileHandler(logFile, encoding="utf-8", mode=self._mode)
        formatter = logging.Formatter(self._logFormat, self._dateFormat)
        fileHandler.setFormatter(formatter)
        return fileHandler

    def backupLogs(self):
        if not self._scheduleBackup:
            return

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        logDir = Path(DEFAULT_LOG_DIR_PATH)
        backupDir = logDir / today
        backupDir.mkdir(parents=True, exist_ok=True)
        
        for logFile in logDir.iterdir():
            if logFile.is_file():
                backupFilename = logFile.name
                backupFilePath = backupDir / backupFilename
                
                counter = 1
                while backupFilePath.exists():
                    backupFilename = f"{logFile.stem}_{counter}{logFile.suffix}"
                    backupFilePath = backupDir / backupFilename
                    counter += 1

                shutil.copy(logFile, backupFilePath)
                
                with logFile.open("w", encoding="utf-8") as file: ...
        
        backupDir = sorted([d for d in logDir.iterdir() if d.is_dir()], reverse=True)
        
        if len(backupDir) > self._backupCount:
            for oldBackupDir in backupDir[self._backupCount:]:
                shutil.rmtree(oldBackupDir)
    

logger = Logger()
