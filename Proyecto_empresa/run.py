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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)