from flask import Flask, render_template, request, redirect, flash, session, url_for, send_file, abort, jsonify
from functools import wraps
from model import db, Administrador, Medico, Paciente, Cita, Factura, Tratamiento, Notificacion
import logging
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
import tempfile
from io import BytesIO
from reportlab.pdfgen import canvas

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MediCitas_plus' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db_empresa'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def requiere_rol(rol_esperado):
    def decorador(f):
        @wraps(f)
        def funcion_decorada(*args, **kwargs):
            if 'rol' in session and session['rol'] == rol_esperado:
                return f(*args, **kwargs)
            else:
                return "Acceso denegado", 403 
        return funcion_decorada
    return decorador

def generar_pdf_factura(factura):
    # Crear un archivo temporal para el PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter,
                          rightMargin=30, leftMargin=30,
                          topMargin=30, bottomMargin=30)
    
    # Contenedor para los elementos del PDF
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_principal_style = ParagraphStyle(
        'TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=6,
        alignment=1,
        textColor=colors.HexColor('#1a237e')
    )
    
    subtitulo_style = ParagraphStyle(
        'Subtitulo',
        parent=styles['Heading2'],
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor('#303f9f'),
        spaceBefore=0,
        spaceAfter=20
    )

    seccion_style = ParagraphStyle(
        'Seccion',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#1a237e'),
        spaceBefore=10,
        spaceAfter=5
    )

    # Estilo para el contenido de las celdas
    celda_style = ParagraphStyle(
        'CeldaStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        alignment=0
    )
    
    # Obtener información relacionada
    cita = Cita.query.get(factura.id_cita)
    paciente = Paciente.query.get(cita.paciente_id)
    medico = Medico.query.get(cita.medico_id)
    
    # Función para crear párrafos con estilo
    def crear_parrafo(texto, estilo=celda_style):
        return Paragraph(str(texto), estilo)

    # Encabezado
    elements.append(Paragraph("MediCitas Plus", titulo_principal_style))
    elements.append(Paragraph("Sistema de Gestión Médica", subtitulo_style))
    
    # Crear tabla de información principal
    datos_principales = [
        [crear_parrafo("FACTURA MÉDICA", seccion_style), 
         crear_parrafo(f"N°: {factura.numero_factura}", seccion_style)],
        [crear_parrafo("Fecha de Emisión:"), crear_parrafo(factura.fecha.strftime("%d/%m/%Y"))],
        [crear_parrafo("Estado:"), crear_parrafo(factura.estado.upper())],
    ]
    
    tabla_principal = Table(datos_principales, colWidths=[doc.width/2]*2)
    tabla_principal.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(tabla_principal)
    elements.append(Spacer(1, 10))
    
    # Información del paciente y médico en dos columnas
    datos_paciente_medico = [
        [crear_parrafo("INFORMACIÓN DEL PACIENTE", seccion_style), 
         crear_parrafo("INFORMACIÓN DEL MÉDICO", seccion_style)],
        [crear_parrafo(f"Nombre: {paciente.nombre} {paciente.apellido}"),
         crear_parrafo(f"Dr(a). {medico.nombre} {medico.apellido}")],
        [crear_parrafo(f"{paciente.tipo_documento}: {paciente.numero_documento}"),
         crear_parrafo(f"Especialidad: {medico.especialidad}")],
        [crear_parrafo(f"Teléfono: {paciente.telefono}"),
         crear_parrafo(f"Reg. Médico: {medico.numero_registro if hasattr(medico, 'numero_registro') else 'N/A'}")],
        [crear_parrafo(f"EPS: {paciente.eps}"), ""],
    ]
    
    tabla_info = Table(datos_paciente_medico, colWidths=[doc.width/2]*2)
    tabla_info.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(tabla_info)
    elements.append(Spacer(1, 15))
    
    # Detalles del servicio
    elements.append(Paragraph("DETALLES DEL SERVICIO", seccion_style))
    datos_servicio = [
        ["Servicio", "Fecha", "Horario", "Valor"],
        [cita.servicio, 
         cita.fecha.strftime("%d/%m/%Y"),
         f"{cita.hora_inicio} - {cita.hora_fin}",
         f"${factura.total:,.2f}"]
    ]
    
    tabla_servicio = Table(datos_servicio, colWidths=[doc.width*0.4, doc.width*0.2, doc.width*0.2, doc.width*0.2])
    tabla_servicio.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (-1,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.15, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eaf6')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(tabla_servicio)
    
    # Total y método de pago
    datos_pago = [
        ["", "Método de Pago:", crear_parrafo(factura.tipo_pago)],
        ["", "TOTAL A PAGAR:", crear_parrafo(f"${factura.total:,.2f}", ParagraphStyle(
            'Total',
            parent=celda_style,
            fontSize=11,
            textColor=colors.HexColor('#1a237e'),
            alignment=2
        ))]
    ]
    
    tabla_pago = Table(datos_pago, colWidths=[doc.width*0.6, doc.width*0.2, doc.width*0.2])
    tabla_pago.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('ALIGN', (-1,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (1,0), (1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LINEABOVE', (1,-1), (-1,-1), 1, colors.HexColor('#1a237e')),
    ]))
    elements.append(Spacer(1, 10))
    elements.append(tabla_pago)
    
    # Pie de página
    elements.append(Spacer(1, 30))
    pie_style = ParagraphStyle(
        'Pie',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Este documento es una factura electrónica válida para efectos fiscales.", pie_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("MediCitas Plus - Cuidando tu salud", pie_style))
    
    # Generar el PDF
    doc.build(elements)
    return temp_file.name

# Rutas pagina principal
@app.route("/")
@app.route("/index")
def index():
    return render_template("pagina_principal/index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        contraseña = request.form['password']
        
        if not correo or not contraseña:
            flash('Por favor ingrese su correo electrónico y contraseña', 'warning')
            return render_template("templates_login/login.html")

        administrador = Administrador.query.filter_by(email=correo, contraseña=contraseña).first()
        medico = Medico.query.filter_by(email=correo, contraseña=contraseña).first()
        paciente = Paciente.query.filter_by(email=correo, contraseña=contraseña).first()

        if administrador:
            session.clear()
            session['usuario_id'] = administrador.id
            session['rol'] = 'Administrador'
            session['nombres'] = administrador.nombre
            session['apellidos'] = administrador.apellido
            crear_notificacion(administrador.id, f"Bienvenido/a {administrador.nombre}! Has iniciado sesión como Administrador", "success")
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard_admin'))
        elif medico:
            session.clear()
            session['usuario_id'] = medico.id
            session['rol'] = 'Medico'
            session['nombres'] = medico.nombre
            session['apellidos'] = medico.apellido
            crear_notificacion(medico.id, f"Bienvenido/a Dr(a). {medico.nombre}! Has iniciado sesión como Médico", "success")
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard_medico'))
        elif paciente:
            session.clear()
            session['usuario_id'] = paciente.id
            session['rol'] = 'Paciente'
            session['nombres'] = paciente.nombre
            session['apellidos'] = paciente.apellido
            crear_notificacion(paciente.id, f"Bienvenido/a {paciente.nombre}! Has iniciado sesión como Paciente", "success")
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard_paciente'))
        else:
            flash('Credenciales incorrectas. Por favor verifique su correo y contraseña.', 'danger')
            return render_template("templates_login/login.html")

    return render_template("templates_login/login.html")

@app.route("/recuperar")
def recuperar():
    return render_template("templates_login/recuperacion.html")

# Rutas del Administrador
@app.route("/dashboard_admin")
@requiere_rol('Administrador')
def dashboard_admin():

    ultimos_medicos = Medico.query.order_by(Medico.id.desc()).limit(4).all()
    ultimos_pacientes = Paciente.query.order_by(Paciente.id.desc()).limit(4).all()
    
    ultimos_registros = []
    
    for medico in ultimos_medicos:
        ultimos_registros.append({
            'tipo': 'medico',
            'nombre': f"{medico.nombre}",
            'especialidad': medico.especialidad,
            'fecha_registro': medico.id 
        })
    
    for paciente in ultimos_pacientes:
        ultimos_registros.append({
            'tipo': 'paciente',
            'nombre': f"{paciente.nombre}",
            'eps': paciente.eps,
            'fecha_registro': paciente.id 
        })
    
    ultimos_registros = sorted(ultimos_registros, key=lambda x: x['fecha_registro'], reverse=True)[:8]
    
    return render_template("templates_dashboard/templates_admin/inicio_admin.html", ultimos_registros=ultimos_registros)

@app.route("/medico_admin")
@requiere_rol('Administrador')
def medico_admin():
    medicos = Medico.query.all()
    return render_template("templates_dashboard/templates_admin/medico/medico_admin.html", medicos=medicos)

@app.route("/editar_medico/<int:id_medico>", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def editar_medico(id_medico):
    medico = Medico.query.get_or_404(id_medico)

    if request.method == 'POST':
        try:
            medico.nombre = request.form['nombre']
            medico.apellido = request.form['apellido']
            medico.tipo_documento = request.form['tipo_documento']
            medico.numero_documento = request.form['numero_documento']
            medico.genero = request.form['genero']
            medico.email = request.form['email']
            medico.telefono = request.form['telefono']
            medico.direccion = request.form['direccion']
            medico.especialidad = request.form['especialidad']
            medico.numero_registro = request.form['registro_medico']
            medico.anios_experiencia = request.form['años']

            nueva_contraseña = request.form.get('contraseña')
            if nueva_contraseña:
                medico.contraseña = nueva_contraseña 
            db.session.commit()

            flash("Médico actualizado con éxito", "success")
            return redirect(url_for('medico_admin'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el médico: {str(e)}", "danger")
            return render_template("templates_dashboard/templates_admin/medico/editar.html", medico=medico)

    return render_template("templates_dashboard/templates_admin/medico/editar.html", medico=medico)

@app.route("/paciente_admin")
@requiere_rol('Administrador')
def paciente_admin():
    pacientes = Paciente.query.all()
    return render_template("templates_dashboard/templates_admin/paciente/paciente_admin.html", pacientes=pacientes)

@app.route("/agregar_paciente", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def agregar_paciente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo_documento = request.form['tipo_documento']
        numero_documento = request.form['numero_documento']
        fecha_nacimiento = request.form['fecha_nacimiento']
        grupo_sanguineo = request.form['grupo_sanguineo']
        genero = request.form['genero']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        eps = request.form['eps']
        contacto_emergencia = request.form['contacto_emergencia']
        telefono_emergencia = request.form['telefono_emergencia']
        contraseña = request.form['contraseña']
        repetir_contraseña = request.form['repetir_contraseña']

        if contraseña != repetir_contraseña:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for('paciente_admin'))

        try:
            nuevo_paciente = Paciente(
                nombre=nombre,
                apellido=apellido,
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                fecha_nacimiento=fecha_nacimiento,
                genero=genero,
                grupo_sanguineo=grupo_sanguineo,
                email=email,
                telefono=telefono,
                direccion=direccion,
                eps=eps,
                contacto_emergencia=contacto_emergencia,
                telefono_emergencia=telefono_emergencia,
                contraseña=contraseña,
                rol='Paciente'
            )

            db.session.add(nuevo_paciente)
            db.session.commit()
            flash("Paciente agregado con éxito", "success")
            return redirect(url_for('paciente_admin'))

        except Exception as e:
            db.session.rollback()
            if 'Duplicate entry' in str(e) and 'email' in str(e):
                flash("Error: El correo electrónico ya está registrado", "danger")
            elif 'Duplicate entry' in str(e) and 'numero_documento' in str(e):
                flash("Error: El número de documento ya está registrado", "danger")
            else:
                flash("Error al agregar el paciente. Por favor, verifique los datos", "danger")
            return redirect(url_for('paciente_admin'))

    return render_template("templates_dashboard/templates_admin/paciente/agregar_paciente.html")

@app.route("/editar_paciente/<int:id_paciente>", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def editar_paciente(id_paciente):
    paciente = Paciente.query.get_or_404(id_paciente)

    if request.method == 'POST':
        try:
            paciente.nombre = request.form['nombre']
            paciente.apellido = request.form['apellido']
            paciente.tipo_documento = request.form['tipo_documento']
            paciente.numero_documento = request.form['numero_documento']
            paciente.fecha_nacimiento = request.form['fecha_nacimiento']
            paciente.genero = request.form['genero']
            paciente.grupo_sanguineo = request.form['grupo_sanguineo']
            paciente.email = request.form['email']
            paciente.telefono = request.form['telefono']
            paciente.direccion = request.form['direccion']
            paciente.eps = request.form['eps']
            paciente.contacto_emergencia = request.form['contacto_emergencia']
            paciente.telefono_emergencia = request.form['telefono_emergencia']
            
            nueva_contraseña = request.form.get('contraseña')
            repetir_contraseña = request.form.get('repetir_contraseña')

            if nueva_contraseña:
                if nueva_contraseña != repetir_contraseña:
                    flash("Las contraseñas no coinciden", "danger")
                    return render_template("templates_dashboard/templates_admin/paciente/editar_paciente.html", paciente=paciente)
                paciente.contraseña = nueva_contraseña
            
            db.session.commit() 

            flash("Paciente actualizado con éxito", "success")
            return redirect(url_for('paciente_admin'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el paciente: {str(e)}", "danger")
            return render_template("templates_dashboard/templates_admin/paciente/editar_paciente.html", paciente=paciente)

    return render_template("templates_dashboard/templates_admin/paciente/editar_paciente.html", paciente=paciente)

@app.route("/citas_admin")
@requiere_rol('Administrador')
def citas_admin():
    citas = Cita.query.all()
    pacientes = Paciente.query.all()
    medicos = Medico.query.all()
    return render_template("templates_dashboard/templates_admin/cita/citas_admin.html", citas=citas, pacientes=pacientes, medicos=medicos)

@app.route("/crear_cita_admin", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def crear_cita_admin():
    pacientes = Paciente.query.all()
    medicos = Medico.query.all()
    
    if request.method == 'POST':
        paciente_id = request.form['paciente']
        medico_id = request.form['medico']
        servicio = request.form['servicio']
        fecha_str = request.form['fecha']
        hora_inicio = request.form['horario_inicio']
        hora_fin = request.form['horario_fin']
        motivo = request.form['motivo']
        estado = request.form['estado']

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            logger.debug(f"Creando cita para fecha: {fecha} ({type(fecha)})")
            
            nueva_cita = Cita(
                paciente_id=paciente_id,
                medico_id=medico_id,
                servicio=servicio,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                motivo=motivo,
                estado=estado
            )

            db.session.add(nueva_cita)
            db.session.commit()
            flash("Cita creada con éxito", "success")
            return redirect(url_for('citas_admin'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear cita: {str(e)}")
            flash("Error al crear la cita. Por favor, verifique los datos", "danger")
            
    # Return for both GET and failed POST
    return render_template("templates_dashboard/templates_admin/cita/crear_cita.html", 
                         pacientes=pacientes,
                         medicos=medicos)

@app.route("/editar_cita_admin/<int:id_cita>", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def editar_cita_admin(id_cita):
    cita = Cita.query.get_or_404(id_cita)
    pacientes = Paciente.query.all()
    medicos = Medico.query.all()

    if request.method == 'POST':
        try:
            cita.paciente_id = request.form['paciente']
            cita.medico_id = request.form['medico']
            cita.servicio = request.form['servicio']
            fecha_str = request.form['fecha']
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            logger.debug(f"Editando cita para fecha: {fecha} ({type(fecha)})")
            cita.fecha = fecha
            cita.hora_inicio = request.form['horario_inicio']
            cita.hora_fin = request.form['horario_fin']
            cita.motivo = request.form['motivo']
            cita.estado = request.form['estado']

            db.session.commit()
            flash("Cita actualizada con éxito", "success")
            return redirect(url_for('citas_admin'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al actualizar cita: {str(e)}")
            flash(f"Error al actualizar la cita: {str(e)}", "danger")
            return render_template("templates_dashboard/templates_admin/cita/editar_cita.html", 
                                cita=cita,
                                pacientes=pacientes,
                                medicos=medicos)

    # Formatear las horas para mostrarlas en el formulario
    if cita.hora_inicio:
        cita.horario_inicio = cita.hora_inicio.strftime('%H:%M')
    if cita.hora_fin:
        cita.horario_fin = cita.hora_fin.strftime('%H:%M')

    return render_template("templates_dashboard/templates_admin/cita/editar_cita.html", 
                         cita=cita,
                         pacientes=pacientes,
                         medicos=medicos)

@app.route("/factura_admin")
@requiere_rol('Administrador')
def factura_admin():
    facturas = Factura.query.all()
    return render_template("templates_dashboard/templates_admin/factura/factura_admin.html", 
                         facturas=facturas)

@app.route("/exportar_factura_pdf/<int:id_factura>")
@requiere_rol('Administrador')
def exportar_factura_pdf(id_factura):
    try:
        factura = Factura.query.get_or_404(id_factura)
        pdf_path = generar_pdf_factura(factura)
        
        return send_file(
            pdf_path,
            download_name=f'factura_{factura.numero_factura}.pdf',
            as_attachment=True
        )
    except Exception as e:
        flash(f'Error al generar el PDF: {str(e)}', 'danger')
        return redirect(url_for('factura_admin'))
    finally:
        # Limpiar el archivo temporal después de enviarlo
        if 'pdf_path' in locals():
            try:
                os.unlink(pdf_path)
            except:
                pass

@app.route("/crear_factura_admin", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def crear_factura_admin():
    try:
        # Obtener todas las citas con sus relaciones
        citas = Cita.query.join(Paciente).join(Medico).all()
        
        # Generar número de factura automáticamente
        ultima_factura = Factura.query.order_by(Factura.id.desc()).first()
        if ultima_factura and ultima_factura.numero_factura.startswith('F'):
            try:
                ultimo_numero = int(ultima_factura.numero_factura[1:])
                nuevo_numero = f"F{(ultimo_numero + 1):03d}"
            except ValueError:
                nuevo_numero = "F001"
        else:
            nuevo_numero = "F001"
        
        logger.debug(f"Número de factura generado: {nuevo_numero}")
        
        if request.method == 'POST':
            cita_id = request.form['cita']
            fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()

            total_str = request.form['total'].replace('$', '').replace(' ', '').replace('.', '').replace(',', '.')
            total = float(total_str)
            
            tipo_pago = request.form['tipo_pago']
            estado = request.form['estado']

            nueva_factura = Factura(
                numero_factura=nuevo_numero,
                id_cita=cita_id,
                fecha=fecha,
                total=total,
                tipo_pago=tipo_pago,
                estado=estado
            )

            db.session.add(nueva_factura)
            db.session.commit()
            flash("Factura creada con éxito", "success")
            return redirect(url_for('factura_admin'))

        return render_template("templates_dashboard/templates_admin/factura/crear_factura.html", 
                            citas=citas,
                            numero_factura=nuevo_numero)
                            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en crear_factura_admin: {str(e)}")
        flash("Error al procesar la factura. Por favor, verifique los datos", "danger")
        return render_template("templates_dashboard/templates_admin/factura/crear_factura.html", 
                            citas=Cita.query.all(),
                            numero_factura="F001")

@app.route("/editar_factura_admin/<int:id_factura>", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def editar_factura_admin(id_factura):
    try:
        # Obtener la factura a editar
        factura = Factura.query.get_or_404(id_factura)
        
        # Obtener todas las citas con sus relaciones
        citas = Cita.query.join(Paciente).join(Medico).all()
        
        if request.method == 'POST':
            factura.id_cita = request.form['cita']
            factura.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()

            total_str = request.form['total'].replace('$', '').replace(' ', '').replace('.', '').replace(',', '.')
            
            factura.total = float(total_str)
            
            factura.tipo_pago = request.form['tipo_pago']
            factura.estado = request.form['estado']

            db.session.commit()
            flash("Factura actualizada con éxito", "success")
            return redirect(url_for('factura_admin'))

        return render_template("templates_dashboard/templates_admin/factura/editar_factura.html", 
                            factura=factura,
                            citas=citas)
                            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error en editar_factura_admin: {str(e)}")
        flash(f"Error al actualizar la factura: {str(e)}", "danger")
        return redirect(url_for('factura_admin'))


@app.route("/perfil_admin", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def perfil_admin():
    # Obtener el administrador actual
    admin = Administrador.query.get(session['usuario_id'])
    
    if request.method == 'POST':
        try:
            # Actualizar datos básicos
            admin.nombre = request.form['nombre']
            admin.apellido = request.form['apellido']
            admin.email = request.form['email']
            admin.telefono = request.form['telefono']
            
            # Verificar si se quiere cambiar la contraseña
            nueva_contraseña = request.form.get('contraseña')
            repetir_contraseña = request.form.get('repetir_contraseña')
            
            if nueva_contraseña:
                if nueva_contraseña != repetir_contraseña:
                    flash('Las contraseñas no coinciden', 'danger')
                    return render_template("templates_dashboard/templates_admin/perfil_admin.html", admin=admin)
                admin.contraseña = nueva_contraseña
            
            db.session.commit()
            
            # Actualizar datos de la sesión
            session['nombres'] = admin.nombre
            session['apellidos'] = admin.apellido
            
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('perfil_admin'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')
            return render_template("templates_dashboard/templates_admin/perfil_admin.html", admin=admin)
    
    return render_template("templates_dashboard/templates_admin/perfil_admin.html", admin=admin)

# Rutas del Medico
@app.route("/dashboard_medico")
@requiere_rol('Medico')
def dashboard_medico():
    medico_id = session.get('usuario_id')
    
    # Obtener las últimas 5 consultas (tratamientos) del médico
    ultimas_consultas = Tratamiento.query.filter_by(medico_id=medico_id)\
        .order_by(Tratamiento.fecha.desc())\
        .limit(5)\
        .all()
    
    # Crear lista de consultas con información del paciente
    consultas_info = []
    for consulta in ultimas_consultas:
        paciente = Paciente.query.get(consulta.paciente_id)
        consultas_info.append({
            'fecha': consulta.fecha,
            'paciente_nombre': f"{paciente.nombre} {paciente.apellido}",
            'motivo': consulta.motivo
        })
    
    return render_template("templates_dashboard/templates_medicos/inicio_medico.html", 
                         nombres=session.get('nombres'), 
                         apellidos=session.get('apellidos'),
                         consultas=consultas_info)

@app.route("/agenda")
@requiere_rol('Medico')
def agenda():
    # Obtener el ID del médico de la sesión
    medico_id = session.get('usuario_id')
    
    # Obtener todas las citas del médico
    citas = Cita.query.filter_by(medico_id=medico_id).order_by(Cita.fecha.desc()).all()
    
    # Para cada cita, obtener la información del paciente
    citas_info = []
    for cita in citas:
        paciente = Paciente.query.get(cita.paciente_id)
        citas_info.append({
            'id': cita.id,
            'hora_inicio': cita.hora_inicio,
            'paciente_nombre': f"{paciente.nombre} {paciente.apellido}",
            'motivo': cita.motivo,
            'estado': cita.estado,
            'fecha': cita.fecha
        })
    
    return render_template("templates_dashboard/templates_medicos/agenda_medica/crear_agenda.html", 
                         citas=citas_info)

@app.route("/atender_cita/<int:id_cita>", methods=['GET', 'POST'])
@requiere_rol('Medico')
def atender_cita(id_cita):
    cita = Cita.query.get_or_404(id_cita)
    paciente = Paciente.query.get(cita.paciente_id)
    
    if request.method == 'POST':
        try:
            estado_anterior = cita.estado
            nuevo_estado = request.form['estado']
            cita.estado = nuevo_estado
            db.session.commit()

            # Notificar al paciente sobre el cambio de estado
            if estado_anterior != nuevo_estado:
                crear_notificacion(
                    paciente.id,
                    f'Tu cita del {cita.fecha.strftime("%d/%m/%Y")} ha sido {nuevo_estado}',
                    'primary' if nuevo_estado == 'completada' else 'warning'
                )

            flash('Cita actualizada con éxito', 'success')
            return redirect(url_for('agenda'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la cita: {str(e)}', 'danger')
    
    return render_template("templates_dashboard/templates_medicos/agenda_medica/editar_agenda.html",
                         cita=cita,
                         paciente=paciente)

@app.route("/historia_medica")
@requiere_rol('Medico')
def historia_medica():
    # Obtener todos los pacientes que tienen tratamientos con este médico
    medico_id = session.get('usuario_id')
    pacientes_con_tratamientos = Paciente.query.join(Tratamiento).filter(
        Tratamiento.medico_id == medico_id
    ).distinct().all()
    
    return render_template("templates_dashboard/templates_medicos/historia_medica.html",
                         pacientes=pacientes_con_tratamientos)

@app.route("/ver_historia/<int:paciente_id>")
@requiere_rol('Medico')
def ver_historia(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    medico_id = session.get('usuario_id')
    
    # Obtener todos los tratamientos del paciente con este médico
    tratamientos = Tratamiento.query.filter_by(
        paciente_id=paciente_id,
        medico_id=medico_id
    ).order_by(Tratamiento.fecha.desc()).all()
    
    return render_template("templates_dashboard/templates_medicos/ver_historia.html",
                         paciente=paciente,
                         tratamientos=tratamientos)

@app.route("/exportar_historia_pdf/<int:paciente_id>")
@requiere_rol('Medico')
def exportar_historia_pdf(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    medico = Medico.query.get(session.get('usuario_id'))
    tratamientos = Tratamiento.query.filter_by(
        paciente_id=paciente_id,
        medico_id=medico.id
    ).order_by(Tratamiento.fecha.desc()).all()

    # Crear PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter,
                          rightMargin=30, leftMargin=30,
                          topMargin=30, bottomMargin=30)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_principal_style = ParagraphStyle(
        'TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=6,
        alignment=1,
        textColor=colors.HexColor('#1a237e')
    )
    
    subtitulo_style = ParagraphStyle(
        'Subtitulo',
        parent=styles['Heading2'],
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor('#303f9f'),
        spaceBefore=0,
        spaceAfter=20
    )

    seccion_style = ParagraphStyle(
        'Seccion',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#1a237e'),
        spaceBefore=15,
        spaceAfter=5
    )

    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=4,
        spaceAfter=4,
        leading=12
    )
    
    # Encabezado
    elements.append(Paragraph("MediCitas Plus", titulo_principal_style))
    elements.append(Paragraph("Historia Clínica", subtitulo_style))
    elements.append(Spacer(1, 10))
    
    # Información del paciente
    datos_paciente = [
        [Paragraph("<b>INFORMACIÓN DEL PACIENTE</b>", seccion_style)],
        [Paragraph(f"<b>Nombre:</b> {paciente.nombre} {paciente.apellido}", normal_style)],
        [Paragraph(f"<b>{paciente.tipo_documento}:</b> {paciente.numero_documento}", normal_style)],
        [Paragraph(f"<b>Fecha de Nacimiento:</b> {paciente.fecha_nacimiento.strftime('%d/%m/%Y')}", normal_style)],
        [Paragraph(f"<b>Grupo Sanguíneo:</b> {paciente.grupo_sanguineo}", normal_style)],
        [Paragraph(f"<b>EPS:</b> {paciente.eps}", normal_style)],
    ]
    
    tabla_info = Table(datos_paciente, colWidths=[doc.width])
    tabla_info.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,0), 0.5, colors.HexColor('#1a237e')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eaf6')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(tabla_info)
    elements.append(Spacer(1, 20))
    
    # Historial de tratamientos
    elements.append(Paragraph("HISTORIAL DE TRATAMIENTOS", seccion_style))
    elements.append(Spacer(1, 10))
    
    for t in tratamientos:
        # Obtener el médico del tratamiento
        medico = Medico.query.get(t.medico_id)
        
        # Crear tabla para cada tratamiento
        datos_tratamiento = [
            [Paragraph(f"<b>Fecha:</b> {t.fecha.strftime('%d/%m/%Y')}", normal_style)],
            [Paragraph(f"<b>Médico:</b> Dr(a). {medico.nombre} {medico.apellido} - {medico.especialidad}", normal_style)],
            [Paragraph("<b>Motivo de Consulta:</b>", normal_style)],
            [Paragraph(t.motivo, normal_style)],
            [Paragraph("<b>Diagnóstico:</b>", normal_style)],
            [Paragraph(t.diagnostico, normal_style)],
            [Paragraph("<b>Tratamiento:</b>", normal_style)],
            [Paragraph(t.tratamiento, normal_style)]
        ]
        
        if t.receta:
            datos_tratamiento.extend([
                [Paragraph("<b>Receta:</b>", normal_style)],
                [Paragraph(t.receta, normal_style)]
            ])
            
        if t.notas:
            datos_tratamiento.extend([
                [Paragraph("<b>Notas Adicionales:</b>", normal_style)],
                [Paragraph(t.notas, normal_style)]
            ])
        
        tabla_tratamiento = Table(datos_tratamiento, colWidths=[doc.width])
        tabla_tratamiento.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BACKGROUND', (0,0), (0,1), colors.HexColor('#e8eaf6')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(tabla_tratamiento)
        elements.append(Spacer(1, 15))
    
    # Pie de página
    elements.append(Spacer(1, 30))
    pie_style = ParagraphStyle(
        'Pie',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Este documento es un registro médico confidencial.", pie_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("MediCitas Plus - Cuidando tu salud", pie_style))
    
    # Generar PDF
    doc.build(elements)
    
    return send_file(
        temp_file.name,
        download_name=f'historia_clinica_{paciente.numero_documento}.pdf',
        as_attachment=True
    )

@app.route("/tratamiento")
@requiere_rol('Medico')
def tratamiento():
    medico_id = session.get('usuario_id')
    print(f"ID del médico en sesión: {medico_id}")  # Debug
    
    tratamientos = Tratamiento.query.filter_by(medico_id=medico_id).all()
    print(f"Número de tratamientos encontrados: {len(tratamientos)}")  # Debug
    
    for t in tratamientos:  # Debug
        print(f"Tratamiento ID: {t.id}, Paciente: {t.paciente.nombre}, Médico ID: {t.medico_id}")
    
    return render_template("templates_dashboard/templates_medicos/tratamiento/tratamientos.html", tratamientos=tratamientos)

@app.route("/buscar_paciente", methods=['POST'])
@requiere_rol('Medico')
def buscar_paciente():
    paciente_id = request.form.get('paciente_id')
    paciente_seleccionado = None
    if paciente_id:
        paciente_seleccionado = Paciente.query.get(paciente_id)
    
    # Mantener los datos del formulario si existen
    form_data = {
        'motivo': request.form.get('motivo', ''),
        'diagnostico': request.form.get('diagnostico', ''),
        'tratamiento': request.form.get('tratamiento', ''),
        'receta': request.form.get('receta', ''),
        'notas': request.form.get('notas', '')
    }
    
    pacientes = Paciente.query.all()
    return render_template("templates_dashboard/templates_medicos/tratamiento/agregar_tratamiento.html",
                         pacientes=pacientes,
                         paciente_seleccionado=paciente_seleccionado,
                         **form_data)

@app.route("/agregar_tratamiento", methods=['GET', 'POST'])
@requiere_rol('Medico')
def agregar_tratamiento():
    if request.method == 'GET':
        pacientes = Paciente.query.all()
        return render_template("templates_dashboard/templates_medicos/tratamiento/agregar_tratamiento.html",
                            pacientes=pacientes,
                            paciente_seleccionado=None)
    
    # Método POST
    paciente_id = request.form.get('paciente_id')
    motivo = request.form.get('motivo')
    diagnostico = request.form.get('diagnostico')
    tratamiento = request.form.get('tratamiento')
    receta = request.form.get('receta')
    notas = request.form.get('notas')
    medico_id = session.get('usuario_id')

    try:
        nuevo_tratamiento = Tratamiento(
            paciente_id=paciente_id,
            medico_id=medico_id,
            motivo=motivo,
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            receta=receta,
            notas=notas,
            fecha=datetime.now()  # Agregamos la fecha actual
        )

        db.session.add(nuevo_tratamiento)
        db.session.commit()
        flash("Tratamiento agregado con éxito", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al agregar el tratamiento: {str(e)}", "danger")

    return redirect(url_for('tratamiento'))

@app.route("/editar_tratamiento/<int:id>", methods=['GET', 'POST'])
@requiere_rol('Medico')
def editar_tratamiento(id):
    tratamiento = Tratamiento.query.get_or_404(id)
    paciente = Paciente.query.get(tratamiento.paciente_id)

    if request.method == 'POST':
        try:
            tratamiento.motivo = request.form['motivo']
            tratamiento.diagnostico = request.form['diagnostico']
            tratamiento.tratamiento = request.form['tratamiento']
            tratamiento.receta = request.form['receta']
            tratamiento.notas = request.form['notas']

            db.session.commit()
            flash("Tratamiento actualizado con éxito", "success")
            return redirect(url_for('tratamiento'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el tratamiento: {str(e)}", "danger")

    return render_template("templates_dashboard/templates_medicos/tratamiento/editar_tratamiento.html",
                         tratamiento=tratamiento,
                         paciente=paciente)

@app.route("/eliminar_tratamiento/<int:id>", methods=['POST'])
@requiere_rol('Medico')
def eliminar_tratamiento(id):
    tratamiento = Tratamiento.query.get_or_404(id)

    try:
        db.session.delete(tratamiento)
        db.session.commit()
        flash("Tratamiento eliminado con éxito", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar el tratamiento: {str(e)}", "danger")

    return redirect(url_for('tratamiento'))

@app.route("/verificar_tratamientos")
def verificar_tratamientos():
    tratamientos = Tratamiento.query.all()
    for t in tratamientos:
        print(f"Tratamiento ID: {t.id}, Paciente: {t.paciente.nombre}, Médico ID: {t.medico_id}")
    return "Verifica la consola del servidor para los resultados"

@app.route("/perfil_medico", methods=['GET', 'POST'])
@requiere_rol('Medico')
def perfil_medico():
    # Obtener el médico actual
    medico = Medico.query.get(session['usuario_id'])
    
    # Diccionario de mapeo de valores a nombres de especialidades
    especialidades_map = {
        'alergologia': 'Alergología',
        'anestesiologia': 'Anestesiología',
        'angiologia': 'Angiología',
        'cardiologia': 'Cardiología',
        'cirugia_cardiovascular': 'Cirugía Cardiovascular',
        'cirugia_general': 'Cirugía General',
        'cirugia_maxilofacial': 'Cirugía Maxilofacial',
        'cirugia_plastica': 'Cirugía Plástica',
        'cirugia_toracica': 'Cirugía Torácica',
        'cirugia_vascular': 'Cirugía Vascular',
        'dermatologia': 'Dermatología',
        'endocrinologia': 'Endocrinología',
        'gastroenterologia': 'Gastroenterología',
        'geriatria': 'Geriatría',
        'ginecologia': 'Ginecología y Obstetricia',
        'hematologia': 'Hematología',
        'infectologia': 'Infectología',
        'medicina_deporte': 'Medicina del Deporte',
        'medicina_familiar': 'Medicina Familiar',
        'medicina_fisica': 'Medicina Física y Rehabilitación',
        'medicina_forense': 'Medicina Forense',
        'medicina_interna': 'Medicina Interna',
        'medicina_nuclear': 'Medicina Nuclear',
        'medicina_preventiva': 'Medicina Preventiva y Salud Pública',
        'nefrologia': 'Nefrología',
        'neumologia': 'Neumología',
        'neurocirugia': 'Neurocirugía',
        'neurologia': 'Neurología',
        'nutriologia': 'Nutriología',
        'oftalmologia': 'Oftalmología',
        'oncologia': 'Oncología',
        'ortopedia': 'Ortopedia y Traumatología',
        'otorrinolaringologia': 'Otorrinolaringología',
        'pediatria': 'Pediatría',
        'psiquiatria': 'Psiquiatría',
        'radiologia': 'Radiología',
        'reumatologia': 'Reumatología',
        'toxicologia': 'Toxicología',
        'urologia': 'Urología'
    }
    
    if request.method == 'POST':
        try:
            # Actualizar datos básicos
            medico.nombre = request.form['nombre']
            medico.apellido = request.form['apellido']
            medico.tipo_documento = request.form['tipo_documento']
            medico.numero_documento = request.form['numero_documento']
            medico.genero = request.form['genero']
            medico.email = request.form['email']
            medico.telefono = request.form['telefono']
            medico.direccion = request.form['direccion']
            
            # Obtener el valor de la especialidad y convertirlo al nombre completo
            especialidad_valor = request.form.get('especialidad', '')
            medico.especialidad = especialidades_map.get(especialidad_valor, especialidad_valor)
            
            medico.numero_registro = request.form.get('registro_medico', '')
            medico.anios_experiencia = request.form.get('años', 0)
            
            # Actualizar contraseña si se proporciona
            nueva_contraseña = request.form.get('contraseña')
            if nueva_contraseña:
                medico.contraseña = nueva_contraseña
            
            db.session.commit()
            
            # Actualizar datos de la sesión
            session['nombres'] = medico.nombre
            session['apellidos'] = medico.apellido
            
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('perfil_medico'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')
            return render_template("templates_dashboard/templates_medicos/perfil_medico.html", medico=medico)
    
    return render_template("templates_dashboard/templates_medicos/perfil_medico.html", medico=medico)

# Rutas del Paciente
@app.route("/dashboard_paciente")
@requiere_rol('Paciente')
def dashboard_paciente():
    # Obtener el ID del paciente de la sesión
    paciente_id = session.get('usuario_id')
    
    # Obtener las citas del paciente
    citas = Cita.query.filter_by(paciente_id=paciente_id).order_by(Cita.fecha.desc()).all()
    
    return render_template("templates_dashboard/templates_paciente/inicio_paciente.html", 
                         nombres=session.get('nombres'), 
                         apellidos=session.get('apellidos'),
                         citas=citas)

@app.route("/mis_citas")
@requiere_rol('Paciente')
def mis_citas():
    # Obtener el ID del paciente de la sesión
    paciente_id = session.get('usuario_id')
    
    # Obtener todas las citas del paciente
    citas = Cita.query.filter_by(paciente_id=paciente_id).order_by(Cita.fecha.desc()).all()
    
    return render_template("templates_dashboard/templates_paciente/mis_citas.html", citas=citas)

@app.route("/solicitar_cita", methods=['GET', 'POST'])
@requiere_rol('Paciente')
def solicitar_cita():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            medico_id = request.form.get('medico')
            servicio = request.form.get('servicio')
            fecha = request.form.get('fecha')
            horario_inicio = request.form.get('horario_inicio')
            horario_fin = request.form.get('horario_fin')
            motivo = request.form.get('motivo')

            # Validar que todos los campos estén presentes
            if not all([medico_id, servicio, fecha, horario_inicio, horario_fin, motivo]):
                flash('Por favor complete todos los campos requeridos', 'error')
                return redirect(url_for('solicitar_cita'))

            # Convertir strings a objetos datetime
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(horario_inicio, '%H:%M').time()
            hora_fin = datetime.strptime(horario_fin, '%H:%M').time()

            # Validar que la fecha sea futura
            if fecha_dt < datetime.now().date():
                flash('La fecha de la cita debe ser futura', 'error')
                return redirect(url_for('solicitar_cita'))

            # Validar que la hora de fin sea posterior a la hora de inicio
            if hora_fin <= hora_inicio:
                flash('La hora de fin debe ser posterior a la hora de inicio', 'error')
                return redirect(url_for('solicitar_cita'))

            # Crear nueva cita
            nueva_cita = Cita(
                paciente_id=session.get('usuario_id'),
                medico_id=medico_id,
                servicio=servicio,
                fecha=fecha_dt,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                motivo=motivo,
                estado='pendiente'
            )

            db.session.add(nueva_cita)
            db.session.commit()

            # Notificar al paciente
            crear_notificacion(
                session.get('usuario_id'),
                f'Tu cita para {servicio} ha sido solicitada para el {fecha_dt.strftime("%d/%m/%Y")}',
                'success'
            )

            # Notificar al médico
            crear_notificacion(
                medico_id,
                f'Nueva cita solicitada para el {fecha_dt.strftime("%d/%m/%Y")} - {servicio}',
                'primary'
            )

            flash('Cita solicitada exitosamente', 'success')
            return redirect(url_for('mis_citas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al solicitar la cita: {str(e)}', 'error')
            return redirect(url_for('solicitar_cita'))

    # Para solicitudes GET, mostrar el formulario
    medicos = Medico.query.all()
    return render_template('templates_dashboard/templates_paciente/solicitar_cita.html', 
                         medicos=medicos,
                         now=datetime.now())

@app.route("/mi_historia")
@requiere_rol('Paciente')
def mi_historia():
    # Obtener el ID del paciente de la sesión
    paciente_id = session.get('usuario_id')
    paciente = Paciente.query.get_or_404(paciente_id)
    
    # Obtener todos los tratamientos del paciente ordenados por fecha
    tratamientos = Tratamiento.query.filter_by(
        paciente_id=paciente_id
    ).order_by(Tratamiento.fecha.desc()).all()
    
    return render_template("templates_dashboard/templates_paciente/mi_historia.html",
                         paciente=paciente,
                         tratamientos=tratamientos)

@app.route("/mis_pagos")
@requiere_rol('Paciente')
def mis_pagos():
    paciente_id = session.get('usuario_id')
    
    facturas = Factura.query.join(Cita).filter(Cita.paciente_id == paciente_id).order_by(Factura.fecha.desc()).all()
    
    total_pagado = sum(factura.total for factura in facturas if factura.estado == 'pagada')
    total_pendiente = sum(factura.total for factura in facturas if factura.estado == 'pendiente')
    
    primera_factura_pendiente = next((f for f in facturas if f.estado == 'pendiente'), None)
    
    db.session.expire_all()
    
    return render_template('templates_dashboard/templates_paciente/mis_pagos.html',
                         facturas=facturas,
                         total_pagado=total_pagado,
                         total_pendiente=total_pendiente,
                         primera_factura_pendiente=primera_factura_pendiente)

@app.route("/procesar_pago/<int:factura_id>", methods=['POST'])
@requiere_rol('Paciente')
def procesar_pago(factura_id):
    try:
        factura = Factura.query.get_or_404(factura_id)
        logger.info(f"Procesando pago para factura ID: {factura_id}")
        logger.info(f"Estado actual de la factura: {factura.estado}")
        
        if factura.cita.paciente_id != session.get('usuario_id'):
            logger.warning(f"Intento de acceso no autorizado a factura {factura_id}")
            abort(403)
        
        if factura.estado != 'pendiente':
            logger.warning(f"Intento de pagar factura no pendiente: {factura_id}, Estado: {factura.estado}")
            flash('Esta factura no está pendiente de pago', 'warning')
            return redirect(url_for('mis_pagos'))
        
        logger.info(f"Actualizando estado de factura {factura_id} de '{factura.estado}' a 'pagada'")
        factura.estado = 'pagada'
        factura.tipo_pago = 'Tarjeta'
        factura.fecha_pago = datetime.now()
        
        db.session.add(factura)
        db.session.flush()
        db.session.commit()

        # Notificar al paciente
        crear_notificacion(
            session.get('usuario_id'),
            f'Pago procesado exitosamente para la factura {factura.numero_factura}',
            'success'
        )
        
        logger.info(f"Factura {factura_id} actualizada exitosamente. Nuevo estado: {factura.estado}")
        flash('Pago procesado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al procesar el pago de la factura {factura_id}: {str(e)}")
        flash(f'Error al procesar el pago: {str(e)}', 'danger')
    
    return redirect(url_for('mis_pagos'))

@app.route("/exportar_factura/<int:factura_id>")
@requiere_rol('Paciente')
def exportar_factura(factura_id):
    try:
        factura = Factura.query.get_or_404(factura_id)
        
        # Verificar que la factura pertenece al paciente actual
        if factura.cita.paciente_id != session.get('usuario_id'):
            abort(403)
        
        # Generar el PDF usando la función existente
        pdf_path = generar_pdf_factura(factura)
        
        return send_file(
            pdf_path,
            download_name=f'factura_{factura.numero_factura}.pdf',
            as_attachment=True
        )
    except Exception as e:
        flash(f'Error al generar la factura: {str(e)}', 'danger')
        return redirect(url_for('mis_pagos'))
    finally:
        # Limpiar el archivo temporal después de enviarlo
        if 'pdf_path' in locals():
            try:
                os.unlink(pdf_path)
            except:
                pass

@app.route("/mi_perfil_paciente", methods=['GET', 'POST'])
@requiere_rol('Paciente')
def mi_perfil_paciente():
    # Obtener el paciente actual
    paciente = Paciente.query.get(session['usuario_id'])
    
    if request.method == 'POST':
        try:
            # Actualizar datos básicos
            paciente.nombre = request.form['nombre']
            paciente.apellido = request.form['apellido']
            paciente.tipo_documento = request.form['tipo_documento']
            paciente.numero_documento = request.form['numero_documento']
            paciente.fecha_nacimiento = request.form['fecha_nacimiento']
            paciente.genero = request.form['genero']
            paciente.grupo_sanguineo = request.form['grupo_sanguineo']
            paciente.email = request.form['email']
            paciente.telefono = request.form['telefono']
            paciente.direccion = request.form['direccion']
            paciente.eps = request.form['eps']
            paciente.contacto_emergencia = request.form['contacto_emergencia']
            paciente.telefono_emergencia = request.form['telefono_emergencia']
            
            # Verificar si se quiere cambiar la contraseña
            nueva_contraseña = request.form.get('contraseña')
            repetir_contraseña = request.form.get('repetir_contraseña')
            
            if nueva_contraseña:
                if nueva_contraseña != repetir_contraseña:
                    flash('Las contraseñas no coinciden', 'danger')
                    return render_template("templates_dashboard/templates_paciente/mi_perfil_paciente.html", paciente=paciente)
                paciente.contraseña = nueva_contraseña
            
            db.session.commit()
            
            # Actualizar datos de la sesión
            session['nombres'] = paciente.nombre
            session['apellidos'] = paciente.apellido
            
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('mi_perfil_paciente'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')
            return render_template("templates_dashboard/templates_paciente/mi_perfil_paciente.html", paciente=paciente)
    
    return render_template("templates_dashboard/templates_paciente/mi_perfil_paciente.html", paciente=paciente)

@app.route("/logout")
def logout():
    if 'usuario_id' in session:
        session.clear()
        flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('login'))

@app.route("/eliminar_medico/<int:id>")
@requiere_rol('Administrador')
def eliminar_medico(id):
    try:
        medico = Medico.query.get_or_404(id)
        
        # Primero eliminamos las citas asociadas
        citas_asociadas = Cita.query.filter_by(medico_id=id).all()
        for cita in citas_asociadas:
            db.session.delete(cita)
            
        # Luego eliminamos los tratamientos asociados
        tratamientos_asociados = Tratamiento.query.filter_by(medico_id=id).all()
        for tratamiento in tratamientos_asociados:
            db.session.delete(tratamiento)
            
        # Finalmente eliminamos al médico
        db.session.delete(medico)
        db.session.commit()
        
        mensaje = f'El médico {medico.nombre} {medico.apellido} fue eliminado exitosamente'
        if len(citas_asociadas) > 0:
            mensaje += f' junto con {len(citas_asociadas)} citas'
        if len(tratamientos_asociados) > 0:
            mensaje += f' y {len(tratamientos_asociados)} tratamientos'
        flash(mensaje, 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el médico: {str(e)}', 'danger')
    return redirect(url_for('medico_admin'))

@app.route("/eliminar_paciente/<int:id>")
@requiere_rol('Administrador')
def eliminar_paciente(id):
    try:
        paciente = Paciente.query.get_or_404(id)
        
        # Primero eliminamos las citas asociadas
        citas_asociadas = Cita.query.filter_by(paciente_id=id).all()
        for cita in citas_asociadas:
            # Eliminamos las facturas asociadas a cada cita
            facturas = Factura.query.filter_by(id_cita=cita.id).all()
            for factura in facturas:
                db.session.delete(factura)
            db.session.delete(cita)
            
        # Luego eliminamos los tratamientos asociados
        tratamientos_asociados = Tratamiento.query.filter_by(paciente_id=id).all()
        for tratamiento in tratamientos_asociados:
            db.session.delete(tratamiento)
            
        # Finalmente eliminamos al paciente
        db.session.delete(paciente)
        db.session.commit()
        
        mensaje = f'El paciente {paciente.nombre} {paciente.apellido} fue eliminado exitosamente'
        if len(citas_asociadas) > 0:
            mensaje += f' junto con {len(citas_asociadas)} citas'
        if len(tratamientos_asociados) > 0:
            mensaje += f' y {len(tratamientos_asociados)} tratamientos'
        flash(mensaje, 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el paciente: {str(e)}', 'danger')
    return redirect(url_for('paciente_admin'))

@app.route("/eliminar_cita_admin/<int:id_cita>")
@requiere_rol('Administrador')
def eliminar_cita_admin(id_cita):
    try:
        # Primero buscamos y eliminamos las facturas asociadas
        facturas = Factura.query.filter_by(id_cita=id_cita).all()
        num_facturas = len(facturas)
        
        for factura in facturas:
            db.session.delete(factura)
        
        # Después eliminamos la cita
        cita = Cita.query.get_or_404(id_cita)
        db.session.delete(cita)
        db.session.commit()
        
        if num_facturas > 0:
            flash(f'Se eliminó la cita y {num_facturas} factura(s) asociada(s)', 'success')
        else:
            flash('Cita eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al eliminar la cita: {str(e)}")
        flash(f'Error al eliminar la cita: {str(e)}', 'danger')
    return redirect(url_for('citas_admin'))

@app.route("/eliminar_factura_admin/<int:id_factura>")
@requiere_rol('Administrador')
def eliminar_factura_admin(id_factura):
    try:
        factura = Factura.query.get_or_404(id_factura)
        db.session.delete(factura)
        db.session.commit()
        flash('Factura eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la factura: {str(e)}', 'danger')
    return redirect(url_for('factura_admin'))

@app.route("/agregar_medico", methods=['GET', 'POST'])
@requiere_rol('Administrador')
def agregar_medico():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        especialidad = request.form['especialidad']
        email = request.form['email']
        telefono = request.form['telefono']
        contraseña = request.form['contraseña']
        repetir_contraseña = request.form['repetir_contraseña']

        if contraseña != repetir_contraseña:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for('medico_admin'))

        try:
            nuevo_medico = Medico(
                nombre=nombre,
                apellido=apellido,
                especialidad=especialidad,
                email=email,
                telefono=telefono,
                contraseña=contraseña,
                rol='Medico'
            )

            db.session.add(nuevo_medico)
            db.session.commit()
            flash("Médico agregado con éxito", "success")
            return redirect(url_for('medico_admin'))

        except Exception as e:
            db.session.rollback()
            if 'Duplicate entry' in str(e) and 'email' in str(e):
                flash("Error: El correo electrónico ya está registrado", "danger")
            else:
                flash("Error al agregar el médico. Por favor, verifique los datos", "danger")
            return redirect(url_for('medico_admin'))

    return render_template("templates_dashboard/templates_admin/medico/agregar.html")

@app.route("/exportar_pdf/<int:id_factura>")
@requiere_rol('Administrador')
def exportar_pdf(id_factura):
    factura = Factura.query.get_or_404(id_factura)
    pdf_path = generar_pdf_factura(factura)
    return send_file(pdf_path, as_attachment=True, download_name=f"factura_{factura.numero_factura}.pdf")

@app.route("/exportar_mi_historia_pdf")
@requiere_rol('Paciente')
def exportar_mi_historia_pdf():
    # Obtener el ID del paciente de la sesión
    paciente_id = session.get('usuario_id')
    paciente = Paciente.query.get_or_404(paciente_id)
    
    # Obtener todos los tratamientos del paciente
    tratamientos = Tratamiento.query.filter_by(
        paciente_id=paciente_id
    ).order_by(Tratamiento.fecha.desc()).all()

    # Crear PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter,
                          rightMargin=30, leftMargin=30,
                          topMargin=30, bottomMargin=30)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_principal_style = ParagraphStyle(
        'TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=6,
        alignment=1,
        textColor=colors.HexColor('#1a237e')
    )
    
    subtitulo_style = ParagraphStyle(
        'Subtitulo',
        parent=styles['Heading2'],
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor('#303f9f'),
        spaceBefore=0,
        spaceAfter=20
    )

    seccion_style = ParagraphStyle(
        'Seccion',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#1a237e'),
        spaceBefore=15,
        spaceAfter=5
    )

    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=4,
        spaceAfter=4,
        leading=12
    )
    
    # Encabezado
    elements.append(Paragraph("MediCitas Plus", titulo_principal_style))
    elements.append(Paragraph("Mi Historia Clínica", subtitulo_style))
    elements.append(Spacer(1, 10))
    
    # Información del paciente
    datos_paciente = [
        [Paragraph("<b>INFORMACIÓN DEL PACIENTE</b>", seccion_style)],
        [Paragraph(f"<b>Nombre:</b> {paciente.nombre} {paciente.apellido}", normal_style)],
        [Paragraph(f"<b>{paciente.tipo_documento}:</b> {paciente.numero_documento}", normal_style)],
        [Paragraph(f"<b>Fecha de Nacimiento:</b> {paciente.fecha_nacimiento.strftime('%d/%m/%Y')}", normal_style)],
        [Paragraph(f"<b>Grupo Sanguíneo:</b> {paciente.grupo_sanguineo}", normal_style)],
        [Paragraph(f"<b>EPS:</b> {paciente.eps}", normal_style)],
    ]
    
    tabla_info = Table(datos_paciente, colWidths=[doc.width])
    tabla_info.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,0), 0.5, colors.HexColor('#1a237e')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eaf6')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(tabla_info)
    elements.append(Spacer(1, 20))
    
    # Historial de tratamientos
    elements.append(Paragraph("HISTORIAL DE TRATAMIENTOS", seccion_style))
    elements.append(Spacer(1, 10))
    
    for t in tratamientos:
        # Obtener el médico del tratamiento
        medico = Medico.query.get(t.medico_id)
        
        # Crear tabla para cada tratamiento
        datos_tratamiento = [
            [Paragraph(f"<b>Fecha:</b> {t.fecha.strftime('%d/%m/%Y')}", normal_style)],
            [Paragraph(f"<b>Médico:</b> Dr(a). {medico.nombre} {medico.apellido} - {medico.especialidad}", normal_style)],
            [Paragraph("<b>Motivo de Consulta:</b>", normal_style)],
            [Paragraph(t.motivo, normal_style)],
            [Paragraph("<b>Diagnóstico:</b>", normal_style)],
            [Paragraph(t.diagnostico, normal_style)],
            [Paragraph("<b>Tratamiento:</b>", normal_style)],
            [Paragraph(t.tratamiento, normal_style)]
        ]
        
        if t.receta:
            datos_tratamiento.extend([
                [Paragraph("<b>Receta:</b>", normal_style)],
                [Paragraph(t.receta, normal_style)]
            ])
            
        if t.notas:
            datos_tratamiento.extend([
                [Paragraph("<b>Notas Adicionales:</b>", normal_style)],
                [Paragraph(t.notas, normal_style)]
            ])
        
        tabla_tratamiento = Table(datos_tratamiento, colWidths=[doc.width])
        tabla_tratamiento.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BACKGROUND', (0,0), (0,1), colors.HexColor('#e8eaf6')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(tabla_tratamiento)
        elements.append(Spacer(1, 15))
    
    # Pie de página
    elements.append(Spacer(1, 30))
    pie_style = ParagraphStyle(
        'Pie',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Este documento es un registro médico confidencial.", pie_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("MediCitas Plus - Cuidando tu salud", pie_style))
    
    # Generar PDF
    doc.build(elements)
    
    return send_file(
        temp_file.name,
        download_name=f'mi_historia_clinica_{paciente.numero_documento}.pdf',
        as_attachment=True
    )

@app.route("/ver_historia_paciente")
@requiere_rol('Paciente')
def ver_historia_paciente():
    # Obtener el ID del paciente de la sesión
    paciente_id = session.get('usuario_id')
    paciente = Paciente.query.get_or_404(paciente_id)
    
    # Obtener todos los tratamientos del paciente ordenados por fecha
    tratamientos = Tratamiento.query.filter_by(
        paciente_id=paciente_id
    ).order_by(Tratamiento.fecha.desc()).all()
    
    return render_template("templates_dashboard/templates_paciente/ver_historia_paciente.html",
                         paciente=paciente,
                         tratamientos=tratamientos)

@app.route('/obtener_notificaciones')
def obtener_notificaciones():
    """Obtiene las notificaciones del usuario actual."""
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'notificaciones': []})
    
    # Obtener notificaciones de los últimos 7 días
    fecha_limite = datetime.now() - timedelta(days=7)
    notificaciones = Notificacion.query.filter(
        Notificacion.usuario_id == usuario_id,
        Notificacion.fecha >= fecha_limite
    ).order_by(Notificacion.fecha.desc()).all()
    
    return jsonify({
        'notificaciones': [{
            'id': n.id,
            'mensaje': n.mensaje,
            'tipo': n.tipo,
            'fecha': n.fecha.strftime('%d/%m/%Y %H:%M'),
            'leida': n.leida
        } for n in notificaciones]
    })

@app.route('/marcar_notificacion_leida/<int:notificacion_id>', methods=['POST'])
def marcar_notificacion_leida(notificacion_id):
    """Marca una notificación como leída."""
    try:
        notificacion = Notificacion.query.get_or_404(notificacion_id)
        notificacion.leida = True
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def crear_notificacion(usuario_id, mensaje, tipo='primary'):
    """Crea una nueva notificación."""
    try:
        notificacion = Notificacion(
            usuario_id=usuario_id,
            mensaje=mensaje,
            tipo=tipo,
            fecha=datetime.now(),
            leida=False
        )
        db.session.add(notificacion)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear notificación: {str(e)}")
        return False

@app.route('/test_notificaciones')
def test_notificaciones():
    """Ruta de prueba para generar notificaciones."""
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    tipos = ['primary', 'success', 'warning']
    mensajes = [
        'Esta es una notificación de prueba tipo información',
        '¡Operación completada con éxito!',
        'Atención: Esta es una notificación de advertencia'
    ]
    
    for tipo, mensaje in zip(tipos, mensajes):
        crear_notificacion(usuario_id, mensaje, tipo)
    
    flash('Notificaciones de prueba creadas', 'success')
    if session.get('rol') == 'Administrador':
        return redirect(url_for('dashboard_admin'))
    elif session.get('rol') == 'Medico':
        return redirect(url_for('dashboard_medico'))
    else:
        return redirect(url_for('dashboard_paciente'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)