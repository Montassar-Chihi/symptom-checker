import uuid
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_login import login_user
import jwt
from models import User
from utils.db import db
from utils.app import app
from security.email_token import confirm_token
from datetime import datetime, timedelta

blp = Blueprint('confirm_email', __name__)

@blp.route('/confirm_email/<token>', methods=["GET"])
class ConfirmEmail(MethodView):
    
    @blp.response(201)
    def get(self,token):
        try:
            email = confirm_token(token)
        except:
            return jsonify({'message' :'The confirmation link is invalid or has expired.'}),403 
        user = User.query.filter_by(email=email).first_or_404()
        if user.active:
            return jsonify({'message' :'Account already confirmed. Please login.'}),201
        else:
            user.active = True
            user.confirmed_at = datetime.utcnow() 
            db.session.add(user)
            db.session.commit()
            json_token = jwt.encode({'email': email,
                                'exp' : datetime.utcnow() + timedelta(minutes = 300)
                    }, app.config['SECRET_KEY'], algorithm="HS256")
            login_user(user)
            return jsonify({'access-token' :json_token,'email': email})