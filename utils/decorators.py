from functools import wraps


def _get_user_from_args(args):
    """Support both instance-method style and direct-object style access."""
    for value in args:
        if hasattr(value, "current_user"):
            return value.current_user
        if hasattr(value, "role") and hasattr(value, "get_name"):
            return value
    return None


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user = _get_user_from_args(args)
        if user is None:
            print("Please login first.")
            return None
        return function(*args, **kwargs)

    return wrapper


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user = _get_user_from_args(args)
        if user is None:
            print("Please login first.")
            return None

        if user.role != "admin":
            print("Admin access required.")
            return None

        return function(*args, **kwargs)

    return wrapper


def role_required(required_role):
    """Allow access only to users with the given role."""

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = _get_user_from_args(args)
            if user is None:
                print("Please login first.")
                return None

            if user.role != required_role:
                print(f"{required_role.capitalize()} access required.")
                return None

            return function(*args, **kwargs)

        return wrapper

    return decorator