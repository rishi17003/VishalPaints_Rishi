import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'aloobhujiya'
    MYSQL_DB = 'vishalpaints'
    MYSQL_CURSORCLASS = 'DictCursor'
