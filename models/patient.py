from utils.db import db

class PatientModel(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    ageOnset = db.Column(db.Integer)
    ageDiag = db.Column(db.Integer) 
    symptoms = db.relationship("SymptomModel", back_populates="patients", lazy="dynamic")
