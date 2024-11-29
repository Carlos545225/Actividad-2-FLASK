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

def odtener_juego_por_id(id):
    conexion = odtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, precio FROM juegos WHERE id = %s", (id,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def actualizar_juego(nombre, descripcion, precio, id):
    conexion = odtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE juegos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s",
                       (nombre, descripcion,precio,id))
    conexion.commit()
    conexion.close()

def eliminar_juego(id):
    conexion = odtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def buscar_juegos(termino):
    conexion = odtener_conexion()
    juegos = []
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, precio FROM juegos WHERE nombre LIKE %s", 
            (f"%{termino}%",)
        )
        juegos = cursor.fetchall()
    conexion.close()
    return juegos