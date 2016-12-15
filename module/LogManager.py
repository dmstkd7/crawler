import logging
import logging.handlers

SAVE_LOG_HISTORY_PATH = './log/history.log'


class LogManager:
    def __init__(self):
        # logger 인스턴스를 생성 및 로그 레벨 설정
        self.logger = logging.getLogger("crumbs")
        self.logger.setLevel(logging.DEBUG)

        # formmater 생성
        self.formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        # fileHandler와 StreamHandler를 생성
        self.fileHandler = logging.FileHandler( SAVE_LOG_HISTORY_PATH )
        self.streamHandler = logging.StreamHandler()

        # handler에 fommater 세팅
        self.fileHandler.setFormatter(self.formatter)
        self.streamHandler.setFormatter(self.formatter)

        # Handler를 logging에 추가
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.streamHandler)


    def writeDebug(self, message):
        self.logger.debug(message)

    def writeInfo(self, message):
        self.logger.info(message)

    def writeWarning(self, message):
        self.logger.warning(message)

    def writeError(self, message):
        self.logger.error(message)

    def writeCritical(self, message):
        self.logger.critical(message)
