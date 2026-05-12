from docuverse.ui import _format_error


def test_format_error_handles_missing_openai_key() -> None:
    message = _format_error(RuntimeError("OPENAI_API_KEY is required"))

    assert "OPENAI_API_KEY is missing" in message


def test_format_error_handles_database_connection_failure() -> None:
    message = _format_error(RuntimeError("connection refused"))

    assert "database does not appear to be running" in message


def test_format_error_handles_missing_chunks() -> None:
    message = _format_error(RuntimeError("no chunks found"))

    assert "No chunks were found" in message
