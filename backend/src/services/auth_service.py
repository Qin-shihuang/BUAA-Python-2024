import bcrypt
import datetime
import jwt

import config
from services.database_service import DatabaseService
from utils.error_codes import RegisterStatus, LoginStatus


class AuthService:
    def __init__(self):
        self.db_service = DatabaseService('account')
        
    def __del__(self):
        self.db_service.close()

    def register(self, username, password):
        username = username.lower()
        if not username.isalnum():
            return RegisterStatus.USERNAME_INVALID
        query = f"SELECT * FROM account WHERE username = '{username}'"
        if self.db_service.query(query):
            return RegisterStatus.USERNAME_TAKEN
        # check if password is valid sha256 hash
        if len(password) != 64 or not all(c in "0123456789abcdef" for c in password):
            return RegisterStatus.PASSWORD_INVALID
        hashed_password = bcrypt.hashpw(password.encode(), config.SALT)
        query = f"INSERT INTO account (username, password) VALUES ('{username}', '{hashed_password.decode()}')"
        self.db_service.query(query)
        return RegisterStatus.REGISTER_SUCCESS

    def login(self, username, password):
        username = username.lower()
        query = f"SELECT * FROM account WHERE username = '{username}'"
        result = self.db_service.query(query)
        if not result or not bcrypt.checkpw(password.encode(), result[0][1].encode()):
            return LoginStatus.INVALID_CREDENTIALS, ''
        return LoginStatus.LOGIN_SUCCESS, create_token(result[0][0])


def create_token(username):
    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    payload = {
        "username": username,
        "exp": exp
    }
    token = jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"
    except Exception as e:
        return False, str(e)