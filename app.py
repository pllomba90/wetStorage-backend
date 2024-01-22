from datetime import datetime, timedelta
import jwt
from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from sqlalchemy import func

app = Flask(__name__)
CORS(app)

from models import db, connect_db, Grade, Downriver_Storage, User


app.config['SECRET_KEY'] = 'secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wet_storage'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_ENABLED'] = True

debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    # db.drop_all()
    db.create_all()


@app.route('/create_user', methods=["POST"])
def create_user(userInfo):
    new_user = User.createUser(
        username=userInfo.username,
        password=userInfo.password)
    db.session.commit()
    if new_user:
        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {
            'sub': new_user.id,
            'username': new_user.username,
            'exp': expiration
        }
        
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Authentication failed'}), 401
    

@app.route('/login', methods=["POST"])
def login(userInfo):
    user = User.authenticate(
        username=userInfo.username,
        password=userInfo.password
    )
    if user:
        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {
            'sub': user.id,
            'username': user.username,
            'exp': expiration
        }
        
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Authentication failed'}), 401
    
@app.route('/grades', methods=["GET", "POST"])
def getGrades():
    if request.method == "GET" : 
        response = [grade.serialize() for grade in Grade.query.all()]
        return jsonify(response)
    
    elif request.method == "POST":
        newGrade = Grade(grade=request.json["grade"], density=request.json["density"])
        db.session.add(newGrade)
        db.session.commit()
        return jsonify(grade=newGrade.serialize())

@app.route('/downriver_strg', methods=['GET'])
def wet_storage():
    print("Route executed")
    if request.method == 'GET':

        response = [bin.serialize() for bin in Downriver_Storage.query.order_by(Downriver_Storage.id).all()]
        print(jsonify(response))
        return jsonify(response)
    
@app.route('/downriver_strg/<string:bin_name>', methods=["GET", "PATCH"])
def insertProduct(bin_name):

    bin = Downriver_Storage.query.filter_by(bin_name=bin_name).first()

    if not bin:
        return jsonify({'error': 'Bin not found'}), 404
    
    if request.method == "GET":
        return jsonify(bin=bin.serialize())
    
    elif request.method == "PATCH":
        bin.crates = request.json.get('crates', bin.crates)
        bin.date = request.json.get('date', bin.date)
        bin.grade = request.json.get('grade', bin.grade)
        bin.quantity = request.json.get('quantity', bin.quantity)
        db.session.commit()
        return jsonify(bin=bin.serialize())
    

if __name__ == '__main__':
    app.run(debug=True)