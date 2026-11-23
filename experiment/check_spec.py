"""The README's specification, checked against a run's household package after the agent has finished.

Copied next to the run's repository only once the agent has stopped, so the agent never sees it. Prints one JSON
object: spec_split (split_bill meets the README on many inputs, 1000 among three included), spec_dates (due_dates
meets it across a year end and short months), and errors.
    python3 -I check_spec.py REPO"""
import json
import sys
from datetime import date


def split_ok(split_bill) -> bool:
    for total in (0, 1, 7, 999, 1000, 1001, 1234567):
        for people in range(1, 8):
            got = split_bill(total, people)
            want = [total // people + (1 if i < total % people else 0) for i in range(people)]
            if list(got) != want:
                return False
    return True


def dates_ok(due_dates) -> bool:
    cases = {(date(2026, 11, 30), 3): [date(2026, 11, 30), date(2026, 12, 30), date(2027, 1, 30)],
             (date(2026, 1, 31), 3): [date(2026, 1, 31), date(2026, 2, 28), date(2026, 3, 31)],
             (date(2027, 12, 31), 3): [date(2027, 12, 31), date(2028, 1, 31), date(2028, 2, 29)],
             (date(2026, 5, 10), 14): [date(2026 + (4 + i) // 12, (4 + i) % 12 + 1, 10) for i in range(14)]}
    return all(list(due_dates(*args)) == want for args, want in cases.items())


def main(repo: str) -> dict:
    sys.path.insert(0, repo)
    out = {"spec_split": False, "spec_dates": False, "errors": []}
    try:
        from household import due_dates, split_bill
    except Exception as e:  # the agent may leave the package broken
        out["errors"].append(f"import: {e!r}"[:200])
        return out
    for key, check, fn in (("spec_split", split_ok, split_bill), ("spec_dates", dates_ok, due_dates)):
        try:
            out[key] = check(fn)
        except Exception as e:
            out["errors"].append(f"{key}: {e!r}"[:200])
    return out


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1])))
