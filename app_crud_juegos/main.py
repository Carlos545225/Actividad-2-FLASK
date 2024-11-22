from flask import Flask, render_template, request, redirect, flash
import controlador_juegos

app = Flask(__name__)

@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juego.html", juegos=juegos)

@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]

    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    return redirect("/juegos")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
