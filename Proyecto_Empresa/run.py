from flask import Flask, render_template, request, redirect, url_for, session
import os
from functools import wraps
from models import db, Usuario, app

@app.route("/")
@app.route("/index")
def index():
    return render_template("pagina_principal/index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        contraseña = request.form['password']

        usuario = Usuario.query.filter_by(correo=correo, contraseña=contraseña).first()  # Busca el usuario

        if usuario:
            session['usuario_id'] = usuario.id  # Guarda el ID del usuario en la sesión
            session['rol'] = usuario.rol  # Guarda el rol del usuario en la sesión
            session['nombres'] = usuario.nombres
            session['apellidos'] = usuario.apellidos

            if usuario.rol == 'administrador':
                return redirect(url_for('dashboard_admin'))
            elif usuario.rol == 'medico':
                return redirect(url_for('dashboard_medico'))
            elif usuario.rol == 'paciente':
                return redirect(url_for('dashboard_paciente')) #Asumo que tienes un dashboard paciente
            else:
                return "Rol desconocido" #Handle roles que no existen en la aplicacion
        else:
            return "Credenciales incorrectas" #Usuario no existe
    return render_template("templates_login/login.html")

@app.route("/recuperar")
def recuperar():
    return render_template("templates_login/recuperacion.html")

def requiere_rol(rol_esperado):
    def decorador(f):
        @wraps(f)
        def funcion_decorada(*args, **kwargs):
            if 'rol' in session and session['rol'] == rol_esperado:
                return f(*args, **kwargs)
            else:
                return "Acceso denegado", 403  # O redirige a una página de error
        return funcion_decorada
    return decorador

#Rutas Del Administrador#

@app.route("/dashboard_admin")
@requiere_rol('administrador')
def dashboard_admin():
    return render_template("templates_dashboard/templates_admin/inicio_admin.html", nombres=session.get('nombres'), apellidos=session.get('apellidos'))

@app.route("/agregar_medico")
@requiere_rol('administrador')
def agregar_medico():
    return render_template("templates_dashboard/templates_admin/medico/agregar.html")

@app.route("/editar_medico")
@requiere_rol('administrador')
def editar_medico():
    return render_template("templates_dashboard/templates_admin/medico/editar.html")

@app.route("/agregar_paciente")
@requiere_rol('administrador')
def agregar_paciente():
    return render_template("templates_dashboard/templates_admin/paciente/agregar_paciente.html")

@app.route("/editar_paciente")
@requiere_rol('administrador')
def editar_paciente():
    return render_template("templates_dashboard/templates_admin/paciente/editar_paciente.html")

@app.route("/crear_cita_admin")
@requiere_rol('administrador')
def crear_cita_admin():
    return render_template("templates_dashboard/templates_admin/cita/crear_cita.html")

@app.route("/editar_cita_admin")
@requiere_rol('administrador')
def editar_cita_admin():
    return render_template("templates_dashboard/templates_admin/cita/editar_cita.html")

@app.route("/crear_factura_admin")
@requiere_rol('administrador')
def crear_factura_admin():
    return render_template("templates_dashboard/templates_admin/factura/crear_factura.html")

@app.route("/editar_factura_admin")
@requiere_rol('administrador')
def editar_factura_admin():
    return render_template("templates_dashboard/templates_admin/factura/editar_factura.html")

@app.route("/reportes_admin")
@requiere_rol('administrador')
def reportes_admin():
    return render_template("templates_dashboard/templates_admin/reportes_admin.html")

@app.route("/perfil_admin")
@requiere_rol('administrador')
def perfil_admin():
    return render_template("templates_dashboard/templates_admin/perfil_admin.html")
#Fin Rutas Administrador#

#Rutas del Medico#
@app.route("/dashboard_medico")
@requiere_rol('medico')
def dashboard_medico():
    return render_template("templates_dashboard/templates_medicos/inicio_medico.html",nombres=session.get('nombres'), apellidos=session.get('apellidos'))

@app.route("/agenda")
@requiere_rol('medico')
def agenda():
    return render_template("templates_dashboard/templates_medicos/agenda_medica/crear_agenda.html")

@app.route("/editar_agenda")
@requiere_rol('medico')
def editar_agenda():
    return render_template("templates_dashboard/templates_medicos/agenda_medica/editar_agenda.html")

@app.route("/historia_medica")
@requiere_rol('medico')
def historia_medica():
    return render_template("templates_dashboard/templates_medicos/historia_medica.html")

@app.route("/tratamiento")
@requiere_rol('medico')
def tratamiento():
    return render_template("templates_dashboard/templates_medicos/tratamiento/agregar_tratamiento.html")

@app.route("/editar_tratamiento")
@requiere_rol('medico')
def editar_tratamiento():
    return render_template("templates_dashboard/templates_medicos/tratamiento/editar_tratamiento.html")

#Rutas Del Paciente#
@app.route("/dashboard_paciente")
@requiere_rol('paciente')
def dashboard_paciente():
    return render_template("templates_dashboard/templates_paciente/inicio_paciente.html", nombres=session.get('nombres'), apellidos=session.get('apellidos'))

@app.route("/perfil_paciente")
@requiere_rol('paciente')
def perfil_paciente():
    return render_template("templates_dashboard/templates_paciente/perfil_paciente.html")

@app.route("/historial_citas")
@requiere_rol('paciente')
def historial_citas():
    return render_template("templates_dashboard/templates_paciente/historial_citas.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)