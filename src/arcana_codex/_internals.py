import json
from http import HTTPStatus

from httpx import Response

from ._utils import Result
from .exceptions import (
    APIException,
    BadRequestException,
    ForbiddenException,
    InternalServerErrorException,
    NotFoundException,
    RateLimitException,
    UnauthorizedException,
    UnprocessableEntityException,
)


def _handle_common_3xx_4xx_5xx_status_code(
    status_code: int, response_text: str
) -> Result[None, type[APIException]]:
    match status_code:
        case HTTPStatus.BAD_REQUEST:
            return Result(
                value=None,
                error=BadRequestException(detail=f"Bad Request: {response_text}"),
            )
        case HTTPStatus.UNAUTHORIZED:
            return Result(
                value=None,
                error=UnauthorizedException(detail=f"Unauthorized: {response_text}"),
            )
        case HTTPStatus.FORBIDDEN:
            return Result(
                value=None,
                error=ForbiddenException(detail=f"Forbidden: {response_text}"),
            )
        case HTTPStatus.NOT_FOUND:
            return Result(
                value=None,
                error=NotFoundException(detail=f"Not Found: {response_text}"),
            )
        case HTTPStatus.UNPROCESSABLE_ENTITY:
            return Result(
                value=None,
                error=UnprocessableEntityException(
                    detail=f"Unprocessable Entity: {response_text}"
                ),
            )
        case HTTPStatus.TOO_MANY_REQUESTS:
            return Result(
                value=None,
                error=RateLimitException(
                    detail=f"Rate Limit Exceeded: {response_text}"
                ),
            )
        case HTTPStatus.INTERNAL_SERVER_ERROR:
            return Result(
                value=None,
                error=InternalServerErrorException(
                    detail=f"Internal Server Error: {response_text}"
                ),
            )
        case _:
            return Result(
                value=None,
                error=APIException(
                    status_code=status_code,
                    detail=f"Unexpected Error: {response_text}",
                ),
            )


def _handle_response(
    response: Response, is_streaming_response: bool = False
) -> Result[dict, None] | Result[None, type[APIException]]:
    match response.status_code:
        case HTTPStatus.OK | HTTPStatus.CREATED | HTTPStatus.ACCEPTED:
            if is_streaming_response:
                value = None
                error = None
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        value = json.loads(line[len("data: ") :].strip())
                        break
                    elif line.startswith("error: "):
                        error = APIException(
                            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=line[len("error: ") :].strip(),
                        )
                        break
                return Result(value=value, error=error)
            else:
                return Result(value=response.json(), error=None)
        case _:
            return _handle_common_3xx_4xx_5xx_status_code(
                response.status_code, response.text
            )


async def _handle_async_response(
    response: Response, is_streaming_response: bool = False
) -> Result[dict, None] | Result[None, type[APIException]]:
    match response.status_code:
        case HTTPStatus.OK | HTTPStatus.CREATED | HTTPStatus.ACCEPTED:
            if is_streaming_response:
                value = None
                error = None
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        value = json.loads(line[len("data: ") :].strip())
                        break
                    elif line.startswith("error: "):
                        error = APIException(
                            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=line[len("error: ") :].strip(),
                        )
                        break
                return Result(value=value, error=error)
            else:
                return Result(value=response.json(), error=None)
        case _:
            return _handle_common_3xx_4xx_5xx_status_code(
                response.status_code, response.text
            )
