from flask import Flask, render_template, redirect, request 
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/", methods=['GET', 'POST'])
def Aritmetica():
    if request.method == "POST":
        num1 = float(request.form.get("n1"))
        num2 = float(request.form.get("n2"))

        suma = num1 + num2
        resta = num1 - num2
        multiplicacion = num1 * num2
        division = num1 / num2 if num2 != 0 else "Error: División por cero"

        return render_template("index.html", 
                               total_suma=suma,
                               total_resta=resta,
                               total_multiplicacion=multiplicacion,
                               total_division=division)
    return render_template("index.html")

@app.route("/divisa", methods=['GET', 'POST'])
def divisa():
    if request.method == "POST":
        num1 = float(request.form.get("n1"))
        dolar = round(4404.19)
        convertir= num1 * dolar

        return render_template("divisa.html", total_divisa=convertir)
                              
    return render_template("divisa.html")


if __name__ == "__main__":
    app.run(debug=True)
