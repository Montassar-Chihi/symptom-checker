import uuid
from flask import  jsonify, make_response, request,redirect
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_login import login_user
import jwt
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

from models import User
from utils.app import app
from security.logout_required import logout_required

blp = Blueprint("Login", __name__)

@blp.route('/login', methods=['POST','GET'])
class Login(MethodView):
    
    @blp.response(201)
    @logout_required
    def post(self):
        try:
            data = request.get_json() 
            email = data["email"]
            password = data["password"]
        except:
            return make_response('bad request',400)
        
        user = User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message' : "wrong credentials"}),401
        
        if not user.active:
            return redirect("/unconfirmed")
        
        # if the above check passes, then we know the user has the right credentials
        token = jwt.encode({'email': email,
                            'exp' : datetime.utcnow() + timedelta(minutes = 300)
                },  app.config['SECRET_KEY'], algorithm="HS256")
        login_user(user)
        return jsonify({'access-token' : token ,'email': email})
    
    @blp.response(200)
    @logout_required
    def get(self):
        return {"instructions": "After logging in you will recieve a token that you must use when navigating in the api."}
