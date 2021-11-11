from db.IModel import IModel
from db.DBConexion import DBConexion
from markupsafe import escape


class Roles(IModel, DBConexion):
    """ Modelo para los metodos de las consutlas """

    def __init__(self) -> None:
        conn = DBConexion()
        self.conn = conn.getConn()

    def view(self, id=None) -> list:
        """ Listar o ver un registro por ID"""
        try:
            query = f"SELECT * FROM rol"
            if(id):
                query += f" WHERE idRol = {escape(id)};"
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
