from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/mi_blog'  # Usuario root sin contraseña
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.titulo

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    posts = Post.query.order_by(Post.fecha_creacion.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/crear', methods=('GET', 'POST'))
def crear_post():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']

        nuevo_post = Post(titulo=titulo, contenido=contenido)
        db.session.add(nuevo_post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('crear_post.html')

if __name__ == '__main__':
    app.run(debug=True)