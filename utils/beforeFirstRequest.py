from flask_security import SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash

from utils.db import db 
from models.user import researcher_role,doctor_role,admin_role

def before_first_request(user_datastore : SQLAlchemyUserDatastore ):
    db.create_all()
    from datetime import date
    try:
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print( 'Clear table %s' % table)
            db.session.execute(table.delete())
        db.session.commit()
        db.session.add(admin_role)
        db.session.add(doctor_role)
        db.session.add(researcher_role)      
        admin = user_datastore.create_user(email='admin@api.net', password=generate_password_hash("password", method='sha256'),confirmed_at=date.today(),active = True,roles=[admin_role])
        db.session.add(admin)
        db.session.commit()
    except:
        db.session.add(admin_role)
        db.session.add(doctor_role)
        db.session.add(researcher_role)      
        admin = user_datastore.create_user(email='admin@api.net', password=generate_password_hash("password", method='sha256'),confirmed_at=date.today(),active = True,roles=[admin_role])
        db.session.add(admin)
        db.session.commit()
    