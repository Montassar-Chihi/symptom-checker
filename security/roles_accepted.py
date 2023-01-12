from functools import wraps
from flask import jsonify

from utils.load_user import get_current_user


# Authentication decorator
def roles_accepted(roles: list=["admin"]):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            for user_role in get_current_user().roles:
                if user_role.name not in roles:
                    return jsonify({"message": "Unauthorized"}), 403
            return f(*args, **kwargs)
        return decorator
    return wrapper
