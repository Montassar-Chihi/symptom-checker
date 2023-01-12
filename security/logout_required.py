from functools import wraps
from flask_login import current_user


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return {"message":"You are already authenticated."}
        return func(*args, **kwargs)
    return decorated_function