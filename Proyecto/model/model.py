import jsonify as jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()


def get_users(username):
    return db.session.query(Alumno).filter_by(username=username).first() or db.session.query(Empresa).filter_by(username=username).first() or db.session.query(Admin).filter_by(username=username).first()

def get_alumn(username):
    return db.session.query(Alumno).filter_by(username=username).first()

def get_emp(username):
    return db.session.query(Empresa).filter_by(username=username).first()

def get_adm(username):
    return db.session.query(Admin).filter_by(username=username).first()

def get_user_id():
    return db.session.query(Alumno.alumno_id).order_by(Alumno.alumno_id.desc()).first().alumno_id + 1

def get_empresa_id():
    return db.session.query(Empresa.empresa_id).order_by(Empresa.empresa_id.desc()).first().empresa_id + 1

def get_user_by_id(alumno_id):
    return db.session.query(Alumno).filter_by(alumno_id=alumno_id).first()

def get_id_by_user(username):
    return db.session.query(Alumno.alumno_id).filter_by(username=username).order_by(Alumno.alumno_id.desc()).first().alumno_id

def get_tableSkill_id():
    return db.session.query(Skill.id).order_by(Skill.id.desc()).first().id + 1

def get_user_tableSkill_id(username):
    return db.session.query(Alumno.alumno_id).order_by(Alumno.alumno_id.desc()).filter_by(username=username).first().alumno_id

def get_Skill_id_by_alumno_id(alumno_id):
    return db.session.query(Skill.id).order_by(Skill.id.desc()).filter_by(alumno_id=alumno_id).first().id

def get_all_skills_foruser(id):
    return db.session.query(Skill).order_by(Skill.id.desc()).filter_by(alumno_id=id)

def get_skills_foruser(alumno_id):
    return Skill.query.get(alumno_id)

def update_skills(alumno_id):
    return Skill.query.filter_by(alumno_id = alumno_id).first()

def update_alumno(alumno_id):
    return Alumno.query.filter_by(alumno_id = alumno_id).first()

def update_ofertaNueva(job_id):
    return OfertaNueva.query.filter_by(job_id = job_id).first()

def update_ofertaAsignada(job_id):
    return OfertaAsignada.query.filter_by(job_id = job_id).first()

def get_ofer_id():
    return db.session.query(OfertaNueva.job_id).order_by(OfertaNueva.job_id.desc()).first().job_id + 1

def get_empId_byOffer(username):
    return db.session.query(Empresa.empresa_id).order_by(Empresa.empresa_id.desc()).filter_by(username=username).first().empresa_id

def get_empId_byNameEmpresa(empresa_nombre):
    return db.session.query(Empresa.empresa_id).order_by(Empresa.empresa_id.desc()).filter_by(empresa_nombre=empresa_nombre).first().empresa_id

def get_empName(username):
    return db.session.query(Empresa.empresa_nombre).order_by(Empresa.empresa_id.desc()).filter_by(username=username).first().empresa_nombre

def get_alumnos():
    return db.session.query(Alumno).order_by(Alumno.alumno_id.desc())

def get_ofertas():
    return db.session.query(OfertaAsignada).order_by(OfertaAsignada.job_id.desc())

def get_ofertas_nuevas():
    return db.session.query(OfertaNueva).order_by(OfertaNueva.job_id.desc())

def get_alumn_sinOfertas():
    return db.session.query(Alumno).order_by(Alumno.alumno_id.desc()).filter_by(ofert_asignada=0)

def get_alumn_sinOfertasByUsername(username):
    return db.session.query(Alumno).order_by(Alumno.alumno_id.desc()).filter_by(ofert_asignada=0, username=username).first()

def get_eliminarOfertaNueva(job_id):
    return db.session.query(OfertaNueva).filter_by(job_id=job_id).delete()

def add_to_db(e):
    db.session.add(e)
    db.session.commit()


class Alumno(db.Model):
    __tablename__ = 'alumnos'
    alumno_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)
    telefono = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    ofert_asignada = db.Column(db.Integer)

    def __init__(self, alumno_id, username, password, nombre, apellido, telefono, email, ofert_asignada):
        self.alumno_id = alumno_id
        self.username = username
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.ofert_asignada = ofert_asignada

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.alumno_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, alumno_id):
        return cls.query.get_or_404(alumno_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class AlumnoSchema(Schema):
    alumno_id = fields.Integer()
    username = fields.String()
    password = fields.String()
    nombre = fields.String()
    apellido = fields.String()
    telefono = fields.String()
    email = fields.String()
    ofert_asignada = fields.Integer()

class AlumnoSchemaSinPass(Schema):
    alumno_id = fields.Integer()
    username = fields.String()
    nombre = fields.String()
    apellido = fields.String()
    telefono = fields.String()
    email = fields.String()
    ofert_asignada = fields.Integer()


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.alumno_id'), unique=True)
    grado = db.Column(db.Integer)
    nota_media = db.Column(db.Integer)
    ingles = db.Column(db.Integer)
    aleman = db.Column(db.Integer)
    frances = db.Column(db.Integer)
    capacidad_analitica = db.Column(db.Integer)
    trabajo_equipo = db.Column(db.Integer)
    comunicacion = db.Column(db.Integer)
    pensamiento_critico = db.Column(db.Integer)
    inovacion = db.Column(db.Integer)
    liderazgo = db.Column(db.Integer)
    decision_making = db.Column(db.Integer)
    problem_solving = db.Column(db.Integer)
    marketing = db.Column(db.Integer)
    e_commerce = db.Column(db.Integer)
    diseno_grafico = db.Column(db.Integer)
    matematicas = db.Column(db.Integer)
    estadistica = db.Column(db.Integer)
    gestion_proyectos = db.Column(db.Integer)
    redes_sociales = db.Column(db.Integer)
    sostenibilidad = db.Column(db.Integer)
    inteligencia_artificial = db.Column(db.Integer)
    big_data = db.Column(db.Integer)
    machine_learning = db.Column(db.Integer)
    analisis_datos = db.Column(db.Integer)
    bases_datos = db.Column(db.Integer)
    cloud = db.Column(db.Integer)
    intenet_of_things =db.Column(db.Integer)
    networks = db.Column(db.Integer)
    sistemas_operativos = db.Column(db.Integer)
    web_desarrollo = db.Column(db.Integer)
    web_diseno = db.Column(db.Integer)
    r = db.Column(db.Integer)
    java = db.Column(db.Integer)
    pascal = db.Column(db.Integer)
    python = db.Column(db.Integer)

    def __init__(self, id, alumno_id, grado, nota_media, ingles, aleman, frances, capacidad_analitica, trabajo_equipo,
                 comunicacion, pensamiento_critico, inovacion, liderazgo, decision_making, problem_solving, marketing,
                 e_commerce, diseno_grafico, matematicas, estadistica, gestion_proyectos, redes_sociales, sostenibilidad,
                 inteligencia_artificial, big_data, machine_learning, analisis_datos, bases_datos, cloud,
                 intenet_of_things, networks, sistemas_operativos, web_desarrollo, web_diseno, r, java, pascal, python):

        self.id = id
        self.alumno_id = alumno_id
        self.grado = grado
        self.nota_media = nota_media
        self.ingles = ingles
        self.aleman = aleman
        self.frances = frances
        self.capacidad_analitica = capacidad_analitica
        self.trabajo_equipo = trabajo_equipo
        self.comunicacion = comunicacion
        self.pensamiento_critico = pensamiento_critico
        self.inovacion = inovacion
        self.liderazgo = liderazgo
        self.decision_making = decision_making
        self.problem_solving = problem_solving
        self.marketing = marketing
        self.e_commerce = e_commerce
        self.diseno_grafico = diseno_grafico
        self.matematicas = matematicas
        self.estadistica = estadistica
        self.gestion_proyectos = gestion_proyectos
        self.redes_sociales = redes_sociales
        self.sostenibilidad = sostenibilidad
        self.inteligencia_artificial = inteligencia_artificial
        self.big_data = big_data
        self.machine_learning = machine_learning
        self.analisis_datos = analisis_datos
        self.bases_datos = bases_datos
        self.cloud = cloud
        self.intenet_of_things = intenet_of_things
        self.networks = networks
        self.sistemas_operativos = sistemas_operativos
        self.web_desarrollo = web_desarrollo
        self.web_diseno = web_diseno
        self.r = r
        self.java = java
        self.pascal = pascal
        self.python = python

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_alumnoID(cls, alumno_id):
        return cls.query.get_or_404

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class SkillsSchema(Schema):
    id = fields.Integer()
    alumno_id = fields.Integer()
    grado = fields.Integer()
    nota_media = fields.Integer()
    ingles = fields.Integer()
    aleman = fields.Integer()
    frances = fields.Integer()
    capacidad_analitica = fields.Integer()
    trabajo_equipo = fields.Integer()
    comunicacion = fields.Integer()
    pensamiento_critico = fields.Integer()
    inovacion = fields.Integer()
    liderazgo = fields.Integer()
    decision_making = fields.Integer()
    problem_solving = fields.Integer()
    marketing = fields.Integer()
    e_commerce = fields.Integer()
    diseno_grafico = fields.Integer()
    matematicas = fields.Integer()
    estadistica = fields.Integer()
    gestion_proyectos = fields.Integer()
    redes_sociales = fields.Integer()
    sostenibilidad = fields.Integer()
    inteligencia_artificial = fields.Integer()
    big_data = fields.Integer()
    machine_learning = fields.Integer()
    analisis_datos = fields.Integer()
    bases_datos = fields.Integer()
    cloud = fields.Integer()
    intenet_of_things = fields.Integer()
    networks = fields.Integer()
    sistemas_operativos =fields.Integer()
    web_desarrollo = fields.Integer()
    web_diseno = fields.Integer()
    r = fields.Integer()
    java = fields.Integer()
    pascal = fields.Integer()
    python = fields.Integer()


class Empresa(db.Model):
    __tablename__ = 'empresas'
    empresa_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    empresa_nombre = db.Column(db.String)
    telefono = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def __init__(self, empresa_id, username, password, empresa_nombre, telefono, email):
        self.empresa_id = empresa_id
        self.username = username
        self.password = password
        self.empresa_nombre = empresa_nombre
        self.telefono = telefono
        self.email = email

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.empresa_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, job_id):
        return cls.query.get_or_404(job_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class EmpresaSchema(Schema):
    empresa_id = fields.Integer()
    username = fields.String()
    password = fields.String()
    empresa_nombre = fields.String()
    telefono = fields.String()
    email = fields.String()

class EmpresaSchemaSinPass(Schema):
    empresa_id = fields.Integer()
    username = fields.String()
    empresa_nombre = fields.String()
    telefono = fields.String()
    email = fields.String()


class OfertaAsignada(db.Model):
    __tablename__ = 'ofertas_asignadas'
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.alumno_id'), unique=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.empresa_id'))
    empresa_nombre = db.Column(db.String)
    job_tittle = db.Column(db.String)
    ciudad = db.Column(db.String)
    grado = db.Column(db.Integer)
    nota_media = db.Column(db.Integer)
    ingles = db.Column(db.Integer)
    aleman = db.Column(db.Integer)
    frances = db.Column(db.Integer)
    trabajo_equipo = db.Column(db.Integer)
    comunicacion = db.Column(db.Integer)
    matematicas = db.Column(db.Integer)
    estadistica = db.Column(db.Integer)
    gestion_proyectos = db.Column(db.Integer)
    sostenibilidad = db.Column(db.Integer)
    big_data = db.Column(db.Integer)
    programacion = db.Column(db.Integer)

    def __init__(self, job_id, alumno_id, empresa_id, empresa_nombre, job_tittle, ciudad, grado, nota_media, ingles, aleman, frances, trabajo_equipo, comunicacion, matematicas, estadistica, gestion_proyectos, sostenibilidad, big_data, programacion):
        self.job_id = job_id
        self.alumno_id = alumno_id
        self.empresa_id = empresa_id
        self.empresa_nombre = empresa_nombre
        self.job_tittle = job_tittle
        self.ciudad = ciudad
        self.grado = grado
        self.nota_media = nota_media
        self.ingles = ingles
        self.aleman = aleman
        self.frances = frances
        self.trabajo_equipo = trabajo_equipo
        self.comunicacion = comunicacion
        self.matematicas = matematicas
        self.estadistica = estadistica
        self.gestion_proyectos = gestion_proyectos
        self.sostenibilidad = sostenibilidad
        self.big_data = big_data
        self.programacion = programacion

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.job_id)

class OfertaNueva(db.Model):
    __tablename__ = 'ofertas_nuevas'
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.empresa_id'))
    empresa_nombre = db.Column(db.String)
    job_tittle = db.Column(db.String)
    ciudad = db.Column(db.String)
    grado = db.Column(db.Integer)
    nota_media = db.Column(db.Integer)
    ingles = db.Column(db.Integer)
    aleman = db.Column(db.Integer)
    frances = db.Column(db.Integer)
    trabajo_equipo = db.Column(db.Integer)
    comunicacion = db.Column(db.Integer)
    matematicas = db.Column(db.Integer)
    estadistica = db.Column(db.Integer)
    gestion_proyectos = db.Column(db.Integer)
    sostenibilidad = db.Column(db.Integer)
    big_data = db.Column(db.Integer)
    programacion = db.Column(db.Integer)

    def __init__(self, job_id, empresa_id, empresa_nombre, job_tittle, ciudad, grado, nota_media, ingles, aleman, frances, trabajo_equipo, comunicacion, matematicas, estadistica, gestion_proyectos, sostenibilidad, big_data, programacion):
        self.job_id = job_id
        self.empresa_id = empresa_id
        self.empresa_nombre = empresa_nombre
        self.job_tittle = job_tittle
        self.ciudad = ciudad
        self.grado = grado
        self.nota_media = nota_media
        self.ingles = ingles
        self.aleman = aleman
        self.frances = frances
        self.trabajo_equipo = trabajo_equipo
        self.comunicacion = comunicacion
        self.matematicas = matematicas
        self.estadistica = estadistica
        self.gestion_proyectos = gestion_proyectos
        self.sostenibilidad = sostenibilidad
        self.big_data = big_data
        self.programacion = programacion

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, job_id):
        return cls.query.get_or_404(job_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class OfertaNuevaSchema(Schema):
    job_id = fields.Integer()
    empresa_id = fields.Integer()
    empresa_nombre = fields.String()
    job_tittle = fields.String()
    ciudad = fields.String()
    grado = fields.Integer()
    nota_media = fields.Integer()
    ingles = fields.Integer()
    aleman = fields.Integer()
    frances = fields.Integer()
    trabajo_equipo = fields.Integer()
    comunicacion = fields.Integer()
    matematicas = fields.Integer()
    estadistica = fields.Integer()
    gestion_proyectos = fields.Integer()
    sostenibilidad = fields.Integer()
    big_data = fields.Integer()
    programacion = fields.Integer()

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, admin_id, username, password):
        self.admin_id = admin_id
        self.username = username
        self.password = password

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.admin_id)

