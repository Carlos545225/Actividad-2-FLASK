from flask import Flask, render_template, request, redirect, flash


app = Flask(__name__)
@app.route("/")
@app.route("/index")
def index():
    return render_template("pagina_principal/index.html")

@app.route("/login")
def login():
    return render_template("templates_login/login.html")

@app.route("/registro")
def registro():
    return render_template("templates_login/registro.html")

@app.route("/recuperar")
def recuperar():
    return render_template("templates_login/recuperacion.html")

@app.route("/dashboard")
def dashboard():
    return render_template("templates_dashboard/dashboard.html")

@app.route("/gestion_de_medicos")
def gestion_de_medicos():
    return render_template("templates_dashboard/gestion_de_medicos.html")

@app.route("/gestion_de_pacientes")
def gestion_de_pacientes():
    return render_template("templates_dashboard/gestion_de_pacientes.html")

@app.route("/gestion_de_facturas")
def gestion_de_facturas():
    return render_template("templates_dashboard/gestion_de_facturacion.html")

@app.route("/gestion_de_citas")
def gestion_de_citas():
    return render_template("templates_dashboard/gestion_de_citas.html")

@app.route("/reportes")
def reportes():
    return render_template("templates_dashboard/reportes.html")





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)