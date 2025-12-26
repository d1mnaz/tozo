from quart import Blueprint, ResponseReturnValue
from quart_rate_limiter import RateLimitExceeded
from quart_schema import RequestSchemaValidationError

from backend.lib.api_error import APIError

blueprint = Blueprint("error", __name__)


@blueprint.app_errorhandler(APIError)
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    return {"code": error.code}, error.status_code


@blueprint.app_errorhandler(500)
async def handle_generic_error(error: Exception) -> ResponseReturnValue:
    return {"code": "INTERNAL_SERVER_ERROR"}, 500


@blueprint.app_errorhandler(RateLimitExceeded)
async def handle_rate_limit_exceeded_error(
    error: RateLimitExceeded,
) -> ResponseReturnValue:
    return {}, error.get_headers(), 429


@blueprint.app_errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(
    error: RequestSchemaValidationError,
) -> ResponseReturnValue:
    if isinstance(error.validation_error, TypeError):
        return {"errors": str(error.validation_error)}, 400
    else:
        return {"errors": error.validation_error.json()}, 400
