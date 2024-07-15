from datetime import datetime, timezone


def current_datetime():
    return datetime.now().replace(microsecond=0)
