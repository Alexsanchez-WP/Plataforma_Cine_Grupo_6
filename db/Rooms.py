from db.IModel import IModel
from db.DBConexion import DBConexion
from markupsafe import escape


class Rooms(IModel, DBConexion):
    """ Modelo para los metodos de las consutlas """

    def __init__(self) -> None:
        conn = DBConexion()
        self.conn = conn.getConn()

    def view(self, id=None) -> list:
        """ Listar o ver un registro por ID"""
        try:
            query = f"SELECT * FROM sala"
            if(id):
                query += f" WHERE idSala = {escape(id)};"
            return self.conn.execute(query).fetchall()
        except Exception as m:
            return []

    def list(self) -> list:
        """ Listar o ver un registro por ID"""
        try:
            query = f"SELECT idSala as id, sala FROM sala"
            return self.conn.execute(query).fetchall()
        except Exception as m:
            return []

    def create(self, params) -> int:
        """Crear un registro"""
        pass

    def edit(self, params) -> int:
        """Editar los registros"""
        pass

    def delete(self, id) -> int:
        """Eliminar un registro"""
        pass
