"""Helpers for logging service locations without credential material."""

from urllib.parse import urlsplit, urlunsplit


REDACTED_ENDPOINT = "<configured>"


def safe_url_for_log(value: str | None) -> str:
    """Return a URL containing location only, with userinfo/query removed.

    Invalid or non-network URLs fail closed rather than echoing their input.
    """
    if not value:
        return REDACTED_ENDPOINT

    try:
        parsed = urlsplit(value)
        if not parsed.scheme or not parsed.hostname:
            return REDACTED_ENDPOINT

        hostname = parsed.hostname
        if ":" in hostname:
            hostname = f"[{hostname}]"
        netloc = hostname
        if parsed.port is not None:
            netloc = f"{netloc}:{parsed.port}"

        return urlunsplit((parsed.scheme, netloc, parsed.path, "", ""))
    except (TypeError, ValueError):
        return REDACTED_ENDPOINT
