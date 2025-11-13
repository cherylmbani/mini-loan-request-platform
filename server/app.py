from flask import Flask, request, jsonify, session, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt

from models import User, Loan, db

app=Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///loans.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY']='super-secret'
app.json.compact=False


CORS(app)
db.init_app(app)
migrate=Migrate(app, db)
api=Api(app)
bcrypt=Bcrypt()

class Welcome(Resource):
    def get(self):
        response_body={
            "message":"Welcome to the loan application"
        }
        response=make_response(response_body, 200)
        return response
    
class SignUp(Resource):
    def post(self):
        data=request.get_json()
        new_user=User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            #phone_number=data['phone_number'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()

        session['user_id']=new_user.id
        new_user_dict=new_user.to_dict()
        response=make_response(new_user_dict, 201)
        return response
class Login(Resource):
    def post(self):
        user=User.query.filter(id=id).first()
        data=request.get_json()
        user=User(
            email=data['email'],
            password=data["password"]
        )
        if user.email=='email' and user.anthenticate():
            session['user_id']=user.id
            db.session.commit()
            return user.to_dict(), 201
        return {'error':"Email or password incorrect"}, 401

class Logout(Resource):
    def post(self):
        session.pop('user_id', None)
        response_body={
            "message":"User deleted successfully"
        }
        response=make_response(response_body, 200)
        return response

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        response = make_response(users_list, 200)
        return response

    def post(self):
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        response = make_response(new_user.to_dict(), 201)
        return response
class LoanResource(Resource):
    def post(self):
        data=request.get_json()
        new_loan=Loan(
            amount=data['amount'],
            loan_type=data['loan-type'],
            application_status=data['application_status'],
            user_id=data['2']

        )
        db.session.add(new_loan)
        db.session.commit()
        response=make_response(new_loan.to_dict(), 201)
        return response

class LoanResourceById(Resource):
    def get(self, id):
        loan=Loan.query.filter_by(id=id).first()
        if not loan:
            response_body={
                'message': 'Loan does not exist'
            }
            response=make_response(response_body, 404)
            return response
        else:
            loan_dict=loan.to_dict()
            response=make_response(loan_dict, 200)
            return response

api.add_resource(Welcome, '/welcome')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserResource, '/users')
api.add_resource(LoanResourceById, '/loans/<int:id>')




if __name__=='__main__':
    app.run(port=5555, debug=True)
   # kill -9 $(lsof -t -i:5555)

