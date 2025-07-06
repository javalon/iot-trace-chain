from fastapi import APIRouter, HTTPException, Query
from app.services.delta_reader import get_device_data
from app.models.device_data import DeviceData
from typing import Optional, Union
from datetime import datetime, timezone

router = APIRouter()

def parse_datetime(value: Union[str, int]) -> datetime:
    try:
        if isinstance(value, int):
            return datetime.fromtimestamp(value, tz=timezone.utc)
        elif isinstance(value, str) and value.isdigit():
            return datetime.fromtimestamp(int(value), tz=timezone.utc)
        else:
            dt = datetime.fromisoformat(value)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {value}")

@router.get("/{device_id}", response_model=list[DeviceData])
def read_device_data(
    device_id: str,
        from_param: Optional[Union[str, int]] = Query(None, alias="from"),
        to_param: Optional[Union[str, int]] = Query(None, alias="to")
    ):
    try:
        from_date = parse_datetime(from_param) if from_param else None
        to_date = parse_datetime(to_param) if to_param else None
        return get_device_data(device_id, start_date=from_date, end_date=to_date)
    except Exception as e:
        raise ValueError(f"Error retrieving data for device {device_id}: {str(e)}") from e
    
