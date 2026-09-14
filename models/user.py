import hashlib


class Patient:
    def __init__(self, name, email, password_hash, role="patient"):
        self.name = name
        self.email = email
        self.__password_hash = password_hash
        self.role = role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.__password_hash == self.hash_password(password)

    @property
    def password_hash(self):
        return self.__password_hash

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self.__password_hash,
            "role": self.role,
        }


class Doctor(Patient):
    def __init__(self, name, email, password_hash):
        super().__init__(name, email, password_hash, role="doctor")


class Admin(Patient):
    def __init__(self, name, email, password_hash):
        super().__init__(name, email, password_hash, role="admin")
