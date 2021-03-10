import sqlite3, random
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('char_brothers.db')
        return con
    except Error:
        print(Error)
