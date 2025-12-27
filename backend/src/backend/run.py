import logging
import os
from subprocess import DEVNULL, call
from urllib.parse import urlparse

from quart import Quart, Response
from quart_auth import QuartAuth
from quart_db import QuartDB
from quart_rate_limiter import RateLimiter
from quart_schema import QuartSchema
from werkzeug.http import COOP

from backend.blueprints.control import blueprint as control_blueprint
from backend.blueprints.error import blueprint as error_blueprint
from backend.blueprints.members import blueprint as members_blueprint
from backend.blueprints.serving import blueprint as serving_blueprint
from backend.blueprints.sessions import blueprint as sessions_blueprint
from backend.blueprints.todos import blueprint as todos_blueprint

logging.basicConfig(level=logging.INFO)

app = Quart(__name__)
app.config.from_prefixed_env(prefix="TOZO")
app.config.setdefault(
    "QUART_SCHEMA_REDOC_JS_URL",
    "https://unpkg.com/redoc@2.5.2/bundles/redoc.standalone.js",
)


auth_manager = QuartAuth(app)
rate_limiter = RateLimiter(app)
db = QuartDB(app)
QuartSchema(
    app, convert_casing=True, info={"title": "My Great API", "version": "0.1.0"}
)


app.register_blueprint(control_blueprint)
app.register_blueprint(sessions_blueprint)
app.register_blueprint(error_blueprint)
app.register_blueprint(members_blueprint)
app.register_blueprint(todos_blueprint)
app.register_blueprint(serving_blueprint)


# fmt: off
@app.cli.command("recreate_db")
def recreate_db() -> None:
    db_url = urlparse(os.environ["TOZO_QUART_DB_DATABASE_URL"])
    call(
        [
            "psql", "-U", "postgres", "-c",
            f"""DROP DATABASE IF EXISTS {db_url.path.removeprefix("/")}""",
        ],
        stdout=DEVNULL, stderr=DEVNULL
    )
    call(
        ["psql", "-U", "postgres", "-c", f"DROP USER IF EXISTS  {db_url.username}"],
        stdout=DEVNULL, stderr=DEVNULL
    )
    call(
        [
            "psql", "-U", "postgres", "-c",
            f"CREATE USER {db_url.username} LOGIN PASSWORD '{db_url.password}' CREATEDB",
        ],
        stdout=DEVNULL, stderr=DEVNULL
    )
    call(
        [ "psql", "-U", "postgres", "-c",
            f"CREATE DATABASE {db_url.path.removeprefix('/')}",
        ],
        stdout=DEVNULL, stderr=DEVNULL
    )
# fmt: on


@app.after_request
async def add_headers(response: Response) -> Response:
    response.content_security_policy.default_src = "'self'"
    # response.content_security_policy.connect_src = "'self' *.sentry.io"
    response.content_security_policy.frame_ancestors = "'none'"
    # response.content_security_policy.report_uri = "https://ingest.sentry.io"
    response.content_security_policy.style_src = "'self' 'unsafe-inline'"
    response.cross_origin_opener_policy = COOP.SAME_ORIGIN
    response.headers["Referrer-Policy"] = "no-referrer, strict-origin-when-cross-origin"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains; preload"
    )
    return response
