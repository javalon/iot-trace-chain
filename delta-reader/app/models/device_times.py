from pydantic import BaseModel

class DeviceTimes(BaseModel):
    max_date: int | None
    min_date: int | None