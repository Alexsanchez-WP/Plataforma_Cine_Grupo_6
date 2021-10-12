from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, EqualTo


class Login(FlaskForm):
    usuario = TextField('Usuario *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='Usuario es requerido')
    ])

    clave = PasswordField('Clave *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='Clave es requerido')
    ])

    boton = SubmitField('Ingresar')


class Registro(FlaskForm):

    nombre = TextField('Nombre *', validators=[
        Length(min=1, max=100, message='Longitud fuera de rango'),
        InputRequired(message='El nombre es requerido')
    ])

    apellido = TextField('Apellido *', validators=[
        Length(min=1, max=100, message='Longitud fuera de rango'),
        InputRequired(message='El apellido es requerido')
    ])

    telefono = TextField('Telefono *', validators=[
        Length(min=7, max=20, message='Longitud fuera de rango'),
        InputRequired(message='El telefono es requerido')
    ])

    correo = EmailField('Email *', validators=[
        Length(min=3, max=100, message='Longitud fuera de rango'),
        InputRequired(message='Email es requerido')
    ])

    confirmar_correo = EmailField('Verificación de Email *', validators=[
        Length(min=3, max=100, message='Longitud fuera de rango'),
        InputRequired(message='Email es requerido'),
        EqualTo(correo, message='El correo y su verificación no corresponden')
    ])

    usuario = TextField('Usuario *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='Usuario es requerido')
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

    municipio = TextField('Municipio *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='El municipio es requerido')
    ])

    cuidad = TextField('Ciudad *', validators=[
        Length(min=5, max=40, message='Longitud fuera de rango'),
        InputRequired(message='La Ciudad es requerido')
    ])

    boton = SubmitField('Registrar')
