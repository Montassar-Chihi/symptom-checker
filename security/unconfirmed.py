import uuid
from flask import jsonify,redirect
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_login import current_user

blp = Blueprint('unconfirmed', __name__)

@blp.route('/unconfirmed', methods=["GET"])
class Unconfirmed(MethodView):
    
    @blp.response(403)
    def get(self):
        try:
            if current_user.confirmed:
                return redirect('/')
        except:
            return jsonify({'message' :'Please confirm your account!'}),403