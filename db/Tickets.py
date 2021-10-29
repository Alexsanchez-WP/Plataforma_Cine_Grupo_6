from db.IModel import IModel
from db.DBConexion import DBConexion
from markupsafe import escape


class Tickets(IModel, DBConexion):
    """ Modelo para los metodos de las consutlas """

    def __init__(self) -> None:
        conn = DBConexion()
        self.conn = conn.getConn()

    def view(self, id=None) -> list:
        """ Listar o ver un registro por ID"""
        try:
            query = f"SELECT * FROM tiquetes as tq INNER JOIN funcion as fn ON fn.idFuncion = tq.fkFuncion"
            if(id):
                query += f" WHERE fkUsuario = {escape(id)};"
            return self.conn.execute(query).fetchall()
        except Exception as m:
            return 0

    def create(self, params) -> int:
        """Crear un registro"""
        try:
            query = "INSERT INTO tiquetes (fkUsuario, fkFuncion, horario, metodo) VALUES (?, ?, ?, ?)"
            datos = (params['usuario'], params['funcion'],
                     params['horario'], params['metodo'])
            data = self.conn.cursor()
            data = self.conn.execute(query, datos).rowcount
            if data != 0:
                self.conn.commit()
            return data
        except Exception as m:
            return 0

    def edit(self, params) -> int:
        """Editar los registros"""
        pass

    def delete(self, id) -> int:
        """Eliminar un registro"""
        pass
