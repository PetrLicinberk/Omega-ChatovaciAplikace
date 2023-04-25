import mysql.connector
import mysql.connector.cursor as c

class DBConnection:
    _instance = None
    def __init__(self) -> None:
        self._connection = None
        self.address = None
        self.name = None
        self.user = None
        self.password = None
    
    def connect(self):
        '''
        Creates new connection to the database.

        :return: database connection
        '''
        connection = mysql.connector.connect(host=self.address, user=self.user, password=self.password, database=self.name)
        return connection

def get_instance():
    '''
    :return: DBConnection instance
    '''
    if type(DBConnection._instance) != DBConnection:
        DBConnection._instance = DBConnection()
    return DBConnection._instance

def get_cursor() -> tuple[mysql.connector.MySQLConnection, c.MySQLCursor]:
    '''
    Creates new connection to the database and new db cursor

    :return: database cursor
    '''
    connection: mysql.connector.MySQLConnection = get_instance().connect()
    cursor: c.MySQLCursor = connection.cursor()
    return connection, cursor