from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo


class Login(FlaskForm):
    usuario = EmailField('Correo *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='El correo es requerido')
    ])

    clave = PasswordField('Clave *', validators=[
        Length(min=8, max=40, message='Longitud fuera de rango'),
        InputRequired(message='la clave es requerida')
    ])

    boton = SubmitField('Ingresar')


class Registro(FlaskForm):

    nombre = TextField('Nombres *', [
        Length(min=5, max=100, message='Longitud fuera de rango'),
        InputRequired(message='El nombre es requerido')
    ])

    apellido = TextField('Apellidos *', validators=[
        Length(min=1, max=100, message='Longitud fuera de rango'),
        InputRequired(message='El apellido es requerido')
    ])

    correo = EmailField('Correo *', validators=[
        Length(min=3, max=100, message='Longitud fuera de rango'),
        InputRequired(message='Correo  es requerido'),
    ])

    confirmar_correo = EmailField('Verificación de Correo *', validators=[
        Length(min=3, max=100, message='Longitud fuera de rango'),
        InputRequired(message='Correo es requerido'),
        EqualTo('correo', message='El correo y su verificación no corresponden')
    ])

    clave = PasswordField('Clave *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='Clave es requerido'),
    ])

    confirmar_clave = PasswordField('Verificación de clave *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='Clave es requerido'),
        EqualTo('clave', message='La clave y su verificación no corresponden')
    ])

    nacimiento = DateField('Fecha de nacimiento *', validators=[
        InputRequired(message='Fecha de nacimiento es requerida')
    ])

    departamento = TextField('Departamento *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='El municipio es requerido')
    ])

    ciudad = TextField('Ciudad *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='La Ciudad es requerido')
    ])

    direccion = TextField('Dirección *', validators=[
        Length(min=7, max=100, message='Longitud fuera de rango'),
        InputRequired(message='La dirección es requerido')
    ])

    telefono = TextField('Telefono / Celular *', validators=[
        Length(min=7, max=20, message='Longitud fuera de rango'),
        InputRequired(message='El telefono es requerido')
    ])

    boton = SubmitField('Registrar')


class ActualizacionUsuarios(FlaskForm):

    nombre = TextField('Nombres *', [
        Length(min=5, max=100, message='Longitud fuera de rango'),
        InputRequired(message='El nombre es requerido')
    ])

    apellido = TextField('Apellidos *', validators=[
        Length(min=1, max=100, message='Longitud fuera de rango'),
        InputRequired(message='El apellido es requerido')
    ])

    telefono = TextField('Telefono / Celular *', validators=[
        Length(min=7, max=20, message='Longitud fuera de rango'),
        InputRequired(message='El telefono es requerido')
    ])

    rol = TextField('Nuevo rol *', validators=[
        Length(min=1, max=2, message='Longitud fuera de rango'),
        InputRequired(message='El nuevo rol es requerido')
    ])

    clave = PasswordField('Contraseña', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
    ])

    nacimiento = DateField('Fecha de nacimiento *', validators=[
        InputRequired(message='Fecha de nacimiento es requerida')
    ])

    municipio = TextField('Departamento *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='El municipio es requerido')
    ])

    ciudad = TextField('Ciudad *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='La Ciudad es requerida')
    ])

    direccion = TextField('Dirección *', validators=[
        Length(min=7, max=100, message='Longitud fuera de rango'),
        InputRequired(message='La dirección es requerido')
    ])

    boton = SubmitField('Registrar')


class Pelicula(FlaskForm):

    nombre = TextField('Nombres *', [
        Length(min=5, max=100, message='Longitud fuera de rango [5-100]'),
        InputRequired(message='El nombre es requerido')
    ])

    actores = TextField('Actores *', validators=[
        Length(min=7, max=200, message='Longitud fuera de rango [7-100]'),
        InputRequired(message='Los actores son requeridos')
    ])

    director = TextField('Director *', validators=[
        Length(min=7, max=100, message='Longitud fuera de rango [7-100]'),
        InputRequired(message='El director es requerido')
    ])

    descripcion = TextAreaField('Descripcion *', validators=[
        Length(min=1, max=1000, message='Longitud fuera de rango [1-400]'),
        InputRequired(message='La descripcion es requerida')
    ])

    imagen = FileField('Imagen *', validators=[
        FileRequired(message='La imagen es requerida'),
        FileAllowed(['jpg', 'png', 'jpeg'],
                    'Solo se permiten imagenes jpg, jpeg y png!')
    ])

    banner = FileField('Banner *', validators=[
        FileRequired(message='El banner es requerida'),
        FileAllowed(['jpg', 'png', 'jpeg'],
                    'Solo se permiten imagenes jpg, jpeg y png!')
    ])

    trailer = TextField('Trailer *', validators=[
        Length(min=5, max=20, message='Longitud fuera de rango [5-20]'),
        InputRequired(message='El trailer es requerido')
    ])

    boton = SubmitField('Registrar')


class ActualizacionPelicula(FlaskForm):

    nombre = TextField('Nombres *', [
        Length(min=5, max=100, message='Longitud fuera de rango [5-100]'),
        InputRequired(message='El nombre es requerido')
    ])

    actores = TextField('Actores *', validators=[
        Length(min=7, max=200, message='Longitud fuera de rango [7-100]'),
        InputRequired(message='Los actores son requeridos')
    ])

    director = TextField('Director *', validators=[
        Length(min=7, max=100, message='Longitud fuera de rango [7-100]'),
        InputRequired(message='El director es requerido')
    ])

    descripcion = TextAreaField('Descripcion *', validators=[
        Length(min=1, max=1000, message='Longitud fuera de rango [1-400]'),
        InputRequired(message='La descripcion es requerida')
    ])

    imagen = FileField('Imagen *', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'],
                    'Solo se permiten imagenes jpg, jpeg y png!')
    ])

    banner = FileField('Banner *', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'],
                    'Solo se permiten imagenes jpg, jpeg y png!')
    ])

    trailer = TextField('Trailer *', validators=[
        Length(min=5, max=20, message='Longitud fuera de rango [5-20]'),
        InputRequired(message='El trailer es requerido')
    ])

    boton = SubmitField('Registrar')
