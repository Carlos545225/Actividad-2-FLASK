# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'  # ¡IMPORTANTE! Cambia esto por algo seguro
# Configura la URI de la base de datos.  Ajusta el usuario, contraseña, host y nombre de la base de datos.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/db_empresa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar warnings
db = SQLAlchemy(app)



class Usuario(db.Model):
    __tablename__ = 'usuario'  # Nombre de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)  # Considera usar hashing
    rol = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.correo}>'


# Puedes agregar modelos para Medico y Paciente si es necesario para funcionalidades adicionales.
# Asegúrate de reflejar la estructura de tus tablas.

# Crear la base de datos si no existe:
with app.app_context():
    db.create_all() # Crea las tablas en la base de datos