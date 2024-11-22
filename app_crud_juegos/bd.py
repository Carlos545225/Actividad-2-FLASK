import pymysql

def odtener_conexion():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='app_crud_juego') 