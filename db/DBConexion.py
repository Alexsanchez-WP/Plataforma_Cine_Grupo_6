import sqlite3


class DBConexion:
    """Conexion a labase de datos"""

    def __init__(self, host='db/bd_cinema.db', password='', user_db='', name_db='') -> None:

        self.host = host
        self.password = password
        self.user_db = user_db
        self.name_db = name_db
        self.__conn = None

        try:
            if not self.__conn:
                with sqlite3.connect(self.host) as con:
                    self.__conn = con
        except Exception as ex:
            self.__conn = None

    def getConn(self) -> list:
        """Retorna la conexion"""
        return self.__conn
