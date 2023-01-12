from utils.db import db

class DiseaseModel(db.Model):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True)
    omimId = db.Column(db.Integer, unique=True)
    diseaseName = db.Column(db.String(800), nullable=False)
    diseaseSymbol = db.Column(db.String(80), nullable=False)
    alternativeNames = db.Column(db.String(800), nullable=False)
    Inheritance = db.Column(db.String(80), nullable=False)
    symptoms = db.relationship("SymptomModel", back_populates="diseases", lazy="dynamic", cascade="all, delete") 

