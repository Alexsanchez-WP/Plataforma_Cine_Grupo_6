import pickle
from db.IModel import IModel
from markupsafe import escape
from db.DBConexion import DBConexion


class Shows(IModel, DBConexion):
    """ Modelo para los metodos de las consutlas """

    def __init__(self) -> None:
        conn = DBConexion()
        self.conn = conn.getConn()

    def view(self, id=None, status=None) -> list:
        """ Listar o ver un registro por ID"""
        try:
            query = f"SELECT * FROM funcion as fs INNER JOIN pelicula as pl ON fs.fkPelicula = pl.idPelicula"
            if(id):
                query += f" AND fs.idFuncion = {escape(id)}"
            if(status):
                query += f" AND fs.estado = {escape(status)}"

            query += " INNER JOIN sala as sl ON fs.fkSala = sl.idSala; "

            data = self.conn.execute(query).fetchall()

            if (id and data):
                return data[0]
            return data
        except Exception as m:
            return []

    def create(self, params) -> int:
        """Crear un registro"""
        try:
            query = f"INSERT INTO funcion ( fkPelicula, hora, dia, fkSala, estado, duracion, edad) VALUES (?,?,?,?,?,?,?)"
            datos = (params['pelicula'], params['hora'], params['dia'], params['sala'],
                     params['estado'], params['duracion'], params['edad'])
            data = self.conn.cursor()
            data = self.conn.execute(query, datos).rowcount
            if data != 0:
                self.conn.commit()
            return data
        except Exception as m:
            return 0

    def edit(self, params):
        """Editar los registros"""
        try:
            if params['id']:
                query = f"UPDATE funcion SET hora = ? , dia = ?, estado = ?, duracion = ?, edad = ?, fkSala = ?, fkPelicula = ? WHERE idFuncion = ?"
                datos = (params['hora'], params['dia'], params['estado'], params['duracion'],
                         params['edad'], params['sala'], params['pelicula'], params['id'])

                data = self.conn.cursor()
                data = self.conn.execute(query, datos).rowcount
                if data != 0:
                    self.conn.commit()
                return datos
            return 0
        except Exception as m:
            return 0

    def timesUpdate(self, id, array):
        """Actuelizar los horarios"""
        try:
            if id:
                query = f"UPDATE funcion SET fechas = ? WHERE idFuncion = ?;"
                datos = (pickle.dumps(array), escape(id))
                data = self.conn.cursor()
                data = self.conn.execute(query, datos).rowcount
                if data != 0:
                    self.conn.commit()
                return datos
            return 0
        except Exception as m:
            return 0

    def delete(self, id) -> int:
        """Eliminar un registro"""
        try:
            if id:
                query = f"DELETE FROM funcion WHERE idFuncion = ?;"
                datos = ((id,))
                user = self.conn.cursor()
                user = self.conn.execute(query, datos).rowcount
                if user != 0:
                    self.conn.commit()
                return user
            return 0
        except Exception as m:
            return 0
