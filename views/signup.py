import uuid
from flask import jsonify, request,make_response
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_mail import Message
from werkzeug.security import generate_password_hash

from models.user import User,researcher_role,doctor_role
from utils.db import db
from security.logout_required import logout_required
from security.email_token import generate_confirmation_token
from utils.mail import mail

blp = Blueprint('Signup', __name__)

@blp.route('/signup', methods=['POST','GET'])
class SignUp(MethodView):
    
    @blp.response(302)
    @logout_required
    def post(self):
        # code to validate and add user to database goes here
        try:
            data = request.get_json() 
            email = data["email"]
            name = data["name"]
            password = data["password"]
            confirmed = False
            role = data["role"]
        except:
            return make_response('bad request',400)
        
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            return jsonify({'message' : "email already exists"}),409
    
        # create a new user with the json data. Hash the password so the plaintext version isn't saved.
        if role == "doctor":
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),
                        active = confirmed,roles=[doctor_role])
        elif role == "researcher":
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),
                        active = confirmed,roles=[researcher_role])
        else :
            return jsonify({"message":"bad request : please choose a role from ['doctor','researcher'] !"}),400
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        email_token = generate_confirmation_token(new_user.email)
        msg = Message("Email confirmation", sender = "tbs.montassar.chihi@gmail.com", recipients = [email])
        msg.body = 'Click on this link to confirm your account : 127.0.0.1:5000/confirm_email/{}'.format(email_token)
        mail.send(msg)
        return jsonify({'Message' :"check your mail to get confirmation link","link":'127.0.0.1:5000/confirm_email/{}'.format(email_token)})
    
    @blp.response(200)
    @logout_required
    def get(self):
        return {"instructions": "Signing up requires confirming your email. You need to choose a role between doctor and researcher. Doctor profile has access to patient and symptomps end points where researcher has access to just the diseases. Add filed 'role' : 'doctor' or 'role' : 'researcher' "}
