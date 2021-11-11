from werkzeug.security import check_password_hash
from db.DBConexion import DBConexion
from markupsafe import escape


class Auth(DBConexion):

    def __init__(self) -> None:
        conn = DBConexion()
        self.conn = conn.getConn()

    def login(self, email, password) -> list:
        try:
            query = f"SELECT * FROM usuario WHERE email = '{escape(email)}';"
            user = self.conn.execute(query).fetchall()
            if(user):
                if(check_password_hash(user[0][4], escape(password))):
                    return user[0]
            return False
        except Exception as m:
            return False

    def register():
        pass
