from functools import wraps
from flask import request,jsonify,make_response
import jwt

from utils.app import app
from models.user import User


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'SECURITY_TOKEN_AUTHENTICATION_HEADER' in request.headers:
            token = request.headers['SECURITY_TOKEN_AUTHENTICATION_HEADER']
            
        if request.args.get('SECURITY_TOKEN_AUTHENTICATION_KEY') != None:
            token = request.args.get('SECURITY_TOKEN_AUTHENTICATION_KEY')          
            
        if not token: # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.filter_by(email=data['email']).first()
            if user == None:
                return make_response(jsonify({"message": "Invalid token!"}), 401)
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)
         # Return the user information attached to the token 
        return f(*args, **kwargs)
    return decorator
