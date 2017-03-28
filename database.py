from psycopg2 import pool

class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1,
                                                          10,
                                                          **kwargs)

    @classmethod
    def getConnection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def userExist(cls, email):
        pass

    @classmethod
    def returnConnection(cls, connection):
        Database.__connection_pool.putconn(connection)

    @classmethod
    def closeAllConnections(cls):
        Database.__connection_pool.closeAll()


class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None
    def __enter__(self):
        self.connection = Database.getConnection()
        self.cursor = self.connection.cursor()
        return self.cursor
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.returnConnection(self.connection)