def not_empty(value):
    return bool(value.strip())


def valid_username(username):
    return len(username.strip()) >= 3


def valid_password(password):
    return len(password) >= 4


def valid_speciality(speciality, specialities):
    return speciality in specialities