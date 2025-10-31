import mysql.connector
from mysql.connector import errorcode

def get_connection(host='localhost', user='root', password='35272114', database='cadastro_db'):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
