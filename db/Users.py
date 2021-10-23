from db.IModel import IModel
from markupsafe import escape
from db.DBConexion import DBConexion
from werkzeug.security import generate_password_hash


class Users(IModel, DBConexion):
    """ Modelo para los metodos de las consutlas """

    def __init__(self) -> None:
        conn = DBConexion()
        self.conn = conn.getConn()

    def view(self, id=None) -> list:
        """ Listar o ver un registro por ID"""
        try:
            query = f"SELECT * FROM usuario"
            if(id):
                query += f" WHERE id = {escape(id)};"
            data = self.conn.execute(query).fetchall()
            if (id and data):
                return data[0]
            return data
        except Exception as m:
            return []

    def create(self, params) -> int:
        """Crear un registro"""
        try:
            query = f"INSERT INTO usuario ( nombres, apellidos, email, fechaNacimiento, departamento, ciudad, direccion, telefono, clave, fkRol) VALUES (?,?,?,?,?,?,?,?,?,?)"
            datos = (params['nmbr'], params['aplld'], params['email'], params['ncmnt'], params['mncp'],
                     params['cdd'], params['drccn'], params['tlfn'],
                     generate_password_hash(params['psswrd']), params['rol'])
            user = self.conn.cursor()
            user = self.conn.execute(query, datos).rowcount
            if user != 0:
                self.conn.commit()
            return user
        except Exception as m:
            return 0

    def edit(self, params):
        """Editar los registros"""
        try:
            if params['id']:
                query = f"UPDATE usuario SET nombres = ? , apellidos = ?, fechaNacimiento = ?, departamento = ?, ciudad = ?, direccion = ?, telefono = ?, fkRol = ?"
                datos = (params['nmbr'], params['aplld'], params['ncmnt'], params['mncp'],
                         params['cdd'], params['drccn'], params['tlfn'], params['rol'])
                if params['psswrd']:
                    query += f", clave = ?;"
                    datos = (params['nmbr'], params['aplld'], params['ncmnt'], params['mncp'],
                             params['cdd'], params['drccn'], params['tlfn'], params['rol'], generate_password_hash(params['psswrd']))
                query += f" WHERE id = {params['id']}"
                user = self.conn.cursor()
                user = self.conn.execute(query, datos).rowcount
                if user != 0:
                    self.conn.commit()
                return user
            return 0
        except Exception as m:
            return 0

    def delete(self, id) -> int:
        """Eliminar un registro"""
        try:
            if id:
                query = f"DELETE FROM usuario WHERE id = ?;"
                datos = (id)
                user = self.conn.cursor()
                user = self.conn.execute(query, datos).rowcount
                if user != 0:
                    self.conn.commit()
                return user
            return 0
        except Exception as m:
            return 0
