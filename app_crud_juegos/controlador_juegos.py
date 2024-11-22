from bd import odtener_conexion

def insertar_juego(nombre, descripcion, precio):
    conexion = odtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO juegos(nombre, descripcion, precio) VALUES (%s,%s,%s)",
        (nombre, descripcion, precio))
    conexion.commit()
    conexion.close()


def obtener_juegos():
    conexion = odtener_conexion()
    juegos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio FROM juegos")
        juegos = cursor.fetchall()
    conexion.close()
    return juegos
    