import sqlite3
from os.path import exists
from logging import getLoggerClass, Formatter
from logging.handlers import RotatingFileHandler

class Formats:
    BASIC_FMT = "%(asctime)s %(levelname)s %(message)s"
    FUNC_FMT = "%(asctime)s: %(levelname)s - %(funcName)s - %(message)s"
    LINE_NO_FMT = "%(asctime)s: %(levelname)s -%(lineno)d - %(message)s"


class Levels:
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    CRITICAL = 50

class Parameters:
    date: str
    time: str
    message: str
    level: str
    func_name: str = "NA"
    line_no: int = -1

    def to_tuple(cls):
        return (cls.date, cls.time, cls.level, cls.message, cls.func_name, cls.line_no)


class LogHandler(RotatingFileHandler):
    def __init__(self, name: str, target_file: str, fmt: str):
        super().__init__(target_file)

        if exists(target_file):
            self.rotation_filename(name)
            self.set_name(name=name)
            self.maxBytes = 2*10**8  # 200 MB
            self.backupCount = 10  # Maximum 10 files from a handler.

            self.fmt = Formatter(fmt)
            self.setFormatter(self.fmt)

        else:
            with open(target_file, "w") as target:
                target.close()


class LoggerService(getLoggerClass()):
    def __init__(self, fmt: str, target_file: str):
        super().__init__(__name__)

        self.default_handler = LogHandler('default', target_file, fmt)
        self.append_handler(self.default_handler)

        self.db_conn = None
        self.db_cursor = None
        self.target_file = target_file
        self.fmt = fmt
    
    def append_handler(self, handler: LogHandler):
        self.addHandler(handler)

    def convert_to_db(self, path_to_db: str):
        self.db_conn = sqlite3.connect(path_to_db)
        self.db_cursor = self.db_conn.cursor()
        self.cmd = "INSERT INTO LOGS VALUES (?, ?, ?, ?, ?, ?)"
        with open(self.target_file, "r") as file:
            data = file.readlines()

        pre_data = []
        params = Parameters()
        for i in range(0, len(data)):
            pre_data.append(data[i].split(' '))

        print(pre_data)

        for x in range(0, len(pre_data)):
            for y in range(0, len(pre_data[x])):
                params.date = pre_data[x][0]
                params.time = pre_data[x][1]
                params.level = pre_data[x][2]
            if self.fmt == Formats.BASIC_FMT:
                params.message = pre_data[x][3]
                params.func_name = "NA"
                params.line_no = -1

            elif self.fmt == Formats.FUNC_FMT:
                params.func_name = pre_data[x][3]
                params.message = pre_data[x][4]
                params.line_no = -1
            print(pre_data)
            self.db_conn.execute("INSERT INTO Logs (Date, Time, Level, Message, [Function Name], [Line No.]) VALUES (?, ?, ?, ?, ?, ?)", params.to_tuple())

        self.db_conn.commit()

