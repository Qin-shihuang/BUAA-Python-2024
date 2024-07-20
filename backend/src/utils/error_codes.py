from enum import Enum
class ErrorCode(Enum):
    # General errors
    SUCCESS = 0
    UNKNOWN_ERROR = 2
    NETWORK_ERROR = 3
    UNAUTHORIZED = 4
    BAD_REQUEST = 5
        
    # Auth errors
    USERNAME_EMPTY = 1001
    USERNAME_INVALID = 1002
    USERNAME_TOO_LONG = 1003
    PASSWORD_EMPTY = 1004
    PASSWORD_INVALID = 1005
    PASSWORDS_MISMATCH = 1006
    USERNAME_TAKEN = 1007
    INVALID_CREDENTIALS = 1008
    
    # File errors
    FILENAME_EMPTY = 2001
    FILENAME_INVALID = 2002
    FILENAME_TOO_LONG = 2003
    FILE_TOO_LARGE = 2004
    FILE_NOT_FOUND = 2005
    
    # Task errors
    TASK_NOT_FOUND = 3001
    
    # Report errors
    REPORT_NOT_FOUND = 4001
    
    @classmethod
    def from_value(cls, value):
        for code in ErrorCode:
            if code.value == value:
                return code
        return ErrorCode.UNKNOWN_ERROR
    
    @classmethod
    def get_error_message(cls, code):
        for error in cls:
            if error.value == code.value:
                return error.name
        return cls.UNKNOWN_ERROR.name
    