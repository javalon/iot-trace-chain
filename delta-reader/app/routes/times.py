from fastapi import APIRouter
from app.services.delta_reader import get_device_times
from app.models.device_times import DeviceTimes

router = APIRouter()

@router.get("/{device_id}", response_model=DeviceTimes)
def read_device_times(device_id: str):
    try:
        return get_device_times(device_id)
    except Exception as e:
        raise ValueError(f"Error retrieving times for device {device_id}: {str(e)}") from e