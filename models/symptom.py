from utils.db import db

class SymptomModel(db.Model):
    __tablename__ = "symptoms"

    id = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(80), nullable=False)
    hpoTerm = db.Column(db.String(80), nullable=False)
    Frequency = db.Column(db.String(80), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey("diseases.id"), unique=False, nullable=True)
    diseases = db.relationship("DiseaseModel", back_populates="symptoms")
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), unique=False, nullable=True)
    patients = db.relationship("PatientModel", back_populates="symptoms")



