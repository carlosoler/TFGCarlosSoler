import json
from functools import wraps

from flask import Flask, render_template, jsonify

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate
import requests

from model.model import db, get_user_id, Alumno, get_users, add_to_db, get_user_by_id, Skill, get_tableSkill_id, \
    get_user_tableSkill_id, get_all_skills_foruser, get_empresa_id, Empresa, get_skills_foruser, update_skills, get_emp, \
    get_users, get_alumn, get_ofer_id, get_empId_byOffer, get_empName, Oferta, get_alumnos, get_ofertas, get_id_by_user

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

def restricted_access_toAlumn(func):
    @wraps(func)
    def wrappper_restricted_access():
        emp = get_emp(username=session['username'])
        if not emp:
            flash('Necesitas tener un usuario de Empresa para acceder a esta página')
            return redirect(url_for('home'))
        return func()
    return wrappper_restricted_access

def restricted_access_toEmp(func):
    @wraps(func)
    def wrappper_restricted_access():
        alum = get_alumn(username=session['username'])
        if not alum:
            flash('Necesitas tener un alumno para acceder a esta página')
            return redirect(url_for('home'))
        return func()
    return wrappper_restricted_access


@app.route('/', methods=["GET", "POST"])
def main():
    page = 'login'
    if request.method == 'POST' and 'nombreUsuario' in request.form and 'pwd' in request.form:
        username = request.form.get('nombreUsuario')
        password = request.form.get('pwd')
        user = get_users(username)
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

@app.route('/resgistroEmpresa', methods=["GET", "POST"])
def registro_empresa():
    if request.method == 'POST':
        id_reg = get_empresa_id()
        nombreUsuario_emp_reg = request.form.get('username')
        contrasena_emp_reg = request.form.get('pass')
        nombre_emp_reg = request.form.get('nombre')
        telefono_reg = request.form.get('tel')
        email_reg = request.form.get('email')
        emp = Empresa(empresa_id=id_reg, username=nombreUsuario_emp_reg, password=contrasena_emp_reg,
                      empresa_nombre=nombre_emp_reg, telefono=telefono_reg, email=email_reg)
        add_to_db(emp)
        flash("Empresa creada correctamente. Por favor inicie sesión con su usuario")
    return render_template('registroEmpresa.html')

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

@app.route('/crearOfertas', methods=["GET", "POST"])
@login_required
@restricted_access_toAlumn
def crearOfertas():
    if session.get('logged_in'):
        if request.method == 'POST':
            id_reg = get_ofer_id()
            id_emp_reg = get_empId_byOffer(session['username'])
            nombre_emp_reg = get_empName(session['username'])
            job_tittle_reg = request.form.get('title_job')
            ciudad_reg = request.form.get('city')
            oferta = Oferta(job_id=id_reg, empresa_id=id_emp_reg, empresa_nombre=nombre_emp_reg, job_tittle=job_tittle_reg,
                          ciudad=ciudad_reg)
            add_to_db(oferta)
            flash("Oferta creada correctamente.")
        return render_template('crearOfertas.html')

@app.route('/mostrar_skills')
@login_required
@restricted_access_toEmp
def mostrar_skills():
    if session.get('logged_in'):
        lista_skills = get_all_skills_foruser(get_user_tableSkill_id(session['username']))
        return render_template('mostrar_skills.html', lista_skills=lista_skills, username=session['username'])

@app.route('/ver_alumnos')
@login_required
@restricted_access_toAlumn
def ver_alumnos():
    if session.get('logged_in'):
        alumnos = get_alumnos()
        return render_template('verAlumnos.html', alumnos=alumnos)

@app.route('/ver_ofertas')
@login_required
@restricted_access_toEmp
def ver_ofertas():
    if session.get('logged_in'):
        ofertas = get_ofertas()
        return render_template('verOfertas.html', ofertas=ofertas)

@app.route('/ver_skills_alumnos')
@login_required
@restricted_access_toAlumn
def ver_skills_alumnos():
    if session.get('logged_in'):
        usuario = request.args.get('username')
        lista_skills = get_all_skills_foruser(get_user_tableSkill_id(usuario))
        return render_template('ver_skill_alumnos.html', lista_skills=lista_skills, username=usuario)

@app.route('/chat')
@login_required
def chat():
    if session.get('logged_in'):
        return render_template('chat.html')

@app.route('/perfil')
@login_required
def perfil():
    if session.get('logged_in'):
        emp = get_emp(username=session['username'])
        alum = get_alumn(username=session['username'])
        return render_template('perfil.html', username=session['username'], emp=emp, alum=alum)

@app.route('/recomendarOfertas', methods=["GET","POST"])
@login_required
@restricted_access_toEmp
def recomendarOfertas():
    if session.get('logged_in'):
        id = get_id_by_user(session['username'])
        if request.method == 'POST':
            r = requests.post('http://127.0.0.1:8001/recomendar.practicas', params={'codigoEstudiante': id})
            ejemplo = r.json()
            return render_template('recomendarOfertas.html', username=session['username'], ejemplo=ejemplo, id=id)
        return render_template('recomendarOfertas.html', username=session['username'], id=id)



@app.route('/survey', methods=["GET", "POST"])
@login_required
@restricted_access_toEmp
def survey():
    if session.get('logged_in'):
        if request.method == 'POST':
            id_user_session = get_user_tableSkill_id(session['username'])
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
            if not id_user_session:
                skills = Skill(id=id_reg, alumno_id=alumno_id_reg, grado=grado_reg, nota_media=nota_media_reg,
                               ingles=ingles_reg, aleman=aleman_reg, frances=frances_reg,
                               capacidad_analitica=capacidad_analitica_reg,
                               trabajo_equipo=trabajo_equipo_reg, comunicacion=comunicacion_reg,
                               pensamiento_critico=pensamiento_critico_reg,
                               inovacion=inovacion_reg, liderazgo=liderazgo_reg, decision_making=decision_making_reg,
                               problem_solving=problem_solving_reg,
                               marketing=marketing_reg, e_commerce=e_commerce_reg, diseno_grafico=diseno_grafico_reg,
                               matematicas=matematicas_reg,
                               estadistica=estadistica_reg, gestion_proyectos=gestion_proyectos_reg,
                               redes_sociales=redes_sociales_reg, sostenibilidad=sostenibilidad_reg,
                               inteligencia_artificial=inteligencia_artificial_reg, big_data=big_data_reg,
                               machine_learning=machine_learning_reg,
                               analisis_datos=analisis_datos_reg, bases_datos=bases_datos_reg, cloud=cloud_reg,
                               intenet_of_things=intenet_of_things_reg,
                               networks=networks_reg, sistemas_operativos=sistemas_operativos_reg,
                               web_desarrollo=web_desarrollo_reg,
                               web_diseno=web_diseno_reg, r=r_reg, java=java_reg, pascal=pascal_reg, python=python_reg)

                add_to_db(skills)
                flash("Skills creadas!")
            else:
                person = update_skills(get_user_tableSkill_id(session['username']))
                person.grado = grado_reg
                person.nota_media = nota_media_reg
                person.ingles = ingles_reg
                person.aleman = aleman_reg
                person.frances = frances_reg
                person.capacidad_analitica = capacidad_analitica_reg
                person.trabajo_equipo = trabajo_equipo_reg
                person.comunicacion = comunicacion_reg
                person.pensamiento_critico = pensamiento_critico_reg
                person.inovacion = inovacion_reg
                person.liderazgo = liderazgo_reg
                person.decision_making = decision_making_reg
                person.problem_solving = problem_solving_reg
                person.marketing = marketing_reg
                person.e_commerce = e_commerce_reg
                person.diseno_grafico = diseno_grafico_reg
                person.matematicas = matematicas_reg
                person.estadistica = estadistica_reg
                person.gestion_proyectos = gestion_proyectos_reg
                person.redes_sociales = redes_sociales_reg
                person.sostenibilidad = sostenibilidad_reg
                person.inteligencia_artificial = inteligencia_artificial_reg
                person.big_data = big_data_reg
                person.machine_learning = machine_learning_reg
                person.analisis_datos = analisis_datos_reg
                person.bases_datos = bases_datos_reg
                person.cloud = cloud_reg
                person.intenet_of_things = intenet_of_things_reg
                person.networks = networks_reg
                person.sistemas_operativos = sistemas_operativos_reg
                person.web_desarrollo = web_desarrollo_reg
                person.web_diseno = web_diseno_reg
                person.r = r_reg
                person.java = java_reg
                person.pascal = pascal_reg
                person.python = python_reg
                db.session.commit()
                flash("Skills modificadas!")
        return render_template('survey.html')


@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run()
