
from functools import wraps


def login_required(function):
    @wraps(function)
    def wrapper(user, *args, **kwargs):
        if user is None:
            print("Please login first.")
            return None

        return function(user, *args, **kwargs)

    return wrapper


def admin_required(function):
    @wraps(function)
    def wrapper(user, *args, **kwargs):
        if user is None:
            print("Please login first.")
            return None

        if user.get_role() != "admin":
            print("Admin access required.")
            return None

        return function(user, *args, **kwargs)

    return wrapper