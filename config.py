import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'rishi@271'
    MYSQL_DB = 'vishal_db1'
    MYSQL_CURSORCLASS = 'DictCursor'
