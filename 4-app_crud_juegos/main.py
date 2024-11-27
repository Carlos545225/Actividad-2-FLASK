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


@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect("/juegos")


@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    juego = controlador_juegos.odtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/detalles/<int:id>")
def detalle_juego(id):
    juego = controlador_juegos.odtener_juego_por_id(id)
    return render_template("detalles_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
