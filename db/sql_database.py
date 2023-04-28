import mysql.connector
from mysql.connector import errorcode

class SQLDataBase():
    def __init__(self):        
        pass

    def get_database(self):  
        # Database object
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="PixelDcs_Dc0",
            database="SQC"
        )
        db_cursor = mydb.cursor()
        return mydb
