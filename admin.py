from flask import abort
from flask_login import current_user
from functools import wraps


# Wrapper if id is not 1 then return abort with 403 error
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function
