from functools import wraps


def role_required(*allowed_roles):
    def decorator(function):
        @wraps(function)
        def wrapper(current_user, *args, **kwargs):
            if current_user.role not in allowed_roles:
                raise PermissionError(
                    "You do not have permission to perform this action."
                )

            return function(current_user, *args, **kwargs)

        return wrapper

    return decorator