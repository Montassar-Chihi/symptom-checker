import uuid
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort

from utils.db import db
from models import DiseaseModel
from security.authorization_token import token_required
from security.roles_accepted import roles_accepted
from resources.schemas import DiseaseSchema,DiseaseUpdateSchema

blp = Blueprint("Diseases", __name__, description="Operations on Diseases")

@blp.route("/disease/<string:disease_id>")
class Disease(MethodView):

    @blp.response(200, DiseaseSchema)
    @token_required   
    @roles_accepted(['admin', 'doctor','researcher'])
    def get(self, disease_id):
        disease = DiseaseModel.query.get_or_404(disease_id)
        return disease
    
    @token_required    
    @roles_accepted(['admin'])  
    def delete(self, disease_id):
        disease = DiseaseModel.query.get_or_404(disease_id)
        db.session.delete(disease)
        db.session.commit()
        return {"message": "Disease deleted."}


    @blp.arguments(DiseaseUpdateSchema)
    @blp.response(200, DiseaseSchema)
    @token_required  
    @roles_accepted(['admin'])
    def put(self, disease_data, disease_id):
        disease = DiseaseModel.query.get_or_404(disease_id)

        if disease:    #by this way we insure idempotency
            disease.diseaseName = disease_data["diseaseName"]
            disease.diseaseSymbol = disease_data["diseaseSymbol"]
            disease.omimId = disease_data["omimId"]
            disease.alternativeNames = disease_data["alternativeNames"]
            disease.Inheritance = disease_data["Inheritance"]
        else:
            disease = DiseaseModel(**disease_data)
            #disease = DiseaseModel(id=disease_id, **disease_data)

        db.session.add(disease)
        db.session.commit()

        return disease
    
#@blp.arguments(DiseaseSchema)
@blp.route("/disease")
class DiseaseList(MethodView):

    @blp.response(200, DiseaseSchema(many=True))
    @token_required 
    @roles_accepted(['admin', 'doctor','researcher'])
    def get(self):
        #return{"diseases":list(diseases.values())}
        return DiseaseModel.query.all()

    @blp.arguments(DiseaseSchema)
    @blp.response(201, DiseaseSchema)
    @token_required 
    @roles_accepted(['admin'])
    def post(self, disease_data):
        disease = DiseaseModel(**disease_data)  

        try:
            db.session.add(disease)
            db.session.commit()  
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the disease.")


        return disease