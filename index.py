# Incluimos las referencias
from logging import debug
from flask import Flask, render_template, request
from markupsafe import escape
from formularios import Login,Registro

# Creamos el objeto Flask
app = Flask(__name__)

# Construimos los decoradores :: Rutas
@app.route('/')
def index():
    # Renderizamos la pagina HTML Inicial o HOMEPAGE
    return render_template('index.html')


@app.route('/estrenos/', methods=['GET', 'POST'])
def proximosEstrenos():
    return render_template('estrenos.html')


@app.route('/cartelera/', methods=['GET', 'POST'])
def cartelera():
    return render_template('cartelera.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    log=Login()
    if request.method == 'GET':
        return render_template('login.html', form=log)
    else:
        user = escape(request.form['Usuario'])
        password = escape(request.form['Clave'])

        return f"Bienvenido {user} !!!"


@app.route('/recuperar-password/', methods=['GET', 'POST'])
def recuperar():
    if request == 'GET':
        return render_template('recuperacion.html')
    else:
        email = escape(request.form['idTxtEmailRecorey'])
        
        return f"Se han enviando los datos al correo {email}"


@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    reg=Registro()
    nmbr=escape(request.form["nombre"])
    aplld=escape(request.form["apellido"])
    eml=escape(request.form["correo"])
    emlCnfrmr=escape(request.form["confirmar_correo"])
    psswrd=escape(request.form["clave"])
    psswrdCnfrmr=escape(request.form["confirmar_clave"])
    ncmnt=escape(request.form["nacimiento"])
    mncp=escape(request.form["municipio"])
    cdd=escape(request.form["ciudad"])
    drccn=escape(request.form["direccion"])
    tlfn=escape(request.form["telefono"])
    usr=escape(request.form["usuario"])

    return render_template('registro.html',form=reg)


@app.route('/tiquetes/', methods=['GET', 'POST'])
def tiquets():
    return render_template('tiquets.html')


@app.route('/funciones/', methods=['GET', 'POST'])
def funciones():
    return render_template('funciones.html')


@app.route('/buscar-pelicula/', methods=['GET', 'POST'])
def buscarPelicula():
    return render_template('buscar_pelicula.html')


"""-------------------------------------------------------------------------------------------------------------"""
if __name__ == '__main__':
    app.run(debug=True, port=5000)
