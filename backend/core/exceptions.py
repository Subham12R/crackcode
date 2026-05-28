from fastapi import HTTPException, status


class CrackCodeException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(CrackCodeException):
    """Resource not found exception."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} with identifier '{identifier}' not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class AuthenticationException(CrackCodeException):
    """Authentication failed exception."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationException(CrackCodeException):
    """Authorization failed exception."""

    def __init__(self, message: str = "Not authorized"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class ValidationException(CrackCodeException):
    """Validation failed exception."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class PlatformSyncException(CrackCodeException):
    """Platform sync failed exception."""

    def __init__(self, platform: str, message: str):
        super().__init__(
            message=f"Failed to sync {platform}: {message}",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )


# HTTP exception mappings for FastAPI
class HTTPExceptionMapper:
    """Map custom exceptions to FastAPI HTTP exceptions."""

    @staticmethod
    def map(exception: CrackCodeException) -> HTTPException:
        return HTTPException(
            status_code=exception.status_code,
            detail=exception.message,
        )