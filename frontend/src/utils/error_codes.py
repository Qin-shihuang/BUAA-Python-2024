from enum import Enum

class LoginStatus(Enum):

    
    LOGIN_SUCCESS = (0, "")
    # Frontend (and backend) errors
    USERNAME_EMPTY = (1, "Username cannot be empty.")
    PASSWORD_EMPTY = (2, "Password cannot be empty.")
    # Backend errors
    INVALID_CREDENTIALS = (3, "Invalid username or password.")
    UNKOWN_ERROR = (4, "An unknown error occurred.")

    @classmethod
    def from_value(cls, value):
        for status in LoginStatus:
            if status.value[0] == value:
                return status
        return LoginStatus.UNKOWN_ERROR
        
    @classmethod
    def get_error_message(cls, code):
        for error in cls:
            if error.value[0] == code.value[0]:
                return error.value[1]
        return cls.UNKOWN_ERROR.value[1]
    
class RegisterStatus(Enum):
    REGISTER_SUCCESS = (0, "")
    # Frontend errors
    USERNAME_EMPTY = (1, "Username cannot be empty.")
    USERNAME_INVALID = (2, "Username can only contain letters and numbers.")
    PASSWORD_EMPTY = (3, "Password cannot be empty.")
    PASSWORD_INVALID = (4, "Password does not satisfy requirements.")
    PASSWORDS_MISMATCH = (5, "Passwords do not match.")
    # Backend errors
    USERNAME_TAKEN = (6, "Username is already taken.")
    UNKOWN_ERROR = (7, "An unknown error occurred.")
    
    @classmethod
    def from_value(cls, value):
        for status in RegisterStatus:
            if status.value[0] == value:
                return status
        return RegisterStatus.UNKOWN_ERROR
    @classmethod
    def get_error_message(cls, code):
        for error in cls:
            if error.value[0] == code.value[0]:
                return error.value[1]
        return cls.UNKOWN_ERROR.value[1]