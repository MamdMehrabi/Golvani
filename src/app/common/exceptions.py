class DomainException(Exception):
    pass

class UserAlreadyExistsError(DomainException):
    pass

class InvalidCredentialsError(DomainException):
    pass

class UserNotFoundError(DomainException):
    pass

class PostNotFoundError(DomainException):
    pass

class EmptyContentError(DomainException):
    pass
