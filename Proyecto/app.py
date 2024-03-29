from functools import wraps
import sqlalchemy
from flask import jsonify

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate
import requests

from model.model import db, get_user_id, Alumno, get_user_by_id, CV, get_tableSkill_id, \
    get_user_tableSkill_id, get_all_skills_foruser, get_empresa_id, Empresa, get_emp, \
    get_users, get_alumn, get_empId_byOffer, get_empName, get_id_by_user, get_adm, \
    get_empId_byNameEmpresa, AlumnoSchema, AlumnoSchemaSinPass, EmpresaSchemaSinPass, EmpresaSchema, \
    CVSchema, get_Skill_id_by_alumno_id, get_Skills_by_alumno_id, get_SkillID_by_alumno_id, Ofertas, OfertasSchema, \
    get_ofer_id, get_ofertas_by_emp_id, get_ofertasid_by_emp_id, get_empNombre_byid, get_ofertasSinAsignar, \
    get_alum_sin_ofertas, get_oferta_by_empID_jobID, get_EmpresaID_by_job_id, comprobar_oferta_alum, get_empID_username, get_CV_ofertaAsignada, comprobar_alum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/jobs'
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
            flash('Necesitas tener un usuario de Alumno para acceder a esta página')
            return redirect(url_for('home'))
        return func()
    return wrappper_restricted_access

def restricted_access_toAlumnConOferta(func):
    @wraps(func)
    def wrappper_restricted_access():
        alum = comprobar_alum(get_id_by_user(session['username']))
        if alum:
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

@app.route('/template/resgistroUsuario', methods=["GET", "POST"])
def registro_usuario():
    if request.method == 'POST':
        user = {
                "apellido": request.form.get('apellido'),
                "email": request.form.get('email'),
                "nombre": request.form.get('nombre'),
                "password": request.form.get('pass'),
                "telefono": request.form.get('tel'),
                "username": request.form.get('username')
        }
        requests.post('http://127.0.0.1:5000/alumnos', json=user)
        flash("Usuario creado correctamente. Por favor inicie sesión con su usuario")
    return render_template('registroUsuario.html')

@app.route('/template/resgistroEmpresa', methods=["GET", "POST"])
def registro_empresa():
    if request.method == 'POST':
        empresa = {
            "username": request.form.get('username'),
            "password": request.form.get('pass'),
            "empresa_nombre":  request.form.get('nombre'),
            "telefono": request.form.get('tel'),
            "email": request.form.get('email')
        }
        requests.post('http://127.0.0.1:5000/empresas', json=empresa)
        flash("Empresa creada correctamente. Por favor inicie sesión con su usuario")
    return render_template('registroEmpresa.html')

@app.route('/template/home')
@login_required
def home():
    if session.get('logged_in'):
        return render_template('home.html', username=session['username'])

@app.route('/template/crearOfertas', methods=["GET", "POST"])
@login_required
@restricted_access_toAlumn
def crearOfertas():
    if session.get('logged_in'):
        if request.method == 'POST':
            id_emp = get_empId_byOffer(session['username'])
            oferta = {
                        "job_id": get_ofer_id(),
                        "empresa_id": id_emp,
                        "alumno_id": "null",
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
                        "programacion": request.form.get('progra_level'),
                        "estado": 'SIN ASIGNAR',
                        "telefono": request.form.get('tel'),
                        "nombre_contacto": request.form.get('nombre')
            }

            requests.post('http://localhost:5000/empresas/%s/ofertas' % id_emp, json=oferta)
            requests.post('http://127.0.0.1:8015/ofertas_nuevas')
            flash("Oferta creada correctamente.")
        return render_template('crearOfertas.html')

@app.route('/template/modificar_alumno', methods=["GET", "POST"])
@login_required
@restricted_access_toEmp
def modificar_alumnos():
    if session.get('logged_in'):
        if request.method == 'POST':
            usuario = session['username']
            id_user_session = get_user_tableSkill_id(session['username'])
            user = {
                "apellido": request.form.get('apellido'),
                "email": request.form.get('email'),
                "nombre": request.form.get('nombre'),
                "password": request.form.get('pass'),
                "telefono": request.form.get('tel'),
                "username": request.form.get('username')
            }
            requests.put('http://127.0.0.1:5000/alumnos/%s' % id_user_session, json=user)
            db.session.commit()
            flash("Alumno modificado")
        return render_template('modificarAlumno.html')

@app.route('/template/modificar_empresa', methods=["GET", "POST"])
@login_required
@restricted_access_toAlumn
def modificar_empresas():
    if session.get('logged_in'):
        if request.method == 'POST':
            usuario = session['username']
            id_user_session = get_empID_username(session['username'])
            user = {
                "email": request.form.get('email'),
                "empresa_nombre": request.form.get('empresa_nombre'),
                "telefono": request.form.get('tel')
            }
            requests.put('http://127.0.0.1:5000/empresas/%s' % id_user_session, json=user)
            db.session.commit()
            flash("Empresa modificada")
        return render_template('modificarEmpresa.html')

@app.route('/template/asignarOfertas', methods=["GET", "POST"])
@login_required
@onlyAdmin
def asignarOfertas():
    ofert_sinAsig = requests.get('http://127.0.0.1:5000/ofertas', params={'estado': 'SIN ASIGNAR'})
    ofertas_nuevas = ofert_sinAsig.json()
    alumno_sinOfer = requests.get('http://127.0.0.1:5000/alumnos', params={'oferta': 'NO'})
    alumnos_sinOfertas = alumno_sinOfer.json()
    if session.get('logged_in'):
        if request.method == 'POST':
            alumno = request.form.get('alumnos')
            oferta_id = request.form.get('ofertas')
            empresa_id = get_EmpresaID_by_job_id(oferta_id)
            alumno_id = get_id_by_user(alumno)

            mod_oferta = {
                "alumno_id": alumno_id,
                "estado": 'ASIGNADA'
            }

            requests.put('http://localhost:5000/empresas/%s/ofertas/%s' % (empresa_id, oferta_id), json=mod_oferta)
            requests.post('http://127.0.0.1:8015/ofertas_nuevas')

            db.session.commit()
            flash("Oferta asignada con éxito!")

    return render_template('asignarOfertas.html', ofertas_nuevas=ofertas_nuevas, alumnos_sinOfertas=alumnos_sinOfertas)

@app.route('/template/mostrar_CV')
@login_required
@restricted_access_toEmp
def mostrar_skills():
    if session.get('logged_in'):
        alumno_id = get_id_by_user(session['username'])
        skills = requests.get('http://127.0.0.1:5000/alumnos/%s/CV' % alumno_id)
        lista_skills = skills.json()
        return render_template('mostrar_skills.html', skill=lista_skills, username=session['username'])

@app.route('/template/ver_alumnos')
@login_required
@restricted_access_toAlumn
def ver_alumnos():
    if session.get('logged_in'):
        alumno_sinOfer = requests.get('http://127.0.0.1:5000/alumnos', params={'oferta': 'NO'})
        alumnos_sinOfertas = alumno_sinOfer.json()
        return render_template('verAlumnos.html', alumnos=alumnos_sinOfertas)

@app.route('/template/ver_ofertas')
@login_required
@restricted_access_toEmp
def ver_ofertas():
    if session.get('logged_in'):
        ofert_sinAsig = requests.get('http://127.0.0.1:5000/ofertas', params={'estado': 'SIN ASIGNAR'})
        ofertas_nuevas = ofert_sinAsig.json()
        id_usuario = get_id_by_user(username=session['username'])
        oferta_asignada = requests.get('http://127.0.0.1:5000/ofertas', params={'alumno': id_usuario}).json()
        return render_template('verOfertas.html', ofertas=ofertas_nuevas, oferta_asignada=oferta_asignada)

@app.route('/template/ver_mis_ofertas_creadas')
@login_required
@restricted_access_toAlumn
def ver_mis_ofertas_creadas():
    if session.get('logged_in'):
        id_user_session = get_empID_username(session['username'])
        emp = requests.get('http://127.0.0.1:5000/empresas/%s' % id_user_session).json()['empresa_nombre']
        ofertas_creadas = requests.get('http://127.0.0.1:5000/empresas/%s/ofertas' % id_user_session).json()
        return render_template('verMisOfertasCreadas.html', ofertas=ofertas_creadas, emp=emp)

@app.route('/template/ver_skills_alumnos')
@login_required
@restricted_access_toAlumn
def ver_skills_alumnos():
    if session.get('logged_in'):
        usuario = request.args.get('username')
        id_usuario = get_id_by_user(usuario)
        skills = requests.get('http://127.0.0.1:5000/alumnos/%s/CV' % id_usuario)
        lista_skills = skills.json()
        return render_template('mostrar_skills.html', skill=lista_skills, username=usuario)

@app.route('/template/perfil')
@login_required
def perfil():
    if session.get('logged_in'):
        emp = get_emp(username=session['username'])
        alum = get_alumn(username=session['username'])
        adm = get_adm(username=session['username'])
        return render_template('perfil.html', username=session['username'], emp=emp, alum=alum, adm=adm)

@app.route('/template/recomendarOfertas', methods=["GET","POST"])
@login_required
@restricted_access_toEmp
@restricted_access_toAlumnConOferta
def recomendarOfertas():
    if session.get('logged_in'):
        id = get_id_by_user(session['username'])
        if request.method == 'POST':
            r = requests.post('http://127.0.0.1:8015/recomendacion_alumno_nuevo', params={'id_alum': id})
            ejemplo = r.json()
            return render_template('recomendarOfertas.html', username=session['username'], ejemplo=ejemplo)
        return render_template('recomendarOfertas.html', username=session['username'])

@app.route('/template/crearCV', methods=["GET", "POST"])
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
                requests.post('http://127.0.0.1:5000/alumnos/%s/CV' % id_user_session, json=skill)
                db.session.commit()
                flash("CV creado")
            else:
                requests.put('http://127.0.0.1:5000/alumnos/%s/CV' % id_user_session, json=skill)
                db.session.commit()
                flash("CV Modificado")
        return render_template('survey.html')

@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('main'))

###################################################################################################################################################################
###########################################################################  END-POINTS ###########################################################################
###################################################################################################################################################################

###########################################################################  ALUMNOS ##############################################################################

@app.route('/alumnos', methods = ['GET'])
def get_alumnos():
    oferta = request.args.get("oferta")
    if not oferta:
        alumnos = Alumno.get_all()
        serializer = AlumnoSchemaSinPass(many=True)
        data = serializer.dump(alumnos)
        return jsonify(data)
    elif oferta == "NO":
        alumnos = get_alum_sin_ofertas()
        serializer = AlumnoSchemaSinPass(many=True)
        data = serializer.dump(alumnos)
        return jsonify(data)
    else:
        return jsonify({"mensaje": "No se encuentra el alumno que busca"})


@app.route('/alumnos/<int:alumno_id>', methods = ['GET'])
def get_alumnos_by_id(alumno_id):
    alumnos = Alumno.get_by_id(alumno_id)
    serializer = AlumnoSchemaSinPass()
    data = serializer.dump(alumnos)
    return jsonify(data)

@app.route('/alumnos/<int:alumno_id>', methods = ['PUT'])
def modificar_atr_alumno(alumno_id):
    alumno_modificar = Alumno.get_by_id(alumno_id)
    data = request.get_json()
    alumno_modificar.nombre = data.get('nombre')
    alumno_modificar.apellido = data.get('apellido')
    alumno_modificar.email = data.get('email')
    alumno_modificar.telefono = data.get('telefono')
    db.session.commit()
    serializer = AlumnoSchema()
    mod_alum = serializer.dump(alumno_modificar)
    return jsonify(mod_alum), 200

@app.route('/alumnos', methods = ['POST'])
def crear_alumno_nuevo():
    data = request.get_json()
    user = Alumno(username=data.get("username"), password=data.get("password"), nombre=data.get("nombre"),
                  apellido=data.get("apellido"), telefono=data.get("telefono"), email=data.get("email"))
    user.save()
    serializer = AlumnoSchema()
    data = serializer.dump(user)
    return jsonify(data), 201

@app.route('/alumnos/<string:alumno_id>/CV', methods = ['GET'])
def get_CV_by_alumno_id(alumno_id):
    cv_id = get_SkillID_by_alumno_id(alumno_id)
    cv = CV.get_by_id(cv_id)
    serializer = CVSchema()
    data = serializer.dump(cv)
    return jsonify(data)

@app.route('/alumnos/<string:alumno_id>/CV', methods = ['POST'])
def crear_CV_by_alumno_id(alumno_id):
    data = request.get_json()
    cv = CV(id=get_tableSkill_id(), alumno_id=alumno_id, grado=data.get("grado"),
               nota_media=data.get("nota_media"),
               ingles=data.get("ingles"), aleman=data.get("aleman"), frances=data.get("frances"),
               capacidad_analitica=data.get("capacidad_analitica"),
               trabajo_equipo=data.get("trabajo_equipo"), comunicacion=data.get("comunicacion"),
               pensamiento_critico=data.get("pensamiento_critico"),
               inovacion=data.get("inovacion"), liderazgo=data.get("liderazgo"),
               decision_making=data.get("decision_making"),
               problem_solving=data.get("problem_solving"), marketing=data.get("marketing"),
               e_commerce=data.get("e_commerce"), diseno_grafico=data.get("diseno_grafico"),
               matematicas=data.get("matematicas"), estadistica=data.get("estadistica"),
               gestion_proyectos=data.get("gestion_proyectos"), redes_sociales=data.get("redes_sociales"),
               sostenibilidad=data.get("sostenibilidad"), inteligencia_artificial=data.get("inteligencia_artificial"),
               big_data=data.get("big_data"), machine_learning=data.get("machine_learning"),
               analisis_datos=data.get("analisis_datos"), bases_datos=data.get("bases_datos"), cloud=data.get("cloud"),
               intenet_of_things=data.get("intenet_of_things"),
               networks=data.get("networks"), sistemas_operativos=data.get("sistemas_operativos"),
               web_desarrollo=data.get("web_desarrollo"),
               web_diseno=data.get("web_diseno"), r=data.get("r"), java=data.get("java"), pascal=data.get("pascal"),
               python=data.get("python")
               )
    cv.save()
    serializer = CVSchema()
    data = serializer.dump(cv)
    return jsonify(data), 201

@app.route('/alumnos/<string:alumno_id>/CV', methods = ['PUT'])
def modificar_CV_by_alumno_id(alumno_id):
    cv_id = get_SkillID_by_alumno_id(alumno_id)

    cv_modificar = CV.get_by_id(cv_id)
    data = request.get_json()
    cv_modificar.grado = data.get('grado')
    cv_modificar.nota_media = data.get('nota_media')
    cv_modificar.ingles = data.get('ingles')
    cv_modificar.aleman = data.get('aleman')
    cv_modificar.frances = data.get('frances')
    cv_modificar.capacidad_analitica = data.get('capacidad_analitica')
    cv_modificar.trabajo_equipo = data.get('trabajo_equipo')
    cv_modificar.comunicacion = data.get('comunicacion')
    cv_modificar.pensamiento_critico = data.get('pensamiento_critico')
    cv_modificar.inovacion = data.get('inovacion')
    cv_modificar.liderazgo = data.get('liderazgo')
    cv_modificar.decision_making = data.get('decision_making')
    cv_modificar.problem_solving = data.get('problem_solving')
    cv_modificar.marketing = data.get('marketing')
    cv_modificar.e_commerce = data.get('e_commerce')
    cv_modificar.diseno_grafico = data.get('diseno_grafico')
    cv_modificar.matematicas = data.get('matematicas')
    cv_modificar.estadistica = data.get('estadistica')
    cv_modificar.gestion_proyectos = data.get('gestion_proyectos')
    cv_modificar.redes_sociales = data.get('redes_sociales')
    cv_modificar.sostenibilidad = data.get('sostenibilidad')
    cv_modificar.inteligencia_artificial = data.get('inteligencia_artificial')
    cv_modificar.big_data = data.get('big_data')
    cv_modificar.machine_learning = data.get('machine_learning')
    cv_modificar.analisis_datos = data.get('analisis_datos')
    cv_modificar.bases_datos = data.get('bases_datos')
    cv_modificar.cloud = data.get('cloud')
    cv_modificar.intenet_of_things = data.get('intenet_of_things')
    cv_modificar.networks = data.get('networks')
    cv_modificar.sistemas_operativos = data.get('sistemas_operativos')
    cv_modificar.web_desarrollo = data.get('web_desarrollo')
    cv_modificar.web_diseno = data.get('web_diseno')
    cv_modificar.r = data.get('r')
    cv_modificar.java = data.get('java')
    cv_modificar.pascal = data.get('pascal')
    cv_modificar.python = data.get('python')

    db.session.commit()
    serializer = CVSchema()
    cv_data = serializer.dump(cv_modificar)
    return jsonify(cv_data), 200

###########################################################################  EMPRESAS ##############################################################################

@app.route('/empresas', methods = ['GET'])
def get_empresas():
    empresas = Empresa.get_all()
    serializer = EmpresaSchemaSinPass(many=True)
    data = serializer.dump(empresas)
    return jsonify(data)

@app.route('/empresas/<string:empresa_id>', methods = ['GET'])
def get_empresas_by_id(empresa_id):
    empresas = Empresa.get_by_id(empresa_id)
    serializer = EmpresaSchemaSinPass()
    data = serializer.dump(empresas)
    return jsonify(data)

@app.route('/empresas/<string:empresa_id>', methods = ['PUT'])
def modificar_atr_empresa(empresa_id):
    empresa_mod = Empresa.get_by_id(empresa_id)
    data = request.get_json()
    empresa_mod.empresa_nombre = data.get('empresa_nombre')
    empresa_mod.email = data.get('email')
    empresa_mod.telefono = data.get('telefono')
    db.session.commit()
    serializer = EmpresaSchema()
    mod_emp = serializer.dump(empresa_mod)
    return jsonify(mod_emp), 200

@app.route('/empresas', methods = ['POST'])
def crear_empresa_nueva():
    data = request.get_json()
    empresa = Empresa(username=data.get("username"), password=data.get("password"),
                      empresa_nombre=data.get("empresa_nombre"), telefono=data.get("telefono"), email=data.get("email"))
    empresa.save()
    serializer = EmpresaSchema()
    data = serializer.dump(empresa)
    return jsonify(data), 201

@app.route('/empresas/<string:empresa_id>/ofertas', methods = ['GET'])
def get_ofertas_by_empresaid(empresa_id):
    data = []
    serializer = OfertasSchema()
    ofertas_id = get_ofertasid_by_emp_id(empresa_id)
    for ofertas in ofertas_id:
        oferta = Ofertas.get_by_id(ofertas[0])
        oferta_json = serializer.dump(oferta)
        data.append(oferta_json)
    return jsonify(data)

@app.route('/empresas/<string:empresa_id>/ofertas', methods = ['POST'])
def crear_ofertas_by_empresaid(empresa_id):
    data = request.get_json()
    nulo = sqlalchemy.sql.null()
    nuevaOferta = Ofertas(job_id=get_ofer_id(), alumno_id=nulo, empresa_id=empresa_id,
                          empresa_nombre=get_empNombre_byid(empresa_id),
                          job_tittle=data.get("job_tittle"), ciudad=data.get("ciudad"), grado=data.get("grado"),
                          nota_media=data.get("nota_media"),
                          ingles=data.get("ingles"), aleman=data.get("aleman"), frances=data.get("frances"),
                          trabajo_equipo=data.get("trabajo_equipo"), comunicacion=data.get("comunicacion"),
                          matematicas=data.get("matematicas"),
                          estadistica=data.get("estadistica"), gestion_proyectos=data.get("gestion_proyectos"),
                          sostenibilidad=data.get("sostenibilidad"),
                          big_data=data.get("big_data"), programacion=data.get("programacion"), estado='SIN ASIGNAR',
                          telefono=data.get("telefono"), nombre_contacto=data.get("nombre_contacto"))

    nuevaOferta.save()
    serializer = OfertasSchema()
    data = serializer.dump(nuevaOferta)
    return jsonify(data), 201

@app.route('/empresas/<string:empresa_id>/ofertas/<string:job_id>', methods = ['GET'])
def get_ofertas_by_empresaid_job_id(empresa_id, job_id):
    oferta = get_oferta_by_empID_jobID(empresa_id, job_id)
    serializer = OfertasSchema()
    data = serializer.dump(oferta)
    if data == {}:
        return jsonify({"mensaje": "La oferta introducida no existe o no esta asignada a la empresa"})
    else:
        return jsonify(data)

@app.route('/empresas/<string:empresa_id>/ofertas/<string:job_id>', methods = ['PUT'])
def mod_ofertas_by_empresaid_job_id(empresa_id, job_id):
    oferta_mod = get_oferta_by_empID_jobID(empresa_id, job_id)
    data = request.get_json()
    oferta_mod.alumno_id = data.get('alumno_id')
    oferta_mod.estado = 'ASIGNADA'

    db.session.commit()
    serializer = OfertasSchema()
    oferta_data = serializer.dump(oferta_mod)
    return jsonify(oferta_data), 200

###########################################################################  OFERTAS ##############################################################################

@app.route('/ofertas', methods = ['GET'])
def ofertas_endpoint():
    estado = request.args.get("estado")
    alumno = request.args.get("alumno")
    if alumno:
        try:
            ofert = comprobar_oferta_alum(alumno)
            oferta_alum = Ofertas.get_by_id(ofert)
            serializer = OfertasSchema()
            data = serializer.dump(oferta_alum)
            return jsonify(data)
        except:
            return jsonify({"mensaje": "No se le ha asignado ninguna oferta a este usuario."})
    elif not estado:
        oferta = Ofertas.get_all()
        serializer = OfertasSchema(many=True)
        data = serializer.dump(oferta)
        return jsonify(data)
    elif estado == "SIN ASIGNAR":
        oferta = get_ofertasSinAsignar()
        serializer = OfertasSchema(many=True)
        data = serializer.dump(oferta)
        return jsonify(data)
    else:
        return jsonify({"mensaje": "No se encuentra la oferta que busca"})

@app.route('/ofertas/<string:job_id>', methods = ['GET'])
def get_ofertas_by_id(job_id):
    oferta = Ofertas.get_by_id(job_id)
    serializer = OfertasSchema()
    data = serializer.dump(oferta)
    return jsonify(data)

@app.route('/ofertas/cvs', methods = ['GET'])
def get_CV_con_oferta_asignada():
    estado = request.args.get("estado")
    if estado == "ASIGNADA":
        cvs = get_CV_ofertaAsignada()
        serializer = CVSchema(many=True)
        data = serializer.dump(cvs)
        return jsonify(data)
    else:
        return jsonify({"mensaje": "No se encuentra el CV que busca"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"mensaje": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"mensaje": "Ha habido un problema. Vuelva a intentarlo por favor"}), 500

@app.errorhandler(405)
def internal_server(error):
    return jsonify({"mensaje": "Este método no está permitido"}), 405

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)

