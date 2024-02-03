from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)



class Grade(db.Model):

    __tablename__ = 'grades'

    grade = db.Column(db.String,
                     primary_key=True)
    density = db.Column(db.Integer,
                        nullable=False)
    
    def serialize(self):
        return {
            'grade' : self.grade,
            'density' : self.density
        }
        
class Downriver_Storage(db.Model):
    
    __tablename__ = "downriver_storage"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)

    bin_name = db.Column(db.String)

    date = db.Column(db.DateTime)

    grade = db.Column(db.String, db.ForeignKey('grades.grade'))
    grade_obj = db.relationship('Grade', backref='downriver_storage')

    crates = db.Column(db.Integer,
                       default=0)

    quantity = db.Column(db.Integer,
                         default=0)
    
    def serialize(self):
        return {
            'bin_name' : self.bin_name,
            'date' : self.date,
            'grade' : self.grade,
            'crates' : self.crates,
            'quantity' : self.quantity
        }
    
class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    
    username = db.Column(db.String,
                        unique=True,
                         nullable=False)
    
    password = db.Column(db.String,
                         nullable=False,
                         )
    
    admin = db.Column(db.Boolean, 
                      default=False)
    
    @classmethod
    def createUser(cls, username, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)

        return user
    
    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    

    
