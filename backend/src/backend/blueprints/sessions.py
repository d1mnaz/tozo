from dataclasses import dataclass
from datetime import timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import EmailStr
from quart import Blueprint, ResponseReturnValue, g
from quart_auth import AuthUser, current_user, login_required, login_user, logout_user
from quart_rate_limiter import rate_exempt, rate_limit
from quart_schema import validate_request, validate_response

from backend.lib.api_error import APIError
from backend.models.member import select_member_by_email

blueprint = Blueprint("sessions", __name__)


@dataclass
class LoginData:
    email: EmailStr
    password: str
    remember: bool = False


@dataclass
class Status:
    member_id: int


@blueprint.post("/sessions/")
@rate_limit(5, timedelta(minutes=1))
@validate_request(LoginData)
async def login(data: LoginData) -> ResponseReturnValue:
    """Login to the app.

    By providing credentials and then saving the returned cookie.
    """
    member = await select_member_by_email(g.connection, data.email)
    ph = PasswordHasher()
    if member is None:
        raise APIError(401, "INVALID_CREDENTIALS")
    try:
        ph.verify(member.password_hash, data.password)
    except VerifyMismatchError:
        raise APIError(401, "INVALID_CREDENTIALS")  # noqa

    if member is None:
        raise APIError(401, "INVALID_CREDENTIALS")
    login_user(AuthUser(str(member.id)), data.remember)
    return {}, 200


@blueprint.delete("/sessions/")
@rate_exempt
async def logout() -> ResponseReturnValue:
    """Logout from the app.

    Deletes the session cookie.
    """
    logout_user()
    return {}


@blueprint.get("/sessions/")
@rate_limit(10, timedelta(minutes=1))
@login_required
@validate_response(Status)
async def status() -> ResponseReturnValue:
    assert current_user.auth_id is not None
    return Status(member_id=int(current_user.auth_id))
