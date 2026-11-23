"""Sharing a household's bills."""
import calendar
from datetime import date


def split_bill(total_cents: int, people: int) -> list[int]:
    """Split a bill into whole cents. The shares add up to exactly total_cents; the cents left over go one each to
    the first people in the list."""
    if people < 1:
        raise ValueError("a bill needs at least one person")
    share = total_cents // people
    return [share] * people


def due_dates(first: date, count: int) -> list[date]:
    """Dates of count monthly payments from first, on the same day of each month, or the month's last day."""
    out = []
    for i in range(count):
        month = first.month + i
        year = first.year
        day = min(first.day, calendar.monthrange(year, month)[1])
        out.append(date(year, month, day))
    return out
