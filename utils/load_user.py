from flask_login import current_user

from models import User

def get_current_user() -> User:
    user = User.query.filter_by(id=current_user.id).first()
    return user
