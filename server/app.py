from flask import Flask, request, jsonify, session, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
import requests

from models import User, Loan, db

app=Flask(__name__)
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
        data=request.get_json()
        email=data['email']
        password=data['password']

        user=User.query.filter_by(email=email).first()
        if user and user.authenticate(password):
            session['user_id']=user.id
            return user.to_dict(), 200
        return {'error': "Invalid email or password"}, 401
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
            loan_type=data['loan_type'],
            application_status="PENDING",
            user_id=data['user_id']

        )
        db.session.add(new_loan)
        db.session.commit()
        '''
        Now that the new loan is created, prepare the data
        that will be sent to the scoring third party
        '''
        scoring_payload={
            "loan_id":new_loan.id,
            "amount":new_loan.amount,
            "callback_url": "https://yourapp.com/scoring/callback"

        }
        ##then send the data but in json format
        requests.post("https://creditapi.com/score", json=scoring_payload)

        #Then respond to the user
        return {
            "message": "Loan submitted successfully", 
        }, 201

        

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


from flask_restful import Resource

class ScoringCallback(Resource):
    def post(self):
        data = request.get_json()
        loan = Loan.query.get(data['loan_id'])
        if not loan:
            return {"error": "Loan not found"}, 404

        loan.score = data['score']
        loan.application_status = data['decision']  # approved / rejected
        db.session.commit()

        return {"message": "Callback processed"}, 200


api.add_resource(Welcome, '/welcome')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserResource, '/users')
api.add_resource(LoanResourceById, '/loans/<int:id>')
api.add_resource(LoanResource, '/loan')
api.add_resource(ScoringCallback, '/scoring/callback')




if __name__=='__main__':
    app.run(port=5555, debug=True)
   # kill -9 $(lsof -t -i:5555)

'''
Client → Flask:

Client sends JSON in the HTTP request.

Flask receives it as raw text.

Flask → Python:

request.get_json() converts JSON → Python dictionary.

You can now do data['amount'], data['user_id'], etc., and assign values to your Python objects (like a Loan instance).

Python object → Flask → Client:

Your Loan or User is a Python object.

.to_dict() converts it → Python dictionary.

Flask automatically converts that dict → JSON to send back to the client.
'''