# Incluimos las referencias
from flask import Flask, render_template, request, session, flash
from markupsafe import escape
from werkzeug.utils import redirect
from formularios import Login, Registro
from db.bd_class import Users, Films

# Creamos el objeto Flask
app = Flask(__name__)
app.secret_key = '5%B7*WsYk^9#gXFo!bqxnL8TeBB%TBui*P6Y5UKW3XMe3mWi'


# Error 404
@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


# Construimos los decoradores :: Rutas
@app.route('/')
@app.route('/home/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    log = Login()
    if request.method == 'GET':
        return render_template('login.html', form=log)
    else:
        if log.validate_on_submit():
            user = escape(request.form['usuario'])
            password = escape(request.form['clave'])

            for User in Users:
                if(User['email'] == user.strip() and User['password'] == password.strip()):
                    session['user_data'] = User
                    if(User['role'] != 'customer'):
                        flash(
                            f"{User['name']}, Bienvenido al area administrativa")
                        return redirect('/admin/')
        flash("El correo o la contraseña no son validos")
        return render_template('login.html', form=log, title='Login')


@app.route('/recuperar-password/', methods=['GET', 'POST'])
def recuperar():
    if request == 'GET':
        return render_template('recuperacion.html')
    else:
        email = escape(request.form['idTxtEmailRecorey'])
        return f"Se han enviando los datos al correo {email}"


@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    reg = Registro()
    if request.method == 'GET':
        return render_template('registro.html', form=reg, title="Registro")
    else:
        if reg.validate_on_submit():
            nmbr = escape(request.form["nombre"])
            aplld = escape(request.form["apellido"])
            eml = escape(request.form["correo"])
            emlCnfrmr = escape(request.form["confirmar_correo"])
            psswrd = escape(request.form["clave"])
            psswrdCnfrmr = escape(request.form["confirmar_clave"])
            ncmnt = escape(request.form["nacimiento"])
            mncp = escape(request.form["municipio"])
            cdd = escape(request.form["ciudad"])
            drccn = escape(request.form["direccion"])
            tlfn = escape(request.form["telefono"])
            usr = escape(request.form["usuario"])
        return render_template('registro.html', form=reg, title="Registro")


@app.route('/tiquetes/', methods=['GET', 'POST'])
def tiquets():
    return render_template('tiquetes.html')


@app.route('/funciones/', methods=['GET', 'POST'])
def funciones():
    return render_template('funciones.html')


@app.route('/buscar-pelicula/', methods=['GET', 'POST'])
def buscarPelicula():
    return render_template('buscar_pelicula.html')


@app.route('/estrenos/', methods=['GET', 'POST'])
def proximosEstrenos():
    return render_template('estrenos.html')


@app.route('/cartelera/', methods=['GET', 'POST'])
def cartelera():
    return render_template('cartelera.html')


@app.route('/logout/')
def logout():
    if session.get('user_data'):
        session.pop('user_data', None)
    return redirect('/')


"""_______________ Admin Area _____________________"""


@app.route('/admin/')
def admin():
    if session.get('user_data'):
        if session.get('user_data')['role'] != 'customer':
            return render_template('admin/index.html')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/login/')


# administracion de Usuarios
@app.route('/admin/usuarios/')
def adminUsuarios():
    if session.get('user_data'):
        if session.get('user_data')['role'] == 'admin':
            return render_template('admin/usuarios/usuarios.html', users=Users)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/usuario/<string:id>')
def adminUsuarioVer(id=None):
    userDone = None
    if session.get('user_data') and session.get('user_data')['role'] == 'admin':
        if id != None:
            for user in Users:
                if user['ID'] == id:
                    userDone = user
        if userDone != None:
            return render_template('/admin/usuarios/usuario.html', user=userDone)
        else:
            flash("El usuario consultado no existe, por favor intente de nuevo")
            return redirect('/admin/usuarios/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/usuario/eliminar/<string:id>', methods=['POST'])
def adminUsuarioEliminar(id=None):
    userDone = False
    if session.get('user_data') and session.get('user_data')['role'] == 'admin':
        if id != None:
            for index, user in enumerate(Users):
                if user['ID'] == id:
                    del Users[index]
                    userDone = True
        if userDone:
            return redirect('/admin/usuarios/')
        else:
            flash("El usuario consultado no existe, por favor intente de nuevo")
            return redirect('/admin/usuarios/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/usuario/editar/<string:id>', methods=['POST'])
def adminUsuarioEditar(id=None):
    userDone = False
    if session.get('user_data') and session.get('user_data')['role'] == 'admin':
        if id != None:
            for user in Users:
                if user['ID'] == id:
                    user['name'] = request.form['nombre']
                    user['role'] = request.form['rol']
                    userDone = True
        if userDone:
            return render_template('admin/usuarios/usuarios.html', users=Users)
        else:
            flash("El usuario a editar no existe, por favor intente de nuevo")
            return redirect('/admin/usuarios/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


# Administracion de peliculas
@app.route('/admin/peliculas/')
def adminPeliculas():
    if session.get('user_data'):
        if session.get('user_data')['role'] != 'customer':
            return render_template('admin/peliculas/peliculas.html', films=Films)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
