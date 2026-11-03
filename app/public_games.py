"""Public game release policy and target-free response serializers.

This module intentionally has no service or framework dependencies so the
release boundary and public contracts can be tested without PostgreSQL, Redis,
or the API runtime.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any, Iterable, Mapping


RIYADH_TZ = timezone(timedelta(hours=3), name="Asia/Riyadh")


def riyadh_today(at: datetime | None = None) -> date:
    """Return the calendar date in Riyadh for an aware instant."""
    if at is None:
        return datetime.now(RIYADH_TZ).date()
    if at.tzinfo is None:
        raise ValueError("at must be timezone-aware")
    return at.astimezone(RIYADH_TZ).date()


def _scheduled_date(value: Any) -> date:
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            return value.astimezone(RIYADH_TZ).date()
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise TypeError("scheduled_date must be an ISO date, date, or datetime")


def is_game_released(game: Mapping[str, Any], *, at: datetime | None = None) -> bool:
    """Fail closed unless the game is scheduled on or before Riyadh today."""
    try:
        scheduled = _scheduled_date(game["scheduled_date"])
        today = riyadh_today(at)
    except (KeyError, TypeError, ValueError):
        return False
    return scheduled <= today


def public_game_summary(game: Mapping[str, Any]) -> dict[str, int]:
    """Serialize only the identifier needed by the archive UI."""
    return {"id": int(game["game_id"])}


def public_games_payload(
    games: Iterable[Mapping[str, Any]], active_id: int | None
) -> dict[str, Any]:
    """Build the target-free current/archive metadata response."""
    return {
        "games": [public_game_summary(game) for game in games],
        "active_id": active_id,
    }


def public_switch_payload(game_id: int) -> dict[str, Any]:
    """Build the archive-switch response without target or cluster data."""
    return {
        "message": f"تم التبديل إلى التحدي #{game_id}",
        "game_id": game_id,
    }
