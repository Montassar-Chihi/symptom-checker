import uuid
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError

from utils.db import db
from security.authorization_token import token_required
from security.roles_accepted import roles_accepted
from models import user as UserModel 
from models.user import admin_role, doctor_role , researcher_role
from resources.schemas import UserSchema,UserUpdateSchema


blp = Blueprint("Users", __name__, description="Operations on Users")

@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    @token_required 
    @roles_accepted(["admin"])  
    def get(self, user_id):
        user = UserModel.User.query.filter_by(id=user_id).first()
        return user
      
    @token_required   
    @roles_accepted(["admin"])  
    def delete(self, user_id):
        user = UserModel.User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}


    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    @token_required   
    @roles_accepted(["admin"])  
    def put(self, user_data, user_id):
        user = UserModel.User.query.get_or_404(user_id)

        if user:    #by this way we insure idempotency
            user.name = user_data["name"]
            user.email = user_data["email"]
            try:
                if user_data["userRole"] == "doctor" :
                    user.userRole = doctor_role
                elif user_data["userRole"] == "researcher" :
                    user.userRole = researcher_role
                elif user_data["userRole"] == "admin" : 
                    user.userRole = admin_role
                else:
                    return jsonify({"Message":"Bad request"}),401
            except : 
                return jsonify({"Message":"Bad request"}),401
        else:
            user = User(**user_data)
            #user = User(id=user_id, **user_data)

        db.session.add(user)
        db.session.commit()

        return user
    
#@blp.arguments(UserSchema)
@blp.route("/user")
class UserList(MethodView):

    @blp.response(200, UserSchema(many=True))
    @token_required   
    @roles_accepted(["admin"])  
    def get(self):
        #return{"users":list(users.values())}
        return UserModel.User.query.all()
    
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    @token_required   
    @roles_accepted(["admin"])  
    def get(self,user_data):
        user = UserModel()
        user.name = user_data["name"]
        user.email = user_data["email"]
        try:
            if user_data["userRole"] == "doctor" :
                user.userRole = doctor_role
            elif user_data["userRole"] == "researcher" :
                user.userRole = researcher_role
            elif user_data["userRole"] == "admin" : 
                user.userRole = admin_role
            else:
                return jsonify({"Message":"Bad request"}),401
        except : 
            return jsonify({"Message":"Bad request"}),401
        try:
            db.session.add(user)
            db.session.commit()  
        except SQLAlchemyError as error:
            print(error)
            abort(500, message="An error occurred while inserting the user.")

        return user