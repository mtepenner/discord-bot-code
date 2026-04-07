import datetime

def format_timedelta(seconds: float) -> str:
    """Converts total seconds into a readable 'HH:MM:SS' string."""
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    return f"{minutes}m {seconds}s"

def format_timestamp(iso_string: str) -> str:
    """Converts a database ISO string into a friendly 12-hour format."""
    dt = datetime.datetime.fromisoformat(iso_string)
    return dt.strftime("%I:%M %p")

def calculate_hours(start_iso: str, end_iso: str) -> float:
    """Calculates the decimal hours between two timestamps for payroll."""
    start = datetime.datetime.fromisoformat(start_iso)
    end = datetime.datetime.fromisoformat(end_iso)
    duration = end - start
    return round(duration.total_seconds() / 3600, 2)

def get_current_iso() -> str:
    """Returns the current time in ISO format for database storage."""
    return datetime.datetime.now().isoformat()
