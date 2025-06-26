from http import HTTPStatus


class APIException(Exception):
    def __init__(self, status_code: int, detail: str | None = None):
        if not detail:  # pragma: no cover
            detail = HTTPStatus(status_code).description
        super().__init__(status_code, detail)


class BadRequestException(APIException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST, detail=detail
        )  # pragma: no cover


class NotFoundException(APIException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND, detail=detail
        )  # pragma: no cover


class ForbiddenException(APIException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN, detail=detail
        )  # pragma: no cover


class UnauthorizedException(APIException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED, detail=detail
        )  # pragma: no cover


class InternalServerErrorException(APIException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=detail
        )  # pragma: no cover


class UnprocessableEntityException(APIException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail
        )  # pragma: no cover


class RateLimitException(APIException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=HTTPStatus.TOO_MANY_REQUESTS, detail=detail
        )  # pragma: no cover
