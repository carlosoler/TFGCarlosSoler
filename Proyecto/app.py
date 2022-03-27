from flask import Flask, render_template

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate

from model.model import db, get_user_id, Alumno, get_user, add_to_db, get_user_by_id

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/JOBS'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '8d438b8cca764385ae8652fefd10487c7eec02a7c5a6fb471ad8ccff0412405d'

login_manager = LoginManager()
login_manager.login_view = 'main'

login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(id):
    return get_user_by_id(id)

@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == 'POST' and 'nombreUsuario' in request.form and 'pwd' in request.form:
        username = request.form.get('nombreUsuario')
        password = request.form.get('pwd')
        user = get_user(username)
        if not user:
            flash('¡El usuario que ha introducido no existe!')
        elif user.password == password:
            return redirect(url_for('home'))
        else:
            flash('Contraseña incorrecta')
    return render_template('login.html')

@app.route('/resgistroUsuario', methods=["GET", "POST"])
def registro_usuario():
    if request.method == 'POST':
        id_reg = get_user_id()
        nombreUsuario_reg = request.form.get('username')
        nombre_reg = request.form.get('nombre')
        apellido_reg = request.form.get('apellido')
        contrasena_reg = request.form.get('pass')
        telefono_reg = request.form.get('tel')
        email_reg = request.form.get('email')
        user = Alumno(alumno_id=id_reg, username=nombreUsuario_reg, password=contrasena_reg, nombre=nombre_reg,
                      apellido=apellido_reg, telefono=telefono_reg, email=email_reg)

        add_to_db(user)
        flash("Usuario creado correctamente. Por favor inicie sesión con su usuario")
    return render_template('resgistroUsuario.html')

@app.route('/resgistroEmpresa')
def registro_empresa():
    return render_template('resgistroEmpresa.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/alumnos')
def alumnos():
    return render_template('alumnos.html')

@app.route('/empresas')
def empresas():
    return render_template('empresas.html')


if __name__ == '__main__':
    app.run()
