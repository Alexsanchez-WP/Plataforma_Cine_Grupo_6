import sqlite3

""" Funcion de la Query para Insertar, Eliminar o Actualizar datos"""


def ejecutar_query_accion(query, datos) -> int:
    try:
        with sqlite3.connect('db/bd_cinema.db') as con:
            cur = con.cursor()
            sal = cur.execute(query, datos).rowcount
            if sal != 0:
                con.commit()
    except Exception as ex:
        sal = 0
    return sal


"""Funcion para traer datos """


def ejecutar_query_seleccion(query) -> list:
    try:
        with sqlite3.connect('db/bd_cinema.db') as con:
            cur = con.cursor()
            sal = cur.execute(query).fetchall()
    except Exception as ex:
        sal = []
    return sal


"""
Este archivo es temporal, se deben implementar el diagrama de clases para la conexion y consulta a la base de datos
"""

Users = [
    {
        'ID': '1',
        'email': 'superadmin@admin.com',
        'password': '12345678',
        'name': 'Super Administrador',
        'role': 'admin'
    },
    {
        'ID': '2',
        'email': 'admin@admin.com',
        'password': '12345678',
        'name': 'Administrador',
        'role': 'user'
    },
    {
        'ID': '3',
        'email': 'cliente1@admin.com',
        'password': '12345678',
        'name': 'Cliente',
        'role': 'customer'
    },
    {
        'ID': '4',
        'email': 'cliente2@admin.com',
        'password': '12345678',
        'name': 'Cliente',
        'role': 'customer'
    }
]

Tickets = [
    {}
]

Comments = [
    {}
]

Films = [
    {
        'ID': '1',
        'image': 'img/films/AD2_2-Poster_480x670.jpg',
        'banner': 'img/films/AD2_3-Imagen-Trailer-(Foto)_1000x510.jpg',
        'trailer': 'https://www.youtube.com/embed/MUD32RTh_qQ',
        'shows': '',
        'name': 'Los Locos Addams 2',
        'actors': 'Charlize Theron, Oscar Isaac, Chloë Grace Moretz, Nick Kroll, Bette Midler, Snoop Dogg, Bill Hader y Javon “Wanna” Walton ',
        'director': 'Greg Tiernan, Laura Brousseau y Kevin Povlovic',
        'categories': 'Familiar, Animada',
        'description': 'La escalofriante familia favorita de todos está de regreso en esta nueva secuela animada de comedia Los Locos Addams 2. En esta nueva película, Los Addams se enredan en aventuras chifladas y se ven envueltos en divertidísimos encuentros con todo tipo de personajes desprevenidos. Siempre manteniéndose fieles a ellos mismos, Los Locos Addams llevan su icónica espeluznante y excéntrica personalidad a donde sea que vayan.',
    },
    {
        'ID': '2',
        'image': 'img/films/BOND_2-Poster_480x670.jpg',
        'banner': 'img/films/BOND_3-Imagen-Trailer-(Foto)_1000x510.jpg',
        'trailer': 'https://www.youtube.com/embed/Yq4KfMa4_9s',
        'shows': '',
        'name': 'Sin Tiempo Para Morir',
        'actors': 'Daniel Craig, Ralph Fiennes, Naomie Harris, Rory Kinnear, Léa Seydoux, Ben Whishaw, Jeffrey Wright, Ana de Armas, Dali Benssalah, David Dencik, Lashana Lynch, Billy Magnussen y Rami Malek. ',
        'director': 'Cary Joji Fukunaga ',
        'categories': 'Acción',
        'description': 'En Sin Tiempo Para Morir, Bond ha dejado el servicio activo y disfruta de una vida tranquila en Jamaica. Su paz es efímera cuando su viejo amigo Félix Leiter de la CIA aparece pidiendo ayuda. La misión de rescatar a un científico secuestrado resulta ser mucho más traicionera de lo esperado, llevando a Bond a la pista de un misterioso villano armado con nueva tecnología peligrosa. '
    },
    {
        'ID': '3',
        'image': 'img/films/El_Ultimo_Duelo Poster Pagina detalle 480x670.png',
        'banner': 'img/films/El_Ultimo_Duelo Banner Derecho 510x510.jpg',
        'trailer': 'https://www.youtube.com/embed/TDxJHR_LZmE',
        'shows': '',
        'name': 'El Último Duelo',
        'actors': 'Matt Damon, Adam Driver, Jodie Comer y Ben Affleck ',
        'director': 'Ridley Scott ',
        'categories': 'Drama',
        'description': 'Una apasionante historia de traición y venganza enmarcada en la brutalidad y opresión femenina de la Francia del siglo XIV. La historia épica, basada en hechos reales descritos en el libro The Last Duel: A True Story of Crime, Scandal, and Trial by Combat in Medieval France, es protagonizada por el ganador de un Óscar® Matt Damon y el dos veces nominado a los premios Óscar® Adam Driver que interpretan a dos lords en disputa, ambos de noble cuna, que deben resolver sus agravios en un duelo a muerte'
    }
]
