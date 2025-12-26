from backend.run import app


async def test_run_as_testing() -> None:
    assert app.config["TESTING"] is True
