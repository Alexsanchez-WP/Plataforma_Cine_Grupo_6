# Incluimos las referencias
import pickle
from flask import Flask, render_template, request, session, flash
from markupsafe import escape
from datetime import datetime
from werkzeug.utils import redirect, secure_filename
from formularios import Login, Registro, Pelicula, Funcion
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
                else:
                    return redirect('/')
        flash(f"El correo o la contraseña no son validos")
        return render_template('login.html', form=log, title='Login')


@app.route('/recuperar-password/', methods=['GET', 'POST'])
# TODO
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
            params = {
                'nmbr': escape(request.form["nombre"].strip()),
                'aplld': escape(request.form["apellido"].strip()),
                'cdd': escape(request.form["ciudad"].strip()),
                'psswrd': escape(request.form["clave"].strip()),
                'mncp': escape(request.form["departamento"].strip()),
                'drccn': escape(request.form["direccion"].strip()),
                'rol': 1,
                'ncmnt': escape(request.form["nacimiento"].strip()),
                'tlfn': escape(request.form["telefono"].strip()),
                'email': escape(request.form["correo"].strip()),
            }

            user = Users().create(params)
            if not user:
                flash(
                    "Por vafor valide los datos, si el usuario ya se encuentra registrado haga click en iniciar sesión")
                return render_template('registro.html', form=reg, title="Registro")

            user = Auth().login(params['email'], params['psswrd'])
            if(user):
                session['user_data'] = user
                return redirect('/')
        flash("Por favor valide que todos los datos sean correctos")
        return render_template('registro.html', form=reg, title="Registro")


@app.route('/tiquetes/', methods=['GET', 'POST'])
# TODO:
def tiquets():
    return render_template('tiquetes.html')


@app.route('/funciones/')
# TODO:
def funciones():
    return render_template('funciones.html')


@app.route('/buscar-pelicula/<string:id>/')
def buscarPelicula(id=None):
    if not id:
        return redirect('/')
    film = Shows().view(id)
    categories = Categories().view()
    time = datetime.fromisoformat(
        film[3] + ' ' + film[2]).strftime("%d %B, %Y - %I:%M %p")
    shows = []
    if film[6]:
        shows = [datetime.fromisoformat(i).strftime(
            "%d %B, %Y - %I:%M %p") for i in pickle.loads(film[6])]
    return render_template('buscar_pelicula.html', film=film, categories=categories, time=time, shows=shows)


@app.route('/estrenos/')
def proximosEstrenos():
    shows = Shows().view(None, '0')
    categories = Categories().view()
    return render_template('estrenos.html', shows=shows, categories=categories)


@app.route('/cartelera/')
def cartelera():
    shows = Shows().view(None, '1')
    categories = Categories().view()
    return render_template('cartelera.html', shows=shows, categories=categories)


@app.route('/logout/')
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
                user = Users().delete(id)
            if user:
                return redirect('/admin/usuarios/')
            else:
                flash(
                    "El usuario consultado no existe, por favor intente de nuevo")
                return redirect('/admin/usuarios/')
        flash("No tiene permiso para ingresar a esta área")
        return redirect('/admin/')
    else:
        flash("El superadministrador no puede ser eliminado")
        return redirect('/admin/usuarios/')


@app.route('/admin/usuario/editar/<string:id>', methods=['POST'])
def adminUsuarioEditar(id=None):
    if session.get('user_data') and session.get('user_data')[12] == 3:
        if id:
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
            films = Films().view()
            categories = Categories().view()
            return render_template('admin/peliculas/peliculas.html', films=films, form=form, categories=categories)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/pelicula/<string:id>')
def adminPeliculaVer(id):
    if session.get('user_data') and session.get('user_data')[12] != 1:
        if id != None:
            film = Films().view(escape(id))
            categories = Categories().view()
            time = datetime.fromisoformat(
                film[3] + ' ' + film[2]).strftime("%d %B, %Y - %I:%M %p")
            if film:
                return render_template('/admin/peliculas/pelicula.html', film=film, categories=categories, time=time)
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
            return render_template('admin/peliculas/peliculas.html', films=films, form=form, categories=categories)
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


@app.route('/admin/pelicula/eliminar/<int:id>', methods=['POST'])
def adminPeliculaEliminar(id=None):
    if session.get('user_data') and session.get('user_data')[12] != 1:
        if id != None:
            data = Films().delete(escape(id))
            if data:
                return redirect('/admin/peliculas/')
            else:
                flash(
                    "La pelicula no existe, por favor intente de nuevo")
                return redirect('/admin/peliculas/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


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


@app.route('/admin/funcion/<string:id>', methods=['GET', 'POST'])
def adminFuncionVer(id):
    if session.get('user_data') and session.get('user_data')[12] != 1:
        if id != None:
            if request.method == 'GET':
                show = Shows().view(escape(id))
                categories = Categories().view()
                rooms = Rooms().list()
                time = datetime.fromisoformat(
                    show[3] + ' ' + show[2]).strftime("%d %B, %Y - %I:%M %p")
                showdates = dates = ''

                if show[6]:
                    dates = [i for i in pickle.loads(show[6])]
                    showdates = [datetime.fromisoformat(i).strftime(
                        "%d %B, %Y - %I:%M %p") for i in pickle.loads(show[6])]
                if show:
                    return render_template('/admin/funciones/funcion.html', rooms=rooms, show=show, categories=categories, time=time, dates=dates, showdates=showdates)
                else:
                    flash("La funcion consultada no existe, por favor intente de nuevo")
                    return redirect('/admin/funciones/')
            else:
                array = [escape(i) for i in request.form.getlist(
                    'datetime[]') if i != '']
                show = Shows().timesUpdate(escape(id), array)

                flash(
                    f"Se actualizaron los horarios para esta función")
                return redirect(f'/admin/funcion/{id}')
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


@app.route('/admin/funcion/editar/<string:id>', methods=['POST'])
def adminFuncionEditar(id=None):
    if session.get('user_data'):
        if session.get('user_data')[12] != 1:
            if id and request.form["hora"].strip() and request.form["dia"].strip() and request.form["estado"].strip() and request.form["duracion"].strip() and request.form["edad"].strip() and request.form["sala"].strip() and request.form["pelicula"].strip():
                params = {
                    'id': escape(id),
                    'hora': escape(request.form["hora"].strip()),
                    'dia': escape(request.form["dia"].strip()),
                    'estado': escape(request.form["estado"].strip()),
                    'duracion': escape(request.form["duracion"].strip()),
                    'edad': escape(request.form["edad"].strip()),
                    'sala': escape(request.form["sala"].strip()),
                    'pelicula': escape(request.form["pelicula"].strip()),
                }
                data = Shows().edit(params)
                if data:
                    flash(
                        f"La funcion fue editada de forma correcta")
                    return redirect('/admin/funciones/')
            flash(
                f"Todos los campos marcados con '*' son obligatorios, por favor valide")
            return redirect('/admin/funciones/')
    flash("No tiene permiso para ingresar a esta área")
    return redirect('/admin/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
