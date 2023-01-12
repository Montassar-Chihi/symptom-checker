import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy import create_engine

from utils.db import db
from models import PatientModel,DiseaseModel,SymptomModel
from security.authorization_token import token_required
from security.roles_accepted import roles_accepted
from resources.schemas import PatientSchema,PatientUpdateSchema,DiseaseSchema,SymptomSchema


blp = Blueprint("Patients", __name__, description="Operations on Patients")

@blp.route("/patient/<string:patient_id>")
class Patient(MethodView):

    @blp.response(200, PatientSchema)
    @token_required 
    @roles_accepted(["admin","doctor"])
    def get(self, patient_id):
        patient = PatientModel.query.get_or_404(patient_id)
        return patient
    
    @token_required 
    @roles_accepted(["admin","doctor"])
    def delete(self, patient_id):
        patient = PatientModel.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted."}


    @blp.arguments(PatientUpdateSchema)
    @blp.response(200, PatientSchema)
    @token_required 
    @roles_accepted(["admin","doctor"])
    def put(self, patient_data, patient_id):
        patient = PatientModel.query.get_or_404(patient_id)

        if patient:    #by this way we insure idempotency
            if "name" in patient_data.keys():
                patient.name = patient_data["name"]
            if "age" in patient_data.keys():
                patient.age = patient_data["age"]
            if "ageOnset" in patient_data.keys():
                patient.ageOnset = patient_data["ageOnset"]
            if "ageDiag" in patient_data.keys():
                patient.ageDiag = patient_data["ageDiag"]
            if "symptom_id" in patient_data.keys():
                patient.symptoms = [SymptomModel.query.get_or_404(id) for id in patient_data["symptom_id"]]
        else:
            patient = PatientModel(**patient_data)
            #patient = PatientModel(id=patient_id, **patient_data)

        try:
            db.session.add(patient)
            db.session.commit()  
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the patient.")

        return patient
    
#@blp.arguments(PatientSchema)
@blp.route("/patient")
class PatientList(MethodView):

    @blp.response(200, PatientSchema(many=True))
    @token_required 
    @roles_accepted(["admin","doctor"])
    def get(self):
        #return{"patients":list(patients.values())}
        return PatientModel.query.all()

    @blp.arguments(PatientSchema)
    @blp.response(201, PatientSchema)
    @token_required 
    @roles_accepted(["admin","doctor"])
    def post(self, patient_data):
        patient = PatientModel(**patient_data)  

        try:
            db.session.add(patient)
            db.session.commit()  
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the patient.")


        return patient
    
    
@blp.route("/patient/<int:patient_id>/symptoms")
class PatientDiagnosis(MethodView):

    @blp.response(200, SymptomSchema(many=True))
    @token_required 
    @roles_accepted(["admin","doctor"])
    def get(self,patient_id):
        patient = PatientModel.query.get_or_404(patient_id)
        symptoms = patient.symptoms
        return symptoms

@blp.route("/patient/<string:patient_id>/diagnosis")
class PatientDiagnosis(MethodView):

    @blp.response(200, DiseaseSchema(many=True))
    @token_required 
    @roles_accepted(["admin","doctor"])
    def get(self, patient_id):
        patient = PatientModel.query.get_or_404(patient_id)
        diseases = list(set([disease for disease in [symptom.diseases for symptom in patient.symptoms]]))
        return diseases