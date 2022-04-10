from flask import Flask, render_template

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate

from model.model import db, get_user_id, Alumno, get_user, add_to_db, get_user_by_id, Skill, get_tableSkill_id, \
    get_user_tableSkill_id, get_all_skills_foruser

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
    page = 'login'
    if request.method == 'POST' and 'nombreUsuario' in request.form and 'pwd' in request.form:
        username = request.form.get('nombreUsuario')
        password = request.form.get('pwd')
        user = get_user(username)
        if not user:
            flash('¡El usuario que ha introducido no existe!')
        elif user.password == password:
            login_user(user)
            session['logged_in'] = True
            session['username'] = user.username
            session.modified = True
            return redirect(url_for('home'))
        else:
            flash('Contraseña incorrecta')
    return render_template('login.html', page=page)

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
    return render_template('registroUsuario.html')

@app.route('/resgistroEmpresa')
def registro_empresa():
    return render_template('resgistroEmpresa.html')

@app.route('/home')
@login_required
def home():
    if session.get('logged_in'):
        return render_template('home.html')

@app.route('/alumnos')
@login_required
def alumnos():
    if session.get('logged_in'):
        return render_template('alumnos.html')

@app.route('/empresas')
@login_required
def empresas():
    if session.get('logged_in'):
        return render_template('empresas.html')

@app.route('/mostrar_skills')
@login_required
def mostrar_skills():
    if session.get('logged_in'):
        lista_skills = get_all_skills_foruser(get_user_tableSkill_id(session['username']))
        return render_template('mostrar_skills.html', lista_skills=lista_skills, username=session['username'])

@app.route('/survey', methods=["GET", "POST"])
@login_required
def survey():
    if session.get('logged_in'):
        if request.method == 'POST':
            id_reg = get_tableSkill_id()
            alumno_id_reg = get_user_tableSkill_id(session['username'])
            grado_reg = request.form.get('grado')
            nota_media_reg = request.form.get('nota_media')
            ingles_reg = request.form.get('ingles_level')
            aleman_reg = request.form.get('aleman_level')
            frances_reg = request.form.get('frances_level')
            capacidad_analitica_reg = request.form.get('capAnalitica_level')
            trabajo_equipo_reg = request.form.get('trabajoEquipo_level')
            comunicacion_reg = request.form.get('comunicacion_level')
            pensamiento_critico_reg = request.form.get('pensamientoCritico_level')
            inovacion_reg = request.form.get('innovacion_level')
            liderazgo_reg = request.form.get('liderazgo_level')
            decision_making_reg = request.form.get('tomaDecisiones_level')
            problem_solving_reg = request.form.get('solucionProblemas_level')
            marketing_reg = request.form.get('marketing_level')
            e_commerce_reg = request.form.get('ecommerce_level')
            diseno_grafico_reg = request.form.get('disenoGrafico_level')
            matematicas_reg = request.form.get('matematicas_level')
            estadistica_reg = request.form.get('estadistica_level')
            gestion_proyectos_reg = request.form.get('gestionProyectos_level')
            redes_sociales_reg = request.form.get('redesSociales_level')
            sostenibilidad_reg = request.form.get('sostenibilidad_level')
            inteligencia_artificial_reg = request.form.get('inteligenciaArtificial_level')
            big_data_reg = request.form.get('bigData_level')
            machine_learning_reg = request.form.get('machineLearning_level')
            analisis_datos_reg = request.form.get('analisisDatos_level')
            bases_datos_reg = request.form.get('basesDatos_level')
            cloud_reg = request.form.get('cloud_level')
            intenet_of_things_reg = request.form.get('iot_level')
            networks_reg = request.form.get('redes_level')
            sistemas_operativos_reg = request.form.get('sistemasOperativos_level')
            web_desarrollo_reg = request.form.get('desarrolloWeb_level')
            web_diseno_reg = request.form.get('disenoWeb_level')
            r_reg = request.form.get('r_level')
            java_reg = request.form.get('java_level')
            pascal_reg = request.form.get('pascal_level')
            python_reg = request.form.get('python_level')

            skills = Skill(id = id_reg, alumno_id = alumno_id_reg, grado = grado_reg, nota_media = nota_media_reg,
                           ingles = ingles_reg, aleman = aleman_reg, frances = frances_reg, capacidad_analitica = capacidad_analitica_reg,
                           trabajo_equipo = trabajo_equipo_reg, comunicacion = comunicacion_reg, pensamiento_critico = pensamiento_critico_reg,
                           inovacion = inovacion_reg, liderazgo = liderazgo_reg, decision_making = decision_making_reg, problem_solving = problem_solving_reg,
                           marketing = marketing_reg,e_commerce = e_commerce_reg, diseno_grafico = diseno_grafico_reg, matematicas = matematicas_reg,
                           estadistica = estadistica_reg, gestion_proyectos = gestion_proyectos_reg, redes_sociales = redes_sociales_reg, sostenibilidad = sostenibilidad_reg,
                           inteligencia_artificial = inteligencia_artificial_reg, big_data = big_data_reg, machine_learning = machine_learning_reg,
                           analisis_datos = analisis_datos_reg, bases_datos = bases_datos_reg, cloud = cloud_reg, intenet_of_things = intenet_of_things_reg,
                           networks = networks_reg, sistemas_operativos = sistemas_operativos_reg, web_desarrollo = web_desarrollo_reg,
                           web_diseno = web_diseno_reg, r = r_reg, java = java_reg, pascal = pascal_reg, python = python_reg)

            add_to_db(skills)
            flash("SKILLs.")
        return render_template('survey.html')

@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run()
