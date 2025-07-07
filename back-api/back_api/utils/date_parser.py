from datetime import datetime, timezone
from typing import List, Dict

def parse_datetime_safe(value: str) -> datetime:
    """
    Safely parse a datetime string into a datetime object.
    If the string is not in a valid format, return None.
    """
    try:
        dt = datetime.fromisoformat(value)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    
def parse_device_data_times(data_array: List[Dict]) -> List[Dict]:
    for d in data_array:
        d["timestamp"] = parse_datetime_safe(d.get("timestamp", ""))
        d["ts_cast"] = parse_datetime_safe(d.get("ts_cast", ""))
        d["date"] = parse_datetime_safe(d.get("date", ""))
    return data_array