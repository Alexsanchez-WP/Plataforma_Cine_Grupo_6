from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField, DateField
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

    apellido = TextField('Apellido *', validators=[
        Length(min=1, max=100, message='Longitud fuera de rango'),
        InputRequired(message='El apellido es requerido')
    ])

    correo = EmailField('Correo *', validators=[
        Length(min=3, max=100, message='Longitud fuera de rango'),
        InputRequired(message='Correo  es requerido')
    ])

    confirmar_correo = EmailField('Verificación de Correo *', validators=[
        Length(min=3, max=100, message='Longitud fuera de rango'),
        InputRequired(message='Correo es requerido'),
        EqualTo(correo, message='El correo y su verificación no corresponden')
    ])

    clave = PasswordField('Clave *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='Clave es requerido')
    ])

    confirmar_clave = PasswordField('Verificación de clave *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='Clave es requerido'),
        EqualTo(clave, message='La clave y su verificación no corresponden')
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
