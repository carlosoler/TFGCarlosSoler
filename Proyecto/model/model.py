from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_user(username):
    return db.session.query(Alumno).filter_by(username=username).first()


def get_user_id():
    return db.session.query(Alumno.alumno_id).order_by(Alumno.alumno_id.desc()).first().alumno_id + 1


def get_user_by_id(alumno_id):
    return db.session.query(Alumno).filter_by(id=alumno_id).first()


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

    def __init__(self, alumno_id, username, password, nombre, apellido, telefono, email):
        self.alumno_id = alumno_id
        self.username = username
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.alumno_id)
