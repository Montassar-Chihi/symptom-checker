from marshmallow import Schema, fields

class PlainSymptomSchema(Schema):
    id = fields.Int(dump_only=True)
    Description = fields.Str()
    hpoTerm = fields.Str()
    Frequency = fields.Str()

class PlainDiseaseSchema(Schema):
    id = fields.Int(dump_only=True)
    omimId = fields.Int()
    diseaseName = fields.Str()
    diseaseSymbol = fields.Str()
    alternativeNames = fields.Str()
    Inheritance = fields.Str()

class DiseaseUpdateSchema(Schema):
    id = fields.Int()
    omimId = fields.Int()
    diseaseName = fields.Str()
    diseaseSymbol = fields.Str()
    alternativeNames = fields.Str()
    Inheritance = fields.Str()
    
class DiseaseSchema(PlainSymptomSchema):
    id = fields.Int(dump_only=True)
    omimId = fields.Int()
    diseaseName = fields.Str()
    diseaseSymbol = fields.Str()
    alternativeNames = fields.Str()
    Inheritance = fields.Str()
    symptoms = fields.List(fields.Nested(PlainSymptomSchema()), dump_only=True)
    #And this here will only be used when returning data to the client and 
    #not when receiving data from them
   
   
    
class PlainPatientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    age = fields.Int()
    ageOnset = fields.Int()
    ageDiag = fields.Int()

class PatientUpdateSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    age = fields.Int()
    ageOnset = fields.Int()
    ageDiag = fields.Int()
    symptom_id = fields.List(fields.Int())
    
class PatientSchema(PlainSymptomSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    age = fields.Int()
    ageOnset = fields.Int()
    ageDiag = fields.Int()
    symptoms = fields.List(fields.Nested(PlainSymptomSchema()), dump_only=True)
 

class SymptomUpdateSchema(Schema):
    id = fields.Int()
    Description = fields.Str()
    hpoTerm = fields.Str()
    Frequency = fields.Str()
    disease_id = fields.Int()
    patient_id = fields.Int()
    
class SymptomSchema(PlainDiseaseSchema,PlainPatientSchema):
    id = fields.Int(dump_only=True)
    Description = fields.Str()
    hpoTerm = fields.Str()
    Frequency = fields.Str()
    disease_id = fields.Int(load_only=True)
    diseases = fields.Nested(PlainDiseaseSchema(), dump_only=True)
    patient_id = fields.Int(load_only=True)
    patients = fields.Nested(PlainPatientSchema(), dump_only=True)

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    
class UserUpdateSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    userRole = fields.Str()



class UserSchema(PlainUserSchema):
    userRole = fields.Str(required=True)
