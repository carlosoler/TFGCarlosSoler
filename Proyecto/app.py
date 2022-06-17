import json
from functools import wraps

from flask import Flask, render_template, jsonify

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate
import requests

from flask_socketio import SocketIO

from model.model import db, get_user_id, Alumno, get_users, add_to_db, get_user_by_id, Skill, get_tableSkill_id, \
    get_user_tableSkill_id, get_all_skills_foruser, get_empresa_id, Empresa, get_skills_foruser, update_skills, get_emp, \
    get_users, get_alumn, get_ofer_id, get_empId_byOffer, get_empName, get_alumnos, get_ofertas, \
    get_id_by_user, OfertaNueva, get_ofertas_nuevas, get_alumn_sinOfertas, update_alumno, update_ofertaAsignada, \
    OfertaAsignada, update_ofertaNueva, get_eliminarOfertaNueva, get_adm, get_alumn_sinOfertasByUsername, \
    OfertaNuevaSchema, get_empId_byNameEmpresa, AlumnoSchema, AlumnoSchemaSinPass, EmpresaSchemaSinPass, EmpresaSchema, \
    SkillsSchema, get_Skill_id_by_alumno_id, get_Skills_by_alumno_id, get_SkillID_by_alumno_id, OfertaAsignadaSchema, \
    get_oferAsignada_id

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/JOBS'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '8d438b8cca764385ae8652fefd10487c7eec02a7c5a6fb471ad8ccff0412405d'
#socketio = SocketIO(app, cors_allowed_origins="*")

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

@app.route('/resgistroEmpresa', methods=["GET", "POST"])
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

@app.route('/home')
@login_required
def home():
    if session.get('logged_in'):
        return render_template('home.html')

@app.route('/crearOfertas', methods=["GET", "POST"])
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

@app.route('/asignarOfertas', methods=["GET", "POST"])
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
        r = requests.get('http://127.0.0.1:5000/alumnosSinOferta')
        alumnos = r.json()
        return render_template('verAlumnos.html', alumnos=alumnos)

@app.route('/ver_ofertas')
@login_required
@restricted_access_toEmp
def ver_ofertas():
    if session.get('logged_in'):
        r = requests.get('http://127.0.0.1:5000/ofertas_nuevas')
        ofertas = r.json()
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
        adm = get_adm(username=session['username'])
        return render_template('perfil.html', username=session['username'], emp=emp, alum=alum, adm=adm)

@app.route('/recomendarOfertas', methods=["GET","POST"])
@login_required
@restricted_access_toAlumnConOferta
def recomendarOfertas():
    if session.get('logged_in'):
        #id = get_id_by_user(session['username'])
        if request.method == 'POST':
            r = requests.post('http://127.0.0.1:4982/recomendacion_alumno_nuevo', params={'alumnonuevo': 71})
            ejemplo = r.json()
            return render_template('recomendarOfertas.html', username=session['username'], ejemplo=ejemplo)
        return render_template('recomendarOfertas.html', username=session['username'])

@app.route('/similitudOfertasNuevas', methods=["GET","POST"])
@login_required
@onlyAdmin
def similitudOfertasNuevas():
    if session.get('logged_in'):
        if request.method == 'POST':
            r = requests.post('http://127.0.0.1:4982/ofertas_nuevas', params={'a': 71, 'b': 80})
            ejemplo = r.json()
            return render_template('similitudOfertasNuevas.html', username=session['username'], ejemplo=ejemplo)
        return render_template('similitudOfertasNuevas.html', username=session['username'])

@app.route('/survey', methods=["GET", "POST"])
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

#END-POINTS ofertas nuevas

@app.route('/ofertas_nuevas', methods = ['GET'])
def get_ofertas_nuevas():
    oferta_nueva = OfertaNueva.get_all()
    serializer = OfertaNuevaSchema(many=True)
    data = serializer.dump(oferta_nueva)
    return jsonify(data)

@app.route('/ofertas_nuevas/<int:job_id>', methods = ['GET'])
def get_ofertas_nuevas_by_id(job_id):
    oferta_nueva = OfertaNueva.get_by_id(job_id)
    serializer = OfertaNuevaSchema()
    data = serializer.dump(oferta_nueva)
    return jsonify(data)

@app.route('/ofertas_nuevas', methods = ['POST'])
def crear_oferta_nueva():
    data = request.get_json()
    nuevaOferta = OfertaNueva(job_id=get_ofer_id(), empresa_id=get_empId_byNameEmpresa(data.get("empresa_nombre")), empresa_nombre=data.get("empresa_nombre"),
        job_tittle=data.get("job_tittle"), ciudad=data.get("ciudad"), grado=data.get("grado"), nota_media=data.get("nota_media"),
        ingles=data.get("ingles"), aleman=data.get("aleman"), frances=data.get("frances"),
        trabajo_equipo=data.get("trabajo_equipo"), comunicacion=data.get("comunicacion"), matematicas=data.get("matematicas"),
        estadistica=data.get("estadistica"), gestion_proyectos=data.get("gestion_proyectos"), sostenibilidad=data.get("sostenibilidad"),
        big_data=data.get("big_data"), programacion=data.get("programacion"))

    nuevaOferta.save()
    serializer = OfertaNuevaSchema()
    data = serializer.dump(nuevaOferta)
    return jsonify(data), 201

@app.route('/ofertas_nuevas/<int:job_id>', methods = ['DELETE'])
def borrar_oferta_nueva(job_id):
    oferta_borrar = OfertaNueva.get_by_id(job_id)
    oferta_borrar.delete()

    return jsonify({"message": "Oferta nueva borrada correctamente"}), 204

#END-POINTS alumnos

@app.route('/alumnos', methods = ['GET'])
def get_alumnos():
    alumnos = Alumno.get_all()
    serializer = AlumnoSchemaSinPass(many=True)
    data = serializer.dump(alumnos)
    return jsonify(data)

@app.route('/alumnosSinOferta', methods = ['GET'])
def get_alumnos_sin_Oferta():
    alumnos = get_alumn_sinOfertas()
    serializer = AlumnoSchemaSinPass(many=True)
    data = serializer.dump(alumnos)
    return jsonify(data)

@app.route('/alumnos/<int:alumno_id>', methods = ['GET'])
def get_alumnos_by_id(alumno_id):
    alumnos = Alumno.get_by_id(alumno_id)
    serializer = AlumnoSchemaSinPass()
    data = serializer.dump(alumnos)
    return jsonify(data)

@app.route('/alumnos', methods = ['POST'])
def crear_alumno_nuevo():
    data = request.get_json()
    user = Alumno(alumno_id=get_user_id(), username=data.get("username"), password=data.get("password"), nombre=data.get("nombre"),
                  apellido=data.get("apellido"), telefono=data.get("telefono"), email=data.get("email"), ofert_asignada= 0)
    user.save()
    serializer = AlumnoSchema()
    data = serializer.dump(user)
    return jsonify(data), 201

@app.route('/alumnos/<int:alumno_id>', methods = ['PUT'])
def modificar_alumno(alumno_id):
    alumno_modificar = Alumno.get_by_id(alumno_id)
    data = request.get_json()
    alumno_modificar.ofert_asignada = data.get('ofert_asignada')
    db.session.commit()
    serializer = AlumnoSchema()
    skill_data = serializer.dump(alumno_modificar)
    return jsonify(skill_data), 200

@app.route('/alumnos/<int:alumno_id>', methods = ['DELETE']) #Solo borra si no tiene skills asociadas, habria que borrar las skills primero
def borrar_alumno(alumno_id):
    alumno_borrar = Alumno.get_by_id(alumno_id)
    alumno_borrar.delete()
    return jsonify({"message": "Alumno borrado correctamente"}), 204

#END-POINTS empresas

@app.route('/empresas', methods = ['GET'])
def get_empresas():
    empresas = Empresa.get_all()
    serializer = EmpresaSchemaSinPass(many=True)
    data = serializer.dump(empresas)
    return jsonify(data)

@app.route('/empresas/<int:empresa_id>', methods = ['GET'])
def get_empresas_by_id(empresa_id):
    empresas = Empresa.get_by_id(empresa_id)
    serializer = EmpresaSchemaSinPass()
    data = serializer.dump(empresas)
    return jsonify(data)

@app.route('/empresas', methods = ['POST'])
def crear_empresa_nueva():
    data = request.get_json()
    empresa = Empresa(empresa_id=get_empresa_id(), username=data.get("username"), password=data.get("password"),
                      empresa_nombre=data.get("empresa_nombre"), telefono=data.get("telefono"), email=data.get("email"))
    empresa.save()
    serializer = EmpresaSchema()
    data = serializer.dump(empresa)
    return jsonify(data), 201

@app.route('/empresas/<int:empresa_id>', methods = ['DELETE'])
def borrar_empresa(empresa_id):
    empresa_borrar = Empresa.get_by_id(empresa_id)
    empresa_borrar.delete()

    return jsonify({"message": "Empresa borrada correctamente"}), 204

#END-POINTS skills

@app.route('/skills/<string:username>', methods = ['GET'])
def get_skills_by_alumno_id(username):
    id_user_session = get_user_tableSkill_id(username)
    skill_id = get_SkillID_by_alumno_id(id_user_session)
    skills = Skill.get_by_id(skill_id)
    serializer = SkillsSchema()
    data = serializer.dump(skills)
    return jsonify(data)

@app.route('/skills/<string:username>', methods = ['POST'])
def crear_skill_nueva(username):
    id_user_session = get_user_tableSkill_id(username)
    data = request.get_json()
    skill = Skill(id= get_tableSkill_id(), alumno_id= id_user_session, grado= data.get("grado"), nota_media = data.get("nota_media"),
                  ingles= data.get("ingles"), aleman= data.get("aleman"), frances= data.get("frances"), capacidad_analitica= data.get("capacidad_analitica"),
                  trabajo_equipo= data.get("trabajo_equipo"), comunicacion= data.get("comunicacion"), pensamiento_critico= data.get("pensamiento_critico"),
                  inovacion= data.get("inovacion"), liderazgo= data.get("liderazgo"), decision_making= data.get("decision_making"),
                  problem_solving= data.get("problem_solving"), marketing= data.get("marketing"), e_commerce= data.get("e_commerce"), diseno_grafico= data.get("diseno_grafico"),
                  matematicas= data.get("matematicas"), estadistica= data.get("estadistica"), gestion_proyectos= data.get("gestion_proyectos"), redes_sociales= data.get("redes_sociales"),
                  sostenibilidad= data.get("sostenibilidad"), inteligencia_artificial= data.get("inteligencia_artificial"), big_data= data.get("big_data"), machine_learning= data.get("machine_learning"),
                  analisis_datos= data.get("analisis_datos"), bases_datos= data.get("bases_datos"), cloud = data.get("cloud"), intenet_of_things= data.get("intenet_of_things"),
                  networks= data.get("networks"), sistemas_operativos= data.get("sistemas_operativos"), web_desarrollo= data.get("web_desarrollo"),
                  web_diseno= data.get("web_diseno"), r= data.get("r"), java= data.get("java"), pascal= data.get("pascal"), python= data.get("python")
                  )
    skill.save()
    serializer = SkillsSchema()
    data = serializer.dump(skill)
    return jsonify(data), 201

@app.route('/skills/<string:username>', methods = ['PUT'])
def modificar_skills_nueva(username):
    id_user_session = get_user_tableSkill_id(username)
    skill_id = get_SkillID_by_alumno_id(id_user_session)
    skill_modificar = Skill.get_by_id(skill_id)
    data = request.get_json()
    skill_modificar.grado = data.get('grado')
    skill_modificar.nota_media = data.get('nota_media')
    skill_modificar.ingles = data.get('ingles')
    skill_modificar.aleman = data.get('aleman')
    skill_modificar.frances = data.get('frances')
    skill_modificar.capacidad_analitica = data.get('capacidad_analitica')
    skill_modificar.trabajo_equipo = data.get('trabajo_equipo')
    skill_modificar.comunicacion = data.get('comunicacion')
    skill_modificar.pensamiento_critico = data.get('pensamiento_critico')
    skill_modificar.inovacion = data.get('inovacion')
    skill_modificar.liderazgo = data.get('liderazgo')
    skill_modificar.decision_making = data.get('decision_making')
    skill_modificar.problem_solving = data.get('problem_solving')
    skill_modificar.marketing = data.get('marketing')
    skill_modificar.e_commerce = data.get('e_commerce')
    skill_modificar.diseno_grafico = data.get('diseno_grafico')
    skill_modificar.matematicas = data.get('matematicas')
    skill_modificar.estadistica = data.get('estadistica')
    skill_modificar.gestion_proyectos = data.get('gestion_proyectos')
    skill_modificar.redes_sociales = data.get('redes_sociales')
    skill_modificar.sostenibilidad = data.get('sostenibilidad')
    skill_modificar.inteligencia_artificial = data.get('inteligencia_artificial')
    skill_modificar.big_data = data.get('big_data')
    skill_modificar.machine_learning = data.get('machine_learning')
    skill_modificar.analisis_datos = data.get('analisis_datos')
    skill_modificar.bases_datos = data.get('bases_datos')
    skill_modificar.cloud = data.get('cloud')
    skill_modificar.intenet_of_things = data.get('intenet_of_things')
    skill_modificar.networks = data.get('networks')
    skill_modificar.sistemas_operativos = data.get('sistemas_operativos')
    skill_modificar.web_desarrollo = data.get('web_desarrollo')
    skill_modificar.web_diseno = data.get('web_diseno')
    skill_modificar.r = data.get('r')
    skill_modificar.java = data.get('java')
    skill_modificar.pascal = data.get('pascal')
    skill_modificar.python = data.get('python')

    db.session.commit()
    serializer = SkillsSchema()
    skill_data = serializer.dump(skill_modificar)
    return jsonify(skill_data), 200

@app.route('/skills/<string:username>', methods = ['DELETE'])
def borrar_skills(username):
    id_user_session = get_user_tableSkill_id(username)
    id_skill = get_Skill_id_by_alumno_id(id_user_session)
    skills_borrar = Skill.get_by_id(id_skill)
    skills_borrar.delete()
    return jsonify({"message": "Skills borradas correctamente"}), 204

#END-POINTS ofertas asignadas

@app.route('/ofertas_asignadas', methods = ['GET'])
def get_ofertas_asignadas():
    oferta_asignada = OfertaAsignada.get_all()
    serializer = OfertaAsignadaSchema(many=True)
    data = serializer.dump(oferta_asignada)
    return jsonify(data)

@app.route('/ofertas_asignadas', methods = ['POST'])
def crear_oferta_asignada_nueva():
    data = request.get_json()
    nuevaOfertaAsignada = OfertaAsignada(job_id=get_oferAsignada_id(),alumno_id = data.get("alumno_id"), empresa_id=get_empId_byNameEmpresa(data.get("empresa_nombre")), empresa_nombre=data.get("empresa_nombre"),
        job_tittle=data.get("job_tittle"), ciudad=data.get("ciudad"), grado=data.get("grado"), nota_media=data.get("nota_media"),
        ingles=data.get("ingles"), aleman=data.get("aleman"), frances=data.get("frances"),
        trabajo_equipo=data.get("trabajo_equipo"), comunicacion=data.get("comunicacion"), matematicas=data.get("matematicas"),
        estadistica=data.get("estadistica"), gestion_proyectos=data.get("gestion_proyectos"), sostenibilidad=data.get("sostenibilidad"),
        big_data=data.get("big_data"), programacion=data.get("programacion"))

    nuevaOfertaAsignada.save()
    serializer = OfertaAsignadaSchema()
    data = serializer.dump(nuevaOfertaAsignada)
    return jsonify(data), 201


@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('main'))

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message": "Ha habido un problema. Vuelva a intentarlo por favor"}), 500

@app.errorhandler(405)
def internal_server(error):
    return jsonify({"message": "Este método no está permitido"}), 405

if __name__ == '__main__':
    app.run()
