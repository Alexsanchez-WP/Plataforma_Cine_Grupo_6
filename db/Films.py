from db.IModel import IModel
from markupsafe import escape
from db.DBConexion import DBConexion


class Films(IModel, DBConexion):
    """ Modelo para los metodos de las consutlas """

    def __init__(self) -> None:
        conn = DBConexion()
        self.conn = conn.getConn()

    def view(self, id=None) -> list:
        """ Listar o ver un registro por ID"""
        try:
            query = f"SELECT * FROM pelicula"
            if(id):
                query += f" WHERE idPelicula = {escape(id)};"
            data = self.conn.execute(query).fetchall()
            if (id and data):
                return data[0]
            return data
        except Exception as m:
            return []

    def create(self, params) -> int:
        """Crear un registro"""
        try:
            query = f"INSERT INTO pelicula ( nombre, actores, director, fkCategoria, descripcion, imagen, banner, trailer) VALUES (?,?,?,?,?,?,?,?)"
            datos = (params['nombre'], params['actores'], params['director'], params['categoria'], params['descripcion'],
                     params['imagen'], params['banner'], params['trailer'])
            data = self.conn.cursor()
            data = self.conn.execute(query, datos).rowcount
            if data != 0:
                self.conn.commit()
            return data
            pass
        except Exception as m:
            return 0

    def edit(self, params):
        """Editar los registros"""
        try:
            if params['id']:
                query = f"UPDATE pelicula SET nombre = ? , actores = ?, director = ?, fkCategoria = ?, descripcion = ?, trailer = ?"
                datos = (params['nombre'], params['actores'], params['director'], params['categoria'],
                         params['descripcion'], params['trailer'])

                if params['imagen']:
                    query += f", imagen = ?"
                    datos_list = list(datos)
                    datos_list.append(params['imagen'])
                    datos = tuple(datos_list)

                if params['banner']:
                    query += f", banner = ?"
                    datos_list = list(datos)
                    datos_list.append(params['banner'])
                    datos = tuple(datos_list)

                query += f" WHERE idPelicula = '{params['id']}'"

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
                query = f"DELETE FROM pelicula WHERE idPelicula = ?;"
                datos = (id)
                user = self.conn.cursor()
                user = self.conn.execute(query, datos).rowcount
                if user != 0:
                    self.conn.commit()
                return user
            return 0
        except Exception as m:
            return 0
