from typing import Any

from sqlalchemy import Integer, cast, text


def interval(seconds: Any) -> Any:
    """Convert seconds to an interval type for PostgreSQL."""
    return cast(seconds, Integer) * text("INTERVAL '1 SECOND'")
