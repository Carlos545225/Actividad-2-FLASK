from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from datetime import datetime

db = SQLAlchemy()

class Administrador(db.Model):
    __tablename__ = 'Administradores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Medico', 'Administrador','Paciente'), nullable=False) 

    def __repr__(self):
        return f'<Administrador {self.email}>'


class Medico(db.Model):
    __tablename__ = 'Medicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    tipo_documento = db.Column(db.Enum('CC', 'CE'), nullable=False) 
    numero_documento = db.Column(db.String(20), unique=True, nullable=False)
    genero = db.Column(db.Enum('Masculino', 'Femenino', 'Otro'), nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    numero_registro = db.Column(db.String(50), unique=True, nullable=False)
    anios_experiencia = db.Column(db.Integer, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Medico', 'Administrador','Paciente'), nullable=False)
    citas = db.relationship('Cita', backref='medico', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Medico {self.email}>'


class Paciente(db.Model):
    __tablename__ = 'Pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    tipo_documento = db.Column(db.Enum('CC', 'TI', 'CE', 'Pasaporte'), nullable=False)  
    numero_documento = db.Column(db.String(20), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.Enum('Masculino', 'Femenino', 'Otro'), nullable=False) 
    grupo_sanguineo = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), nullable=False)  
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    eps = db.Column(db.String(100), nullable=False)
    contacto_emergencia = db.Column(db.String(100), nullable=False)
    telefono_emergencia = db.Column(db.String(20), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Paciente', 'Administrador','Medico'), nullable=False)
    citas = db.relationship('Cita', backref='paciente', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Paciente {self.email}>'
    
class Cita(db.Model):
    __tablename__ = 'Citas'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('Medicos.id'), nullable=False)
    servicio = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'confirmada', 'en_progreso', 'finalizada', 'cancelada'), nullable=False)

    def __repr__(self):
        return f'<Cita {self.id}>'

class Factura(db.Model):
    __tablename__ = 'Facturas'
    id = db.Column(db.Integer, primary_key=True)
    numero_factura = db.Column(db.String(50), unique=True, nullable=False)
    id_cita = db.Column(db.Integer, db.ForeignKey('Citas.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
    tipo_pago = db.Column(db.Enum('Efectivo', 'Tarjeta', 'Transferencia'), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'pagada', 'cancelada'), nullable=False)
    
    cita = db.relationship('Cita', backref=db.backref('factura', cascade='all, delete-orphan', single_parent=True), lazy=True)

    def __repr__(self):
        return f'<Factura {self.numero_factura}>'

class Tratamiento(db.Model):
    __tablename__ = 'Tratamientos'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('Medicos.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    diagnostico = db.Column(db.Text, nullable=False)
    tratamiento = db.Column(db.Text, nullable=False)
    receta = db.Column(db.Text)
    notas = db.Column(db.Text)
    
    # Relaciones
    paciente = db.relationship('Paciente', backref=db.backref('tratamientos', lazy=True))
    medico = db.relationship('Medico', backref=db.backref('tratamientos', lazy=True))

    def __repr__(self):
        return f'<Tratamiento {self.id} - Paciente: {self.paciente_id}>'

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), default='primary')  # primary, success, warning
    fecha = db.Column(db.DateTime, default=datetime.now)
    leida = db.Column(db.Boolean, default=False)





