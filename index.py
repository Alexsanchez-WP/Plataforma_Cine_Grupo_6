# Incluimos las referencias
from flask import Flask, render_template, request, session, flash
from markupsafe import escape
from datetime import datetime
from werkzeug.utils import redirect, secure_filename
from formularios import Login, Registro, ActualizacionUsuarios, Pelicula, ActualizacionPelicula, Funcion
# from db.bd_class import Users, Films, ejecutar_query_accion, ejecutar_query_seleccion
from werkzeug.security import generate_password_hash, check_password_hash
from db.Auth import Auth
from db.Users import Users
from db.Roles import Roles
from db.Films import Films
from db.Shows import Shows
from db.Rooms import Rooms
from db.Categories import Categories

files_path = "static/uploads/"

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
# FIXME
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
            user = Auth().login(user, password)
            if(user):
                session['user_data'] = user
                if(user[12] != 1):
                    flash(f"Bienvenido al area administrativa {user[1]}")
                    return redirect('/admin/')
        flash(f"El correo o la contraseña no son validos")
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


@app.route('/funciones/')
def funciones():
    return render_template('funciones.html')


@app.route('/buscar-pelicula/<string:id>/')
# FIXME
def buscarPelicula(id=None):
    if not id:
        return redirect('/')
    film = Shows().view(id)
    time = datetime.fromisoformat(
        film[3] + ' ' + film[2]).strftime("%d %B, %Y - %I:%M %p")
    categories = Categories().view()
    shows = []
    if film[6]:
        list_shows = film[6].split(",")
        for show in list_shows:
            shows.append(datetime.fromisoformat(
                show).strftime("%d %B, %Y - %I:%M %p"))
    return render_template('buscar_pelicula.html', film=film, categories=categories, time=time, shows=shows)


@app.route('/estrenos/')
# FIXME
def proximosEstrenos():
    shows = Shows().view(None, '0')
    categories = Categories().view()
    return render_template('estrenos.html', shows=shows, categories=categories)


@app.route('/cartelera/')
# FIXME
def cartelera():
    shows = Shows().view(None, '1')
    categories = Categories().view()
    return render_template('cartelera.html', shows=shows, categories=categories)


@app.route('/logout/')
# FIXME
def logout():
    if session.get('user_data'):
        session.pop('user_data', None)
    return redirect('/')


"""_______________ Admin Area _____________________"""


@app.route('/admin/')
def admin():
    if session.get('user_data'):
        if session.get('user_data')[12] != 1:
            return render_template('admin/index.html')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/login/')

# administracion de Usuarios


@app.route('/admin/usuarios/')
def adminUsuarios():
    reg = Registro()
    if session.get('user_data'):
        if session.get('user_data')[12] == 3:
            users = Users().view()
            roles = Roles().view()
            return render_template('admin/usuarios/usuarios.html', users=users, roles=roles, form=reg)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/usuario/<string:id>')
def adminUsuarioVer(id):
    if session.get('user_data') and session.get('user_data')[12] == 3:
        if id != None:
            user = Users().view(id)
            roles = Roles().view()
            if user:
                return render_template('/admin/usuarios/usuario.html', user=user, roles=roles)
            else:
                flash("El usuario consultado no existe, por favor intente de nuevo")
                return redirect('/admin/usuarios/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/usuario/eliminar/<int:id>', methods=['POST'])
def adminUsuarioEliminar(id=None):
    if id > 1:
        if session.get('user_data') and session.get('user_data')[12] == 3:
            if id != None:
                user = Users().delete(escape(id))
            if user:
                return redirect('/admin/usuarios/')
            else:
                flash("El usuario consultado no existe, por favor intente de nuevo")
                return redirect('/admin/usuarios/')
        flash("No tiene permiso para ingresar a esta área")
        return redirect('/admin/')
    else:
        flash("El superadministrador no puede ser eliminado")
        return redirect('/admin/usuarios/')


@app.route('/admin/usuario/editar/<string:id>', methods=['POST'])
def adminUsuarioEditar(id=None):
    update = ActualizacionUsuarios()
    if not update.validate_on_submit():
        # TODO:
        params = {
            'id': escape(id.strip()),
            'nmbr': escape(request.form["nombre"].strip()),
            'aplld': escape(request.form["apellido"].strip()),
            'cdd': escape(request.form["ciudad"].strip()),
            'psswrd': escape(request.form["clave"].strip()),
            'mncp': escape(request.form["departamento"].strip()),
            'drccn': escape(request.form["direccion"].strip()),
            'rol': escape(request.form["rol"].strip()),
            'ncmnt': escape(request.form["nacimiento"].strip()),
            'tlfn': escape(request.form["telefono"].strip()),
        }

        if session.get('user_data') and session.get('user_data')[12] == 3:
            if id:
                user = Users().edit(params)
            if not user:
                flash(
                    f"Todos los campos marcados con '*' son obligatorios, por favor valide")
            return redirect('/admin/usuarios/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/usuario/save/', methods=['POST'])
def adminUsuarioCrear():
    reg = Registro(request.form)
    if session.get('user_data') and session.get('user_data')[12] == 3:
        if reg.validate_on_submit():
            params = {
                'nmbr': escape(request.form["nombre"].strip()),
                'aplld': escape(request.form["apellido"].strip()),
                'cdd': escape(request.form["ciudad"].strip()),
                'psswrd': escape(request.form["clave"].strip()),
                'mncp': escape(request.form["departamento"].strip()),
                'drccn': escape(request.form["direccion"].strip()),
                'rol': escape(request.form["rol"].strip()),
                'ncmnt': escape(request.form["nacimiento"].strip()),
                'tlfn': escape(request.form["telefono"].strip()),
                'email': escape(request.form["correo"].strip()),
            }
            user = Users().create(params)
            if user:
                flash(
                    f"Usuario creado de forma correcta")
                return redirect('/admin/usuarios/')
        flash(
            f"Todos los campos marcados con '*' son obligatorios, por favor valide")
        users = Users().view()
        roles = Roles().view()
        return render_template('admin/usuarios/usuarios.html', users=users, roles=roles, form=reg)
    flash(f"No tiene permiso para ingresar a esta área")
    return redirect('/admin/')

# Administracion de peliculas


@app.route('/admin/peliculas/')
def adminPeliculas():
    if session.get('user_data'):
        if session.get('user_data')[12] != 1:
            form = Pelicula()
            formUpdate = ActualizacionPelicula()
            films = Films().view()
            categories = Categories().view()
            return render_template('admin/peliculas/peliculas.html', films=films, form=form, formUpdate=formUpdate, categories=categories)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/pelicula/<string:id>')
def adminPeliculaVer(id):
    if session.get('user_data') and session.get('user_data')[12] != 1:
        if id != None:
            film = Films().view(escape(id))
            categories = Categories().view()
            if film:
                return render_template('/admin/peliculas/pelicula.html', film=film, categories=categories)
            else:
                flash("El usuario consultado no existe, por favor intente de nuevo")
                return redirect('/admin/peliculas/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/pelicula/save/', methods=['POST'])
def adminPeliculasCrear():
    if session.get('user_data'):
        if session.get('user_data')[12] != 1:
            form = Pelicula()
            formUpdate = ActualizacionPelicula()
            films = Films().view()
            categories = Categories().view()
            if form.validate_on_submit() and request.form["categoria"].strip():

                img = form.imagen.data
                img_name = secure_filename(img.filename)
                img_rute = files_path+img_name.replace(" ", "")
                img.save(img_rute)

                bnn = form.banner.data
                bnn_name = secure_filename(bnn.filename)
                bnn_rute = files_path+bnn_name.replace(" ", "")
                bnn.save(bnn_rute)

                params = {
                    'nombre': escape(request.form["nombre"].strip()),
                    'actores': escape(request.form["actores"].strip()),
                    'director': escape(request.form["director"].strip()),
                    'categoria': escape(request.form["categoria"].strip()),
                    'descripcion': escape(request.form["descripcion"].strip()),
                    'imagen': img_rute,
                    'banner': bnn_rute,
                    'trailer': escape(request.form["trailer"].strip()),
                }
                user = Films().create(params)
                if user:
                    flash(
                        f"La pelicula fue creada de forma correcta")
                    return redirect('/admin/peliculas/')
            flash(
                f"Todos los campos marcados con '*' son obligatorios, por favor valide")
            return render_template('admin/peliculas/peliculas.html', films=films, form=form, formUpdate=formUpdate, categories=categories)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/pelicula/eliminar/<int:id>', methods=['POST'])
def adminPeliculaEliminar(id=None):
    if session.get('user_data') and session.get('user_data')[12] != 1:
        if id != None:
            user = Films().delete(escape(id))
            if user:
                return redirect('/admin/peliculas/')
            else:
                flash("La pelicula no existe, por favor intente de nuevo")
                return redirect('/admin/peliculas/')
        flash("No tiene permiso para ingresar a esta área")
        return redirect('/admin/')
    else:
        flash("El superadministrador no puede ser eliminado")
        return redirect('/admin/peliculas/')


@app.route('/admin/pelicula/editar/<string:id>', methods=['POST'])
def adminPeliculaEditar(id=None):
    if session.get('user_data'):
        if session.get('user_data')[12] != 1:
            form = Pelicula()
            films = Films().view()
            categories = Categories().view()

            if id and request.form["nombre"].strip() and request.form["actores"].strip() and request.form["director"].strip() and request.form["categoria"].strip() and request.form["descripcion"].strip() and request.form["trailer"].strip():

                img_rute = None
                bnn_rute = None

                if request.files["imagen"].filename:
                    img = request.files["imagen"]
                    img_name = secure_filename(img.filename)
                    img_rute = files_path+img_name.replace(" ", "")
                    img.save(img_rute)

                if request.files["banner"].filename:
                    bnn = request.files["banner"]
                    bnn_name = secure_filename(bnn.filename)
                    bnn_rute = files_path+bnn_name.replace(" ", "")
                    bnn.save(bnn_rute)

                params = {
                    'id': escape(id),
                    'nombre': escape(request.form["nombre"].strip()),
                    'actores': escape(request.form["actores"].strip()),
                    'director': escape(request.form["director"].strip()),
                    'categoria': escape(request.form["categoria"].strip()),
                    'descripcion': escape(request.form["descripcion"].strip()),
                    'imagen': img_rute,
                    'banner': bnn_rute,
                    'trailer': escape(request.form["trailer"].strip()),
                }
                data = Films().edit(params)
                if data:
                    flash(
                        f"La pelicula fue editada de forma correcta")
                    return redirect('/admin/peliculas/')
            flash(
                f"Todos los campos marcados con '*' son obligatorios, por favor valide")
            return render_template('admin/peliculas/peliculas.html', films=films, form=form, categories=categories)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')

# Administracion de funciones


@app.route('/admin/funciones/')
# FIXME
def adminFunciones():
    if session.get('user_data'):
        if session.get('user_data')[12] != 1:
            form = Funcion()
            shows = Shows().view()
            films = Films().list()
            rooms = Rooms().view()
            return render_template('admin/funciones/funciones.html', films=films, form=form,  shows=shows, rooms=rooms)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/funcion/<string:id>')
def adminFuncionVer(id):
    if session.get('user_data') and session.get('user_data')[12] != 1:
        if id != None:
            film = Films().view(escape(id))
            categories = Categories().view()
            if film:
                return render_template('/admin/funciones/funcion.html', film=film, categories=categories)
            else:
                flash("El usuario consultado no existe, por favor intente de nuevo")
                return redirect('/admin/funciones/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/funcion/save/', methods=['POST'])
def adminFuncioneCrear():
    if session.get('user_data'):
        if session.get('user_data')[12] != 1:

            form = Funcion()
            shows = Shows().view()
            films = Films().list()
            rooms = Rooms().view()
            if form.validate_on_submit() and request.form["pelicula"]:

                params = {
                    'hora': escape(request.form["hora"].strip()),
                    'dia': escape(request.form["dia"].strip()),
                    'estado': escape(request.form["estado"].strip()),
                    'sala': escape(request.form["sala"].strip()),
                    'pelicula': escape(request.form["pelicula"].strip()),
                    'duracion': escape(request.form["duracion"].strip()),
                    'edad': escape(request.form["edad"].strip()),
                }
                data = Shows().create(params)
                if data:
                    flash(
                        f"La funcion fue creada de forma correcta")
                    return redirect('/admin/funciones/')
            flash(
                f"Todos los campos marcados con '*' son obligatorios, por favor valide")
            return render_template('admin/funciones/funciones.html', films=films, form=form,  shows=shows, rooms=rooms)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/funcion/eliminar/<int:id>', methods=['POST'])
# FIXME
def adminFuncionEliminar(id=None):
    if session.get('user_data') and session.get('user_data')[12] != 1:
        if id != None:
            show = Shows().delete(escape(id))
            if show:
                return redirect('/admin/funciones/')
            else:
                flash("La funcion no existe, por favor intente de nuevo")
                return redirect('/admin/funciones/')
        flash("No tiene permiso para ingresar a esta área")
        return redirect('/admin/')
    else:
        flash("El superadministrador no puede ser eliminado")
        return redirect('/admin/funciones/')


@app.route('/admin/pelicula/editar/<string:id>', methods=['POST'])
def adminFuncionEditar(id=None):
    if session.get('user_data'):
        if session.get('user_data')[12] != 1:
            form = Pelicula()
            films = Films().view()
            categories = Categories().view()

            if id and request.form["nombre"].strip() and request.form["actores"].strip() and request.form["director"].strip() and request.form["categoria"].strip() and request.form["descripcion"].strip() and request.form["trailer"].strip():

                img_rute = None
                bnn_rute = None

                if request.files["imagen"].filename:
                    img = request.files["imagen"]
                    img_name = secure_filename(img.filename)
                    img_rute = files_path+img_name.replace(" ", "")
                    img.save(img_rute)

                if request.files["banner"].filename:
                    bnn = request.files["banner"]
                    bnn_name = secure_filename(bnn.filename)
                    bnn_rute = files_path+bnn_name.replace(" ", "")
                    bnn.save(bnn_rute)

                params = {
                    'id': escape(id),
                    'nombre': escape(request.form["nombre"].strip()),
                    'actores': escape(request.form["actores"].strip()),
                    'director': escape(request.form["director"].strip()),
                    'categoria': escape(request.form["categoria"].strip()),
                    'descripcion': escape(request.form["descripcion"].strip()),
                    'imagen': img_rute,
                    'banner': bnn_rute,
                    'trailer': escape(request.form["trailer"].strip()),
                }
                data = Films().edit(params)
                if data:
                    flash(
                        f"La pelicula fue editada de forma correcta")
                    return redirect('/admin/peliculas/')
            flash(
                f"Todos los campos marcados con '*' son obligatorios, por favor valide")
            return render_template('admin/peliculas/peliculas.html', films=films, form=form, categories=categories)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
