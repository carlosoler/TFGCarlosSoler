from functools import wraps

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate
import requests

from back.model.model import db, get_user_id, get_user_by_id, get_user_tableSkill_id, get_all_skills_foruser, get_empresa_id, \
    get_emp, \
    get_users, get_alumn, get_ofer_id, get_empId_byOffer, get_empName, get_id_by_user, get_alumn_sinOfertas, get_adm, get_alumn_sinOfertasByUsername, \
    get_Skills_by_alumno_id, get_oferAsignada_id

app3 = Flask(__name__)
app3.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/JOBS'
app3.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app3.secret_key = '8d438b8cca764385ae8652fefd10487c7eec02a7c5a6fb471ad8ccff0412405d'
#socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.login_view = 'main'

login_manager.init_app(app3)
db.init_app(app3)
migrate = Migrate(app3, db)

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

def restricted_access_toAlumnConOferta(func):
    @wraps(func)
    def wrappper_restricted_access():
        alum = get_alumn_sinOfertasByUsername(username=session['username'])
        if not alum:
            flash('Este nombre de usuario tiene ya una oferta asignada')
            return redirect(url_for('home'))
        return func()
    return wrappper_restricted_access

def onlyAdmin(func):
    @wraps(func)
    def wrappper_restricted_access():
        adm = get_adm(username=session['username'])
        if not adm:
            flash('Necesitas ser un administrador para acceder a esta página')
            return redirect(url_for('home'))
        return func()
    return wrappper_restricted_access


@app3.route('/', methods=["GET", "POST"])
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

@app3.route('/resgistroUsuario', methods=["GET", "POST"])
def registro_usuario():
    if request.method == 'POST':
        user = {
                    "alumno_id": get_user_id(),
                    "apellido": request.form.get('apellido'),
                    "email": request.form.get('email'),
                    "nombre": request.form.get('nombre'),
                    "ofert_asignada": 0,
                    "password": request.form.get('pass'),
                    "telefono": request.form.get('tel'),
                    "username": request.form.get('username')
                }
        requests.post('http://127.0.0.1:5000/alumnos', json=user)
        flash("Usuario creado correctamente. Por favor inicie sesión con su usuario")
    return render_template('registroUsuario.html')

@app3.route('/resgistroEmpresa', methods=["GET", "POST"])
def registro_empresa():
    if request.method == 'POST':
        empresa = {
            "empresa_id": get_empresa_id(),
            "username": request.form.get('username'),
            "password": request.form.get('pass'),
            "empresa_nombre":  request.form.get('nombre'),
            "telefono": request.form.get('tel'),
            "email": request.form.get('email')
        }
        requests.post('http://127.0.0.1:5000/empresas', json=empresa)
        flash("Empresa creada correctamente. Por favor inicie sesión con su usuario")
    return render_template('registroEmpresa.html')

@app3.route('/home')
@login_required
def home():
    if session.get('logged_in'):
        return render_template('home.html')

@app3.route('/crearOfertas', methods=["GET", "POST"])
@login_required
@restricted_access_toAlumn
def crearOfertas():
    if session.get('logged_in'):
        if request.method == 'POST':
            oferta = {
                        "job_id": get_ofer_id(),
                        "empresa_id": get_empId_byOffer(session['username']),
                        "empresa_nombre": get_empName(session['username']),
                        "job_tittle": request.form.get('title_job'),
                        "ciudad": request.form.get('city'),
                        "grado": request.form.get('grado'),
                        "nota_media": request.form.get('nota_media'),
                        "ingles": request.form.get('ingles_level'),
                        "aleman": request.form.get('aleman_level'),
                        "frances": request.form.get('frances_level'),
                        "trabajo_equipo": request.form.get('trabajoEquipo_level'),
                        "comunicacion": request.form.get('comunicacion_level'),
                        "matematicas": request.form.get('matematicas_level'),
                        "estadistica": request.form.get('estadistica_level'),
                        "gestion_proyectos": request.form.get('gestionProyectos_level'),
                        "sostenibilidad": request.form.get('sostenibilidad_level'),
                        "big_data": request.form.get('bigData_level'),
                        "programacion": request.form.get('progra_level')
            }

            requests.post('http://127.0.0.1:5000/ofertas_nuevas', json=oferta)
            flash("Oferta creada correctamente.")
        return render_template('crearOfertas.html')

@app3.route('/asignarOfertas', methods=["GET", "POST"])
@login_required
@onlyAdmin
def asignarOfertas():
    r = requests.get('http://127.0.0.1:5000/ofertas_nuevas')
    ofertas_nuevas = r.json()
    alumnos_sinOfertas = get_alumn_sinOfertas()
    if session.get('logged_in'):
        if request.method == 'POST':
            alumno = request.form.get('alumnos')
            oferta_id = request.form.get('ofertas')
            alumno_id_mod = get_id_by_user(alumno)

            #Cambiamos el valor de oferta asignada a 1
            mod_oferta_asignada = {
                "ofert_asignada": 1
            }
            requests.put('http://127.0.0.1:5000/alumnos/%d' % alumno_id_mod, json=mod_oferta_asignada)

            #Creamos oferta asignada
            oferta_nueva = requests.get('http://127.0.0.1:5000/ofertas_nuevas/%s' % oferta_id)
            oferta_nueva_js = oferta_nueva.json()

            ofertaAsig = {
                "job_id": get_oferAsignada_id(),
                "alumno_id": alumno_id_mod,
                "empresa_id": oferta_nueva_js['empresa_id'],
                "empresa_nombre": oferta_nueva_js['empresa_nombre'],
                "job_tittle": oferta_nueva_js['job_tittle'],
                "ciudad": oferta_nueva_js['ciudad'],
                "grado": oferta_nueva_js['grado'],
                "nota_media": oferta_nueva_js['nota_media'],
                "ingles": oferta_nueva_js['ingles'],
                "aleman": oferta_nueva_js['aleman'],
                "frances": oferta_nueva_js['frances'],
                "trabajo_equipo": oferta_nueva_js['trabajo_equipo'],
                "comunicacion": oferta_nueva_js['comunicacion'],
                "matematicas": oferta_nueva_js['matematicas'],
                "estadistica": oferta_nueva_js['estadistica'],
                "gestion_proyectos": oferta_nueva_js['gestion_proyectos'],
                "sostenibilidad": oferta_nueva_js['sostenibilidad'],
                "big_data": oferta_nueva_js['big_data'],
                "programacion": oferta_nueva_js['programacion']
            }
            requests.post('http://127.0.0.1:5000/ofertas_asignadas', json=ofertaAsig)

            requests.delete('http://127.0.0.1:5000/ofertas_nuevas/%s' % oferta_id)

            db.session.commit()
            flash("Oferta asignada con éxito!")

    return render_template('asignarOfertas.html', ofertas_nuevas=ofertas_nuevas, alumnos_sinOfertas=alumnos_sinOfertas)

@app3.route('/mostrar_skills')
@login_required
@restricted_access_toEmp
def mostrar_skills():
    if session.get('logged_in'):
        lista_skills = get_all_skills_foruser(get_user_tableSkill_id(session['username']))
        return render_template('mostrar_skills.html', lista_skills=lista_skills, username=session['username'])

@app3.route('/ver_alumnos')
@login_required
@restricted_access_toAlumn
def ver_alumnos():
    if session.get('logged_in'):
        r = requests.get('http://127.0.0.1:5000/alumnosSinOferta')
        alumnos = r.json()
        return render_template('verAlumnos.html', alumnos=alumnos)

@app3.route('/ver_ofertas')
@login_required
@restricted_access_toEmp
def ver_ofertas():
    if session.get('logged_in'):
        r = requests.get('http://127.0.0.1:5000/ofertas_nuevas')
        ofertas = r.json()
        return render_template('verOfertas.html', ofertas=ofertas)

@app3.route('/ver_skills_alumnos')
@login_required
@restricted_access_toAlumn
def ver_skills_alumnos():
    if session.get('logged_in'):
        usuario = request.args.get('username')
        lista_skills = get_all_skills_foruser(get_user_tableSkill_id(usuario))
        return render_template('ver_skill_alumnos.html', lista_skills=lista_skills, username=usuario)

@app3.route('/chat')
@login_required
def chat():
    if session.get('logged_in'):
        return render_template('chat.html')

@app3.route('/perfil')
@login_required
def perfil():
    if session.get('logged_in'):
        emp = get_emp(username=session['username'])
        alum = get_alumn(username=session['username'])
        adm = get_adm(username=session['username'])
        return render_template('perfil.html', username=session['username'], emp=emp, alum=alum, adm=adm)

@app3.route('/recomendarOfertas', methods=["GET","POST"])
@login_required
@restricted_access_toAlumnConOferta
def recomendarOfertas():
    if session.get('logged_in'):
        #id = get_id_by_user(session['username'])
        if request.method == 'POST':
            #r = requests.post('http://127.0.0.1:3097/prueba_json', json=json_alum)
            r = requests.post('http://127.0.0.1:5253/recomendacion_alumno_nuevo', params={'alumnonuevo': session['username']})
            ejemplo = r.json()
            print(ejemplo)
            return render_template('recomendarOfertas.html', username=session['username'], ejemplo=ejemplo)
        return render_template('recomendarOfertas.html', username=session['username'])

@app3.route('/similitudOfertasNuevas', methods=["GET","POST"])
@login_required
@onlyAdmin
def similitudOfertasNuevas():
    if session.get('logged_in'):
        if request.method == 'POST':
            r = requests.post('http://127.0.0.1:4982/ofertas_nuevas', params={'a': 71, 'b': 80})
            ejemplo = r.json()
            return render_template('similitudOfertasNuevas.html', username=session['username'], ejemplo=ejemplo)
        return render_template('similitudOfertasNuevas.html', username=session['username'])

@app3.route('/survey', methods=["GET", "POST"])
@login_required
@restricted_access_toEmp
def survey():
    if session.get('logged_in'):
        if request.method == 'POST':
            usuario = session['username']
            id_user_session = get_user_tableSkill_id(session['username'])
            alumno_id_skill = get_Skills_by_alumno_id(id_user_session)
            skill = {
                "grado": request.form.get('grado'),
                "nota_media": request.form.get('nota_media'),
                "ingles": request.form.get('ingles_level'),
                "aleman": request.form.get('aleman_level'),
                "frances": request.form.get('frances_level'),
                "capacidad_analitica": request.form.get('capAnalitica_level'),
                "trabajo_equipo": request.form.get('trabajoEquipo_level'),
                "comunicacion": request.form.get('comunicacion_level'),
                "pensamiento_critico": request.form.get('pensamientoCritico_level'),
                "inovacion": request.form.get('innovacion_level'),
                "liderazgo": request.form.get('liderazgo_level'),
                "decision_making": request.form.get('tomaDecisiones_level'),
                "problem_solving": request.form.get('solucionProblemas_level'),
                "marketing": request.form.get('marketing_level'),
                "e_commerce": request.form.get('ecommerce_level'),
                "diseno_grafico": request.form.get('disenoGrafico_level'),
                "matematicas": request.form.get('matematicas_level'),
                "estadistica": request.form.get('estadistica_level'),
                "gestion_proyectos": request.form.get('gestionProyectos_level'),
                "redes_sociales": request.form.get('redesSociales_level'),
                "sostenibilidad": request.form.get('sostenibilidad_level'),
                "inteligencia_artificial": request.form.get('inteligenciaArtificial_level'),
                "big_data": request.form.get('bigData_level'),
                "machine_learning": request.form.get('machineLearning_level'),
                "analisis_datos": request.form.get('analisisDatos_level'),
                "bases_datos": request.form.get('basesDatos_level'),
                "cloud": request.form.get('cloud_level'),
                "intenet_of_things": request.form.get('iot_level'),
                "networks": request.form.get('redes_level'),
                "sistemas_operativos": request.form.get('sistemasOperativos_level'),
                "web_desarrollo": request.form.get('desarrolloWeb_level'),
                "web_diseno": request.form.get('disenoWeb_level'),
                "r": request.form.get('r_level'),
                "java": request.form.get('java_level'),
                "pascal": request.form.get('pascal_level'),
                "python": request.form.get('python_level'),
            }
            if not alumno_id_skill:
                requests.post('http://127.0.0.1:5000/skills/%s' % usuario, json=skill)
                db.session.commit()
                flash("Skills creadas")
            else:
                requests.put('http://127.0.0.1:5000/skills/%s' % usuario, json=skill)
                db.session.commit()
                flash("Skills Modificadas")
        return render_template('survey.html')

@app3.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('main'))


if __name__ == '__main__':
    app3.run(port=5001)