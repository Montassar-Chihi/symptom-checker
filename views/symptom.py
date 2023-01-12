import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from utils.db import db
from models import SymptomModel,DiseaseModel
from security.authorization_token import token_required
from security.roles_accepted import roles_accepted
from resources.schemas import SymptomSchema,SymptomUpdateSchema


blp = Blueprint("Symptoms", __name__, description="Operations on Symptoms")

@blp.route("/symptoms/<int:symptom_id>")
class Symptom(MethodView):

    @blp.response(200, SymptomSchema)
    @token_required 
    @roles_accepted(["admin","doctor"])
    def get(self, symptom_id):
        symptom = SymptomModel.query.get_or_404(symptom_id)
        return symptom
    
    @token_required    
    @roles_accepted(["admin"])
    def delete(self, symptom_id):
        symptom = SymptomModel.query.get_or_404(symptom_id)
        db.session.delete(symptom)
        db.session.commit()
        return {"message": "Symptom deleted."}


    @blp.arguments(SymptomUpdateSchema)
    @blp.response(200, SymptomSchema)
    @token_required 
    @roles_accepted(["admin"])
    def put(self, symptom_data, symptom_id):
        symptom = SymptomModel.query.get_or_404(symptom_id)

        if symptom:    #by this way we insure idempotency
            symptom.Description = symptom_data["Description"]
            symptom.hpoTerm = symptom_data["hpoTerm"]
            symptom.Frequency = symptom_data["Frequency"]
            if "disease_id" in symptom_data.keys():
                symptom.disease_id = symptom_data["disease_id"]
                symptom.diseases = DiseaseModel.query.get_or_404(symptom_data["disease_id"])
        else:
            symptom = SymptomModel(**symptom_data)
            #symptom = SymptomModel(id=symptom_id, **symptom_data)

        db.session.add(symptom)
        db.session.commit()

        return symptom
    
#@blp.arguments(SymptomSchema)
@blp.route("/symptoms")
class SymptomList(MethodView):

    @blp.response(200, SymptomSchema(many=True))
    @token_required 
    @roles_accepted(["admin","doctor"])
    def get(self):
        #return{"symptoms":list(symptoms.values())}
        return SymptomModel.query.all()

    @blp.arguments(SymptomSchema)
    @blp.response(201, SymptomSchema)
    @token_required 
    @roles_accepted(["admin","doctor"])
    def post(self, symptom_data ):
        symptom = SymptomModel()  
        
        symptom.Description = symptom_data["Description"]
        symptom.hpoTerm = symptom_data["hpoTerm"]
        symptom.Frequency = symptom_data["Frequency"]
        if "disease_id" in symptom_data.keys():
            symptom.disease_id = symptom_data["disease_id"]
            symptom.diseases = DiseaseModel.query.get_or_404(symptom_data["disease_id"])
        
        try:
            db.session.add(symptom)
            db.session.commit()  
        except SQLAlchemyError as error:
            print(error)
            abort(500, message="An error occurred while inserting the symptom.")

        return symptom