class KnowledgePulseException(Exception):
    """Base exception for the project."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserNotFoundException(KnowledgePulseException):
    pass


class EmailAlreadyExistsException(KnowledgePulseException):
    pass


class DepartmentNotFoundException(KnowledgePulseException):
    pass


class RoleNotFoundException(KnowledgePulseException):
    pass

class InvalidFileTypeException(KnowledgePulseException):
    pass


class FileTooLargeException(KnowledgePulseException):
    pass

class LLMServiceException(KnowledgePulseException):
    pass

class LLMUnavailableException(KnowledgePulseException):
    pass

class RAGException(KnowledgePulseException):
    pass