# Incluimos las referencias
from logging import debug
from flask import Flask, render_template, request
from markupsafe import escape

# Creamos el objeto Flask
app = Flask(__name__)

# Construimos los decoradores :: Rutas


@app.route('/')
def index():
    # Renderizamos la pagina HTML Inicial o HOMEPAGE
    return render_template('index.html')


@app.route('/estrenos', methods=['GET', 'POST'])
def proximosEstrenos():
    return render_template('estrenos.html')


@app.route('/cartelera', methods=['GET', 'POST'])
def cartelera():
    return render_template('cartelera.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:  # Recuperamos los datos del formulario de Login
        # Txt del Usuario con validacion de Script's
        usuario = escape(request.form['idTxtUser'])
        # Txt del Password con validacion de Script's
        password = escape(request.form['idTxtPsswrd'])
        # Retornamos un mensaje de bienvenidad al usuario
        return f"Bienvenido {usuario} !!!"


@app.route('/recuperarPassword', methods=['GET', 'POST'])
def recuperar():
    if request == 'GET':
        return render_template('recuperacion.html')
    else:
        email = escape(request.form['idTxtEmailRecorey'])
        return f"Se han enviando los datos al correo {email}"


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('registro.html')


@app.route('/tiquetes', methods=['GET', 'POST'])
def tiquets():
    return render_template('tiquets.html')


@app.route('/funciones', methods=['GET', 'POST'])
def funciones():
    return render_template('funciones.html')


@app.route('/buscar_pelicula', methods=['GET', 'POST'])
def buscarPelicula():
    return render_template('buscar_pelicula.html')


"""-------------------------------------------------------------------------------------------------------------"""
if __name__ == '__main__':
    app.run(debug=True, port=5000)
